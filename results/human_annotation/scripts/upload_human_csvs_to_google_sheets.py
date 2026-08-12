import argparse
import csv
import json
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


DRIVE_FOLDER_MIME = "application/vnd.google-apps.folder"
GOOGLE_SHEET_MIME = "application/vnd.google-apps.spreadsheet"
HUMAN_SUFFIX = "_human.csv"
SCOPES = (
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
)
DEFAULT_CONFIG_PATH = Path("results/human_annotation/google_oauth_config.json")
ANNOTATION_LABEL_OPTIONS = ("A", "B", "tie", "unclear")
DATA_VALIDATION_ROW_CAP = 2000
INSTALL_HINT = (
    "Missing Google client dependencies. Install them with:\n"
    "  uv sync --extra human-annotation\n"
    "or, if you prefer the helper script:\n"
    "  results/human_annotation/scripts/install_google_deps.sh\n"
    "or manually with your chosen interpreter:\n"
    "  <python> -m pip install google-api-python-client google-auth google-auth-oauthlib"
)


@dataclass(frozen=True)
class ExportCsvTarget(object):
    csv_path: Path
    relative_path: Path
    folder_parts: Tuple[str, ...]
    sheet_name: str


def remove_suffix(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def discover_human_csv_targets(input_root):
    targets = []  # type: List[ExportCsvTarget]
    for csv_path in sorted(input_root.rglob("*" + HUMAN_SUFFIX)):
        relative_path = csv_path.relative_to(input_root)
        folder_parts = relative_path.parts[:-1]
        sheet_name = remove_suffix(csv_path.name, ".csv")
        targets.append(
            ExportCsvTarget(
                csv_path=csv_path,
                relative_path=relative_path,
                folder_parts=tuple(folder_parts),
                sheet_name=sheet_name,
            )
        )
    return targets


def prefixed_folder_parts(folder_parts, folder_prefix=""):
    prefix_parts = tuple(part for part in folder_prefix.split("/") if part)
    return prefix_parts + folder_parts


def load_config(config_path):
    if not config_path.is_file():
        return {}
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Expected config file {} to contain a JSON object.".format(config_path))
    return payload


def build_drive_service(oauth_client_secrets_path, oauth_token_path, open_browser):
    try:
        from google.auth.transport.requests import Request
        from google.auth.exceptions import RefreshError
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ModuleNotFoundError as exc:
        raise SystemExit("{}\nOriginal import error: {}".format(INSTALL_HINT, exc))

    credentials = None
    if oauth_token_path.is_file():
        credentials = Credentials.from_authorized_user_file(
            str(oauth_token_path),
            scopes=list(SCOPES),
        )

    if credentials is not None and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except RefreshError:
            credentials = None
            try:
                oauth_token_path.unlink()
            except OSError:
                pass

    if credentials is None or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(oauth_client_secrets_path),
            scopes=list(SCOPES),
        )
        credentials = flow.run_local_server(
            host="127.0.0.1",
            port=0,
            open_browser=open_browser,
        )
        oauth_token_path.parent.mkdir(parents=True, exist_ok=True)
        oauth_token_path.write_text(credentials.to_json(), encoding="utf-8")

    return (
        build("drive", "v3", credentials=credentials),
        build("sheets", "v4", credentials=credentials),
    )


def _escape_drive_query(value):
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _find_child_by_name(drive_service, parent_id, name, mime_type):
    query = (
        "'{}' in parents and name = '{}' and mimeType = '{}' and trashed = false".format(
            _escape_drive_query(parent_id),
            _escape_drive_query(name),
            mime_type,
        )
    )
    response = (
        drive_service.files()
        .list(
            q=query,
            spaces="drive",
            fields="files(id,name,webViewLink)",
            pageSize=1,
        )
        .execute()
    )
    files = response.get("files", [])
    return files[0] if files else None


def ensure_drive_folder_path(drive_service, root_folder_id, folder_parts):
    parent_id = root_folder_id
    for folder_name in folder_parts:
        existing = _find_child_by_name(
            drive_service,
            parent_id=parent_id,
            name=folder_name,
            mime_type=DRIVE_FOLDER_MIME,
        )
        if existing is None:
            created = (
                drive_service.files()
                .create(
                    body={
                        "name": folder_name,
                        "mimeType": DRIVE_FOLDER_MIME,
                        "parents": [parent_id],
                    },
                    fields="id,name",
                )
                .execute()
            )
            parent_id = str(created["id"])
        else:
            parent_id = str(existing["id"])
    return parent_id


