#!/usr/bin/env python3
"""Build a source-ordered final JSONL from matrix judge outputs.

The source JSONL is the canonical order. For each source row, this script finds
the corresponding matrix row by (tgt_lang, doc_id), extracts the best
hypothesis via `hypos[best]`, and writes an aligned audit-friendly final file.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "wmt26_genmt_blindset_filter_parse.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Align matrix judge outputs to the source JSONL order and emit an "
            "audit-friendly final file."
        )
    )
    parser.add_argument(
        "--matrix-dir",
        type=Path,
        required=True,
        help="directory containing *-llm-matrix.jsonl files",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"source jsonl whose row order is canonical (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="output aligned final jsonl path",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=None,
        help="optional machine-readable report path",
    )
    parser.add_argument(
        "--matrix-lang-prefix",
        default="",
        help="optional filename prefix before <lang>-llm-matrix.jsonl",
    )
    parser.add_argument(
        "--langs",
        default="all",
        help="comma-separated target languages to include, or 'all'",
    )
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail on any missing/extra/malformed data (default: true)",
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


def wanted_langs(langs_arg: str) -> set[str] | None:
    if langs_arg.strip().lower() in {"all", "*"}:
        return None
    return {part.strip() for part in langs_arg.split(",") if part.strip()}


def matrix_lang_from_path(path: Path, prefix: str) -> str:
    stem = path.stem
    suffix = "-llm-matrix"
    if not stem.endswith(suffix):
        raise ValueError(f"unexpected matrix filename: {path.name}")
    lang = stem[: -len(suffix)]
    if prefix and lang.startswith(prefix):
        lang = lang[len(prefix):]
    return lang


def preview(values: list[str], limit: int = 5) -> str:
    if not values:
        return "-"
    shown = ", ".join(values[:limit])
    if len(values) > limit:
        shown += ", ..."
    return shown


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "n/a"
    return f"{numerator / denominator:.2%}"


def load_source_rows(source_path: Path, langs: set[str] | None):
    rows: list[dict[str, Any]] = []
    by_lang: dict[str, list[dict[str, Any]]] = defaultdict(list)
    duplicates: list[str] = []
    seen_pairs: set[tuple[str, str]] = set()

    for line_no, record in iter_jsonl(source_path):
        lang = record.get("tgt_lang")
        doc_id = record.get("doc_id")
        if not isinstance(lang, str) or not isinstance(doc_id, str):
            raise SystemExit(
                f"{source_path}:{line_no}: expected string tgt_lang and doc_id"
            )
        if langs is not None and lang not in langs:
            continue
        pair = (lang, doc_id)
        if pair in seen_pairs:
            duplicates.append(f"{lang}:{doc_id}")
        seen_pairs.add(pair)
        rows.append(record)
        by_lang[lang].append(record)

    if duplicates:
        raise SystemExit(
            "duplicate (tgt_lang, doc_id) pairs in source: "
            f"{preview(sorted(duplicates), limit=10)}"
        )
    return rows, by_lang


def validate_best_and_choose(path: Path, line_no: int, record: dict[str, Any]) -> tuple[int, str]:
    best = record.get("best")
    hypos = record.get("hypos")
    if not isinstance(best, int):
        raise ValueError(f"{path}:{line_no}: missing integer best")
    if not isinstance(hypos, list) or not hypos:
        raise ValueError(f"{path}:{line_no}: missing non-empty hypos list")
    if best < 0 or best >= len(hypos):
        raise ValueError(
            f"{path}:{line_no}: best={best} out of range for {len(hypos)} hypos"
        )
    chosen = hypos[best]
    if not isinstance(chosen, str):
        raise ValueError(f"{path}:{line_no}: chosen hypothesis is not a string")
    return best, chosen


def load_matrix_rows(matrix_dir: Path, prefix: str, langs: set[str] | None):
    files = sorted(matrix_dir.glob("*-llm-matrix.jsonl"))
    if not files:
        raise SystemExit(f"no *-llm-matrix.jsonl files found in {matrix_dir}")

    by_lang: dict[str, dict[str, dict[str, Any]]] = {}
    malformed: list[str] = []

    for path in files:
        try:
            lang = matrix_lang_from_path(path, prefix)
        except ValueError as exc:
            malformed.append(str(exc))
            continue
        if langs is not None and lang not in langs:
            continue

        rows_for_lang: dict[str, dict[str, Any]] = {}
        duplicates: list[str] = []
        for line_no, record in iter_jsonl(path):
            doc_id = record.get("doc_id")
            if not isinstance(doc_id, str):
                malformed.append(f"{path}:{line_no}: expected string doc_id")
                continue
            if doc_id in rows_for_lang:
                duplicates.append(doc_id)
                continue
            try:
                best_idx, chosen = validate_best_and_choose(path, line_no, record)
            except ValueError as exc:
                malformed.append(str(exc))
                continue

            rows_for_lang[doc_id] = {
                "path": path,
                "lang": lang,
                "record": record,
                "best_idx": best_idx,
                "chosen": chosen,
            }

        if duplicates:
            malformed.append(
                f"{path}: duplicate doc_id(s): {preview(sorted(duplicates), limit=10)}"
            )
        by_lang[lang] = rows_for_lang

    return by_lang, malformed


def build_output_row(source_row: dict[str, Any], matrix_info: dict[str, Any]) -> dict[str, Any]:
    record = matrix_info["record"]
    out = dict(source_row)
    out["hypothesis"] = matrix_info["chosen"]
    out["judge_best_idx"] = matrix_info["best_idx"]
    out["judge_best_hypothesis"] = matrix_info["chosen"]
    out["judge_scores"] = record.get("score")
    out["judge_position_disagreements"] = record.get("position_disagreements")
    out["judge_pairs_judged"] = record.get("pairwise_comparisons")
    out["judge_identical_pairs_auto_tied"] = record.get("identical_shortcuts")
    out["judge_matrix_file"] = matrix_info["path"].name
    return out


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
    actual_by_lang, malformed = load_matrix_rows(
        matrix_dir, args.matrix_lang_prefix, langs
    )

    expected_langs = set(expected_by_lang)
    actual_langs = set(actual_by_lang)
    missing_files = sorted(expected_langs - actual_langs)
    extra_files = sorted(actual_langs - expected_langs)

    failures = 0
    total_expected = 0
    total_actual = 0
    total_matched = 0
    report: dict[str, Any] = {
        "source": str(source_path),
        "matrix_dir": str(matrix_dir),
        "output": str(out_path),
        "strict": args.strict,
        "expected_langs": sorted(expected_langs),
        "actual_langs": sorted(actual_langs),
        "missing_files": missing_files,
        "extra_files": extra_files,
        "malformed": malformed,
        "per_lang": [],
    }

    print(f"source: {source_path}")
    print(f"matrix:  {matrix_dir}")
    print(f"output:  {out_path}")
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

    output_rows: list[dict[str, Any]] = []

    for lang in sorted(expected_langs & actual_langs):
        expected_rows = expected_by_lang[lang]
        actual_rows = actual_by_lang[lang]
        expected_ids = [row["doc_id"] for row in expected_rows]
        expected_set = set(expected_ids)
        actual_set = set(actual_rows)
        matched = expected_set & actual_set
        missing_ids = sorted(expected_set - actual_set)
        extra_ids = sorted(actual_set - expected_set)

        total_expected += len(expected_set)
        total_actual += len(actual_set)
        total_matched += len(matched)

        entry = {
            "lang": lang,
            "expected": len(expected_set),
            "actual": len(actual_set),
            "matched": len(matched),
            "missing_ids": missing_ids,
            "extra_ids": extra_ids,
        }
        report["per_lang"].append(entry)

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
        total_actual += len(actual_by_lang[lang])

    print(
        "OVERALL "
        f"matched={total_matched} expected={total_expected} actual={total_actual} "
        f"recall={pct(total_matched, total_expected)} "
        f"precision={pct(total_matched, total_actual)}"
    )

    if args.strict and failures:
        if args.report_json is not None:
            args.report_json.parent.mkdir(parents=True, exist_ok=True)
            args.report_json.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        raise SystemExit(1)

    for source_row in source_rows:
        lang = source_row["tgt_lang"]
        doc_id = source_row["doc_id"]
        matrix_info = actual_by_lang.get(lang, {}).get(doc_id)
        if matrix_info is None:
            if args.strict:
                raise SystemExit(f"missing aligned winner for {lang}:{doc_id}")
            continue

        matrix_source = matrix_info["record"].get("source_doc")
        source_source = source_row.get("source_doc")
        if (
            isinstance(matrix_source, str)
            and isinstance(source_source, str)
            and matrix_source != source_source
        ):
            msg = (
                f"source_doc mismatch for {lang}:{doc_id} "
                f"({matrix_info['path'].name})"
            )
            if args.strict:
                raise SystemExit(msg)
            print(f"WARNING {msg}", file=sys.stderr)

        output_rows.append(build_output_row(source_row, matrix_info))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for record in output_rows:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    if args.report_json is not None:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        report["written_rows"] = len(output_rows)
        args.report_json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"wrote {len(output_rows)} aligned rows to {out_path}")


if __name__ == "__main__":
    main()
