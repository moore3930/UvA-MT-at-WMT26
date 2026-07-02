#!/usr/bin/env python3
"""Report judge position-disagreement rates by language for two matrix dirs."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from common import iter_jsonl, preview


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUBMISSION = (
    REPO_ROOT
    / "final_submission/out/two-best/gemini-3.5-flash__gpt-final/submission.jsonl"
)
DEFAULT_MODEL_A_DIR = (
    REPO_ROOT / "results/gemini-2.5-flash/artifacts/gemini-3.5-flash/matrix"
)
DEFAULT_MODEL_B_DIR = (
    REPO_ROOT / "results/gemini-2.5-flash/artifacts/gpt-final/matrix"
)
DEFAULT_MODEL_A_NAME = "gemini-3.5-flash"
DEFAULT_MODEL_B_NAME = "gpt-final"


@dataclass
class LangStats:
    docs: int = 0
    disagreements: int = 0
    unordered_pairs: int = 0

    @property
    def rate_pct(self) -> float:
        if self.unordered_pairs == 0:
            return 0.0
        return 100.0 * self.disagreements / self.unordered_pairs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate judge position-disagreement rates per language direction "
            "for the two matrix dirs used by a submission."
        )
    )
    parser.add_argument("--submission", type=Path, default=DEFAULT_SUBMISSION)
    parser.add_argument("--model-a-dir", type=Path, default=DEFAULT_MODEL_A_DIR)
    parser.add_argument("--model-b-dir", type=Path, default=DEFAULT_MODEL_B_DIR)
    parser.add_argument("--model-a-name", default=DEFAULT_MODEL_A_NAME)
    parser.add_argument("--model-b-name", default=DEFAULT_MODEL_B_NAME)
    return parser.parse_args()


def load_submission_langs(path: Path) -> list[str]:
    langs: list[str] = []
    seen: set[str] = set()

    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        lang = record.get("tgt_lang")
        if not isinstance(doc_id, str) or not isinstance(lang, str):
            raise SystemExit(f"{path}:{line_no}: expected string doc_id and tgt_lang")
        if lang not in seen:
            seen.add(lang)
            langs.append(lang)

    return langs


def load_lang_stats(matrix_dir: Path, lang: str) -> LangStats:
    path = matrix_dir / f"{lang}-llm-matrix.jsonl"
    if not path.exists():
        raise SystemExit(f"missing matrix file for {lang}: {path}")

    stats = LangStats()
    malformed: list[str] = []
    seen_doc_ids: set[str] = set()

    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        k = record.get("k")
        disagreements = record.get("position_disagreements")
        if not isinstance(doc_id, str):
            malformed.append(f"{path}:{line_no}: expected string doc_id")
            continue
        if doc_id in seen_doc_ids:
            malformed.append(f"{path}:{line_no}: duplicate doc_id={doc_id}")
            continue
        if not isinstance(k, int) or k < 1:
            malformed.append(f"{path}:{line_no}: expected integer k >= 1")
            continue
        if not isinstance(disagreements, int) or disagreements < 0:
            malformed.append(
                f"{path}:{line_no}: expected integer position_disagreements >= 0"
            )
            continue

        unordered_pairs = k * (k - 1) // 2
        if disagreements > unordered_pairs:
            malformed.append(
                f"{path}:{line_no}: position_disagreements={disagreements} exceeds "
                f"{unordered_pairs} unordered pairs"
            )
            continue

        seen_doc_ids.add(doc_id)
        stats.docs += 1
        stats.disagreements += disagreements
        stats.unordered_pairs += unordered_pairs

    if malformed:
        raise SystemExit(f"malformed matrix rows: {preview(malformed, limit=3)}")

    return stats


def main() -> None:
    args = parse_args()
    submission_path = args.submission.resolve()
    model_a_dir = args.model_a_dir.resolve()
    model_b_dir = args.model_b_dir.resolve()

    for path in (submission_path, model_a_dir, model_b_dir):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    langs = load_submission_langs(submission_path)
    rows: list[tuple[str, LangStats, LangStats]] = []
    total_a = LangStats()
    total_b = LangStats()

    for lang in langs:
        stats_a = load_lang_stats(model_a_dir, lang)
        stats_b = load_lang_stats(model_b_dir, lang)
        rows.append((lang, stats_a, stats_b))
        total_a.docs += stats_a.docs
        total_a.disagreements += stats_a.disagreements
        total_a.unordered_pairs += stats_a.unordered_pairs
        total_b.docs += stats_b.docs
        total_b.disagreements += stats_b.disagreements
        total_b.unordered_pairs += stats_b.unordered_pairs

    print(f"submission: {submission_path}")
    print(f"model A:    {args.model_a_name} -> {model_a_dir}")
    print(f"model B:    {args.model_b_name} -> {model_b_dir}")
    print(
        "metric: position_disagreements / unordered candidate pairs "
        "(judge order-sensitivity)"
    )
    print()
    print(f"| Lang | Docs | {args.model_a_name} | {args.model_b_name} |")
    print("|---|---:|---:|---:|")
    print(
        f"| `ALL` | {total_a.docs} | {total_a.rate_pct:.2f}% | "
        f"{total_b.rate_pct:.2f}% |"
    )
    for lang, stats_a, stats_b in rows:
        if stats_a.docs != stats_b.docs:
            raise SystemExit(
                f"{lang}: doc-count mismatch between models: "
                f"{stats_a.docs} vs {stats_b.docs}"
            )
        print(
            f"| `{lang}` | {stats_a.docs} | {stats_a.rate_pct:.2f}% | "
            f"{stats_b.rate_pct:.2f}% |"
        )


if __name__ == "__main__":
    main()
