#!/usr/bin/env python3
"""Merge a selected-language two-best export with older per-language results."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import iter_jsonl, load_source_rows, preview, wanted_langs


DEFAULT_SELECTED_LANGS = (
    "arz_Arab,bel_Cyrl,ces_Latn,deu_Latn,ekk_Latn,hye_Armn,ind_Latn,isl_Latn,"
    "jpn_Jpan,kaz_Cyrl,kor_Hang,lij_Latn,lld_Latn,rus_Cyrl,sme_Latn,tha_Thai,"
    "ukr_Cyrl,zho_Hans,zho_Hant_TW"
)

DEFAULT_OLDER_LANGS = (
    "arz,cs,cs_CZ,de_AT,de_CH,de_DE,de_IT,et_EE,is,ko_KR,ru,ru_RU,vie_Latn,zh_CN"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Merge the selected-language two-best output with the older merged "
            "per-language results and write a full source-ordered final JSONL."
        )
    )
    parser.add_argument("--selected-input", type=Path, required=True)
    parser.add_argument("--older-input", type=Path, default=None)
    parser.add_argument("--older-merged-dir", type=Path, default=None)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--filtered-source-out", type=Path, default=None)
    parser.add_argument("--per-lang-dir", type=Path, default=None)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument("--selected-langs", default=DEFAULT_SELECTED_LANGS)
    parser.add_argument("--older-langs", default=DEFAULT_OLDER_LANGS)
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail on missing/extra rows and language mismatches (default: true)",
    )
    return parser.parse_args()


def load_flat_rows(path: Path) -> tuple[dict[str, dict[str, dict[str, Any]]], list[str]]:
    by_lang: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    malformed: list[str] = []
    duplicates: list[str] = []
    for line_no, record in iter_jsonl(path):
        lang = record.get("tgt_lang")
        doc_id = record.get("doc_id")
        if not isinstance(lang, str) or not isinstance(doc_id, str):
            malformed.append(f"{path}:{line_no}: expected string tgt_lang and doc_id")
            continue
        if doc_id in by_lang[lang]:
            duplicates.append(f"{lang}:{doc_id}")
            continue
        by_lang[lang][doc_id] = record
    if duplicates:
        malformed.append(
            f"{path}: duplicate (tgt_lang, doc_id) rows: {preview(sorted(duplicates), limit=10)}"
        )
    return dict(by_lang), malformed


def load_per_lang_rows(
    merged_dir: Path, expected_langs: set[str]
) -> tuple[dict[str, dict[str, dict[str, Any]]], list[str], list[str]]:
    by_lang: dict[str, dict[str, dict[str, Any]]] = {}
    malformed: list[str] = []
    missing_files: list[str] = []

    for lang in sorted(expected_langs):
        path = merged_dir / f"{lang}.jsonl"
        if not path.is_file():
            missing_files.append(lang)
            continue
        rows_for_lang: dict[str, dict[str, Any]] = {}
        duplicates: list[str] = []
        for line_no, record in iter_jsonl(path):
            doc_id = record.get("doc_id")
            row_lang = record.get("tgt_lang")
            if not isinstance(doc_id, str) or not isinstance(row_lang, str):
                malformed.append(f"{path}:{line_no}: expected string doc_id and tgt_lang")
                continue
            if row_lang != lang:
                malformed.append(
                    f"{path}:{line_no}: expected tgt_lang={lang!r}, got {row_lang!r}"
                )
                continue
            if doc_id in rows_for_lang:
                duplicates.append(doc_id)
                continue
            rows_for_lang[doc_id] = record
        if duplicates:
            malformed.append(
                f"{path}: duplicate doc_id(s): {preview(sorted(duplicates), limit=10)}"
            )
        by_lang[lang] = rows_for_lang

    return by_lang, malformed, missing_files


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in rows:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    selected_input = args.selected_input.resolve()
    older_input = args.older_input.resolve() if args.older_input is not None else None
    older_merged_dir = (
        args.older_merged_dir.resolve() if args.older_merged_dir is not None else None
    )
    source_path = args.source.resolve()
    out_path = args.out.resolve()

    selected_langs = wanted_langs(args.selected_langs)
    older_langs = wanted_langs(args.older_langs)
    if selected_langs is None or older_langs is None:
        raise SystemExit("selected-langs and older-langs must not be 'all'")
    if selected_langs & older_langs:
        raise SystemExit(
            "selected-langs and older-langs overlap: "
            f"{preview(sorted(selected_langs & older_langs), limit=10)}"
        )

    if not selected_input.is_file():
        raise SystemExit(f"missing selected input: {selected_input}")
    if older_input is None and older_merged_dir is None:
        raise SystemExit("either --older-input or --older-merged-dir is required")
    if older_input is not None and not older_input.is_file():
        raise SystemExit(f"missing older input: {older_input}")
    if older_merged_dir is not None and not older_merged_dir.is_dir():
        raise SystemExit(f"missing older merged dir: {older_merged_dir}")
    if not source_path.is_file():
        raise SystemExit(f"missing source file: {source_path}")

    all_langs = selected_langs | older_langs
    source_rows, source_by_lang = load_source_rows(source_path, all_langs)

    missing_source_langs = sorted(all_langs - set(source_by_lang))
    if missing_source_langs:
        raise SystemExit(
            "missing expected languages in source: "
            f"{preview(missing_source_langs, limit=10)}"
        )

    selected_rows, selected_malformed = load_flat_rows(selected_input)
    if selected_malformed:
        raise SystemExit(f"malformed selected input: {preview(selected_malformed, limit=3)}")

    selected_found = set(selected_rows)
    missing_selected_langs = sorted(selected_langs - selected_found)
    unexpected_selected_langs = sorted(selected_found - selected_langs)
    if missing_selected_langs:
        raise SystemExit(
            "selected input is missing expected languages: "
            f"{preview(missing_selected_langs, limit=10)}"
        )
    if args.strict and unexpected_selected_langs:
        raise SystemExit(
            "selected input has unexpected languages: "
            f"{preview(unexpected_selected_langs, limit=10)}"
        )

    if older_input is not None:
        older_rows, older_malformed = load_flat_rows(older_input)
        missing_older_files: list[str] = []
        if older_malformed:
            raise SystemExit(f"malformed older input: {preview(older_malformed, limit=3)}")
        older_rows = {
            lang: rows for lang, rows in older_rows.items() if lang in older_langs
        }
        older_found = set(older_rows)
        missing_older_langs = sorted(older_langs - older_found)
        if missing_older_langs:
            raise SystemExit(
                "older input is missing expected languages: "
                f"{preview(missing_older_langs, limit=10)}"
            )
    else:
        assert older_merged_dir is not None
        older_rows, older_malformed, missing_older_files = load_per_lang_rows(
            older_merged_dir, older_langs
        )
        if older_malformed:
            raise SystemExit(
                f"malformed older merged rows: {preview(older_malformed, limit=3)}"
            )
        if missing_older_files:
            raise SystemExit(
                "older merged dir is missing expected language files: "
                f"{preview(sorted(missing_older_files), limit=10)}"
            )

    merged_rows: list[dict[str, Any]] = []
    filtered_source_rows: list[dict[str, Any]] = []
    by_lang_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected_used: set[tuple[str, str]] = set()
    older_used: set[tuple[str, str]] = set()
    failures: list[str] = []

    for source_row in source_rows:
        lang = source_row["tgt_lang"]
        doc_id = source_row["doc_id"]

        if lang in selected_langs:
            record = selected_rows.get(lang, {}).get(doc_id)
            if record is not None:
                selected_used.add((lang, doc_id))
        else:
            record = older_rows.get(lang, {}).get(doc_id)
            if record is not None:
                older_used.add((lang, doc_id))

        if record is None:
            failures.append(f"missing row for {lang}:{doc_id}")
            continue

        if record.get("doc_id") != doc_id or record.get("tgt_lang") != lang:
            failures.append(f"field mismatch for {lang}:{doc_id}")
            continue

        merged_rows.append(record)
        filtered_source_rows.append(source_row)
        by_lang_rows[lang].append(record)

    if failures:
        raise SystemExit(f"merge failures: {preview(failures, limit=5)}")

    selected_expected_pairs = {
        (row["tgt_lang"], row["doc_id"])
        for lang in selected_langs
        for row in source_by_lang[lang]
    }
    older_expected_pairs = {
        (row["tgt_lang"], row["doc_id"])
        for lang in older_langs
        for row in source_by_lang[lang]
    }

    selected_loaded_pairs = {
        (lang, doc_id)
        for lang, rows in selected_rows.items()
        for doc_id in rows
    }
    older_loaded_pairs = {
        (lang, doc_id)
        for lang, rows in older_rows.items()
        for doc_id in rows
    }

    missing_selected_rows = sorted(selected_expected_pairs - selected_used)
    missing_older_rows = sorted(older_expected_pairs - older_used)
    extra_selected_rows = sorted(selected_loaded_pairs - selected_expected_pairs)
    extra_older_rows = sorted(older_loaded_pairs - older_expected_pairs)

    if missing_selected_rows:
        raise SystemExit(
            "selected input is missing expected rows: "
            f"{preview([f'{lang}:{doc_id}' for lang, doc_id in missing_selected_rows], limit=10)}"
        )
    if missing_older_rows:
        raise SystemExit(
            "older merged input is missing expected rows: "
            f"{preview([f'{lang}:{doc_id}' for lang, doc_id in missing_older_rows], limit=10)}"
        )
    if args.strict and extra_selected_rows:
        raise SystemExit(
            "selected input has rows not present in source: "
            f"{preview([f'{lang}:{doc_id}' for lang, doc_id in extra_selected_rows], limit=10)}"
        )
    if args.strict and extra_older_rows:
        raise SystemExit(
            "older merged input has rows not present in source: "
            f"{preview([f'{lang}:{doc_id}' for lang, doc_id in extra_older_rows], limit=10)}"
        )

    write_jsonl(out_path, merged_rows)

    if args.filtered_source_out is not None:
        write_jsonl(args.filtered_source_out.resolve(), filtered_source_rows)

    if args.per_lang_dir is not None:
        per_lang_dir = args.per_lang_dir.resolve()
        per_lang_dir.mkdir(parents=True, exist_ok=True)
        for lang, rows in sorted(by_lang_rows.items()):
            write_jsonl(per_lang_dir / f"{lang}.jsonl", rows)

    report = {
        "selected_input": str(selected_input),
        "older_input": str(older_input) if older_input is not None else None,
        "older_merged_dir": str(older_merged_dir) if older_merged_dir is not None else None,
        "source": str(source_path),
        "output": str(out_path),
        "selected_lang_count": len(selected_langs),
        "older_lang_count": len(older_langs),
        "merged_lang_count": len(all_langs),
        "selected_langs": sorted(selected_langs),
        "older_langs": sorted(older_langs),
        "selected_rows": len(selected_used),
        "older_rows": len(older_used),
        "merged_rows": len(merged_rows),
    }
    if args.report_json is not None:
        report_path = args.report_json.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"selected input: {selected_input}")
    print(f"older merged dir: {older_merged_dir}")
    print(f"source: {source_path}")
    print(f"output: {out_path}")
    print(f"selected languages: {len(selected_langs)}")
    print(f"older languages: {len(older_langs)}")
    print(f"merged languages: {len(all_langs)}")
    print(f"selected rows: {len(selected_used)}")
    print(f"older rows: {len(older_used)}")
    print(f"merged rows: {len(merged_rows)}")


if __name__ == "__main__":
    main()
