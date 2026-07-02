#!/usr/bin/env python3
"""Score blind human annotations for randomized best-pair comparisons."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from common import iter_jsonl, preview


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANNOTATION_DIR = (
    REPO_ROOT
    / "results/gemini-2.5-flash/experiments/gpt-final_rus_Cyrl_rubric-v5/annotation"
)
DEFAULT_BLIND = DEFAULT_ANNOTATION_DIR / "best_pair_annotation_blind.jsonl"
DEFAULT_KEY = DEFAULT_ANNOTATION_DIR / "best_pair_annotation_key.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Recover win counts from a blind best-pair human annotation file."
        )
    )
    parser.add_argument("--blind", type=Path, default=DEFAULT_BLIND)
    parser.add_argument("--key", type=Path, default=DEFAULT_KEY)
    return parser.parse_args()


def load_by_pair_id(path: Path) -> dict[str, tuple[int, dict]]:
    rows: dict[str, tuple[int, dict]] = {}
    for line_no, record in iter_jsonl(path):
        pair_id = record.get("pair_id")
        if not isinstance(pair_id, str):
            raise SystemExit(f"{path}:{line_no}: expected string pair_id")
        if pair_id in rows:
            raise SystemExit(f"{path}:{line_no}: duplicate pair_id={pair_id}")
        rows[pair_id] = (line_no, record)
    return rows


def normalize_winner(value: object) -> str:
    if not isinstance(value, str):
        return ""
    winner = value.strip().lower()
    if winner in {"a", "b", "tie"}:
        return winner
    return ""


def pct(n: int, d: int) -> str:
    if d == 0:
        return "n/a"
    return f"{100.0 * n / d:.2f}%"


def main() -> None:
    args = parse_args()
    blind_path = args.blind.resolve()
    key_path = args.key.resolve()

    for path in (blind_path, key_path):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    blind_rows = load_by_pair_id(blind_path)
    key_rows = load_by_pair_id(key_path)

    blind_ids = set(blind_rows)
    key_ids = set(key_rows)
    if blind_ids != key_ids:
        missing_in_key = sorted(blind_ids - key_ids)
        missing_in_blind = sorted(key_ids - blind_ids)
        problems: list[str] = []
        if missing_in_key:
            problems.append(f"missing in key: {preview(missing_in_key, limit=5)}")
        if missing_in_blind:
            problems.append(f"missing in blind: {preview(missing_in_blind, limit=5)}")
        raise SystemExit("pair_id mismatch: " + "; ".join(problems))

    label_wins: Counter[str] = Counter()
    doc_wins: Counter[str] = Counter()
    invalid_rows: list[str] = []
    pending_rows: list[str] = []
    annotated = 0

    label_a_name = ""
    label_b_name = ""

    for pair_id in sorted(blind_ids):
        blind_line_no, blind_row = blind_rows[pair_id]
        key_line_no, key_row = key_rows[pair_id]

        doc_id = blind_row.get("doc_id")
        if not isinstance(doc_id, str):
            invalid_rows.append(f"{blind_path}:{blind_line_no}: invalid doc_id")
            continue

        label_a = key_row.get("candidate_a_label")
        label_b = key_row.get("candidate_b_label")
        if not isinstance(label_a, str) or not isinstance(label_b, str):
            invalid_rows.append(
                f"{key_path}:{key_line_no}: missing candidate labels for {pair_id}"
            )
            continue
        label_a_name = key_row.get("label_a", label_a_name) or label_a_name
        label_b_name = key_row.get("label_b", label_b_name) or label_b_name

        winner = normalize_winner(blind_row.get("human_winner"))
        if not winner:
            raw = blind_row.get("human_winner")
            if isinstance(raw, str) and raw.strip():
                invalid_rows.append(
                    f"{blind_path}:{blind_line_no}: invalid human_winner={raw!r}"
                )
            else:
                pending_rows.append(pair_id)
            continue

        annotated += 1
        if winner == "a":
            label_wins[label_a] += 1
            doc_wins[doc_id] += 1
        elif winner == "b":
            label_wins[label_b] += 1
            doc_wins[doc_id] += 1
        else:
            label_wins["tie"] += 1

    decided = annotated - label_wins["tie"]
    total = len(blind_ids)

    print(f"blind:     {blind_path}")
    print(f"key:       {key_path}")
    print(f"total:     {total}")
    print(f"annotated: {annotated}")
    print(f"pending:   {len(pending_rows)}")
    print(f"invalid:   {len(invalid_rows)}")
    print()
    print("| Outcome | Count | Share |")
    print("|---|---:|---:|")
    if label_a_name:
        print(
            f"| `{label_a_name}` | {label_wins[label_a_name]} | "
            f"{pct(label_wins[label_a_name], decided)} |"
        )
    if label_b_name:
        print(
            f"| `{label_b_name}` | {label_wins[label_b_name]} | "
            f"{pct(label_wins[label_b_name], decided)} |"
        )
    print(f"| `tie` | {label_wins['tie']} | {pct(label_wins['tie'], annotated)} |")

    if invalid_rows:
        print()
        print("invalid rows:")
        for row in invalid_rows[:10]:
            print(f"- {row}")
        if len(invalid_rows) > 10:
            print(f"- ... and {len(invalid_rows) - 10} more")


if __name__ == "__main__":
    main()
