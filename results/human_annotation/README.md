# Human Annotation Workflow

This directory contains the export, Google Sheets upload/download, and result-recovery workflow for human evaluation of:

- `results/gemini-2.5-flash/judged/gemini-3.5-flash/*`
- `results/gemini-2.5-flash/judged/gpt-5.5/*`

The comparison is:

- one document at a time
- best judged hypothesis vs best judged hypothesis
- blinded as `A` vs `B`
- labels allowed: `A`, `B`, `tie`, `unclear`

The scripts default to using all shared items for:

- `en-ar_AR`
- `en-ru_RU`
- `en-zh_CN`

Item order is shuffled deterministically, and A/B order is also shuffled deterministically per item.

## Setup

Install the Google client dependencies into the repo environment:

```bash
uv sync --extra human-annotation
```

The scripts prefer:

```bash
/home/stroshi/UvA-MT-at-WMT26/.venv/bin/python
```

Google OAuth defaults live in:

- [google_oauth_config.json](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/google_oauth_config.json)

You will need:

- a valid Google OAuth client secrets file
- a token path where the login token can be stored
- Drive + Sheets API access enabled for that Google project

## Run Order

### 1. Export blinded CSVs

```bash
results/human_annotation/scripts/export_all_langs.sh
```

This writes:

- `snapshots/<snapshot_id>/.../*.internal.json`
- `snapshots/<snapshot_id>/.../*_human.csv`

### 2. Upload to Google Sheets

```bash
results/human_annotation/scripts/upload_all_langs_to_google_sheets.sh
```

This writes upload manifests under:

- `upload_manifests/<snapshot_id>/`

### 3. Annotate in Google Sheets

For each row, fill the `label` column with one of:

- `A`
- `B`
- `tie`
- `unclear`

Instructions for annotators are in:

- [human_annotation_instructions.txt](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/human_annotation_instructions.txt)

### 4. Download completed CSVs

```bash
results/human_annotation/scripts/download_all_langs_from_google_sheets.sh
```

This writes labelled CSVs under:

- `labelled_snapshot/<snapshot_id>/`

For an existing snapshot, set `SNAPSHOT_ID` explicitly so the downloader uses the
saved manifests for that run:

```bash
SNAPSHOT_ID=20260630_best_of_8_judge_selected \
results/human_annotation/scripts/download_all_langs_from_google_sheets.sh
```

If you want to download just one language from a specific manifest, run the
lower-level script directly. Example for `en-ru_RU`:

```bash
./.venv/bin/python results/human_annotation/scripts/download_human_csvs_from_google_sheets.py \
  --config-path results/human_annotation/google_oauth_config.json \
  --manifest-path results/human_annotation/upload_manifests/20260630_best_of_8_judge_selected/google_upload_manifest_en-ru_RU_best_of_8_judge_selected.json \
  --output-root results/human_annotation/labelled_snapshot/20260630_best_of_8_judge_selected/en-ru_RU
```

### 5. Recover results and summarize

```bash
results/human_annotation/scripts/summarize_all_langs.sh
```

For an existing snapshot, set `SNAPSHOT_ID` explicitly:

```bash
SNAPSHOT_ID=20260630_best_of_8_judge_selected \
results/human_annotation/scripts/summarize_all_langs.sh
```

Direct Python equivalent:

```bash
./.venv/bin/python results/human_annotation/scripts/summarize_labelled_snapshot.py \
  --snapshot-id 20260630_best_of_8_judge_selected \
  --snapshot-root results/human_annotation/snapshots \
  --labelled-root results/human_annotation/labelled_snapshot \
  --output-dir results/human_annotation/plots/20260630_best_of_8_judge_selected
```

This writes:

- `plots/<snapshot_id>/manual_label_raw_statistics_all_languages.json`
- `plots/<snapshot_id>/recovered_votes_all_languages.jsonl`

### 6. Generate plots

```bash
results/human_annotation/scripts/plot_all_langs.sh
```

For an existing snapshot, set `SNAPSHOT_ID` explicitly:

```bash
SNAPSHOT_ID=20260630_best_of_8_judge_selected \
results/human_annotation/scripts/plot_all_langs.sh
```

Direct Python equivalent:

```bash
./.venv/bin/python results/human_annotation/scripts/plot_labelled_snapshot_barplots.py \
  --summary-path results/human_annotation/plots/20260630_best_of_8_judge_selected/manual_label_raw_statistics_all_languages.json \
  --output-dir results/human_annotation/plots/20260630_best_of_8_judge_selected
```

This writes:

- `plots/<snapshot_id>/manual_label_decisive_win_rates_all_languages.svg`
- `plots/<snapshot_id>/manual_label_label_mix_all_languages.svg`

## Useful Overrides

All wrappers accept environment-variable overrides.

### Change snapshot id

```bash
SNAPSHOT_ID=20260701_best_of_8_judge_selected \
results/human_annotation/scripts/export_all_langs.sh
```

### Export only a subset

`SAMPLE_SIZE` is empty by default, which means all shared items.

```bash
SAMPLE_SIZE=100 \
results/human_annotation/scripts/export_all_langs.sh
```

### Change shuffle seed

```bash
SAMPLE_SEED=42 \
results/human_annotation/scripts/export_all_langs.sh
```

### Exclude documents already used in earlier snapshots

Comma-separated:

```bash
EXCLUDE_SNAPSHOT_IDS=20260630_best_of_8_judge_selected \
results/human_annotation/scripts/export_all_langs.sh
```

### Override Google upload location

```bash
GOOGLE_REMOTE_DISK_ROOT=UvA-MT-at-WMT26 \
GOOGLE_FOLDER_PREFIX=human_annotation/my_snapshot \
results/human_annotation/scripts/upload_all_langs_to_google_sheets.sh
```

## Main Scripts

- [scripts/export_all_langs.sh](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/export_all_langs.sh)
- [scripts/upload_all_langs_to_google_sheets.sh](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/upload_all_langs_to_google_sheets.sh)
- [scripts/download_all_langs_from_google_sheets.sh](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/download_all_langs_from_google_sheets.sh)
- [scripts/summarize_all_langs.sh](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/summarize_all_langs.sh)
- [scripts/plot_all_langs.sh](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/plot_all_langs.sh)

Lower-level utilities:

- [scripts/export_best_vs_best_for_annotation.py](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/export_best_vs_best_for_annotation.py)
- [scripts/upload_human_csvs_to_google_sheets.py](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/upload_human_csvs_to_google_sheets.py)
- [scripts/download_human_csvs_from_google_sheets.py](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/download_human_csvs_from_google_sheets.py)
- [scripts/summarize_labelled_snapshot.py](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/summarize_labelled_snapshot.py)
- [scripts/plot_labelled_snapshot_barplots.py](/home/stroshi/UvA-MT-at-WMT26/results/human_annotation/scripts/plot_labelled_snapshot_barplots.py)
