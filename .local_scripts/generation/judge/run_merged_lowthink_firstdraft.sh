#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOBS=1

LANGS=(
  arz arz_Arab bel_Cyrl
)

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_merged_lowthink_firstdraft.sh [options] [-- extra pairwise_matrix args...]

Runs a first-draft low-thinking Gemini judge pass over roughly 20% of the
merged language files under:
  results/merged/gemini-3.5-flash__gpt-final

Current merged set size: 33 files
Default first-draft size: 7 files (explicit list)

Options:
  -j N          languages run in parallel (default: 1)
  -l "a b c"    explicit target languages to run
  -h            show this help

Environment overrides:
  JUDGE_MODEL              default: gemini-2.5-flash
  JUDGE_REASONING_EFFORT   default: none
  JUDGE_TEMPERATURE        default: 0.0
  JUDGE_CONCURRENCY        default: 64
  JUDGE_JSON_ONLY          default: 1
EOF
}

while getopts "j:l:h" opt; do
  case "${opt}" in
    j) JOBS="${OPTARG}" ;;
    l) read -r -a LANGS <<< "${OPTARG}" ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
EXTRA=("$@")

export SOURCE_MODEL="${SOURCE_MODEL:-merged/gemini-3.5-flash__gpt-final}"
export RESULT_FILE_PREFIX="${RESULT_FILE_PREFIX:-}"
export JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
export JUDGE_REASONING_EFFORT="${JUDGE_REASONING_EFFORT:-none}"
export JUDGE_TEMPERATURE="${JUDGE_TEMPERATURE:-0.0}"
export JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-64}"
export JUDGE_JSON_ONLY="${JUDGE_JSON_ONLY:-1}"

echo "First-draft merged run: ${#LANGS[@]} languages"
CMD=(bash "${SCRIPT_DIR}/run_merged_lowthink_all.sh" -j "${JOBS}" -l "${LANGS[*]}")
CMD+=(${EXTRA[@]+"${EXTRA[@]}"})
"${CMD[@]}"
