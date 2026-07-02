#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_two_best_tournament_lang.sh <lang> [extra args...]

Examples:
  .local_scripts/generation/judge/run_two_best_tournament_lang.sh arz
  .local_scripts/generation/judge/run_two_best_tournament_lang.sh arz --limit 20

Environment overrides:
  MODEL_A                  default: gemini-3.5-flash
  MODEL_B                  default: gpt-final
  PAIR_NAME                default: <MODEL_A>__<MODEL_B>
  TIE_WINNER_DEFAULT       default: gpt-final
  JUDGE_MODEL              default: gemini-2.5-flash
  JUDGE_REASONING_EFFORT   default: none
  JUDGE_TEMPERATURE        default: 0.0
  JUDGE_CONCURRENCY        default: 32
  JUDGE_JSON_ONLY          default: 1
  JUDGE_REQUEST_TIMEOUT    default: 180
  JUDGE_STALL_REPORT_SECONDS default: 60
  RESULTS_ROOT             default: results
  JUDGE_CACHE_ROOT         default: /fnwi_fs/ivi/irlab/personal/stroshi/wmt2026_cache
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

MODEL_A="${MODEL_A:-gemini-3.5-flash}"
MODEL_B="${MODEL_B:-gpt-final}"
PAIR_NAME="${PAIR_NAME:-${MODEL_A}__${MODEL_B}}"
TIE_WINNER_DEFAULT="${TIE_WINNER_DEFAULT:-${MODEL_B}}"

MODEL_A_INPUT="${REPO_ROOT}/${RESULTS_ROOT}/${MODEL_A}/${LANG}.jsonl"
MODEL_B_INPUT="${REPO_ROOT}/${RESULTS_ROOT}/${MODEL_B}/${LANG}.jsonl"
MODEL_A_MATRIX="${REPO_ROOT}/${RESULTS_ROOT}/${JUDGE_MODEL}/artifacts/${MODEL_A}/matrix/${LANG}-llm-matrix.jsonl"
MODEL_B_MATRIX="${REPO_ROOT}/${RESULTS_ROOT}/${JUDGE_MODEL}/artifacts/${MODEL_B}/matrix/${LANG}-llm-matrix.jsonl"
OUT_DIR="${REPO_ROOT}/${RESULTS_ROOT}/${JUDGE_MODEL}/artifacts/two-best/${PAIR_NAME}"
OUT_PATH="${OUT_DIR}/cross-matrix/${LANG}-winner-cross.jsonl"
CACHE_PATH="${JUDGE_CACHE_ROOT}/${JUDGE_MODEL}/artifacts/two-best/${PAIR_NAME}/cache/${LANG}-winner-cross.cache.jsonl"

for path in "${MODEL_A_INPUT}" "${MODEL_B_INPUT}" "${MODEL_A_MATRIX}" "${MODEL_B_MATRIX}"; do
  if [[ ! -f "${path}" ]]; then
    echo "Required input not found: ${path}" >&2
    exit 1
  fi
done

mkdir -p "${OUT_DIR}/cross-matrix" "$(dirname "${CACHE_PATH}")"

PAIRWISE_ARGS=(
  --model-a-input "${MODEL_A_INPUT}"
  --model-b-input "${MODEL_B_INPUT}"
  --model-a-matrix "${MODEL_A_MATRIX}"
  --model-b-matrix "${MODEL_B_MATRIX}"
  --model-a-name "${MODEL_A}"
  --model-b-name "${MODEL_B}"
  --tie-winner-default "${TIE_WINNER_DEFAULT}"
  --out "${OUT_PATH}"
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

"${PYTHON_BIN}" "${REPO_ROOT}/pairwise_matrix_two_best_tournament.py" "${PAIRWISE_ARGS[@]}" "$@"
