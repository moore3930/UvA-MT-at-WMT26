#!/usr/bin/env python3
"""Shared helpers for final_submission scripts."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


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


def validate_matrix_record(path: Path, line_no: int, record: dict[str, Any]) -> tuple[int, list[str]]:
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
    if any(not isinstance(hypo, str) for hypo in hypos):
        raise ValueError(f"{path}:{line_no}: all hypos must be strings")
    return best, hypos


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
                best_idx, hypos = validate_matrix_record(path, line_no, record)
            except ValueError as exc:
                malformed.append(str(exc))
                continue

            rows_for_lang[doc_id] = {
                "path": path,
                "lang": lang,
                "record": record,
                "best_idx": best_idx,
                "hypos": hypos,
            }

        if duplicates:
            malformed.append(
                f"{path}: duplicate doc_id(s): {preview(sorted(duplicates), limit=10)}"
            )
        by_lang[lang] = rows_for_lang

    return by_lang, malformed
