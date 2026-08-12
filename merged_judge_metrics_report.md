# Merged Judge Metrics Report

Current scope: finished merged judged languages `arz`, `arz_Arab`, `bel_Cyrl` only.

Merged results source:
- `results/merged/gemini-3.5-flash__gpt-final/`

Judge artifacts source:
- `results/gemini-2.5-flash/artifacts/merged/gemini-3.5-flash__gpt-final/matrix/`

Judged export source:
- `results/gemini-2.5-flash/judged/merged/gemini-3.5-flash__gpt-final/`

## Per-Hypothesis Winner Percentages

These are computed over the currently finished 3 languages (`546` docs total), using `judge_best_hypo_key` and mapping merged `hypo_i` back to `(model, original_hypo_id)` through `merge_meta`.

| merged hypo | model | original hypo | winner % | avg win-rate % |
|---|---|---:|---:|---:|
| `hypo_0` | `gemini-3.5-flash` | `hypo_0` | 10.99% | 43.89% |
| `hypo_1` | `gemini-3.5-flash` | `hypo_1` | 7.69% | 46.49% |
| `hypo_2` | `gemini-3.5-flash` | `hypo_2` | 5.49% | 46.68% |
| `hypo_3` | `gemini-3.5-flash` | `hypo_3` | 6.59% | 47.69% |
| `hypo_4` | `gemini-3.5-flash` | `hypo_4` | 4.40% | 47.36% |
| `hypo_5` | `gemini-3.5-flash` | `hypo_5` | 3.48% | 47.66% |
| `hypo_6` | `gemini-3.5-flash` | `hypo_6` | 4.40% | 47.69% |
| `hypo_7` | `gemini-3.5-flash` | `hypo_7` | 2.38% | 47.54% |
| `hypo_8` | `gpt-final` | `hypo_0` | 4.58% | 48.12% |
| `hypo_9` | `gpt-final` | `hypo_1` | 6.78% | 52.59% |
| `hypo_10` | `gpt-final` | `hypo_2` | 10.62% | 54.10% |
| `hypo_11` | `gpt-final` | `hypo_3` | 7.14% | 52.82% |
| `hypo_12` | `gpt-final` | `hypo_4` | 6.96% | 54.26% |
| `hypo_13` | `gpt-final` | `hypo_5` | 7.51% | 54.12% |
| `hypo_14` | `gpt-final` | `hypo_6` | 5.68% | 55.20% |
| `hypo_15` | `gpt-final` | `hypo_7` | 5.31% | 53.79% |

Model totals:

| model | winner % |
|---|---:|
| `gpt-final` | 54.58% |
| `gemini-3.5-flash` | 45.42% |

## Pairwise Stability Metrics

Definitions:
- `tie frequency`: percent of ordered non-diagonal matrix cells with `winloss == 0`
- `AB/BA contradiction`: percent of unordered pairs where the two directions do not mirror, i.e. `AB != -BA`
- `strict contradiction`: same underlying winner in both orders
- `tie-involved contradiction`: one direction is a tie, the other is decisive
- `both directions tie`: both directions are ties

Overall:

| scope | tie frequency | AB/BA contradiction | strict contradiction | tie-involved contradiction | both directions tie |
|---|---:|---:|---:|---:|---:|
| `arz` | 7.14% | 41.43% | 38.91% | 2.52% | 5.88% |
| `arz_Arab` | 9.57% | 81.60% | 75.82% | 5.78% | 6.68% |
| `bel_Cyrl` | 6.62% | 78.96% | 76.65% | 2.31% | 5.46% |
| `overall` | 7.83% | 69.61% | 65.98% | 3.63% | 6.02% |

## Pairwise Metrics Split By Model Pair Type

Split by pair type:
- `gemini-gemini`: both hypotheses from `gemini-3.5-flash`
- `gpt-gpt`: both hypotheses from `gpt-final`
- `cross-model`: one hypothesis from each model

Overall across the finished 3 languages:

| pair type | tie frequency | AB/BA contradiction | strict contradiction | tie-involved contradiction | both directions tie |
|---|---:|---:|---:|---:|---:|
| `gemini-gemini` | 23.26% | 56.46% | 53.11% | 3.36% | 21.58% |
| `gpt-gpt` | 4.56% | 73.67% | 70.33% | 3.34% | 2.89% |
| `cross-model` | 2.52% | 73.58% | 69.71% | 3.87% | 0.58% |

Per language:

| language | pair type | tie frequency | AB/BA contradiction |
|---|---|---:|---:|
| `arz` | `gemini-gemini` | 13.54% | 38.12% |
| `arz` | `gpt-gpt` | 10.79% | 44.57% |
| `arz` | `cross-model` | 2.76% | 41.50% |
| `arz_Arab` | `gemini-gemini` | 30.08% | 63.31% |
| `arz_Arab` | `gpt-gpt` | 2.90% | 87.14% |
| `arz_Arab` | `cross-model` | 3.52% | 87.18% |
| `bel_Cyrl` | `gemini-gemini` | 23.80% | 63.51% |
| `bel_Cyrl` | `gpt-gpt` | 1.51% | 82.23% |
| `bel_Cyrl` | `cross-model` | 1.33% | 84.29% |

## Caveat

`arz_Arab` and `bel_Cyrl` had `57` failed ordered pairwise calls total. In the saved matrices those unresolved calls remain `0`, so the current tie and contradiction metrics are slightly inflated toward ties.
