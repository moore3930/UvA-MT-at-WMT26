#!/usr/bin/env python3
"""Create a blind annotation set from two matrix files' chosen best outputs."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from common import iter_jsonl


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX_A = (
    REPO_ROOT / "results/gemini-2.5-flash/artifacts/gpt-final/matrix/rus_Cyrl-llm-matrix.jsonl"
)
DEFAULT_MATRIX_B = (
    REPO_ROOT
    / "results/gemini-2.5-flash/experiments/gpt-final_rus_Cyrl_rubric-v5/rus_Cyrl-llm-matrix.jsonl"
)
DEFAULT_OUT_DIR = (
    REPO_ROOT
    / "results/gemini-2.5-flash/experiments/gpt-final_rus_Cyrl_rubric-v5/annotation"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a blind human-annotation set from docs where two judge runs "
            "chose different best hypotheses."
        )
    )
    parser.add_argument("--matrix-a", type=Path, default=DEFAULT_MATRIX_A)
    parser.add_argument("--matrix-b", type=Path, default=DEFAULT_MATRIX_B)
    parser.add_argument("--label-a", default="default")
    parser.add_argument("--label-b", default="rubric_v5")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--seed", type=int, default=20260702)
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="max number of disagreement docs to include (default: all)",
    )
    return parser.parse_args()


def load_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        hypos = record.get("hypos")
        best = record.get("best")
        source_doc = record.get("source_doc")
        tgt_lang = record.get("tgt_lang")
        if not isinstance(doc_id, str):
            raise SystemExit(f"{path}:{line_no}: expected string doc_id")
        if doc_id in rows:
            raise SystemExit(f"{path}:{line_no}: duplicate doc_id={doc_id}")
        if not isinstance(best, int):
            raise SystemExit(f"{path}:{line_no}: expected integer best")
        if not isinstance(hypos, list) or any(not isinstance(x, str) for x in hypos):
            raise SystemExit(f"{path}:{line_no}: expected list[str] hypos")
        if best < 0 or best >= len(hypos):
            raise SystemExit(f"{path}:{line_no}: best={best} out of range")
        if not isinstance(source_doc, str):
            raise SystemExit(f"{path}:{line_no}: expected string source_doc")
        if not isinstance(tgt_lang, str):
            raise SystemExit(f"{path}:{line_no}: expected string tgt_lang")
        rows[doc_id] = record
    return rows


def main() -> None:
    args = parse_args()
    matrix_a_path = args.matrix_a.resolve()
    matrix_b_path = args.matrix_b.resolve()
    out_dir = args.out_dir.resolve()

    for path in (matrix_a_path, matrix_b_path):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    rows_a = load_rows(matrix_a_path)
    rows_b = load_rows(matrix_b_path)
    shared_doc_ids = sorted(set(rows_a) & set(rows_b))
    if not shared_doc_ids:
        raise SystemExit("no shared doc_ids between the two matrix files")

    disagreement_doc_ids = []
    for doc_id in shared_doc_ids:
        rec_a = rows_a[doc_id]
        rec_b = rows_b[doc_id]
        best_a = rec_a["hypos"][rec_a["best"]]
        best_b = rec_b["hypos"][rec_b["best"]]
        if best_a != best_b:
            disagreement_doc_ids.append(doc_id)

    total_disagreement_docs = len(disagreement_doc_ids)
    rng = random.Random(args.seed)
    rng.shuffle(disagreement_doc_ids)
    if args.limit > 0:
        disagreement_doc_ids = disagreement_doc_ids[: args.limit]

    out_dir.mkdir(parents=True, exist_ok=True)
    blind_path = out_dir / "best_pair_annotation_blind.jsonl"
    key_path = out_dir / "best_pair_annotation_key.jsonl"
    summary_path = out_dir / "best_pair_annotation_summary.md"

    with blind_path.open("w", encoding="utf-8") as blind_handle, key_path.open(
        "w", encoding="utf-8"
    ) as key_handle:
        for idx, doc_id in enumerate(disagreement_doc_ids, start=1):
            rec_a = rows_a[doc_id]
            rec_b = rows_b[doc_id]
            best_text_a = rec_a["hypos"][rec_a["best"]]
            best_text_b = rec_b["hypos"][rec_b["best"]]

            if rng.random() < 0.5:
                candidate_a = best_text_a
                candidate_b = best_text_b
                candidate_a_label = args.label_a
                candidate_b_label = args.label_b
            else:
                candidate_a = best_text_b
                candidate_b = best_text_a
                candidate_a_label = args.label_b
                candidate_b_label = args.label_a

            pair_id = f"best-pair-{idx:04d}"
            blind_row = {
                "pair_id": pair_id,
                "doc_id": doc_id,
                "tgt_lang": rec_a["tgt_lang"],
                "source_doc": rec_a["source_doc"],
                "candidate_a": candidate_a,
                "candidate_b": candidate_b,
                "human_winner": "",
                "notes": "",
            }
            key_row = {
                "pair_id": pair_id,
                "doc_id": doc_id,
                "tgt_lang": rec_a["tgt_lang"],
                "candidate_a_label": candidate_a_label,
                "candidate_b_label": candidate_b_label,
                "label_a": args.label_a,
                "label_b": args.label_b,
                "matrix_a_path": str(matrix_a_path),
                "matrix_b_path": str(matrix_b_path),
                "matrix_a_best_idx": rec_a["best"],
                "matrix_b_best_idx": rec_b["best"],
                "matrix_a_best_text": best_text_a,
                "matrix_b_best_text": best_text_b,
            }
            blind_handle.write(json.dumps(blind_row, ensure_ascii=False) + "\n")
            key_handle.write(json.dumps(key_row, ensure_ascii=False) + "\n")

    summary_path.write_text(
        "\n".join(
            [
                "# Best Pair Annotation Set",
                "",
                f"- Matrix A: `{matrix_a_path}`",
                f"- Matrix B: `{matrix_b_path}`",
                f"- Label A: `{args.label_a}`",
                f"- Label B: `{args.label_b}`",
                f"- Shared docs: `{len(shared_doc_ids)}`",
                f"- Disagreement docs available: `{total_disagreement_docs}`",
                f"- Docs written to blind file: `{len(disagreement_doc_ids)}`",
                f"- Seed: `{args.seed}`",
                f"- Blind file: `{blind_path}`",
                f"- Key file: `{key_path}`",
                "",
                "Annotate `human_winner` in the blind file with one of:",
                "- `A`",
                "- `B`",
                "- `tie`",
                "",
                "You can also add free-form comments in `notes`.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"blind: {blind_path}")
    print(f"key:   {key_path}")
    print(f"docs:  {len(disagreement_doc_ids)}")


if __name__ == "__main__":
    main()
