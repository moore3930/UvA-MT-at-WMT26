#!/usr/bin/env python3
"""Project an audit-friendly final JSONL into a thin WMT submission JSONL."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Write a thin WMT submission JSONL containing doc_id, tgt_lang, "
            "hypothesis, plus any explicitly requested extra fields."
        )
    )
    parser.add_argument("--input", type=Path, required=True, help="aligned final jsonl")
    parser.add_argument("--out", type=Path, required=True, help="submission jsonl")
    parser.add_argument(
        "--copy-fields",
        default="",
        help="comma-separated extra fields to copy through (e.g. thinking)",
    )
    parser.add_argument(
        "--require-non-empty-hypothesis",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail if any hypothesis is empty (default: true)",
    )
    return parser.parse_args()


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


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    out_path = args.out.resolve()
    extra_fields = [field.strip() for field in args.copy_fields.split(",") if field.strip()]

    if not input_path.is_file():
        raise SystemExit(f"missing input file: {input_path}")

    written = 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for line_no, record in iter_jsonl(input_path):
            doc_id = record.get("doc_id")
            tgt_lang = record.get("tgt_lang")
            hypothesis = record.get("hypothesis")

            if not isinstance(doc_id, str):
                raise SystemExit(f"{input_path}:{line_no}: expected string doc_id")
            if not isinstance(tgt_lang, str):
                raise SystemExit(f"{input_path}:{line_no}: expected string tgt_lang")
            if not isinstance(hypothesis, str):
                raise SystemExit(f"{input_path}:{line_no}: expected string hypothesis")
            if args.require_non_empty_hypothesis and not hypothesis.strip():
                raise SystemExit(f"{input_path}:{line_no}: empty hypothesis")

            out_record = {
                "doc_id": doc_id,
                "tgt_lang": tgt_lang,
                "hypothesis": hypothesis,
            }
            for field in extra_fields:
                if field in record:
                    out_record[field] = record[field]

            handle.write(json.dumps(out_record, ensure_ascii=False) + "\n")
            written += 1

    print(f"input:  {input_path}")
    print(f"output: {out_path}")
    print(f"rows:   {written}")
    if extra_fields:
        print(f"copied extra fields: {', '.join(extra_fields)}")


if __name__ == "__main__":
    main()
