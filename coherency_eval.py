#!/usr/bin/env python3
"""coherency_eval.py

Measure how consistent the LLM pairwise judgements are with the HUMAN scores.

Inputs per language pair:
  - dev/<pair>.jsonl            : holds raw human scores score_0..score_{K-1}
                                  (and hypo_0.., used to rebuild the human matrix
                                   at any threshold)
  - dev/<pair>-llm-matrix.jsonl : the LLM directed K x K winloss matrix produced
                                  by pairwise_matrix.py (winloss / score / best)

Why rebuild the human matrix here (instead of reading *-human-matrix.jsonl)?
Because we want to sweep the win/loss threshold, and that needs the raw scores.
With threshold 0 the rebuilt human matrix is identical to *-human-matrix.jsonl.

The two matrices are NOT directly comparable cell-by-cell:
  - human matrix is antisymmetric (winloss[i][j] = -winloss[j][i]);
  - the LLM matrix is DIRECTED (position bias -> winloss[i][j] != -winloss[j][i]).
So we first SYMMETRIZE the LLM matrix per unordered pair {i,j}:
    both orders say i wins  -> i wins (+1)
    both orders say j wins  -> j wins (-1)
    orders disagree         -> tie  ( 0)
(this is exactly the swap=True consensus rule in contrastive_judge.judge_pair).

Metrics reported (per language pair):
  1. pairwise agreement rate + 3x3 confusion matrix (human vs LLM verdict)
  2. directional accuracy
       - strict     : over pairs human calls a winner; LLM tie counts as wrong
       - both-clear : over pairs BOTH call a winner; pure direction agreement
  3. ranking correlation per doc, averaged: Kendall tau-b and Spearman rho
       (human raw score vs LLM net score)
  4. Best@1 / Best@2 : is the LLM's best hypo the human-best / in human top-2
  5. threshold sweep : metrics 1-2 recomputed at several human thresholds

Usage:
  python3 coherency_eval.py                          # both pairs, dir=dev
  python3 coherency_eval.py --pairs en-zh
  python3 coherency_eval.py --thresholds 0,5,10,25
  python3 coherency_eval.py --dump dev/coherency.jsonl     # nested jsonl
  python3 coherency_eval.py --csv dev/coherency_sweep.csv  # flat csv
  python3 coherency_eval.py --tsv dev/coherency_sweep.tsv  # flat tsv (Excel)

Export formats:
  --dump : one nested json record per language pair (with embedded sweep)
  --csv / --tsv : one FLAT row per (pair, threshold), Excel-friendly
"""

import argparse
import json
import os
import sys
from pathlib import Path

# default dev/ dir is resolved relative to this script, so the tool works
# regardless of the current working directory.
DEFAULT_DIR = str(Path(__file__).resolve().parent / "dev")


# ----------------------------- IO -----------------------------

