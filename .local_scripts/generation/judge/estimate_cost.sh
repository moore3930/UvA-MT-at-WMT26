#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/estimate_cost.sh [lang[,lang...]] [extra estimator args...]

Defaults:
  langs: all files under results/<SOURCE_MODEL>/

Environment overrides:
  SOURCE_MODEL                    default: gemini-3.5-flash
  JUDGE_MODEL                     default: gemini-2.5-flash
  JUDGE_JSON_ONLY                 default: 1
  RESULT_FILE_PREFIX              default: empty
  COST_PROMPT_CHARS_PER_TOKEN     default: 2.0
  COST_VISIBLE_OUTPUT_TOKENS      default: 20
  COST_THINKING_TOKENS            default: 0
  RESULTS_ROOT                    default: results
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

set_judge_defaults

LANGS="${1:-all}"
if [[ $# -ge 1 ]]; then
  shift
fi

ARGS=(
  --input-dir "${INPUT_RESULTS_DIR}"
  --model "${JUDGE_MODEL}"
  --langs "${LANGS}"
  --result-file-prefix "${RESULT_FILE_PREFIX}"
  --prompt-chars-per-token "${COST_PROMPT_CHARS_PER_TOKEN}"
  --visible-output-tokens-per-call "${COST_VISIBLE_OUTPUT_TOKENS}"
  --thinking-tokens-per-call "${COST_THINKING_TOKENS}"
)

if [[ "${JUDGE_JSON_ONLY}" == "1" ]]; then
  ARGS+=(--json-only)
fi

"${PYTHON_BIN}" "${SCRIPT_DIR}/estimate_judge_cost.py" "${ARGS[@]}" "$@"
