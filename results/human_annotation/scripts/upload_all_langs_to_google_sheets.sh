#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults
ensure_human_annotation_dirs

for lang in ar_AR ru_RU zh_CN; do
  validate_annotation_lang "${lang}"
  INPUT_ROOT="${SNAPSHOTS_ROOT}/${SNAPSHOT_ID}/en-${lang}"
  MANIFEST_PATH="${MANIFEST_ROOT}/${SNAPSHOT_ID}/google_upload_manifest_en-${lang}_${ANNOTATION_STRATEGY_NAME}.json"
  FOLDER_PREFIX="${GOOGLE_FOLDER_PREFIX}/en-${lang}"

  "${PYTHON_BIN}" "${SCRIPT_DIR}/upload_human_csvs_to_google_sheets.py" \
    --config-path "${ANNOTATION_CONFIG_PATH}" \
    --input-root "${INPUT_ROOT}" \
    --drive-root-folder-id "${GOOGLE_DRIVE_ROOT_FOLDER_ID}" \
    --remote-disk-root "${GOOGLE_REMOTE_DISK_ROOT}" \
    --folder-prefix "${FOLDER_PREFIX}" \
    --if-exists "${GOOGLE_IF_EXISTS}" \
    --manifest-path "${MANIFEST_PATH}"
done
