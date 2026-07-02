#!/usr/bin/env python3
"""Build a per-hypothesis structural-alignment mask for matrix outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import load_matrix_rows, load_source_rows, pct, preview, wanted_langs
from structure_alignment import check_structure


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "wmt26_genmt_blindset_filter_parse.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate every hypothesis structurally and write a mask JSONL."
    )
    parser.add_argument("--matrix-dir", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument("--matrix-lang-prefix", default="")
    parser.add_argument("--langs", default="all")
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail on coverage/malformed issues (default: true)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_path = args.source.resolve()
    matrix_dir = args.matrix_dir.resolve()
    out_path = args.out.resolve()
    langs = wanted_langs(args.langs)

    if not source_path.is_file():
        raise SystemExit(f"missing source file: {source_path}")
    if not matrix_dir.is_dir():
        raise SystemExit(f"missing matrix dir: {matrix_dir}")

    source_rows, expected_by_lang = load_source_rows(source_path, langs)
    matrix_by_lang, malformed = load_matrix_rows(matrix_dir, args.matrix_lang_prefix, langs)

    expected_langs = set(expected_by_lang)
    actual_langs = set(matrix_by_lang)
    missing_files = sorted(expected_langs - actual_langs)
    extra_files = sorted(actual_langs - expected_langs)

    failures = 0
    total_expected = 0
    total_actual = 0
    total_matched = 0

    checked_docs = 0
    aligned_best_docs = 0
    docs_with_invalid_best = 0
    docs_with_no_valid_hypothesis = 0
    kind_counts = {"html": 0, "json": 0, "unstructured": 0}

    report: dict[str, Any] = {
        "source": str(source_path),
        "matrix_dir": str(matrix_dir),
        "output": str(out_path),
        "strict": args.strict,
        "missing_files": missing_files,
        "extra_files": extra_files,
        "malformed": malformed,
        "checked_docs": 0,
        "aligned_best_docs": 0,
        "docs_with_invalid_best": 0,
        "docs_with_no_valid_hypothesis": 0,
        "kind_counts": kind_counts,
        "per_lang": [],
    }

    print(f"source: {source_path}")
    print(f"matrix:  {matrix_dir}")
    print(f"mask:    {out_path}")
    print(f"languages: expected={len(expected_langs)} actual={len(actual_langs)}")

    if missing_files:
        failures += len(missing_files)
        print(
            f"MISSING FILES ({len(missing_files)}): "
            f"{preview([f'{lang}-llm-matrix.jsonl' for lang in missing_files], limit=10)}"
        )
    if extra_files:
        failures += len(extra_files)
        print(
            f"EXTRA FILES ({len(extra_files)}): "
            f"{preview([f'{lang}-llm-matrix.jsonl' for lang in extra_files], limit=10)}"
        )
    if malformed:
        failures += len(malformed)
        print(f"MALFORMED ({len(malformed)}): {preview(malformed, limit=3)}")

    for lang in sorted(expected_langs & actual_langs):
        expected_rows = expected_by_lang[lang]
        actual_rows = matrix_by_lang[lang]
        expected_ids = [row["doc_id"] for row in expected_rows]
        expected_set = set(expected_ids)
        actual_set = set(actual_rows)
        matched = expected_set & actual_set
        missing_ids = sorted(expected_set - actual_set)
        extra_ids = sorted(actual_set - expected_set)

        total_expected += len(expected_set)
        total_actual += len(actual_set)
        total_matched += len(matched)

        report["per_lang"].append(
            {
                "lang": lang,
                "expected": len(expected_set),
                "actual": len(actual_set),
                "matched": len(matched),
                "missing_ids": missing_ids,
                "extra_ids": extra_ids,
            }
        )

        if not missing_ids and not extra_ids:
            print(
                f"OK   {lang:12} rows={len(actual_rows)} expected={len(expected_set)} "
                f"recall={pct(len(matched), len(expected_set))} "
                f"precision={pct(len(matched), len(actual_set))}"
            )
        else:
            failures += 1
            print(
                f"BAD  {lang:12} rows={len(actual_rows)} expected={len(expected_set)} "
                f"missing={len(missing_ids)} extra={len(extra_ids)} "
                f"recall={pct(len(matched), len(expected_set))} "
                f"precision={pct(len(matched), len(actual_set))}"
            )
            if missing_ids:
                print(f"  missing: {preview(missing_ids)}")
            if extra_ids:
                print(f"  extra: {preview(extra_ids)}")

    for lang in missing_files:
        total_expected += len(expected_by_lang[lang])
    for lang in extra_files:
        total_actual += len(matrix_by_lang[lang])

    if args.strict and failures:
        if args.report_json is not None:
            args.report_json.parent.mkdir(parents=True, exist_ok=True)
            args.report_json.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        raise SystemExit(1)

    source_lookup = {(row["tgt_lang"], row["doc_id"]): row for row in source_rows}
    out_rows: list[dict[str, Any]] = []
    for (lang, doc_id), source_row in source_lookup.items():
        matrix_info = matrix_by_lang.get(lang, {}).get(doc_id)
        if matrix_info is None:
            continue

        hypos = matrix_info["hypos"]
        best_idx = matrix_info["best_idx"]
        checks = [check_structure(source_row.get("source_doc", ""), hypo) for hypo in hypos]
        mask = [1 if check["passed"] else 0 for check in checks]
        valid_indices = [idx for idx, bit in enumerate(mask) if bit == 1]
        kind = checks[0]["kind"] if checks else "unstructured"
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        checked_docs += 1
        if mask[best_idx] == 1:
            aligned_best_docs += 1
        else:
            docs_with_invalid_best += 1
        if not valid_indices:
            docs_with_no_valid_hypothesis += 1

        out_rows.append(
            {
                "doc_id": doc_id,
                "tgt_lang": lang,
                "matrix_file": matrix_info["path"].name,
                "check_kind": kind,
                "source_metric": checks[0]["source_metric"] if checks else None,
                "hypothesis_metrics": [check["hypothesis_metric"] for check in checks],
                "alignment_mask": mask,
                "valid_hypothesis_indices": valid_indices,
                "judge_best_idx": best_idx,
                "judge_best_passed": bool(mask[best_idx]),
                "k": len(hypos),
            }
        )

    report.update(
        {
            "checked_docs": checked_docs,
            "aligned_best_docs": aligned_best_docs,
            "docs_with_invalid_best": docs_with_invalid_best,
            "docs_with_no_valid_hypothesis": docs_with_no_valid_hypothesis,
            "kind_counts": kind_counts,
            "written_rows": len(out_rows),
            "overall": {
                "matched": total_matched,
                "expected": total_expected,
                "actual": total_actual,
            },
        }
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for row in out_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.report_json is not None:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(
        "OVERALL "
        f"matched={total_matched} expected={total_expected} actual={total_actual} "
        f"recall={pct(total_matched, total_expected)} "
        f"precision={pct(total_matched, total_actual)}"
    )
    print(
        "MASK "
        f"docs={checked_docs} best_valid={aligned_best_docs} "
        f"best_invalid={docs_with_invalid_best} no_valid={docs_with_no_valid_hypothesis}"
    )
    print(f"wrote {len(out_rows)} mask rows to {out_path}")


if __name__ == "__main__":
    main()
