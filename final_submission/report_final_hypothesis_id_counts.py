#!/usr/bin/env python3
"""Summarize how often each hypothesis id was selected for each model."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

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
DEFAULT_OUT = DEFAULT_INPUT.parent / "reports" / "final_hypothesis_id_counts.md"
DEFAULT_JSON = DEFAULT_INPUT.parent / "reports" / "final_hypothesis_id_counts.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a markdown report of final hypothesis-id selection counts "
            "for each model from a merged preliminary_final.jsonl."
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


def format_count_table(title: str, counts: Counter[str]) -> list[str]:
    total = sum(counts.values())
    lines = [
        f"## {title}",
        "",
        "| hypothesis id | count | pct within model |",
        "| --- | ---: | ---: |",
    ]
    for hypo_key in sorted(counts, key=lambda x: int(x.split('_', 1)[1])):
        lines.append(
            f"| {hypo_key} | {counts[hypo_key]} | {pct(counts[hypo_key], total)} |"
        )
    lines.append("")
    lines.append(f"- total for model: `{total}`")
    lines.append("")
    return lines


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    out_path = args.out.resolve()
    json_path = args.json_out.resolve()

    if not input_path.is_file():
        raise SystemExit(f"missing input file: {input_path}")

    final_counts: dict[str, Counter[str]] = defaultdict(Counter)
    selected_counts: dict[str, Counter[str]] = defaultdict(Counter)
    switched_rows: list[dict[str, object]] = []
    final_model_totals: Counter[str] = Counter()

    for line_no, row in iter_jsonl(input_path):
        final_model = row.get("two_best_final_model_name")
        final_hypo = row.get("two_best_final_hypo_key")
        selected_model = row.get("two_best_selected_model_name")
        selected_idx = row.get("two_best_selected_best_idx")
        doc_id = row.get("doc_id")
        tgt_lang = row.get("tgt_lang")

        if not isinstance(final_model, str):
            raise SystemExit(
                f"{input_path}:{line_no}: expected string two_best_final_model_name"
            )
        if not isinstance(final_hypo, str):
            raise SystemExit(
                f"{input_path}:{line_no}: expected string two_best_final_hypo_key"
            )
        if not isinstance(selected_model, str):
            raise SystemExit(
                f"{input_path}:{line_no}: expected string two_best_selected_model_name"
            )
        if not isinstance(selected_idx, int):
            raise SystemExit(
                f"{input_path}:{line_no}: expected int two_best_selected_best_idx"
            )

        selected_hypo = f"hypo_{selected_idx}"

        final_counts[final_model][final_hypo] += 1
        selected_counts[selected_model][selected_hypo] += 1
        final_model_totals[final_model] += 1

        if final_model != selected_model or final_hypo != selected_hypo:
            switched_rows.append(
                {
                    "doc_id": doc_id,
                    "tgt_lang": tgt_lang,
                    "selected_model_name": selected_model,
                    "selected_hypo_key": selected_hypo,
                    "final_model_name": final_model,
                    "final_hypo_key": final_hypo,
                    "alignment_fixed": row.get("two_best_alignment_fixed"),
                    "alignment_fix_reason": row.get("two_best_alignment_fix_reason"),
                }
            )

    md_lines = [
        "# Final Hypothesis Id Counts",
        "",
        f"- Input: `{input_path}`",
        f"- Final rows: `{sum(final_model_totals.values())}`",
        f"- Final model totals: `gemini-3.5-flash={final_model_totals['gemini-3.5-flash']}`, `gpt-final={final_model_totals['gpt-final']}`",
        f"- Rows where final model/hypothesis differs from raw selected winner: `{len(switched_rows)}`",
        "",
        "## Summary",
        "",
        "| model | final rows |",
        "| --- | ---: |",
        f"| gemini-3.5-flash | {final_model_totals['gemini-3.5-flash']} |",
        f"| gpt-final | {final_model_totals['gpt-final']} |",
        "",
    ]

    for model_name in sorted(final_counts):
        md_lines.extend(format_count_table(f"{model_name} Final Counts", final_counts[model_name]))

    md_lines.extend(
        [
            "## Final Vs Raw Selected Differences",
            "",
            "| doc_id | tgt_lang | selected model | selected hypo | final model | final hypo | reason |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in switched_rows:
        md_lines.append(
            "| {doc_id} | {tgt_lang} | {selected_model_name} | {selected_hypo_key} | {final_model_name} | {final_hypo_key} | {alignment_fix_reason} |".format(
                **row
            )
        )

    report = {
        "input": str(input_path),
        "final_model_totals": dict(final_model_totals),
        "final_counts": {k: dict(v) for k, v in final_counts.items()},
        "selected_counts": {k: dict(v) for k, v in selected_counts.items()},
        "switched_rows": switched_rows,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"input: {input_path}")
    print(f"markdown: {out_path}")
    print(f"json: {json_path}")
    print(
        "final_rows: %d switched_rows: %d"
        % (sum(final_model_totals.values()), len(switched_rows))
    )


if __name__ == "__main__":
    main()
