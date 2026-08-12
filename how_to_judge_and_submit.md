# How To Judge And Submit

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

## `gpt-final` Provenance

`results/gpt-final/` is not one single GPT model. It is a per-language merged GPT set:

- from `results/gpt-5.5/`:
  - `arz`, `arz_Arab`
- from `results/gpt-5.4/`:
  - `bel_Cyrl`, `ces_Latn`, `deu_Latn`, `ekk_Latn`, `hye_Armn`, `ind_Latn`, `isl_Latn`, `jpn_Jpan`, `kaz_Cyrl`, `kor_Hang`, `lij_Latn`, `lld_Latn`, `rus_Cyrl`, `sme_Latn`, `tha_Thai`, `ukr_Cyrl`, `zho_Hans`, `zho_Hant_TW`
- from `results/gpt-4o-mini/`:
  - `cs`, `cs_CZ`, `de_AT`, `de_CH`, `de_DE`, `de_IT`, `et_EE`, `is`, `ko_KR`, `ru`, `ru_RU`, `vie_Latn`, `zh_CN`

## 1. Judge `results/gpt-final`

This reads samples from `results/gpt-final` and writes structured judge outputs under:

- `results/gemini-3.5-flash/experiments/gpt-final_rubric-v5-structured/`

Command:

```bash
SOURCE_MODEL=gpt-final \
JUDGE_MODEL=gemini-3.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_judge_all_v5.sh -j 5 -l "$LANGS_SPACE"
```

## 2. Judge `results/gemini-3.5-flash`

This reads samples from `results/gemini-3.5-flash` and writes structured judge outputs under:

- `results/gemini-3.5-flash/experiments/gemini-3.5-flash_rubric-v5-structured/`

Command:

```bash
SOURCE_MODEL=gemini-3.5-flash \
JUDGE_MODEL=gemini-3.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_judge_all_v5.sh -j 5 -l "$LANGS_SPACE"
```

## 3. Judge The Best-From-Each-Model Head-To-Head

This compares the judged best hypothesis from `gemini-3.5-flash` against the judged best hypothesis from `gpt-final`, using the structured single-model judge outputs from the same experiment tag.

Outputs go under:

- `results/gemini-3.5-flash/experiments/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/`

Command:

```bash
MODEL_A=gemini-3.5-flash \
MODEL_B=gpt-final \
PAIR_NAME=gemini-3.5-flash__gpt-final \
JUDGE_MODEL=gemini-3.5-flash \
EXPERIMENT_TAG=rubric-v5-structured \
JUDGE_CONCURRENCY=32 \
JUDGE_STALL_REPORT_SECONDS=20 \
JUDGE_STRUCTURED_OUTPUT=1 \
bash .local_scripts/generation/judge/run_two_best_tournament_all.sh -j 5 -l "$LANGS_SPACE"
```
## 4. Merge With The Older Run For The Remaining Languages

This step should be done after the selected-language two-best output from section 5 is ready.

Paths involved:

- selected-language merge input from section 5:
  - `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- older full preliminary input:
  - `final_submission/out/two-best/gemini-3.5-flash__gpt-final/preliminary_final.jsonl`
- new structured single-model judged outputs:
  - `results/gemini-3.5-flash/experiments/gemini-3.5-flash_rubric-v5-structured/judged/`
  - `results/gemini-3.5-flash/experiments/gpt-final_rubric-v5-structured/judged/`
- new structured two-best cross-model outputs:
  - `results/gemini-3.5-flash/experiments/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/cross-matrix/`
- older full merged run:
  - `results/merged/gemini-3.5-flash__gpt-final/`

Small stats right now:

- new structured run coverage: `19` selected languages
- older merged run coverage: `33` languages
- older-only remainder to keep during merge: `14` languages

Goal:

- replace the selected `19` language outputs in `results/merged/gemini-3.5-flash__gpt-final/` with the new structured two-best results
- keep the remaining `14` older-language files
- then build one final full-output file covering all `33` languages

Command:

```bash
bash final_submission/run_merge_two_submissions.sh
```

Main output directory:

- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/`

Main merged artifacts:

- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/submission.jsonl`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/source.filtered.jsonl`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/per_language/`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/reports/pipeline_summary.md`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/reports/merge_report.json`
- `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/reports/wmt_alignment_stdout.txt`


## 5. Build The Two-Best Output For The Selected Languages

This uses the structured single-model judge outputs plus the structured two-best cross-model judge outputs.

Output directory:

- `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/`

Command:

```bash
bash final_submission/run_two_best_submission_pipeline.sh \
  --model-a gemini-3.5-flash \
  --model-b gpt-final \
  --judge-model gemini-3.5-flash \
  --experiment-tag rubric-v5-structured \
  --langs "$LANGS_CSV"
```

Main output file:

- `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- `final_submission/out/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/submission.jsonl`

This is only the new output for the selected 19 languages. It is not yet the final full deliverable.


## 6. Final Submission

Only after the merge step above:

Scripts run:

- `bash final_submission/run_two_best_submission_pipeline.sh --model-a gemini-3.5-flash --model-b gpt-final --judge-model gemini-3.5-flash --experiment-tag rubric-v5-structured --langs "$LANGS_CSV"`
- `bash final_submission/run_merge_two_submissions.sh`

Final artifacts:

- deliver:
  - `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/submission.jsonl`
- source-ordered merged final:
  - `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- per-language merged files:
  - `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/per_language/`
- merge summary:
  - `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/reports/pipeline_summary.md`
- WMT alignment report:
  - `final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/reports/wmt_alignment_stdout.txt`

Final checks completed:

- `19` selected-language merged files present
- `33` merged language files present in total
- WMT alignment: `1914 checked, 1914 aligned, 0 misaligned`
- `doc_id` and `tgt_lang` align one-to-one with `wmt26_genmt_blindset_filter_parse.jsonl`
