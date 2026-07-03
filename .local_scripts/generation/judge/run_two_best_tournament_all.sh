#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

JOBS=1
LANGS=()
PIDS=()
PLANG=()
INTERRUPTED=0

cleanup_children() {
  local sig="${1:-TERM}"
  local pid
  if [[ ${#PIDS[@]} -eq 0 ]]; then
    return 0
  fi
  echo
  echo "[cleanup] stopping ${#PIDS[@]} in-flight language job(s) with SIG${sig}" >&2
  for pid in "${PIDS[@]}"; do
    if kill -0 "${pid}" 2>/dev/null; then
      kill "-${sig}" "${pid}" 2>/dev/null || true
    fi
  done
  for pid in "${PIDS[@]}"; do
    wait "${pid}" 2>/dev/null || true
  done
}

on_interrupt() {
  local sig="$1"
  INTERRUPTED=1
  trap - INT TERM
  cleanup_children "${sig}"
  exit 130
}

trap 'on_interrupt INT' INT
trap 'on_interrupt TERM' TERM

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_two_best_tournament_all.sh [options] [-- extra args...]

Runs the cross-model winner-only judge stage over result files under:
  results/<MODEL_A>/ and results/<MODEL_B>/

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
  JUDGE_STRUCTURED_OUTPUT  default: 1 (required)
  JUDGE_MAX_FILES          default: all files
  EXPERIMENT_TAG           default: empty (use legacy artifacts paths)
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
JUDGE_STRUCTURED_OUTPUT="${JUDGE_STRUCTURED_OUTPUT:-1}"
export JUDGE_STRUCTURED_OUTPUT
require_structured_output

MODEL_A="${MODEL_A:-gemini-3.5-flash}"
MODEL_B="${MODEL_B:-gpt-final}"
PAIR_NAME="${PAIR_NAME:-${MODEL_A}__${MODEL_B}}"
EXPERIMENT_TAG="${EXPERIMENT_TAG:-}"
INPUT_DIR_A="${REPO_ROOT}/${RESULTS_ROOT}/${MODEL_A}"
INPUT_DIR_B="${REPO_ROOT}/${RESULTS_ROOT}/${MODEL_B}"

if [[ ! -d "${INPUT_DIR_A}" ]]; then
  echo "Missing results dir for MODEL_A: ${INPUT_DIR_A}" >&2
  exit 1
fi
if [[ ! -d "${INPUT_DIR_B}" ]]; then
  echo "Missing results dir for MODEL_B: ${INPUT_DIR_B}" >&2
  exit 1
fi

if [[ ${#LANGS[@]} -eq 0 ]]; then
  shopt -s nullglob
  FILES=("${INPUT_DIR_A}"/*.jsonl)
  shopt -u nullglob

  if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "No input result files found under ${INPUT_DIR_A}" >&2
    exit 1
  fi

  for file in "${FILES[@]}"; do
    LANGS+=("$(basename "${file}" .jsonl)")
  done
fi

TOTAL_FILES=${#LANGS[@]}
MAX_FILES="${JUDGE_MAX_FILES:-0}"
if [[ "${MAX_FILES}" =~ ^[0-9]+$ ]] && [[ "${MAX_FILES}" -gt 0 ]] && [[ "${MAX_FILES}" -lt "${TOTAL_FILES}" ]]; then
  LANGS=("${LANGS[@]:0:${MAX_FILES}}")
fi

n=${#LANGS[@]}

echo "=================================================="
echo " model A          : ${MODEL_A}"
echo " model B          : ${MODEL_B}"
echo " pair name        : ${PAIR_NAME}"
echo " judge model      : ${JUDGE_MODEL}"
echo " reasoning effort : ${JUDGE_REASONING_EFFORT}"
echo " temperature      : ${JUDGE_TEMPERATURE}"
echo " judge concurrency: ${JUDGE_CONCURRENCY}"
echo " json only        : ${JUDGE_JSON_ONLY}"
echo " structured out   : ${JUDGE_STRUCTURED_OUTPUT}"
echo " experiment tag   : ${EXPERIMENT_TAG:-<legacy-artifacts>}"
echo " parallel langs   : ${JOBS}"
echo " target languages : ${LANGS[*]}"
[[ ${#EXTRA[@]} -gt 0 ]] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

build_cmd() {
  CMD=(bash "${SCRIPT_DIR}/run_two_best_tournament_lang.sh" "$1")
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
  LOGDIR="${PWD}/genlogs/judge_two_best_all"
  mkdir -p "${LOGDIR}"
  echo "up to ${JOBS} languages in parallel; per-language logs in ${LOGDIR}/"
  done_count=0

  reap_one_finished() {
    local pid lang rc idx
    # bash 3.2 (macOS default) has no `wait -n`; poll until a child exits.
    while :; do
      for idx in "${!PIDS[@]}"; do
        if ! kill -0 "${PIDS[$idx]}" 2>/dev/null; then
          break 2
        fi
      done
      sleep 1
    done

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
      # re-pack arrays; guard empty case (bash 3.2 + set -u errors on "${x[@]}")
      if [[ "${#PIDS[@]}" -gt 0 ]]; then
        PIDS=("${PIDS[@]}")
        PLANG=("${PLANG[@]}")
      else
        PIDS=()
        PLANG=()
      fi
      print_running
      return 0
    done

    echo "[warn] polled but no finished job was identified" >&2
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
