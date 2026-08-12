#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults
ensure_human_annotation_dirs

OUTPUT_DIR="${PLOTS_ROOT}/${SNAPSHOT_ID}"
SUMMARY_PATH="${OUTPUT_DIR}/manual_label_raw_statistics_all_languages.json"

"${PYTHON_BIN}" "${SCRIPT_DIR}/plot_labelled_snapshot_barplots.py" \
  --summary-path "${SUMMARY_PATH}" \
  --output-dir "${OUTPUT_DIR}"
