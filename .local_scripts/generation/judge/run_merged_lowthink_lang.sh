#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_merged_lowthink_lang.sh <lang> [extra pairwise_matrix args...]

Examples:
  .local_scripts/generation/judge/run_merged_lowthink_lang.sh arz
  .local_scripts/generation/judge/run_merged_lowthink_lang.sh arz --limit 20

Runs the low-thinking Gemini judge on one merged result file under:
  results/merged/gemini-3.5-flash__gpt-final

Defaults preserved from .local_scripts/gemini/low_thinking_en_ru:
  JUDGE_MODEL=gemini-2.5-flash
  JUDGE_REASONING_EFFORT=none
  JUDGE_TEMPERATURE=0.0
  JUDGE_CONCURRENCY=64
  JUDGE_JSON_ONLY=1
EOF
}

if [[ $# -lt 1 || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

export SOURCE_MODEL="${SOURCE_MODEL:-merged/gemini-3.5-flash__gpt-final}"
export RESULT_FILE_PREFIX="${RESULT_FILE_PREFIX:-}"
export JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
export JUDGE_REASONING_EFFORT="${JUDGE_REASONING_EFFORT:-none}"
export JUDGE_TEMPERATURE="${JUDGE_TEMPERATURE:-0.0}"
export JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-64}"
export JUDGE_JSON_ONLY="${JUDGE_JSON_ONLY:-1}"

"${SCRIPT_DIR}/run_judge_lang.sh" "$@"