def upload_csv_as_google_sheet(drive_service, target, parent_folder_id, if_exists):
    try:
        from googleapiclient.http import MediaIoBaseUpload
    except ModuleNotFoundError as exc:
        raise SystemExit("{}\nOriginal import error: {}".format(INSTALL_HINT, exc))

    existing = _find_child_by_name(
        drive_service,
        parent_id=parent_folder_id,
        name=target.sheet_name,
        mime_type=GOOGLE_SHEET_MIME,
    )
    if existing is not None:
        if if_exists == "skip":
            return {
                "action": "skipped",
                "sheet_id": existing["id"],
                "sheet_name": target.sheet_name,
                "web_view_link": existing.get("webViewLink"),
                "relative_path": str(target.relative_path),
            }
        if if_exists == "replace":
            drive_service.files().delete(fileId=existing["id"]).execute()
        else:
            raise ValueError("Unsupported if_exists mode: {!r}".format(if_exists))

    csv_bytes = target.csv_path.read_bytes()
    media = MediaIoBaseUpload(
        BytesIO(csv_bytes),
        mimetype="text/csv",
        resumable=False,
    )
    created = (
        drive_service.files()
        .create(
            body={
                "name": target.sheet_name,
                "mimeType": GOOGLE_SHEET_MIME,
                "parents": [parent_folder_id],
            },
            media_body=media,
            fields="id,name,webViewLink",
        )
        .execute()
    )
    return {
        "action": "created",
        "sheet_id": created["id"],
        "sheet_name": created["name"],
        "web_view_link": created.get("webViewLink"),
        "relative_path": str(target.relative_path),
    }


def _load_csv_shape(csv_path):
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    if not rows:
        return [], 0
    headers = rows[0]
    data_row_count = max(len(rows) - 1, 0)
    return headers, data_row_count


def _rgb(red, green, blue):
    return {"red": red, "green": green, "blue": blue}


def _column_width_for_header(header):
    if header == "item_id":
        return 110
    if header == "label":
        return 100
    if header in {"src", "hypo_A", "hypo_B"}:
        return 360
    return 160


def build_sheet_format_requests(sheet_id, headers, data_row_count):
    column_count = len(headers)
    row_count = data_row_count + 1 if headers else 0
    validation_end_row = max(row_count, DATA_VALIDATION_ROW_CAP)
    requests = []  # type: List[Dict[str, Any]]

    requests.append(
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1,
                    },
                },
                "fields": "gridProperties.frozenRowCount",
            }
        }
    )

    if row_count > 0 and column_count > 0:
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": row_count,
                        "startColumnIndex": 0,
                        "endColumnIndex": column_count,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "wrapStrategy": "WRAP",
                            "verticalAlignment": "TOP",
                            "horizontalAlignment": "LEFT",
                            "textFormat": {
                                "fontSize": 10,
                            },
                        }
                    },
                    "fields": (
                        "userEnteredFormat.wrapStrategy,"
                        "userEnteredFormat.verticalAlignment,"
                        "userEnteredFormat.horizontalAlignment,"
                        "userEnteredFormat.textFormat.fontSize"
                    ),
                }
            }
        )
        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": column_count,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": _rgb(0.90, 0.93, 0.98),
                            "textFormat": {
                                "bold": True,
                                "fontSize": 10,
                            },
                        }
                    },
                    "fields": (
                        "userEnteredFormat.backgroundColor,"
                        "userEnteredFormat.textFormat.bold,"
                        "userEnteredFormat.textFormat.fontSize"
                    ),
                }
            }
        )

    for column_index, header in enumerate(headers):
        requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": column_index,
                        "endIndex": column_index + 1,
                    },
                    "properties": {
                        "pixelSize": _column_width_for_header(header),
                    },
                    "fields": "pixelSize",
                }
            }
        )
        if header == "label":
            requests.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 1,
                            "endRowIndex": row_count,
                            "startColumnIndex": column_index,
                            "endColumnIndex": column_index + 1,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": _rgb(0.98, 0.96, 0.88),
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            )
            requests.append(
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 1,
                            "endRowIndex": validation_end_row,
                            "startColumnIndex": column_index,
                            "endColumnIndex": column_index + 1,
                        },
                        "rule": {
                            "condition": {
                                "type": "ONE_OF_LIST",
                                "values": [
                                    {"userEnteredValue": option}
                                    for option in ANNOTATION_LABEL_OPTIONS
                                ],
                            },
                            "showCustomUi": True,
                            "strict": True,
                        },
                    }
                }
            )
    return requests


