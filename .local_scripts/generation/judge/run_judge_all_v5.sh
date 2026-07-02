#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
source "${SCRIPT_DIR}/lib.sh"

JOBS=1
LANGS=(
  arz_Arab bel_Cyrl ces_Latn deu_Latn ekk_Latn hye_Armn ind_Latn isl_Latn
  jpn_Jpan kaz_Cyrl kor_Hang lij_Latn lld_Latn rus_Cyrl sme_Latn tha_Thai
  ukr_Cyrl zho_Hans zho_Hant_TW
)

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_judge_all_v5.sh [options] [-- extra pairwise_matrix args...]

Runs the judge over a reduced language set using `rubric/v5.txt` and isolated
experiment output/cache roots so the run does not clash with the default judge
artifacts.

Default language set:
  arz_Arab bel_Cyrl ces_Latn deu_Latn ekk_Latn hye_Armn ind_Latn isl_Latn
  jpn_Jpan kaz_Cyrl kor_Hang lij_Latn lld_Latn rus_Cyrl sme_Latn tha_Thai
  ukr_Cyrl zho_Hans zho_Hant_TW

Environment overrides:
  SOURCE_MODEL             default: gpt-final
  JUDGE_MODEL              default: gemini-2.5-flash
  EXPERIMENT_TAG           default: rubric-v5
  JUDGE_REASONING_EFFORT   default: none
  JUDGE_TEMPERATURE        default: 0.0
  JUDGE_CONCURRENCY        default: 32
  JUDGE_JSON_ONLY          default: 1
  JUDGE_STRUCTURED_OUTPUT  default: 1 (required)
  JUDGE_STALL_REPORT_SECONDS default: 20
  RESULT_FILE_PREFIX       default: empty
  RESULTS_ROOT             default: results

Options:
  -j N          languages run in parallel (default: 1)
  -l "a b c"    explicit target languages to run instead of the default subset
  -h            show this help
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

SOURCE_MODEL="${SOURCE_MODEL:-gpt-final}"
JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
EXPERIMENT_TAG="${EXPERIMENT_TAG:-rubric-v5}"
JUDGE_STALL_REPORT_SECONDS="${JUDGE_STALL_REPORT_SECONDS:-20}"
JUDGE_STRUCTURED_OUTPUT="${JUDGE_STRUCTURED_OUTPUT:-1}"
EXPERIMENT_ROOT_DEFAULT="${REPO_ROOT}/results/${JUDGE_MODEL}/experiments/${SOURCE_MODEL}_${EXPERIMENT_TAG}"
ARTIFACT_ROOT="${ARTIFACT_ROOT:-${EXPERIMENT_ROOT_DEFAULT}}"
CACHE_ARTIFACT_ROOT="${CACHE_ARTIFACT_ROOT:-${EXPERIMENT_ROOT_DEFAULT}}"
JUDGED_ROOT="${JUDGED_ROOT:-${EXPERIMENT_ROOT_DEFAULT}/judged}"
export SOURCE_MODEL JUDGE_MODEL EXPERIMENT_TAG JUDGE_STALL_REPORT_SECONDS JUDGE_STRUCTURED_OUTPUT
export ARTIFACT_ROOT CACHE_ARTIFACT_ROOT JUDGED_ROOT

set_judge_defaults
require_structured_output

