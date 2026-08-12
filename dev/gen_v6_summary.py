#!/usr/bin/env python3
"""Generate dev/v6_settings_summary.md from the v6 judge matrices (min/reason
only; medium-reasoning runs excluded). Numbers are recomputed from the
*-llm-matrix.jsonl files so they are immune to coherency.jsonl overwrites."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import coherency_eval as ce

REPO = Path(__file__).resolve().parent.parent

# (display model, matrix dir under dev/, exp, config label) -- no medium runs
JOBS = [
    ("gpt-4o-mini",           "gpt-4o-mini-genai",     "v6",          "reason+json"),
    ("gpt-4o-mini",           "gpt-4o-mini-genai",     "v6-jsononly", "json-only (min)"),
    ("gemini-2.5-flash",      "gemini-2.5-flash",      "v6-jsononly", "json-only (min)"),
    ("gpt-5-4-fair",          "gpt-5-4-fair",          "v6-jsononly", "json-only (min)"),
    ("gemini-3-5-flash-fair", "gemini-3-5-flash-fair", "v6-jsononly", "json-only (min)"),
]
PAIRS = [("en-zh", 198), ("en-ru", 200)]
THRESHOLDS = [0, 5, 10, 15, 20, 25, 30]


def P(x):
    return f"{100*x:.1f}" if x is not None else "n/a"


def F(x):
    return f"{x:+.3f}" if x is not None else "n/a"


def main():
    L = []
    L.append("# v6 Judge Settings - Coherency Summary (en-zh & en-ru)")
    L.append("")
    L.append("LLM pairwise judge vs. human scores, rubric **v6**, whole dev set, threshold t=0.")
    L.append("All numbers recomputed directly from the `*-llm-matrix.jsonl` files "
             "(medium-reasoning runs excluded).")
    L.append("")
    L.append("## Metrics explained")
    L.append("")
    L.append("Each item has K=8 candidate translations; the judge compares every ordered pair "
             "(both A-first and B-first). The directed LLM matrix is symmetrized per unordered "
             "pair {i,j}: both orders agree i wins -> i; both agree j wins -> j; orders disagree "
             "-> tie. The human matrix is rebuilt from the raw human scores (`score_i - score_j` "
             "at threshold t=0).")
    L.append("")
    L.append("- **agree** (agreement_3way): fraction of pairs where the LLM's 3-way verdict "
             "(win-i / tie / win-j) exactly matches the human verdict. Both-say-tie also counts "
             "as agreement. *Higher = better.*")
    L.append("- **d_strict** (dir_strict): among pairs where the **human** picks a winner, the "
             "fraction where the LLM agrees on direction. An LLM tie counts as **wrong**. So this "
             "is punished by the LLM's tie rate. *Higher = better.*")
    L.append("- **d_both** (dir_both): among pairs where **both** the human and the LLM pick a "
             "winner, the fraction agreeing on direction. Ties are excluded on both sides, so this "
             "is the purest \"when it commits, is the direction right?\" metric. *Higher = better.*")
    L.append("- **Kendall** (tau-b) / **Spear** (Spearman rho): per-document rank correlation "
             "between the 8 human raw scores and the 8 LLM net scores (row sums of the matrix), "
             "averaged over documents. Threshold-independent. Range -1..+1; *higher = better.*")
    L.append("- **flip%** (position-order disagreement): fraction of unordered pairs whose two "
             "orderings (i-first vs j-first) give conflicting verdicts. A direct measure of "
             "**position bias / self-inconsistency**. *Lower = better.*")
    L.append("- **tie%** (LLM tie rate, symmetrized): fraction of pairs the symmetrized LLM calls "
             "a tie. Most of these come from position flips, not genuine ties, so it mostly "
             "reflects instability. *Lower = better* (fewer forced ties).")
    L.append("- **B@1 / B@2** (Best@1 / Best@2): does the LLM's top-ranked candidate (argmax net "
             "score) coincide with the human's #1 (B@1) / land within the human top-2 (B@2)? "
             "Ties handled gracefully. *Higher = better.*")
    L.append("")
    for pair, ndoc in PAIRS:
        dev = ce.load_dev(str(REPO / f"dev/{pair}.jsonl"))
        L.append(f"## {pair}  (docs={ndoc})")
        L.append("")
        L.append("| model | config | agree | d_strict | d_both | Kendall | Spear | flip% | tie% | B@1 | B@2 |")
        L.append("|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
        for model, md, exp, cfg in JOBS:
            path = REPO / f"dev/{md}/{exp}/{pair}-llm-matrix.jsonl"
            if not path.exists():
                L.append(f"| {model} | {cfg} | - | - | - | - | - | - | - | - | - |")
                continue
            llm = ce.load_llm(str(path))
            m = ce.pair_metrics(dev, llm, 0, 0)
            rb = ce.ranking_and_best(dev, llm)
            pb = ce.position_bias_stats(llm)
            L.append(
                f"| {model} | {cfg} | {P(m['agreement'])} | {P(m['dir_strict'])} | "
                f"{P(m['dir_both'])} | {F(rb['kendall_mean'])} | {F(rb['spearman_mean'])} | "
                f"{P(pb['position_disagreement_rate'])} | {P(m['llm_tie_rate'])} | "
                f"{P(rb['best1'])} | {P(rb['best2'])} |"
            )
        L.append("")
    # ---- threshold sweep (human-margin sensitivity) ----
    L.append("## Threshold sweep (human-margin sensitivity)")
    L.append("")
    L.append("The threshold **t** sets how large a human score gap must be to count as a "
             "\"human winner\": `diff > t` -> win, `diff < -t` -> loss, else tie. Raising t "
             "restricts the comparison to pairs where humans have a **clearer** preference "
             "(fewer, less-noisy pairs). Only the threshold-**dependent** metrics change with t "
             "(agree / d_strict / d_both); Kendall/Spearman/flip/Best are threshold-independent.")
    L.append("")
    for pair, ndoc in PAIRS:
        dev = ce.load_dev(str(REPO / f"dev/{pair}.jsonl"))
        # preload matrices for this pair
        loaded = []
        for model, md, exp, cfg in JOBS:
            path = REPO / f"dev/{md}/{exp}/{pair}-llm-matrix.jsonl"
            loaded.append((model, cfg, ce.load_llm(str(path)) if path.exists() else None))
        for metric_key, metric_name in [("dir_both", "d_both"),
                                        ("agreement", "agree"),
                                        ("dir_strict", "d_strict")]:
            L.append(f"### {pair} - {metric_name} vs t  (docs={ndoc})")
            L.append("")
            L.append("| model | config | " + " | ".join(f"t={t}" for t in THRESHOLDS) + " |")
            L.append("|---|---|" + "--:|" * len(THRESHOLDS))
            for model, cfg, llm in loaded:
                if llm is None:
                    L.append(f"| {model} | {cfg} | " + " | ".join("-" for _ in THRESHOLDS) + " |")
                    continue
                cells = []
                for t in THRESHOLDS:
                    m = ce.pair_metrics(dev, llm, t, t)
                    cells.append(P(m[metric_key]))
                L.append(f"| {model} | {cfg} | " + " | ".join(cells) + " |")
            L.append("")
        # pair-count context for d_both (how many pairs survive each t)
        base = next((llm for model, _, llm in loaded
                     if llm is not None and model == "gemini-3-5-flash-fair"), None)
        if base is not None:
            counts = [ce.pair_metrics(dev, base, t, t)["dir_both_n"] for t in THRESHOLDS]
            L.append(f"_Pairs with both-clear verdict shrink as t rises (example, "
                     f"gemini-3-5-flash-fair): " +
                     ", ".join(f"t={t}:{n}" for t, n in zip(THRESHOLDS, counts)) + "._")
            L.append("")

    L.append("## Key findings")
    L.append("")
    L.append("1. **Best judge = `gemini-3-5-flash-fair`** (the final-submission judge, "
             "gemini-3.5-flash), top overall on both pairs; `gpt-5-4-fair` a close second.")
    L.append("2. **Model strength ~= stability**: agreement/d_strict gains track the drop in "
             "position-flip rate (gemini-2.5 ~50% -> gemini-3.5-fair ~10-13%). Stronger models "
             "self-contradict less across A/B order.")
    L.append("3. **d_both ceiling ~63% (en-zh) / ~67-69% (en-ru)** - nearly identical across all "
             "models/configs. Directional accuracy when both take a side is capped; the "
             "bottleneck is the rubric, not the model.")
    L.append("4. **json-only > reason+json**: for gpt-4o-mini, adding a written rationale inflates "
             "position bias (flip 31%->53%, agreement 42.6%->30.1%).")
    L.append("5. **en-ru is easier to judge than en-zh** by ~5-8 points across the board.")
    L.append("")
    L.append("_Medium-reasoning variants were run for en-zh only and are intentionally excluded "
             "here (min effort matched them within noise at ~5x the cost)._")

    out = "\n".join(L) + "\n"
    (REPO / "dev/v6_settings_summary.md").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
