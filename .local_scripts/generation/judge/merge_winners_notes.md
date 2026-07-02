# Notes: Cross-Model Winner Merge Stage

## Findings

- `pairwise_matrix.py` computes a direction-aware score within one candidate pool:
  - `score[i] = sum(row_i) - sum(col_i)`
  - `best = argmax(score[i], -i)`
- The existing 8x8 GPT and 8x8 Gemini matrices already give the within-model score contribution for their own selected winner.
- To make a fair global GPT-vs-Gemini decision, we still need fresh cross-model judgments; the existing intra-model matrices do not tell us how the GPT winner performs against Gemini candidates, or vice versa.

## Required Cross-Model Workload

Let:
- `g*` = selected GPT winner for a document
- `m*` = selected Gemini winner for the same document
- `G[0..7]` = all GPT hypotheses
- `M[0..7]` = all Gemini hypotheses

Then the needed fresh judgments are:
- `g*` vs every `M[i]`, in both orders
- `m*` vs every `G[i]`, in both orders

Naively that is `16 + 16 = 32` ordered comparisons per document, but the shared
pair `g*` vs `m*` appears in both sets, so the unique maximum is:
- `15` unordered cross pairs
- `30` ordered API calls per document

This is the key requirement behind “all 16 judge counts for each winner.”

## Recommended Inputs

- GPT selected winners:
  - `final_submission/out/.../preliminary_final.jsonl` for the GPT run
- Gemini selected winners:
  - `final_submission/out/.../preliminary_final.jsonl` for the Gemini run
- GPT full 8-hypothesis source rows:
  - `results/gpt-final/<lang>.jsonl`
- Gemini full 8-hypothesis source rows:
  - `results/gemini-3.5-flash/<lang>.jsonl`
- Existing matrix summaries for within-model scores:
  - `results/gemini-2.5-flash/artifacts/gpt-final/matrix/*-llm-matrix.jsonl`
  - `results/gemini-2.5-flash/artifacts/gemini-3.5-flash/matrix/*-llm-matrix.jsonl`

## Recommended Scoring Rule

For each document:

1. Read the already-selected GPT winner text and Gemini winner text.
2. Read the full GPT and Gemini 8-hypothesis pools.
3. Judge only the cross-model ordered pairs needed for:
   - GPT winner vs Gemini pool
   - Gemini winner vs GPT pool
4. Convert those cross judgments into two cross-score contributions:
   - `gpt_cross_score`
   - `gemini_cross_score`
5. Add them to the already-known within-model selected-winner scores:
   - `gpt_total = gpt_intra_score + gpt_cross_score`
   - `gemini_total = gemini_intra_score + gemini_cross_score`
6. Choose the model with the higher total score.

This preserves the existing matrix semantics while avoiding a full 16x16 rerun.

## Recommended New Scripts

- `pairwise_matrix_two_best_tounament.py`
  - specialized judge engine for the cross-model winner stage
  - schedules only the needed ordered pairs
  - skips byte-identical pairs
  - writes per-document cross-judging artifacts plus aggregate scores
- `.local_scripts/generation/judge/run_two_best_tournament_lang.sh`
  - one language entrypoint
- `.local_scripts/generation/judge/run_two_best_tournament_all.sh`
  - all-language queue runner, mirroring `run_judge_all.sh`
- `.local_scripts/generation/judge/export_two_best_tournament_results.py`
  - merges cross-stage scores with the already-selected GPT/Gemini winners
  - writes the final merged winner rows

## Cache Reuse

- Use the same `JUDGE_CACHE_ROOT` as before.
- Keep the same judge model and prompt family.
- Even though this is a new stage, exact repeated ordered comparisons can still
  hit the existing cache when the prompt text matches.

## Suggested Output Layout

- Cross-stage artifacts:
  - `results/<judge-model>/artifacts/two-best/gemini-3.5-flash__gpt-final/`
- Final merged winners:
  - `results/<judge-model>/judged/two-best/gemini-3.5-flash__gpt-final/`

Suggested artifact contents:
- `cross-matrix/<lang>-winner-cross.jsonl`
- `cache/<lang>-winner-cross.cache.jsonl`
- `log/<lang>-winner-cross.log`
- final per-language merged JSONL

## Important Policy Recommendation

- Use the structure-filtered winners from the final-submission preliminary files,
  not the raw matrix `best` winners.

Why:
- that keeps the merge stage aligned with the structural safety work already done
- it avoids reintroducing a broken winner that the submission pipeline already
  repaired within a model
