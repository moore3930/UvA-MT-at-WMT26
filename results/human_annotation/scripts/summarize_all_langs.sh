#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults
ensure_human_annotation_dirs

OUTPUT_DIR="${PLOTS_ROOT}/${SNAPSHOT_ID}"

"${PYTHON_BIN}" "${SCRIPT_DIR}/summarize_labelled_snapshot.py" \
  --snapshot-id "${SNAPSHOT_ID}" \
  --snapshot-root "${SNAPSHOTS_ROOT}" \
  --labelled-root "${LABELLED_ROOT}" \
  --output-dir "${OUTPUT_DIR}"
