# How To Judge And Submit

Run all commands from the repo root:

```bash
cd /home/stroshi/UvA-MT-at-WMT26
```

## Selected Languages

These commands use the reduced language set:

```bash
LANGS_SPACE="arz_Arab bel_Cyrl ces_Latn deu_Latn ekk_Latn hye_Armn ind_Latn isl_Latn jpn_Jpan kaz_Cyrl kor_Hang lij_Latn lld_Latn rus_Cyrl sme_Latn tha_Thai ukr_Cyrl zho_Hans zho_Hant_TW"
LANGS_CSV="arz_Arab,bel_Cyrl,ces_Latn,deu_Latn,ekk_Latn,hye_Armn,ind_Latn,isl_Latn,jpn_Jpan,kaz_Cyrl,kor_Hang,lij_Latn,lld_Latn,rus_Cyrl,sme_Latn,tha_Thai,ukr_Cyrl,zho_Hans,zho_Hant_TW"
```

## Important

Structured outputs are required for this workflow.

- `run_judge_all_v5.sh` now fails if `JUDGE_STRUCTURED_OUTPUT=1` is not set
- `run_two_best_tournament_all.sh` now fails if `JUDGE_STRUCTURED_OUTPUT=1` is not set

Use:

```bash
EXPERIMENT_TAG=rubric-v5-structured
JUDGE_STRUCTURED_OUTPUT=1
```

## 1. Judge `results/gpt-final`

This reads samples from `results/gpt-final` and writes structured judge outputs under:

- `results/gemini-2.5-flash/experiments/gpt-final_rubric-v5-structured/`

Command:

```bash
SOURCE_MODEL=gpt-final \
JUDGE_MODEL=gemini-2.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_judge_all_v5.sh -j 5 -l "$LANGS_SPACE"
```

## 2. Judge `results/gemini-3.5-flash`

This reads samples from `results/gemini-3.5-flash` and writes structured judge outputs under:

- `results/gemini-2.5-flash/experiments/gemini-3.5-flash_rubric-v5-structured/`

Command:

```bash
SOURCE_MODEL=gemini-3.5-flash \
JUDGE_MODEL=gemini-2.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_judge_all_v5.sh -j 5 -l "$LANGS_SPACE"
```

## 3. Judge The Best-From-Each-Model Head-To-Head

This compares the judged best hypothesis from `gemini-3.5-flash` against the judged best hypothesis from `gpt-final`, using the structured single-model judge outputs from the same experiment tag.

Outputs go under:

- `results/gemini-2.5-flash/experiments/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/`

Command:

```bash
MODEL_A=gemini-3.5-flash \
MODEL_B=gpt-final \
PAIR_NAME=gemini-3.5-flash__gpt-final \
JUDGE_MODEL=gemini-2.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_two_best_tournament_all.sh -j 5 -l "$LANGS_SPACE"
```

## 4. Merge With The Older Run For The Remaining Languages

This step should be done after the selected-language two-best output from section 5 is ready.

TODO after the structured judge runs finish and the selected-language two-best output looks good:

- merge the new structured-output results for the selected languages with the older run for the remaining unused languages
- build one final full-output file covering all languages

## 5. Build The Two-Best Output For The Selected Languages

This uses the structured single-model judge outputs plus the structured two-best cross-model judge outputs.

Output directory:

- `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/`

Command:

```bash
bash final_submission/run_two_best_submission_pipeline.sh \
  --model-a gemini-3.5-flash \
  --model-b gpt-final \
  --judge-model gemini-2.5-flash \
  --experiment-tag rubric-v5-structured \
  --langs "$LANGS_CSV"
```

Main output file:

- `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/submission.jsonl`

This is only the new output for the selected 19 languages. It is not yet the final full deliverable.

## 6. Final Submission

Only after the merge step above:

- produce the final full submission artifact for delivery
