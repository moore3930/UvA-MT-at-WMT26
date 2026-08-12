# Final Hypothesis Id Counts

- Input: `/home/stroshi/UvA-MT-at-WMT26/final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- Final rows: `18317`
- Final model totals: `gemini-3.5-flash=11624`, `gpt-final=6693`
- Rows where final model/hypothesis differs from raw selected winner: `3`

## Summary

| model | final rows |
| --- | ---: |
| gemini-3.5-flash | 11624 |
| gpt-final | 6693 |

## gemini-3.5-flash Final Counts

| hypothesis id | count | pct within model |
| --- | ---: | ---: |
| hypo_0 | 3266 | 28.10% |
| hypo_1 | 2342 | 20.15% |
| hypo_2 | 1588 | 13.66% |
| hypo_3 | 1247 | 10.73% |
| hypo_4 | 996 | 8.57% |
| hypo_5 | 832 | 7.16% |
| hypo_6 | 738 | 6.35% |
| hypo_7 | 615 | 5.29% |

- total for model: `11624`

## gpt-final Final Counts

| hypothesis id | count | pct within model |
| --- | ---: | ---: |
| hypo_0 | 1564 | 23.37% |
| hypo_1 | 881 | 13.16% |
| hypo_2 | 778 | 11.62% |
| hypo_3 | 733 | 10.95% |
| hypo_4 | 680 | 10.16% |
| hypo_5 | 690 | 10.31% |
| hypo_6 | 673 | 10.06% |
| hypo_7 | 694 | 10.37% |

- total for model: `6693`

## Final Vs Raw Selected Differences

| doc_id | tgt_lang | selected model | selected hypo | final model | final hypo | reason |
| --- | --- | --- | --- | --- | --- | --- |
| 00531-arz_Arab | arz_Arab | gemini-3.5-flash | hypo_1 | gpt-final | hypo_2 | combined_valid_fallback |
| 08795-deu_Latn | deu_Latn | gpt-final | hypo_5 | gpt-final | hypo_0 | combined_valid_fallback |
| 45812-vie_Latn | vie_Latn | gemini-3.5-flash | hypo_0 | gpt-final | hypo_5 | combined_valid_fallback |
