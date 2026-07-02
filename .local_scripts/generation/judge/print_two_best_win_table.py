#!/usr/bin/env python3
"""Print a simple per-language win table for two-best cross-matrix outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CROSS_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-2.5-flash"
    / "artifacts"
    / "two-best"
    / "gemini-3.5-flash__gpt-final"
    / "cross-matrix"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print a simple table of strict wins, ties, and tie-resolved "
            "selected counts for each finished two-best language file."
        )
    )
    parser.add_argument(
        "--cross-dir",
        type=Path,
        default=DEFAULT_CROSS_DIR,
        help="directory containing *-winner-cross.jsonl files",
    )
    parser.add_argument(
        "--langs",
        default="all",
        help='comma-separated language ids or "all" (default: all)',
    )
    return parser.parse_args()


def wanted_langs(langs_arg: str) -> set[str] | None:
    if langs_arg.strip().lower() in {"all", "*"}:
        return None
    return {part.strip() for part in langs_arg.split(",") if part.strip()}


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


def language_from_path(path: Path) -> str:
    suffix = "-winner-cross"
    stem = path.stem
    if not stem.endswith(suffix):
        raise SystemExit(f"unexpected file name: {path.name}")
    return stem[: -len(suffix)]


def summarize_file(path: Path) -> dict[str, Any]:
    strict_a = strict_b = ties = 0
    selected_a = selected_b = 0
    rows = 0
    model_a_name = model_b_name = None

    for line_no, record in iter_jsonl(path):
        rows += 1
        if model_a_name is None:
            model_a_name = record.get("model_a_name")
            model_b_name = record.get("model_b_name")
        a_total = record.get("model_a_total_score")
        b_total = record.get("model_b_total_score")
        if not isinstance(a_total, (int, float)) or not isinstance(b_total, (int, float)):
            raise SystemExit(f"{path}:{line_no}: missing numeric total scores")

        if a_total > b_total:
            strict_a += 1
        elif b_total > a_total:
            strict_b += 1
        else:
            ties += 1

        selected_name = record.get("selected_model_name")
        if selected_name == model_a_name:
            selected_a += 1
        elif selected_name == model_b_name:
            selected_b += 1
        elif selected_name is None:
            # Backward-compatible fallback for older rows without selected_* fields.
            if a_total > b_total:
                selected_a += 1
            elif b_total > a_total:
                selected_b += 1
        else:
            raise SystemExit(
                f"{path}:{line_no}: selected_model_name={selected_name!r} does not "
                f"match model_a/model_b names"
            )

    if rows == 0:
        raise SystemExit(f"{path}: file is empty")

    return {
        "lang": language_from_path(path),
        "rows": rows,
        "model_a_name": model_a_name or "model_a",
        "model_b_name": model_b_name or "model_b",
        "strict_a": strict_a,
        "strict_b": strict_b,
        "ties": ties,
        "selected_a": selected_a,
        "selected_b": selected_b,
    }


def format_table(rows: list[dict[str, Any]]) -> str:
    headers = [
        "lang",
        "rows",
        "strict_a",
        "strict_b",
        "ties",
        "selected_a",
        "selected_b",
    ]
    table = [headers]
    for row in rows:
        table.append([
            row["lang"],
            str(row["rows"]),
            str(row["strict_a"]),
            str(row["strict_b"]),
            str(row["ties"]),
            str(row["selected_a"]),
            str(row["selected_b"]),
        ])

    widths = [max(len(r[i]) for r in table) for i in range(len(headers))]
    lines = []
    for idx, row in enumerate(table):
        lines.append("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
        if idx == 0:
            lines.append("  ".join("-" * widths[i] for i in range(len(widths))))
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    cross_dir = args.cross_dir.resolve()
    langs = wanted_langs(args.langs)

    if not cross_dir.is_dir():
        raise SystemExit(f"missing cross-matrix dir: {cross_dir}")

    files = sorted(cross_dir.glob("*-winner-cross.jsonl"))
    if not files:
        raise SystemExit(f"no *-winner-cross.jsonl files found in {cross_dir}")

    summaries = []
    for path in files:
        lang = language_from_path(path)
        if langs is not None and lang not in langs:
            continue
        summaries.append(summarize_file(path))

    if not summaries:
        raise SystemExit("no matching language files found")

    model_a_name = summaries[0]["model_a_name"]
    model_b_name = summaries[0]["model_b_name"]
    if any(row["model_a_name"] != model_a_name or row["model_b_name"] != model_b_name for row in summaries):
        raise SystemExit("model names differ across files; refusing to print mixed table")

    print(f"model_a={model_a_name}  model_b={model_b_name}")
    print(format_table(summaries))


if __name__ == "__main__":
    main()