def load_dev(path):
    """doc_id -> {'scores': [..], 'hypos': [..]} from dev/<pair>.jsonl."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            n = sum(1 for k in r if k.startswith("hypo_"))
            out[r["doc_id"]] = {
                "scores": [r.get(f"score_{i}") for i in range(n)],
                "hypos": [r.get(f"hypo_{i}") for i in range(n)],
            }
    return out


def load_llm(path):
    """doc_id -> the full llm-matrix record."""
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            out[r["doc_id"]] = r
    return out


# ------------------------- verdict logic -------------------------

def human_verdict(si, sj, win_k, loss_n):
    """+1 if hypo i beats j, -1 if loses, 0 tie -- from raw human scores."""
    if si is None or sj is None:
        return 0
    diff = si - sj
    if diff > win_k:
        return 1
    if diff < -loss_n:
        return -1
    return 0


def llm_sym_verdict(lm, i, j):
    """Symmetrize the directed LLM matrix for the unordered pair {i, j}."""
    a = lm[i][j]        # i shown first vs j
    b = -lm[j][i]       # j shown first vs i, remapped to i's perspective
    if a == 1 and b == 1:
        return 1
    if a == -1 and b == -1:
        return -1
    return 0            # orders disagree -> tie


# ----------------------- rank correlations -----------------------

def _avg_ranks(a):
    order = sorted(range(len(a)), key=lambda i: a[i])
    ranks = [0.0] * len(a)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[order[j + 1]] == a[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def _pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    d = (sxx * syy) ** 0.5
    return sxy / d if d > 0 else None


def spearman(x, y):
    return _pearson(_avg_ranks(x), _avg_ranks(y))


def kendall_tau_b(x, y):
    n = len(x)
    c = d = tx = ty = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            if dx == 0 and dy == 0:
                continue
            if dx == 0:
                ty += 1
                continue
            if dy == 0:
                tx += 1
                continue
            if (dx > 0) == (dy > 0):
                c += 1
            else:
                d += 1
    denom = ((c + d + tx) * (c + d + ty)) ** 0.5
    return (c - d) / denom if denom > 0 else None


# ------------------------- core evaluation -------------------------

def pair_metrics(dev, llm, win_k, loss_n):
    """Pairwise + directional metrics at one human threshold."""
    # confusion[(h, l)] over i<j pairs; h,l in {1,0,-1}
    confusion = {(h, l): 0 for h in (1, 0, -1) for l in (1, 0, -1)}
    dir_corr = dir_tot = 0          # human has winner; llm tie = wrong
    both_corr = both_tot = 0        # both have a winner
    h_tie = l_tie = total = 0

    for did in sorted(set(dev) & set(llm)):
        scores = dev[did]["scores"]
        lm = llm[did]["winloss"]
        n = len(lm)
        for i in range(n):
            for j in range(i + 1, n):
                h = human_verdict(scores[i], scores[j], win_k, loss_n)
                l = llm_sym_verdict(lm, i, j)
                confusion[(h, l)] += 1
                total += 1
                if h == 0:
                    h_tie += 1
                if l == 0:
                    l_tie += 1
                if h != 0:
                    dir_tot += 1
                    if l == h:
                        dir_corr += 1
                    if l != 0:
                        both_tot += 1
                        if l == h:
                            both_corr += 1

    agree = sum(confusion[(v, v)] for v in (1, 0, -1))
    return {
        "confusion": confusion,
        "total": total,
        "agreement": agree / total if total else None,
        "dir_strict": dir_corr / dir_tot if dir_tot else None,
        "dir_strict_n": dir_tot,
        "dir_both": both_corr / both_tot if both_tot else None,
        "dir_both_n": both_tot,
        "human_tie_rate": h_tie / total if total else None,
        "llm_tie_rate": l_tie / total if total else None,
    }


def ranking_and_best(dev, llm):
    """Per-doc Kendall/Spearman (human raw vs llm net) and Best@1/Best@2."""
    taus, rhos = [], []
    n_skip_corr = 0
    best1 = best2 = best_tot = 0

    for did in sorted(set(dev) & set(llm)):
        scores = dev[did]["scores"]
        rec = llm[did]
        llm_score = rec["score"]
        llm_best = rec["best"]
        n = len(scores)
        if any(s is None for s in scores):
            n_skip_corr += 1
        else:
            t = kendall_tau_b(scores, llm_score)
            r = spearman(scores, llm_score)
            if t is not None:
                taus.append(t)
            if r is not None:
                rhos.append(r)

        # Best@k: how many hypos have a STRICTLY higher human score than the
        # LLM's pick.  <k strictly-greater -> hit@k (ties handled gracefully).
        best_tot += 1
        sb = scores[llm_best]
        if sb is not None:
            greater = sum(1 for s in scores if s is not None and s > sb)
            if greater < 1:
                best1 += 1
            if greater < 2:
                best2 += 1

    mean = lambda xs: sum(xs) / len(xs) if xs else None
    return {
        "kendall_mean": mean(taus),
        "spearman_mean": mean(rhos),
        "n_corr_docs": len(taus),
        "n_skip_corr": n_skip_corr,
        "best1": best1 / best_tot if best_tot else None,
        "best2": best2 / best_tot if best_tot else None,
        "best_n": best_tot,
    }


# ----------------------------- report -----------------------------

def pct(x):
    return f"{100 * x:.1f}%" if x is not None else "n/a"


def fnum(x):
    return f"{x:+.3f}" if x is not None else "n/a"


def print_confusion(conf):
    labels = [(1, "LLM win-i"), (0, "LLM tie"), (-1, "LLM win-j")]
    hdr = "                 " + "".join(f"{name:>12}" for _, name in labels)
    print(hdr)
    for h, hname in [(1, "human win-i"), (0, "human tie"), (-1, "human win-j")]:
        row = "".join(f"{conf[(h, l)]:>12}" for l, _ in labels)
        print(f"  {hname:<14}{row}")


def report_pair(pair, dev, llm, thresholds):
    """Print the console report and return a self-contained record dict."""
    docs = sorted(set(dev) & set(llm))
    # alignment sanity check
    mism = 0
    for did in docs:
        if dev[did]["hypos"] != llm[did].get("hypos", dev[did]["hypos"]):
            mism += 1
    print("=" * 64)
    print(f"[{pair}]  aligned docs = {len(docs)}"
          + (f"   (WARNING: {mism} hypo-text mismatches)" if mism else ""))
    print("=" * 64)

    # primary metrics at the first threshold (default 0)
    k0 = thresholds[0]
    m = pair_metrics(dev, llm, k0, k0)
    rb = ranking_and_best(dev, llm)

    print(f"\n-- pairwise (human threshold = {k0}) --")
    print(f"  agreement (3-way)        : {pct(m['agreement'])}")
    print(f"  human tie rate           : {pct(m['human_tie_rate'])}")
    print(f"  LLM  tie rate (sym)      : {pct(m['llm_tie_rate'])}")
    print("  confusion (rows=human, cols=LLM):")
    print_confusion(m["confusion"])

    print("\n-- directional accuracy --")
    print(f"  strict   (human winner; LLM tie=wrong) : "
          f"{pct(m['dir_strict'])}  (n={m['dir_strict_n']})")
    print(f"  both-clear (both call a winner)        : "
          f"{pct(m['dir_both'])}  (n={m['dir_both_n']})")

    print("\n-- ranking correlation (per-doc mean) --")
    print(f"  Kendall tau-b : {fnum(rb['kendall_mean'])}  "
          f"(over {rb['n_corr_docs']} docs)")
    print(f"  Spearman rho  : {fnum(rb['spearman_mean'])}")
    if rb["n_skip_corr"]:
        print(f"  (skipped {rb['n_skip_corr']} docs with missing scores)")

    print("\n-- best hypo agreement --")
    print(f"  Best@1 : {pct(rb['best1'])}   Best@2 : {pct(rb['best2'])}  "
          f"(n={rb['best_n']})")

    if len(thresholds) > 1:
        print("\n-- threshold sweep (human win_k=loss_n=t) --")
        print(f"  {'t':>4}{'agree':>9}{'h_tie':>8}{'l_tie':>8}"
              f"{'dir_strict':>12}{'dir_both':>10}")
        for t in thresholds:
            mt = pair_metrics(dev, llm, t, t)
            print(f"  {t:>4}{pct(mt['agreement']):>9}"
                  f"{pct(mt['human_tie_rate']):>8}{pct(mt['llm_tie_rate']):>8}"
                  f"{pct(mt['dir_strict']):>12}{pct(mt['dir_both']):>10}")

    print()

    # build a self-contained record (full threshold sweep) for export
    sweep = []
    for t in thresholds:
        mt = m if t == k0 else pair_metrics(dev, llm, t, t)
        sweep.append({
            "threshold": t,
            "agreement": mt["agreement"],
            "human_tie_rate": mt["human_tie_rate"],
            "llm_tie_rate": mt["llm_tie_rate"],
            "dir_strict": mt["dir_strict"],
            "dir_both": mt["dir_both"],
        })
    return {
        "pair": pair,
        "n_docs": len(docs),
        "primary_threshold": k0,
        "agreement": m["agreement"],
        "dir_strict": m["dir_strict"],
        "dir_both": m["dir_both"],
        "human_tie_rate": m["human_tie_rate"],
        "llm_tie_rate": m["llm_tie_rate"],
        # threshold-independent metrics
        "kendall_mean": rb["kendall_mean"],
        "spearman_mean": rb["spearman_mean"],
        "best1": rb["best1"],
        "best2": rb["best2"],
        # per-threshold sweep
        "sweep": sweep,
    }


# ----------------------------- export -----------------------------

# columns for the flat (one row per pair x threshold) table
_FLAT_COLS = [
    "pair", "n_docs", "threshold", "agreement_3way", "human_tie_rate",
    "llm_tie_rate", "dir_strict", "dir_both", "kendall_mean", "spearman_mean",
    "best1", "best2",
]


def flatten(records):
    """Explode the nested records into one flat row per (pair, threshold)."""
    rows = []
    for r in records:
        for s in r["sweep"]:
            rows.append({
                "pair": r["pair"],
                "n_docs": r["n_docs"],
                "threshold": s["threshold"],
                "agreement_3way": s["agreement"],
                "human_tie_rate": s["human_tie_rate"],
                "llm_tie_rate": s["llm_tie_rate"],
                "dir_strict": s["dir_strict"],
                "dir_both": s["dir_both"],
                # threshold-independent metrics repeated per row (self-contained)
                "kendall_mean": r["kendall_mean"],
                "spearman_mean": r["spearman_mean"],
                "best1": r["best1"],
                "best2": r["best2"],
            })
    return rows


def write_jsonl(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_table(records, path, delimiter):
    import csv
    rows = flatten(records)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=_FLAT_COLS, delimiter=delimiter)
        w.writeheader()
        for row in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v)
                        for k, v in row.items()})


def parse_args():
    p = argparse.ArgumentParser(
        description="LLM vs human pairwise-judgement coherency evaluation")
    p.add_argument("--pairs", default="en-zh,en-ru",
                   help="comma-separated language pairs (default: en-zh,en-ru)")
    p.add_argument("--dir", default=DEFAULT_DIR,
                   help="dir holding the SHARED dev/human jsonl (experiment-independent); "
                        "defaults to the dev/ next to this script")
    p.add_argument("--model", default="gpt-4o-mini",
                   help="judge model name; forms a <dir>/<model>/ level above the experiment")
    p.add_argument("--exp", default="",
                   help="experiment name; LLM matrices are read from <dir>/<model>/<exp>/ "
                        "and exports default there (separates judge models/prompts)")
    p.add_argument("--dev", default="", help="explicit dev jsonl (single pair)")
    p.add_argument("--llm", default="", help="explicit llm-matrix jsonl (single pair)")
    p.add_argument("--thresholds", default="0,5,10,25",
                   help="comma-separated human thresholds; first is the primary")
    p.add_argument("--dump", default="", help="write per-pair summary jsonl here")
    p.add_argument("--csv", default="",
                   help="write flat (pair x threshold) comma-separated table here")
    p.add_argument("--tsv", default="",
                   help="write flat tab-separated table here (Excel-friendly)")
    return p.parse_args()


def main():
    args = parse_args()
    thresholds = [float(x) if "." in x else int(x)
                  for x in args.thresholds.split(",") if x.strip() != ""]
    if not thresholds:
        thresholds = [0]

    # experiment dir = <dir>/<model>/<exp>  (model/exp components optional)
    exp_dir = args.dir
    if args.model:
        exp_dir = os.path.join(exp_dir, args.model.replace("/", "_"))
    if args.exp:
        exp_dir = os.path.join(exp_dir, args.exp)

    # build the (pair, dev_path, llm_path) work list
    jobs = []
    if args.dev or args.llm:
        if not (args.dev and args.llm):
            sys.exit("--dev and --llm must be given together")
        pair = os.path.splitext(os.path.basename(args.dev))[0]
        jobs.append((pair, args.dev, args.llm))
    else:
        # dev/human set is SHARED (dir root); llm matrices live in exp_dir
        for pair in [p.strip() for p in args.pairs.split(",") if p.strip()]:
            dev_p = os.path.join(args.dir, f"{pair}.jsonl")
            llm_p = os.path.join(exp_dir, f"{pair}-llm-matrix.jsonl")
            jobs.append((pair, dev_p, llm_p))

    records = []
    for pair, dev_p, llm_p in jobs:
        if not os.path.exists(dev_p):
            print(f"[skip {pair}] missing {dev_p}")
            continue
        if not os.path.exists(llm_p):
            print(f"[skip {pair}] missing {llm_p}")
            continue
        dev = load_dev(dev_p)
        llm = load_llm(llm_p)
        records.append(report_pair(pair, dev, llm, thresholds))

    # export targets: explicit paths win; otherwise auto-write all three into
    # the experiment dir (<dir>/<model>/<exp>/) with standard names.
    dump_p, csv_p, tsv_p = args.dump, args.csv, args.tsv
    if (args.model or args.exp) and not (args.dump or args.csv or args.tsv):
        os.makedirs(exp_dir, exist_ok=True)
        dump_p = os.path.join(exp_dir, "coherency.jsonl")
        csv_p = os.path.join(exp_dir, "coherency_sweep.csv")
        tsv_p = os.path.join(exp_dir, "coherency_sweep.tsv")

    # exports (all derived from the same in-memory records)
    if dump_p:
        write_jsonl(records, dump_p)
        print(f"per-pair summary (jsonl) -> {dump_p}")
    if csv_p:
        write_table(records, csv_p, ",")
        print(f"flat table (csv) -> {csv_p}")
    if tsv_p:
        write_table(records, tsv_p, "\t")
        print(f"flat table (tsv) -> {tsv_p}")


if __name__ == "__main__":
    main()
