import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


ANNOTATION_COLUMNS = ["label"]
HUMAN_CSV_SUFFIX = "_human.csv"
INTERNAL_JSON_SUFFIX = ".internal.json"


def clean_text(value):
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def remove_suffix(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def load_jsonl(path):
    rows = []  # type: List[Dict[str, Any]]
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rows.append(json.loads(line))
    return rows


def rows_by_doc_id(rows):
    mapping = {}  # type: Dict[str, Dict[str, Any]]
    for row in rows:
        doc_id = str(row["doc_id"])
        if doc_id in mapping:
            raise ValueError("Duplicate doc_id {!r}".format(doc_id))
        mapping[doc_id] = row
    return mapping


def natural_doc_sort_key(doc_id):
    match = re.match(r"^(\d+)", doc_id)
    if match:
        return (int(match.group(1)), doc_id)
    return (10 ** 18, doc_id)


def stable_seeded_hex(seed, namespace, item_id):
    payload = "{}:{}:{}".format(seed, namespace, item_id).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def select_items_stably(item_ids, sample_size=None, seed=0):
    ordered = sorted(item_ids, key=natural_doc_sort_key)
    shuffled = sorted(
        ordered,
        key=lambda item_id: (
            stable_seeded_hex(seed, "item_order", item_id),
            natural_doc_sort_key(item_id),
        ),
    )
    if sample_size is None or sample_size >= len(shuffled):
        return shuffled
    return shuffled[:sample_size]


def show_model_b_in_slot_a(seed, doc_id):
    return int(stable_seeded_hex(seed, "pair_orientation", doc_id)[0], 16) % 2 == 0


def empty_annotation_fields():
    return {"label": ""}


def load_internal_records(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Expected records list in {}".format(path))
    by_item_id = {}  # type: Dict[str, Dict[str, Any]]
    for record in records:
        if not isinstance(record, dict):
            continue
        by_item_id[str(record["item_id"])] = record
    return payload, by_item_id


def create_labelled_csv_reader(handle):
    sample = handle.read(4096)
    handle.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        delimiter = str(dialect.delimiter)
    except csv.Error:
        first_line = sample.splitlines()[0] if sample else ""
        delimiter = ";" if first_line.count(";") > first_line.count(",") else ","
    reader = csv.DictReader(handle, delimiter=delimiter)
    if reader.fieldnames is not None:
        reader.fieldnames = [str(name).lstrip("\ufeff").strip() for name in reader.fieldnames]
    return reader


def row_is_effectively_blank(row):
    return all(not str(value).strip() for value in row.values())


def normalize_binary_choice(raw_label):
    label = clean_text(raw_label)
    lowered = label.lower()
    if lowered == "":
        return None
    if lowered == "a":
        return "A"
    if lowered == "b":
        return "B"
    if lowered == "tie":
        return "tie"
    if lowered == "unclear":
        return "unclear"
    raise ValueError("Unsupported label {!r}; expected A, B, tie, or unclear.".format(raw_label))


def match_internal_and_labelled_pairs(snapshot_root, labelled_root):
    pairs = []  # type: List[Tuple[Path, Path]]
    for labelled_csv_path in sorted(labelled_root.rglob("*" + HUMAN_CSV_SUFFIX)):
        relative_path = labelled_csv_path.relative_to(labelled_root)
        internal_relative_path = Path(
            remove_suffix(str(relative_path), HUMAN_CSV_SUFFIX) + INTERNAL_JSON_SUFFIX
        )
        internal_json_path = snapshot_root / internal_relative_path
        if not internal_json_path.is_file():
            raise FileNotFoundError(
                "Could not find matching internal json for {}: expected {}".format(
                    labelled_csv_path,
                    internal_json_path,
                )
            )
        pairs.append((internal_json_path, labelled_csv_path))
    if not pairs:
        raise FileNotFoundError("No labelled CSV files found under {}".format(labelled_root))
    return pairs


def load_optional_jsonl_by_doc_id(path):
    if path is None or not path.is_file():
        return {}
    return rows_by_doc_id(load_jsonl(path))
