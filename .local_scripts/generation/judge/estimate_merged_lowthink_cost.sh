#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/estimate_merged_lowthink_cost.sh [lang[,lang...]] [extra estimator args...]

Defaults:
  input dir: results/merged/gemini-3.5-flash__gpt-final
  judge model: gemini-2.5-flash
  JSON-only: on
  prompt chars/token: 3.65
  visible output tokens/call: 20
  thinking tokens/call: 0

Examples:
  .local_scripts/generation/judge/estimate_merged_lowthink_cost.sh all --max-hypos 16
  .local_scripts/generation/judge/estimate_merged_lowthink_cost.sh arz --max-hypos 16
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

export SOURCE_MODEL="${SOURCE_MODEL:-merged/gemini-3.5-flash__gpt-final}"
export RESULT_FILE_PREFIX="${RESULT_FILE_PREFIX:-}"
export JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
export JUDGE_JSON_ONLY="${JUDGE_JSON_ONLY:-1}"
export COST_PROMPT_CHARS_PER_TOKEN="${COST_PROMPT_CHARS_PER_TOKEN:-3.65}"
export COST_VISIBLE_OUTPUT_TOKENS="${COST_VISIBLE_OUTPUT_TOKENS:-20}"
export COST_THINKING_TOKENS="${COST_THINKING_TOKENS:-0}"

"${SCRIPT_DIR}/estimate_cost.sh" "$@"