n=${#LANGS[@]}

echo "=================================================="
echo " source model     : ${SOURCE_MODEL}"
echo " judge model      : ${JUDGE_MODEL}"
echo " experiment tag   : ${EXPERIMENT_TAG}"
echo " rubric file      : ${REPO_ROOT}/rubric/v5.txt"
echo " reasoning effort : ${JUDGE_REASONING_EFFORT}"
echo " temperature      : ${JUDGE_TEMPERATURE}"
echo " judge concurrency: ${JUDGE_CONCURRENCY}"
echo " stall seconds    : ${JUDGE_STALL_REPORT_SECONDS}"
echo " json only        : ${JUDGE_JSON_ONLY}"
echo " structured out   : ${JUDGE_STRUCTURED_OUTPUT}"
echo " result prefix    : ${RESULT_FILE_PREFIX:-<empty>}"
echo " artifact root    : ${ARTIFACT_ROOT}"
echo " cache root       : ${CACHE_ARTIFACT_ROOT}"
echo " judged root      : ${JUDGED_ROOT}"
echo " parallel langs   : ${JOBS}"
echo " target languages : ${LANGS[*]}"
[[ ${#EXTRA[@]} -gt 0 ]] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

build_cmd() {
  CMD=(bash "${SCRIPT_DIR}/run_judge_lang.sh" "$1" --rubric-file "${REPO_ROOT}/rubric/v5.txt")
  CMD+=(${EXTRA[@]+"${EXTRA[@]}"})
}

print_running() {
  local count="${#PLANG[@]}"
  if [[ "${count}" -eq 0 ]]; then
    echo "[queue] running 0/${JOBS}: <none>"
  else
    echo "[queue] running ${count}/${JOBS}: ${PLANG[*]}"
  fi
}

fail=()

if [[ "${JOBS}" -le 1 ]]; then
  i=0
  for lang in "${LANGS[@]}"; do
    i=$((i + 1))
    echo
    echo "###### [${i}/${n}] tgt_lang=${lang} ######"
    build_cmd "${lang}"
    echo "+ ${CMD[*]}"
    if ! "${CMD[@]}"; then
      echo "!! FAILED: ${lang}" >&2
      fail+=("${lang}")
    fi
  done
else
  LOGDIR="${PWD}/genlogs/judge_all_v5"
  mkdir -p "${LOGDIR}"
  echo "up to ${JOBS} languages in parallel; per-language logs in ${LOGDIR}/"
  PIDS=()
  PLANG=()
  done_count=0

  reap_one_finished() {
    local wait_rc pid lang rc idx
    wait -n || wait_rc=$?
    wait_rc="${wait_rc:-0}"

    for idx in "${!PIDS[@]}"; do
      pid="${PIDS[$idx]}"
      if kill -0 "${pid}" 2>/dev/null; then
        continue
      fi
      lang="${PLANG[$idx]}"
      wait "${pid}" || rc=$?
      rc="${rc:-0}"
      done_count=$((done_count + 1))
      if [[ "${rc}" -ne 0 ]]; then
        echo "[done ${done_count}/${n}] FAILED ${lang} (see ${LOGDIR}/${lang}.log)" >&2
        fail+=("${lang}")
      else
        echo "[done ${done_count}/${n}] ok ${lang}"
      fi
      unset 'PIDS[idx]'
      unset 'PLANG[idx]'
      PIDS=("${PIDS[@]}")
      PLANG=("${PLANG[@]}")
      print_running
      return 0
    done

    echo "[warn] wait -n returned ${wait_rc}, but no finished job was identified" >&2
    return 1
  }

  i=0
  for lang in "${LANGS[@]}"; do
    while [[ "${#PIDS[@]}" -ge "${JOBS}" ]]; do
      reap_one_finished
    done
    i=$((i + 1))
    build_cmd "${lang}"
    echo "[start ${i}/${n}] ${lang}  (log: ${LOGDIR}/${lang}.log)"
    ( "${CMD[@]}" > "${LOGDIR}/${lang}.log" 2>&1 ) &
    PIDS+=("$!")
    PLANG+=("${lang}")
    print_running
  done
  while [[ "${#PIDS[@]}" -gt 0 ]]; do
    reap_one_finished
  done
fi

echo
echo "=================================================="
if [[ ${#fail[@]} -eq 0 ]]; then
  echo "All ${n} language(s) completed."
else
  echo "Completed with failures: ${fail[*]}"
  exit 1
fi
