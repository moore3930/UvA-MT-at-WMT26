# en-ru Judge Comparison

| Metric | gemini-2.5-flash | gpt-4o-mini | Better |
|---|---:|---:|---|
| agreement | 49.9% | 24.9% | Gemini |
| dir_strict | 50.3% | 24.0% | Gemini |
| dir_both | 67.8% | 70.4% | GPT-4o-mini |
| LLM tie rate | 25.9% | 66.0% | Gemini |
| Kendall tau-b | 0.305 | 0.246 | Gemini |
| Spearman rho | 0.389 | 0.304 | Gemini |
| Best@1 | 34.0% | 27.5% | Gemini |
| Best@2 | 52.0% | 39.0% | Gemini |
| Position disagreements | 25.6% | 65.7% | Gemini |

## Metric Notes

| Metric | Short explanation |
|---|---|
| agreement | Exact 3-way match with human pairwise verdicts |
| dir_strict | Direction accuracy when humans chose a winner; LLM ties count as wrong |
| dir_both | Direction accuracy only on pairs where both human and LLM chose a winner |
| LLM tie rate | How often the judge ends up with a tie after symmetrization |
| Kendall tau-b | Rank correlation between human scores and LLM ranking |
| Spearman rho | Rank-order correlation between human scores and LLM ranking |
| Best@1 | How often the LLM top choice matches the human best |
| Best@2 | How often the LLM top choice is in the human top 2 |
| Position disagreements | How often A-first vs B-first judgments disagree |

`gemini-2.5-flash` is clearly stronger overall on `en-ru`. It has much higher agreement with human judgments, much better strict directional accuracy, better ranking correlation, better best-hypothesis selection, much lower tie rate, and dramatically lower position bias. `gpt-4o-mini` is only slightly better on `dir_both`, but it ties 66.0% of pairs, so that metric is measured on a much smaller and easier subset of cases.

Caveat: the Gemini run had 1 failed ordered pair out of 11,168, which is negligible for the overall conclusion.
