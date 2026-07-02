#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

JOBS=1

LANGS=(
  arz arz_Arab bel_Cyrl ces_Latn cs cs_CZ de_AT de_CH de_DE
  de_IT deu_Latn ekk_Latn et_EE hye_Armn ind_Latn is isl_Latn jpn_Jpan
  kaz_Cyrl ko_KR kor_Hang lij_Latn lld_Latn ru ru_RU rus_Cyrl sme_Latn
  tha_Thai ukr_Cyrl vie_Latn zh_CN zho_Hans zho_Hant_TW
)

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_merged_lowthink_all.sh [options] [-- extra pairwise_matrix args...]

Runs the low-thinking Gemini judge over the merged result set:
  results/merged/gemini-3.5-flash__gpt-final

Defaults preserved from .local_scripts/gemini/low_thinking_en_ru:
  JUDGE_MODEL=gemini-2.5-flash
  JUDGE_REASONING_EFFORT=none
  JUDGE_TEMPERATURE=0.0
  JUDGE_CONCURRENCY=64
  JUDGE_JSON_ONLY=1

Options:
  -j N          languages run in parallel (default: 1)
  -l "a b c"    explicit target languages to run
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

export SOURCE_MODEL="${SOURCE_MODEL:-merged/gemini-3.5-flash__gpt-final}"
export RESULT_FILE_PREFIX="${RESULT_FILE_PREFIX:-}"
export JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
export JUDGE_REASONING_EFFORT="${JUDGE_REASONING_EFFORT:-none}"
export JUDGE_TEMPERATURE="${JUDGE_TEMPERATURE:-0.0}"
export JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-64}"
export JUDGE_JSON_ONLY="${JUDGE_JSON_ONLY:-1}"

n=${#LANGS[@]}

echo "=================================================="
echo " source model     : ${SOURCE_MODEL}"
echo " judge model      : ${JUDGE_MODEL}"
echo " reasoning effort : ${JUDGE_REASONING_EFFORT}"
echo " temperature      : ${JUDGE_TEMPERATURE}"
echo " judge concurrency: ${JUDGE_CONCURRENCY}"
echo " json only        : ${JUDGE_JSON_ONLY}"
echo " parallel langs   : ${JOBS}"
echo " target languages : ${LANGS[*]}"
[[ ${#EXTRA[@]} -gt 0 ]] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

build_cmd() {
  CMD=(bash "${SCRIPT_DIR}/run_merged_lowthink_lang.sh" "$1")
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
  LOGDIR="${PWD}/genlogs/judge_merged_lowthink_all"
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
