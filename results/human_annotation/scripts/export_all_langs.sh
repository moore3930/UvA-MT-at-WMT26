#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults
ensure_human_annotation_dirs

EXCLUDE_ARGS=()
SAMPLE_ARGS=()
if [[ -n "${EXCLUDE_SNAPSHOT_IDS:-}" ]]; then
  IFS=',' read -r -a _exclude_ids <<< "${EXCLUDE_SNAPSHOT_IDS}"
  for snapshot_id in "${_exclude_ids[@]}"; do
    if [[ -n "${snapshot_id}" ]]; then
      EXCLUDE_ARGS+=(--exclude-snapshot-id "${snapshot_id}")
    fi
  done
fi

if [[ -n "${SAMPLE_SIZE}" ]]; then
  SAMPLE_ARGS+=(--sample-size "${SAMPLE_SIZE}")
fi

for lang in ar_AR ru_RU zh_CN; do
  validate_annotation_lang "${lang}"
  "${PYTHON_BIN}" "${SCRIPT_DIR}/export_best_vs_best_for_annotation.py" \
    --lang "${lang}" \
    --judged-root "${JUDGED_RESULTS_ROOT}" \
    --aligned-inputs-root "${ALIGNED_INPUTS_ROOT}" \
    --snapshot-root "${SNAPSHOTS_ROOT}" \
    --snapshot-id "${SNAPSHOT_ID}" \
    --seed "${SAMPLE_SEED}" \
    --model-a "${SOURCE_MODEL_A}" \
    --model-b "${SOURCE_MODEL_B}" \
    --strategy-name "${ANNOTATION_STRATEGY_NAME}" \
    "${SAMPLE_ARGS[@]}" \
    "${EXCLUDE_ARGS[@]}"
done