def format_uploaded_google_sheet(sheets_service, spreadsheet_id, csv_path):
    spreadsheet = (
        sheets_service.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id,
            fields="sheets(properties(sheetId,title,index))",
        )
        .execute()
    )
    sheets = spreadsheet.get("sheets", [])
    if not sheets:
        raise ValueError("Spreadsheet {} does not contain any sheets.".format(spreadsheet_id))
    first_sheet_id = int(sheets[0]["properties"]["sheetId"])
    headers, data_row_count = _load_csv_shape(csv_path)
    requests = build_sheet_format_requests(first_sheet_id, headers, data_row_count)
    if requests:
        (
            sheets_service.spreadsheets()
            .batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests},
            )
            .execute()
        )


def upload_all_human_csvs(
    input_root,
    oauth_client_secrets_path,
    oauth_token_path,
    drive_root_folder_id,
    remote_disk_root,
    folder_prefix,
    if_exists,
    manifest_path,
    open_browser,
):
    drive_service, sheets_service = build_drive_service(
        oauth_client_secrets_path=oauth_client_secrets_path,
        oauth_token_path=oauth_token_path,
        open_browser=open_browser,
    )
    targets = discover_human_csv_targets(input_root)
    results = []  # type: List[Dict[str, Any]]
    for target in targets:
        parent_folder_id = ensure_drive_folder_path(
            drive_service,
            root_folder_id=drive_root_folder_id,
            folder_parts=prefixed_folder_parts(
                prefixed_folder_parts(target.folder_parts, folder_prefix=folder_prefix),
                folder_prefix=remote_disk_root,
            ),
        )
        result = upload_csv_as_google_sheet(
            drive_service,
            target=target,
            parent_folder_id=parent_folder_id,
            if_exists=if_exists,
        )
        if result["action"] == "created":
            format_uploaded_google_sheet(
                sheets_service,
                spreadsheet_id=str(result["sheet_id"]),
                csv_path=target.csv_path,
            )
        results.append(result)
        print(
            "{}: {} -> {}".format(
                result["action"],
                target.relative_path,
                result.get("web_view_link") or result["sheet_id"],
            )
        )

    if manifest_path is not None:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "input_root": str(input_root),
                    "oauth_client_secrets_path": str(oauth_client_secrets_path),
                    "oauth_token_path": str(oauth_token_path),
                    "drive_root_folder_id": drive_root_folder_id,
                    "remote_disk_root": remote_disk_root,
                    "folder_prefix": folder_prefix,
                    "if_exists": if_exists,
                    "uploaded_count": len(results),
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return results


def parse_args():
    parser = argparse.ArgumentParser(
        description="Upload human annotation CSV exports as Google Sheets while mirroring the local subtree."
    )
    parser.add_argument("--config-path", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--input-root", type=Path, default=None)
    parser.add_argument("--oauth-client-secrets-path", type=Path, default=None)
    parser.add_argument("--oauth-token-path", type=Path, default=None)
    parser.add_argument("--drive-root-folder-id", default=None)
    parser.add_argument("--remote-disk-root", default=None)
    parser.add_argument("--folder-prefix", default=None)
    parser.add_argument("--if-exists", choices=("skip", "replace"), default=None)
    parser.add_argument("--manifest-path", type=Path, default=None)
    parser.add_argument("--open-browser", action=argparse.BooleanOptionalAction, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(args.config_path)

    input_root = Path(args.input_root or config.get("input_root") or "results/human_annotation/snapshots")
    oauth_client_secrets_path = Path(
        args.oauth_client_secrets_path
        or config.get("oauth_client_secrets_path")
        or "/home/stroshi/.google_api_user/client_secret.json"
    )
    oauth_token_path = Path(
        args.oauth_token_path
        or config.get("oauth_token_path")
        or "/home/stroshi/.google_api_user/token.json"
    )
    drive_root_folder_id = str(args.drive_root_folder_id or config.get("drive_root_folder_id") or "root")
    remote_disk_root = str(args.remote_disk_root or config.get("remote_disk_root") or "")
    folder_prefix = str(args.folder_prefix or config.get("folder_prefix") or "")
    if_exists = str(args.if_exists or config.get("if_exists") or "skip")
    manifest_path_value = args.manifest_path or config.get("manifest_path")
    manifest_path = None if manifest_path_value in (None, "") else Path(manifest_path_value)
    open_browser = args.open_browser if args.open_browser is not None else bool(config.get("open_browser", True))

    upload_all_human_csvs(
        input_root=input_root,
        oauth_client_secrets_path=oauth_client_secrets_path,
        oauth_token_path=oauth_token_path,
        drive_root_folder_id=drive_root_folder_id,
        remote_disk_root=remote_disk_root,
        folder_prefix=folder_prefix,
        if_exists=if_exists,
        manifest_path=manifest_path,
        open_browser=open_browser,
    )


if __name__ == "__main__":
    main()
