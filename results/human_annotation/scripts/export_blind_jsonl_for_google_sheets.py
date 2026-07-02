#!/usr/bin/env python3
"""Convert a blind JSONL annotation set into the human-annotation CSV layout."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT_PATH = (
    REPO_ROOT
    / "results/gemini-2.5-flash/experiments/gpt-final_rus_Cyrl_rubric-v5/annotation/best_pair_annotation_blind.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    REPO_ROOT
    / "results/human_annotation/snapshots/20260702_rus_best_pair_default_vs_rubric_v5/en-ru_RU/default_vs_rubric_v5"
)
DEFAULT_STRATEGY_NAME = "best_pair_disagreement_default_vs_rubric_v5"
DEFAULT_COMPARISON_NAME = "default_vs_rubric_v5"
CSV_HEADERS = ("item_id", "doc_id", "src", "hypo_A", "hypo_B", "label", "notes")


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a randomized blind JSONL pair file into a *_human.csv file "
            "compatible with the results/human_annotation Google Sheets uploader."
        )
    )
    parser.add_argument("--input-path", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--strategy-name",
        default=DEFAULT_STRATEGY_NAME,
        help="Used for output filenames and metadata.",
    )
    parser.add_argument(
        "--comparison-name",
        default=DEFAULT_COMPARISON_NAME,
        help="Used in metadata only.",
    )
    parser.add_argument(
        "--snapshot-id",
        default="20260702_rus_best_pair_default_vs_rubric_v5",
        help="Used in metadata only.",
    )
    return parser.parse_args()


def require_str(path: Path, line_no: int, record: dict, key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str):
        raise SystemExit(f"{path}:{line_no}: expected string {key}")
    return value


def main() -> None:
    args = parse_args()
    input_path = args.input_path.resolve()
    output_dir = args.output_dir.resolve()

    if not input_path.exists():
        raise SystemExit(f"missing input path: {input_path}")

    rows: list[dict[str, str]] = []
    seen_item_ids: set[str] = set()
    seen_doc_ids: set[str] = set()
    language_label = ""

    for line_no, record in iter_jsonl(input_path):
        pair_id = require_str(input_path, line_no, record, "pair_id")
        doc_id = require_str(input_path, line_no, record, "doc_id")
        tgt_lang = require_str(input_path, line_no, record, "tgt_lang")
        source_doc = require_str(input_path, line_no, record, "source_doc")
        candidate_a = require_str(input_path, line_no, record, "candidate_a")
        candidate_b = require_str(input_path, line_no, record, "candidate_b")

        if pair_id in seen_item_ids:
            raise SystemExit(f"{input_path}:{line_no}: duplicate pair_id={pair_id}")
        if doc_id in seen_doc_ids:
            raise SystemExit(f"{input_path}:{line_no}: duplicate doc_id={doc_id}")
        seen_item_ids.add(pair_id)
        seen_doc_ids.add(doc_id)
        language_label = tgt_lang

        rows.append(
            {
                "item_id": pair_id,
                "doc_id": doc_id,
                "src": source_doc,
                "hypo_A": candidate_a,
                "hypo_B": candidate_b,
                "label": "",
                "notes": "",
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"{args.strategy_name}_human.csv"
    metadata_path = output_dir / f"{args.strategy_name}.internal.json"

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_HEADERS))
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "schema_version": "blind_jsonl_human_export_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": args.snapshot_id,
        "strategy_name": args.strategy_name,
        "comparison_name": args.comparison_name,
        "language_pair": "en-ru_RU",
        "target_language_label": language_label,
        "source_blind_jsonl": str(input_path),
        "exported_sample_size": len(rows),
        "csv_path": str(csv_path),
        "records": rows,
    }
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"csv:      {csv_path}")
    print(f"metadata: {metadata_path}")
    print(f"rows:     {len(rows)}")


if __name__ == "__main__":
    main()
