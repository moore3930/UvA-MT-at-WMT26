# v6 Judge Settings - Coherency Summary (en-zh & en-ru)

LLM pairwise judge vs. human scores, rubric **v6**, whole dev set, threshold t=0.
All numbers recomputed directly from the `*-llm-matrix.jsonl` files (medium-reasoning runs excluded).

## Metrics explained

Each item has K=8 candidate translations; the judge compares every ordered pair (both A-first and B-first). The directed LLM matrix is symmetrized per unordered pair {i,j}: both orders agree i wins -> i; both agree j wins -> j; orders disagree -> tie. The human matrix is rebuilt from the raw human scores (`score_i - score_j` at threshold t=0).

- **agree** (agreement_3way): fraction of pairs where the LLM's 3-way verdict (win-i / tie / win-j) exactly matches the human verdict. Both-say-tie also counts as agreement. *Higher = better.*
- **d_strict** (dir_strict): among pairs where the **human** picks a winner, the fraction where the LLM agrees on direction. An LLM tie counts as **wrong**. So this is punished by the LLM's tie rate. *Higher = better.*
- **d_both** (dir_both): among pairs where **both** the human and the LLM pick a winner, the fraction agreeing on direction. Ties are excluded on both sides, so this is the purest "when it commits, is the direction right?" metric. *Higher = better.*
- **Kendall** (tau-b) / **Spear** (Spearman rho): per-document rank correlation between the 8 human raw scores and the 8 LLM net scores (row sums of the matrix), averaged over documents. Threshold-independent. Range -1..+1; *higher = better.*
- **flip%** (position-order disagreement): fraction of unordered pairs whose two orderings (i-first vs j-first) give conflicting verdicts. A direct measure of **position bias / self-inconsistency**. *Lower = better.*
- **tie%** (LLM tie rate, symmetrized): fraction of pairs the symmetrized LLM calls a tie. Most of these come from position flips, not genuine ties, so it mostly reflects instability. *Lower = better* (fewer forced ties).
- **B@1 / B@2** (Best@1 / Best@2): does the LLM's top-ranked candidate (argmax net score) coincide with the human's #1 (B@1) / land within the human top-2 (B@2)? Ties handled gracefully. *Higher = better.*

## en-zh  (docs=198)

| model | config | agree | d_strict | d_both | Kendall | Spear | flip% | tie% | B@1 | B@2 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 30.1 | 29.5 | 63.6 | +0.185 | +0.237 | 53.5 | 53.7 | 13.6 | 28.8 |
| gpt-4o-mini | json-only (min) | 42.6 | 42.7 | 62.4 | +0.206 | +0.259 | 31.3 | 31.6 | 21.7 | 33.8 |
| gemini-2.5-flash | json-only (min) | 25.9 | 25.4 | 62.6 | +0.181 | +0.238 | 51.4 | 59.3 | 20.7 | 33.8 |
| gpt-5-4-fair | json-only (min) | 51.0 | 51.5 | 63.0 | +0.220 | +0.287 | 18.0 | 18.4 | 19.7 | 32.3 |
| gemini-3-5-flash-fair | json-only (min) | 54.0 | 54.6 | 63.3 | +0.240 | +0.311 | 13.5 | 13.9 | 20.2 | 33.8 |

## en-ru  (docs=200)

| model | config | agree | d_strict | d_both | Kendall | Spear | flip% | tie% | B@1 | B@2 |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 38.4 | 38.3 | 67.9 | +0.265 | +0.334 | 43.4 | 43.7 | 28.0 | 43.0 |
| gpt-4o-mini | json-only (min) | 46.2 | 46.3 | 66.4 | +0.270 | +0.342 | 30.2 | 30.5 | 29.5 | 41.0 |
| gemini-2.5-flash | json-only (min) | 31.4 | 30.9 | 67.5 | +0.277 | +0.359 | 48.3 | 54.3 | 32.5 | 48.0 |
| gpt-5-4-fair | json-only (min) | 56.6 | 57.2 | 69.0 | +0.338 | +0.425 | 16.8 | 17.2 | 36.0 | 51.5 |
| gemini-3-5-flash-fair | json-only (min) | 59.6 | 60.4 | 67.5 | +0.327 | +0.416 | 10.3 | 10.6 | 36.0 | 52.0 |

## Threshold sweep (human-margin sensitivity)

The threshold **t** sets how large a human score gap must be to count as a "human winner": `diff > t` -> win, `diff < -t` -> loss, else tie. Raising t restricts the comparison to pairs where humans have a **clearer** preference (fewer, less-noisy pairs). Only the threshold-**dependent** metrics change with t (agree / d_strict / d_both); Kendall/Spearman/flip/Best are threshold-independent.

### en-zh - d_both vs t  (docs=198)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 63.6 | 66.8 | 69.4 | 71.1 | 71.8 | 73.6 | 76.2 |
| gpt-4o-mini | json-only (min) | 62.4 | 65.0 | 67.7 | 69.6 | 70.1 | 72.0 | 75.3 |
| gemini-2.5-flash | json-only (min) | 62.6 | 66.9 | 69.9 | 72.6 | 72.6 | 75.2 | 77.0 |
| gpt-5-4-fair | json-only (min) | 63.0 | 66.5 | 68.8 | 71.6 | 71.5 | 73.1 | 74.1 |
| gemini-3-5-flash-fair | json-only (min) | 63.3 | 67.0 | 69.4 | 71.2 | 72.0 | 73.7 | 75.3 |

