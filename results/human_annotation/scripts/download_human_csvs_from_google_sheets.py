import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from upload_human_csvs_to_google_sheets import build_drive_service


DEFAULT_CONFIG_PATH = Path("results/human_annotation/google_oauth_config.json")


def load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.is_file():
        return {}
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected config file {config_path} to contain a JSON object.")
    return payload


def _download_sheet_csv_bytes(drive_service: Any, *, sheet_id: str) -> bytes:
    from googleapiclient.http import MediaIoBaseDownload
    from io import BytesIO

    request = drive_service.files().export_media(fileId=sheet_id, mimeType="text/csv")
    buffer = BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buffer.getvalue()


def sync_manifest(
    *,
    manifest_path: Path,
    output_root: Path,
    oauth_client_secrets_path: Path,
    oauth_token_path: Path,
    open_browser: bool,
) -> List[Path]:
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected manifest {manifest_path} to contain a JSON object.")

    results = payload.get("results")
    if not isinstance(results, list):
        raise ValueError(f"Manifest {manifest_path} is missing a results list.")

    drive_service, _ = build_drive_service(
        oauth_client_secrets_path=oauth_client_secrets_path,
        oauth_token_path=oauth_token_path,
        open_browser=open_browser,
    )

    written_paths = []  # type: List[Path]
    for item in results:
        if not isinstance(item, dict):
            continue
        sheet_id = item.get("sheet_id")
        relative_path = item.get("relative_path")
        if not isinstance(sheet_id, str) or not sheet_id:
            raise ValueError(f"Manifest entry missing sheet_id: {item!r}")
        if not isinstance(relative_path, str) or not relative_path:
            raise ValueError(f"Manifest entry missing relative_path: {item!r}")

        output_path = output_root / Path(relative_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(_download_sheet_csv_bytes(drive_service, sheet_id=sheet_id))
        written_paths.append(output_path)
        print(f"downloaded: {sheet_id} -> {output_path}")

    sync_manifest_path = output_root / "_download_sync_manifest.json"
    sync_manifest_path.write_text(
        json.dumps(
            {
                "source_manifest_path": str(manifest_path),
                "output_root": str(output_root),
                "downloaded_count": len(written_paths),
                "files": [str(path.relative_to(output_root)) for path in written_paths],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    written_paths.append(sync_manifest_path)
    return written_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download previously uploaded Google Sheets back to local CSV files using an upload manifest."
        )
    )
    parser.add_argument(
        "--manifest-path",
        type=Path,
        required=True,
        help="Upload manifest JSON containing sheet ids and relative paths.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        required=True,
        help="Directory where downloaded CSV files will be written.",
    )
    parser.add_argument(
        "--config-path",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Path to a JSON config file with default OAuth settings.",
    )
    parser.add_argument(
        "--oauth-client-secrets-path",
        type=Path,
        default=None,
        help="Path to a Google OAuth desktop-app client secrets JSON file.",
    )
    parser.add_argument(
        "--oauth-token-path",
        type=Path,
        default=None,
        help="Path where the reusable OAuth token JSON is stored.",
    )
    parser.add_argument(
        "--open-browser",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Whether to open the OAuth consent page in a browser automatically.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config_path)

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
    open_browser = (
        args.open_browser
        if args.open_browser is not None
        else bool(config.get("open_browser", True))
    )

    outputs = sync_manifest(
        manifest_path=args.manifest_path,
        output_root=args.output_root,
        oauth_client_secrets_path=oauth_client_secrets_path,
        oauth_token_path=oauth_token_path,
        open_browser=open_browser,
    )
    print(f"Downloaded {len(outputs) - 1} CSV files to {args.output_root}")


if __name__ == "__main__":
    main()
