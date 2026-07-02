#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LANGS=(
  arz_Arab bel_Cyrl ces_Latn deu_Latn ekk_Latn hye_Armn ind_Latn isl_Latn
  jpn_Jpan kaz_Cyrl kor_Hang lij_Latn lld_Latn rus_Cyrl sme_Latn tha_Thai
  ukr_Cyrl zho_Hans zho_Hant_TW
)

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_judge_all_v5_gpt_final_j1.sh [-- extra pairwise_matrix args...]

Runs the same Gemini judge pipeline as `run_judge_all_v5.sh`, but explicitly:
  - uses input results from `results/gpt-final`
  - keeps the judge as `gemini-2.5-flash`
  - uses `rubric/v5.txt`
  - runs one language at a time (`-j 1`)

Examples:
  .local_scripts/generation/judge/run_judge_all_v5_gpt_final_j1.sh
  .local_scripts/generation/judge/run_judge_all_v5_gpt_final_j1.sh -- --limit 20
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

EXTRA=()
if [[ "${1:-}" == "--" ]]; then
  shift
  EXTRA=("$@")
fi

export SOURCE_MODEL="${SOURCE_MODEL:-gpt-final}"
export JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
export JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-32}"
export JUDGE_STALL_REPORT_SECONDS="${JUDGE_STALL_REPORT_SECONDS:-20}"
export EXPERIMENT_TAG="${EXPERIMENT_TAG:-rubric-v5}"

LANGS_SPACE="$(IFS=' '; echo "${LANGS[*]}")"

exec bash "${SCRIPT_DIR}/run_judge_all_v5.sh" -j 1 -l "${LANGS_SPACE}" "${EXTRA[@]}"