### en-zh - agree vs t  (docs=198)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 30.1 | 38.5 | 44.0 | 48.0 | 50.0 | 52.3 | 53.4 |
| gpt-4o-mini | json-only (min) | 42.6 | 42.0 | 40.2 | 39.6 | 38.1 | 36.8 | 36.2 |
| gemini-2.5-flash | json-only (min) | 25.9 | 35.0 | 42.7 | 47.4 | 51.1 | 54.4 | 56.0 |
| gpt-5-4-fair | json-only (min) | 51.0 | 46.2 | 39.9 | 36.0 | 31.8 | 29.1 | 27.0 |
| gemini-3-5-flash-fair | json-only (min) | 54.0 | 47.3 | 40.3 | 34.3 | 28.9 | 25.2 | 22.8 |

### en-zh - d_strict vs t  (docs=198)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 29.5 | 31.9 | 33.7 | 35.7 | 36.6 | 39.7 | 42.3 |
| gpt-4o-mini | json-only (min) | 42.7 | 44.9 | 46.7 | 49.0 | 50.2 | 52.0 | 55.1 |
| gemini-2.5-flash | json-only (min) | 25.4 | 27.0 | 28.7 | 29.8 | 30.5 | 33.1 | 34.6 |
| gpt-5-4-fair | json-only (min) | 51.5 | 54.9 | 56.8 | 59.8 | 60.4 | 63.4 | 65.2 |
| gemini-3-5-flash-fair | json-only (min) | 54.6 | 58.0 | 60.7 | 62.3 | 62.9 | 64.7 | 66.4 |

_Pairs with both-clear verdict shrink as t rises (example, gemini-3-5-flash-fair): t=0:4690, t=5:3583, t=10:2657, t=15:1980, t=20:1445, t=25:1045, t=30:794._

### en-ru - d_both vs t  (docs=200)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 67.9 | 71.5 | 74.1 | 75.7 | 78.2 | 80.0 | 81.8 |
| gpt-4o-mini | json-only (min) | 66.4 | 69.2 | 71.4 | 73.1 | 74.9 | 77.1 | 78.4 |
| gemini-2.5-flash | json-only (min) | 67.5 | 71.2 | 73.9 | 75.7 | 78.1 | 81.0 | 83.0 |
| gpt-5-4-fair | json-only (min) | 69.0 | 72.3 | 75.1 | 77.1 | 78.9 | 81.3 | 82.9 |
| gemini-3-5-flash-fair | json-only (min) | 67.5 | 70.7 | 73.1 | 75.5 | 77.4 | 80.0 | 81.0 |

### en-ru - agree vs t  (docs=200)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 38.4 | 41.4 | 43.9 | 44.7 | 45.3 | 46.0 | 46.3 |
| gpt-4o-mini | json-only (min) | 46.2 | 46.2 | 45.3 | 43.3 | 42.1 | 40.9 | 39.2 |
| gemini-2.5-flash | json-only (min) | 31.4 | 37.0 | 41.2 | 45.1 | 47.6 | 49.3 | 50.8 |
| gpt-5-4-fair | json-only (min) | 56.6 | 52.3 | 47.8 | 43.0 | 38.3 | 35.1 | 31.5 |
| gemini-3-5-flash-fair | json-only (min) | 59.6 | 54.1 | 47.7 | 41.5 | 36.2 | 32.0 | 27.5 |

### en-ru - d_strict vs t  (docs=200)

| model | config | t=0 | t=5 | t=10 | t=15 | t=20 | t=25 | t=30 |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| gpt-4o-mini | reason+json | 38.3 | 40.5 | 42.7 | 43.9 | 45.6 | 47.6 | 49.6 |
| gpt-4o-mini | json-only (min) | 46.3 | 48.9 | 51.1 | 52.6 | 54.9 | 57.5 | 59.1 |
| gemini-2.5-flash | json-only (min) | 30.9 | 32.7 | 34.0 | 35.5 | 36.8 | 37.9 | 39.0 |
| gpt-5-4-fair | json-only (min) | 57.2 | 60.2 | 63.0 | 65.1 | 66.7 | 69.6 | 71.0 |
| gemini-3-5-flash-fair | json-only (min) | 60.4 | 63.7 | 66.2 | 68.5 | 70.6 | 73.7 | 74.7 |

_Pairs with both-clear verdict shrink as t rises (example, gemini-3-5-flash-fair): t=0:4916, t=5:4073, t=10:3313, t=15:2647, t=20:2113, t=25:1676, t=30:1303._

## Key findings

1. **Best judge = `gemini-3-5-flash-fair`** (the final-submission judge, gemini-3.5-flash), top overall on both pairs; `gpt-5-4-fair` a close second.
2. **Model strength ~= stability**: agreement/d_strict gains track the drop in position-flip rate (gemini-2.5 ~50% -> gemini-3.5-fair ~10-13%). Stronger models self-contradict less across A/B order.
3. **d_both ceiling ~63% (en-zh) / ~67-69% (en-ru)** - nearly identical across all models/configs. Directional accuracy when both take a side is capped; the bottleneck is the rubric, not the model.
4. **json-only > reason+json**: for gpt-4o-mini, adding a written rationale inflates position bias (flip 31%->53%, agreement 42.6%->30.1%).
5. **en-ru is easier to judge than en-zh** by ~5-8 points across the board.

_Medium-reasoning variants were run for en-zh only and are intentionally excluded here (min effort matched them within noise at ~5x the cost)._
