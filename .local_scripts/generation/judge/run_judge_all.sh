#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

JOBS=1
LANGS=()

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_judge_all.sh [options] [-- extra pairwise_matrix args...]

This runs judge export over result files under `results/<SOURCE_MODEL>/`.

Environment overrides:
  SOURCE_MODEL             default: gemini-3.5-flash
  JUDGE_MODEL              default: gemini-2.5-flash
  JUDGE_REASONING_EFFORT   default: none
  JUDGE_TEMPERATURE        default: 0.0
  JUDGE_CONCURRENCY        default: 32
  JUDGE_JSON_ONLY          default: 1
  JUDGE_MAX_FILES          default: all files
  RESULT_FILE_PREFIX       default: empty
  JUDGE_CACHE_ROOT         default: /fnwi_fs/ivi/irlab/personal/stroshi/wmt2026_cache
  JUDGE_CACHE_SOURCE_MODEL default: merged/gemini-3.5-flash__gpt-final for
                           SOURCE_MODEL in {gpt-final, gemini-3.5-flash};
                           otherwise SOURCE_MODEL
  RESULTS_ROOT             default: results

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

set_judge_defaults

if [[ ${#LANGS[@]} -eq 0 ]]; then
  shopt -s nullglob
  FILES=("${INPUT_RESULTS_DIR}"/$(result_glob_pattern))
  shopt -u nullglob

  if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "No input result files found under ${INPUT_RESULTS_DIR}" >&2
    exit 1
  fi

  for file in "${FILES[@]}"; do
    LANGS+=("$(lang_from_result_file "${file}")")
  done
fi

TOTAL_FILES=${#LANGS[@]}
MAX_FILES="${JUDGE_MAX_FILES:-0}"
if [[ "${MAX_FILES}" =~ ^[0-9]+$ ]] && [[ "${MAX_FILES}" -gt 0 ]] && [[ "${MAX_FILES}" -lt "${TOTAL_FILES}" ]]; then
  LANGS=("${LANGS[@]:0:${MAX_FILES}}")
fi

n=${#LANGS[@]}

echo "=================================================="
echo " source model     : ${SOURCE_MODEL}"
echo " judge model      : ${JUDGE_MODEL}"
echo " reasoning effort : ${JUDGE_REASONING_EFFORT}"
echo " temperature      : ${JUDGE_TEMPERATURE}"
echo " judge concurrency: ${JUDGE_CONCURRENCY}"
echo " json only        : ${JUDGE_JSON_ONLY}"
echo " result prefix    : ${RESULT_FILE_PREFIX:-<empty>}"
echo " cache root       : ${JUDGE_CACHE_ROOT}"
echo " cache source     : ${JUDGE_CACHE_SOURCE_MODEL}"
echo " parallel langs   : ${JOBS}"
echo " target languages : ${LANGS[*]}"
[[ ${#EXTRA[@]} -gt 0 ]] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

build_cmd() {
  CMD=(bash "${SCRIPT_DIR}/run_judge_lang.sh" "$1")
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
  LOGDIR="${PWD}/genlogs/judge_all"
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
