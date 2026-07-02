#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_judge_lang.sh <lang> [extra pairwise_matrix args...]

Examples:
  .local_scripts/generation/judge/run_judge_lang.sh ru_RU
  .local_scripts/generation/judge/run_judge_lang.sh zh_CN --limit 20

Environment overrides:
  SOURCE_MODEL             default: gemini-3.5-flash
  JUDGE_MODEL              default: gemini-2.5-flash
  JUDGE_REASONING_EFFORT   default: none
  JUDGE_TEMPERATURE        default: 0.0
  JUDGE_CONCURRENCY        default: 32
  JUDGE_JSON_ONLY          default: 1
  JUDGE_STRUCTURED_OUTPUT  default: 0
  JUDGE_REQUEST_TIMEOUT    default: 180
  JUDGE_STALL_REPORT_SECONDS default: 60
  RESULT_FILE_PREFIX       default: empty
  JUDGE_CACHE_ROOT         default: /fnwi_fs/ivi/irlab/personal/stroshi/wmt2026_cache
  JUDGE_CACHE_SOURCE_MODEL default: merged/gemini-3.5-flash__gpt-final for
                           SOURCE_MODEL in {gpt-final, gemini-3.5-flash};
                           otherwise SOURCE_MODEL
  RESULTS_ROOT             default: results
  OPENAI_BASE_URL          default: Gemini OpenAI-compatible endpoint
  OPENAI_API_KEY           resolved from env or ~/.gemini_api_key
EOF
}

if [[ $# -lt 1 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

LANG="$1"
shift

set_judge_defaults
export_gemini_env
validate_judge_lang "${LANG}"
ensure_judge_dirs

INPUT_FILE="$(input_result_path "${LANG}")"
MATRIX_OUT="$(matrix_output_path "${LANG}")"
CACHE_PATH="$(cache_output_path "${LANG}")"
JUDGED_OUT="$(judged_output_path "${LANG}")"

validate_input_result "${INPUT_FILE}"

PAIRWISE_ARGS=(
  --in "${INPUT_FILE}"
  --out "${MATRIX_OUT}"
  --cache-path "${CACHE_PATH}"
  --model "${JUDGE_MODEL}"
  --temperature "${JUDGE_TEMPERATURE}"
  --concurrency "${JUDGE_CONCURRENCY}"
  --request-timeout "${JUDGE_REQUEST_TIMEOUT}"
  --stall-report-seconds "${JUDGE_STALL_REPORT_SECONDS}"
)

if [[ -n "${JUDGE_REASONING_EFFORT}" ]]; then
  PAIRWISE_ARGS+=(--reasoning-effort "${JUDGE_REASONING_EFFORT}")
fi

if [[ "${JUDGE_JSON_ONLY}" == "1" ]]; then
  PAIRWISE_ARGS+=(--json-only)
fi

if [[ "${JUDGE_STRUCTURED_OUTPUT}" == "1" ]]; then
  PAIRWISE_ARGS+=(--structured-output-winner-only)
fi

"${PYTHON_BIN}" "${REPO_ROOT}/pairwise_matrix.py" "${PAIRWISE_ARGS[@]}" "$@"

"${PYTHON_BIN}" "${SCRIPT_DIR}/export_judged_results.py" \
  --input "${INPUT_FILE}" \
  --matrix "${MATRIX_OUT}" \
  --out "${JUDGED_OUT}" \
  --judge-model "${JUDGE_MODEL}" \
  --source-model "${SOURCE_MODEL}" \
  --judge-reasoning-effort "${JUDGE_REASONING_EFFORT}"
