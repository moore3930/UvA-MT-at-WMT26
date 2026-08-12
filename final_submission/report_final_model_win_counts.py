#!/usr/bin/env python3
"""Summarize final per-model win counts from a merged two-best preliminary file."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import iter_jsonl


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    REPO_ROOT
    / "final_submission"
    / "out"
    / "merge_two_submissions"
    / "gemini-3.5-flash__gpt-final_rubric-v5-structured"
    / "preliminary_final.jsonl"
)
DEFAULT_OUT = DEFAULT_INPUT.parent / "reports" / "final_model_win_counts.md"
DEFAULT_JSON = DEFAULT_INPUT.parent / "reports" / "final_model_win_counts.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a markdown table of final per-language win counts for "
            "gpt-final vs gemini-3.5-flash from a merged preliminary_final.jsonl."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    return parser.parse_args()


def pct(n: int, d: int) -> str:
    if d == 0:
        return "0.00%"
    return f"{(100.0 * n / d):.2f}%"


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    out_path = args.out.resolve()
    json_path = args.json_out.resolve()

    if not input_path.is_file():
        raise SystemExit(f"missing input file: {input_path}")

    overall_final: Counter[str] = Counter()
    overall_selected: Counter[str] = Counter()
    per_lang: dict[str, Counter[str]] = defaultdict(Counter)
    switched_rows = 0
    final_models: set[str] = set()
    selected_models: set[str] = set()

    for line_no, row in iter_jsonl(input_path):
        lang = row.get("tgt_lang")
        final_model = row.get("two_best_final_model_name")
        selected_model = row.get("two_best_selected_model_name")
        if not isinstance(lang, str):
            raise SystemExit(f"{input_path}:{line_no}: expected string tgt_lang")
        if not isinstance(final_model, str):
            raise SystemExit(
                f"{input_path}:{line_no}: expected string two_best_final_model_name"
            )
        if not isinstance(selected_model, str):
            raise SystemExit(
                f"{input_path}:{line_no}: expected string two_best_selected_model_name"
            )

        overall_final[final_model] += 1
        overall_selected[selected_model] += 1
        per_lang[lang]["rows"] += 1
        per_lang[lang][final_model] += 1
        final_models.add(final_model)
        selected_models.add(selected_model)

        if final_model != selected_model:
            switched_rows += 1

    expected_models = {"gemini-3.5-flash", "gpt-final"}
    unexpected = sorted(final_models - expected_models)
    if unexpected:
        raise SystemExit(f"unexpected final model names: {unexpected}")

    rows = []
    for lang in sorted(per_lang):
        total = per_lang[lang]["rows"]
        gemini = per_lang[lang]["gemini-3.5-flash"]
        gpt = per_lang[lang]["gpt-final"]
        winner = "tie"
        if gemini > gpt:
            winner = "gemini-3.5-flash"
        elif gpt > gemini:
            winner = "gpt-final"
        rows.append(
            {
                "lang": lang,
                "rows": total,
                "gemini_3_5_flash": gemini,
                "gpt_final": gpt,
                "gemini_pct": pct(gemini, total),
                "gpt_pct": pct(gpt, total),
                "winner": winner,
            }
        )

    total_rows = sum(row["rows"] for row in rows)
    total_gemini = overall_final["gemini-3.5-flash"]
    total_gpt = overall_final["gpt-final"]

    md_lines = [
        "# Final Model Win Counts",
        "",
        f"- Input: `{input_path}`",
        f"- Total rows: `{total_rows}`",
        f"- Final wins: `gemini-3.5-flash={total_gemini}` (`{pct(total_gemini, total_rows)}`), `gpt-final={total_gpt}` (`{pct(total_gpt, total_rows)}`)",
        f"- Final-vs-selected model switches after alignment fallback: `{switched_rows}`",
        "",
        "| lang | rows | gemini-3.5-flash | gpt-final | gemini % | gpt % | winner |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        md_lines.append(
            "| {lang} | {rows} | {gemini_3_5_flash} | {gpt_final} | {gemini_pct} | {gpt_pct} | {winner} |".format(
                **row
            )
        )

    report = {
        "input": str(input_path),
        "total_rows": total_rows,
        "overall_final": dict(overall_final),
        "overall_selected": dict(overall_selected),
        "switched_rows": switched_rows,
        "rows": rows,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"input: {input_path}")
    print(f"markdown: {out_path}")
    print(f"json: {json_path}")
    print(f"total_rows: {total_rows}")
    print(
        "final_wins: gemini-3.5-flash=%d gpt-final=%d switched_rows=%d"
        % (total_gemini, total_gpt, switched_rows)
    )


if __name__ == "__main__":
    main()
