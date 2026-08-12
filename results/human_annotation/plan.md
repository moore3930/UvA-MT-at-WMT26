# Human Annotation Plan

## Goal
Build a reusable human-annotation workflow under `results/human_annotation/` for comparing the judge-selected best hypothesis from:
- `results/gemini-2.5-flash/judged/gemini-3.5-flash/*`
- `results/gemini-2.5-flash/judged/gpt-5.5/*`

for each of:
- `en-ar_AR`
- `en-ru_RU`
- `en-zh_CN`

using:
- 100 random shared documents per language
- blind A/B order shuffling per item
- Google Sheets upload/download for annotation
- post-hoc summaries and plots showing which source model is preferred

## Implemented Workflow

### Label space
- `A`
- `B`
- `tie`
- `unclear`

### Human CSV schema
- `item_id`
- `src`
- `hypo_A`
- `hypo_B`
- `label`

### Internal JSON schema
- `item_id`
- `doc_id`
- `language_pair`
- `source`
- `hypothesis_A`
- `hypothesis_B`
- `A_candidate_label`
- `B_candidate_label`
- `model_a`
- `model_b`
- `model_a_candidate`
- `model_b_candidate`
- `sample_seed`
- `snapshot_id`
- `judge_model`

## Output Layout

```text
results/human_annotation/
  google_oauth_config.json
  human_annotation_instructions.txt
  scripts/
    lib.sh
    annotation_utils.py
    export_best_vs_best_for_annotation.py
    upload_human_csvs_to_google_sheets.py
    download_human_csvs_from_google_sheets.py
    summarize_labelled_snapshot.py
    plot_labelled_snapshot_barplots.py
    export_all_langs.sh
    upload_all_langs_to_google_sheets.sh
    download_all_langs_from_google_sheets.sh
    summarize_all_langs.sh
    plot_all_langs.sh
  snapshots/
    <snapshot_id>/
      en-ru_RU/
        gemini-3.5-flash_vs_gpt-5.5/
          best_of_8_judge_selected.internal.json
          best_of_8_judge_selected_human.csv
  labelled_snapshot/
    <snapshot_id>/
      ...
  upload_manifests/
    <snapshot_id>/
      ...
  plots/
    <snapshot_id>/
      manual_label_raw_statistics_all_languages.json
      recovered_votes_all_languages.jsonl
      manual_label_decisive_win_rates_all_languages.svg
      manual_label_label_mix_all_languages.svg
```

## Implemented Scripts

### Export
- `export_best_vs_best_for_annotation.py`
  - joins judged outputs by `doc_id`
  - samples 100 shared docs per language with a fixed seed
  - shuffles which model appears as `A` or `B`
  - writes blinded CSV plus matching internal JSON

### Google Sheets
- `upload_human_csvs_to_google_sheets.py`
  - uploads `*_human.csv` files as Google Sheets
  - applies dropdown validation for `A`, `B`, `tie`, `unclear`
  - writes upload manifests
- `download_human_csvs_from_google_sheets.py`
  - re-downloads labelled CSVs from saved manifests

### Recovery and stats
- `summarize_labelled_snapshot.py`
  - matches labelled CSVs back to `.internal.json`
  - recovers the underlying preferred model
  - writes JSON summaries and recovered per-item JSONL

### Plots
- `plot_labelled_snapshot_barplots.py`
  - generates dependency-free SVG plots:
    - decisive win rates
    - label-mix stacked chart

### Shell wrappers
- `export_all_langs.sh`
- `upload_all_langs_to_google_sheets.sh`
- `download_all_langs_from_google_sheets.sh`
- `summarize_all_langs.sh`
- `plot_all_langs.sh`

## Main Statistics
- Per language and overall:
  - `model_a_wins`
  - `model_b_wins`
  - `tie`
  - `unclear`
  - `blank`
- Decisive win rates after excluding `tie` and `unclear`
- Decisive margin:
  - `(model_a_wins - model_b_wins) / decisive_items`

## Validation
- Python scripts pass `python3 -m py_compile`.
- Shell scripts pass `bash -n`.
- The workflow passed a temp-directory smoke test:
  - export -> synthetic labels -> summary -> SVG plots
