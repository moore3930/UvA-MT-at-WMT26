#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HUMAN_ANNOTATION_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${HUMAN_ANNOTATION_ROOT}/../.." && pwd)"
REPO_VENV_PYTHON="${REPO_ROOT}/.venv/bin/python"

set_human_annotation_defaults() {
  if [[ -z "${PYTHON_BIN:-}" ]]; then
    if [[ -x "${REPO_VENV_PYTHON}" ]]; then
      export PYTHON_BIN="${REPO_VENV_PYTHON}"
    elif command -v python >/dev/null 2>&1; then
      export PYTHON_BIN="python"
    else
      export PYTHON_BIN="python3"
    fi
  else
    export PYTHON_BIN
  fi
  export SNAPSHOT_ID="${SNAPSHOT_ID:-$(date +%Y%m%d)_best_of_8_judge_selected}"
  export SAMPLE_SIZE="${SAMPLE_SIZE:-}"
  export SAMPLE_SEED="${SAMPLE_SEED:-20260630}"

  export SOURCE_MODEL_A="${SOURCE_MODEL_A:-gemini-3.5-flash}"
  export SOURCE_MODEL_B="${SOURCE_MODEL_B:-gpt-5.5}"
  export JUDGED_RESULTS_ROOT="${JUDGED_RESULTS_ROOT:-${REPO_ROOT}/results/gemini-2.5-flash/judged}"
  export ALIGNED_INPUTS_ROOT="${ALIGNED_INPUTS_ROOT:-${REPO_ROOT}/results/gemini-3.5-flash/aligned_inputs}"

  export SNAPSHOTS_ROOT="${SNAPSHOTS_ROOT:-${HUMAN_ANNOTATION_ROOT}/snapshots}"
  export LABELLED_ROOT="${LABELLED_ROOT:-${HUMAN_ANNOTATION_ROOT}/labelled_snapshot}"
  export PLOTS_ROOT="${PLOTS_ROOT:-${HUMAN_ANNOTATION_ROOT}/plots}"
  export MANIFEST_ROOT="${MANIFEST_ROOT:-${HUMAN_ANNOTATION_ROOT}/upload_manifests}"

  export ANNOTATION_CONFIG_PATH="${ANNOTATION_CONFIG_PATH:-${HUMAN_ANNOTATION_ROOT}/google_oauth_config.json}"
  export ANNOTATION_STRATEGY_NAME="${ANNOTATION_STRATEGY_NAME:-best_of_8_judge_selected}"
  export ANNOTATION_COMPARISON_NAME="${ANNOTATION_COMPARISON_NAME:-${SOURCE_MODEL_A}_vs_${SOURCE_MODEL_B}}"

  export GOOGLE_DRIVE_ROOT_FOLDER_ID="${GOOGLE_DRIVE_ROOT_FOLDER_ID:-root}"
  export GOOGLE_REMOTE_DISK_ROOT="${GOOGLE_REMOTE_DISK_ROOT:-UvA-MT-at-WMT26}"
  export GOOGLE_FOLDER_PREFIX="${GOOGLE_FOLDER_PREFIX:-human_annotation/${SNAPSHOT_ID}}"
  export GOOGLE_IF_EXISTS="${GOOGLE_IF_EXISTS:-skip}"
}

validate_annotation_lang() {
  local lang="${1:-}"
  case "${lang}" in
    ar_AR|ru_RU|zh_CN)
      ;;
    *)
      echo "Unsupported language '${lang}'. Expected one of: ar_AR, ru_RU, zh_CN" >&2
      return 1
      ;;
  esac
}

ensure_human_annotation_dirs() {
  mkdir -p \
    "${SNAPSHOTS_ROOT}" \
    "${LABELLED_ROOT}" \
    "${PLOTS_ROOT}" \
    "${MANIFEST_ROOT}"
}
