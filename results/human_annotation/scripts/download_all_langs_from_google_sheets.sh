#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults
ensure_human_annotation_dirs

for lang in ar_AR ru_RU zh_CN; do
  validate_annotation_lang "${lang}"
  MANIFEST_PATH="${MANIFEST_ROOT}/${SNAPSHOT_ID}/google_upload_manifest_en-${lang}_${ANNOTATION_STRATEGY_NAME}.json"
  OUTPUT_ROOT="${LABELLED_ROOT}/${SNAPSHOT_ID}/en-${lang}"

  "${PYTHON_BIN}" "${SCRIPT_DIR}/download_human_csvs_from_google_sheets.py" \
    --config-path "${ANNOTATION_CONFIG_PATH}" \
    --manifest-path "${MANIFEST_PATH}" \
    --output-root "${OUTPUT_ROOT}"
done
