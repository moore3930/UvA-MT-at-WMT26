#!/usr/bin/env python3
"""Merge matrix judge output back into generation JSONL rows."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HYPO_RE = re.compile(r"^hypo_(\d+)$")


def parse_args():
    p = argparse.ArgumentParser(
        description="Merge full round-robin judge results into generation JSONL.")
    p.add_argument("--input", required=True, help="original generation jsonl")
    p.add_argument("--matrix", required=True, help="pairwise_matrix output jsonl")
    p.add_argument("--out", required=True, help="final judged jsonl output path")
    p.add_argument("--judge-model", required=True, help="judge model name")
    p.add_argument("--source-model", default="", help="source generation model name")
    p.add_argument("--judge-mode", default="full_round_robin",
                   help="judge mode label to store in output")
    p.add_argument("--judge-reasoning-effort", default="",
                   help="reasoning effort label to store in output")
    return p.parse_args()


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def extract_hypos(rec: dict) -> list[str]:
    idx = sorted(int(m.group(1)) for k in rec for m in [HYPO_RE.match(k)] if m)
    return [rec[f"hypo_{i}"] for i in idx]


def aggregate_pairwise_stats(winloss: list[list[int]]) -> tuple[list[int], list[int], list[int], list[float]]:
    k = len(winloss)
    wins = [0] * k
    losses = [0] * k
    ties = [0] * k

    for i in range(k):
        for j in range(k):
            if i == j:
                continue
            cell = winloss[i][j]
            if cell == 1:
                wins[i] += 1
                losses[j] += 1
            elif cell == -1:
                wins[j] += 1
                losses[i] += 1
            else:
                ties[i] += 1
                ties[j] += 1

    win_rates = []
    for i in range(k):
        total = wins[i] + losses[i] + ties[i]
        if total:
            win_rates.append((wins[i] + 0.5 * ties[i]) / total)
        else:
            win_rates.append(0.0)
    return wins, losses, ties, win_rates


def main():
    args = parse_args()
    input_path = Path(args.input)
    matrix_path = Path(args.matrix)
    out_path = Path(args.out)

    matrices = {rec["doc_id"]: rec for rec in iter_jsonl(matrix_path)}
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r", encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            doc_id = rec.get("doc_id")
            matrix = matrices.get(doc_id)
            if matrix is None:
                raise SystemExit(f"missing matrix row for doc_id={doc_id}")

            input_hypos = extract_hypos(rec)
            matrix_hypos = list(matrix.get("hypos") or [])
            if input_hypos != matrix_hypos:
                raise SystemExit(f"hypothesis mismatch for doc_id={doc_id}")

            winloss = matrix["winloss"]
            wins = matrix.get("pairwise_wins")
            losses = matrix.get("pairwise_losses")
            ties = matrix.get("pairwise_ties")
            if wins is None or losses is None or ties is None:
                wins, losses, ties, _unused = aggregate_pairwise_stats(winloss)
            _, _, _, win_rates = aggregate_pairwise_stats(winloss)
            best_idx = int(matrix["best"])
            best_field = f"hypo_{best_idx}"

            out_rec = dict(rec)
            out_rec.update({
                "judge_model": args.judge_model,
                "judge_source_model": args.source_model or None,
                "judge_mode": args.judge_mode,
                "judge_reasoning_effort": args.judge_reasoning_effort or None,
                "judge_best_idx": best_idx,
                "judge_best_hypo_key": best_field,
                "judge_best_hypothesis": rec.get(best_field, ""),
                "judge_scores": matrix.get("score"),
                "judge_pairwise_wins": wins,
                "judge_pairwise_losses": losses,
                "judge_pairwise_ties": ties,
                "judge_win_rates": [round(x, 6) for x in win_rates],
                "judge_position_disagreements": matrix.get("position_disagreements"),
                "judge_pairs_judged": matrix.get("pairwise_comparisons"),
                "judge_identical_pairs_auto_tied": matrix.get("identical_shortcuts"),
            })
            fout.write(json.dumps(out_rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
