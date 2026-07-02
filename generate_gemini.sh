#!/usr/bin/env bash
#
# generate_gemini.sh -- Gemini-oriented wrapper around sequential_scaling.py.
#
# Mirrors generate.sh closely, but resolves the repo .venv Python, exports the
# Gemini OpenAI-compatible endpoint, resolves a Gemini API key, and exposes
# reasoning-effort directly.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="${SCRIPT_DIR}/sequential_scaling.py"
REPO_ROOT="${SCRIPT_DIR}"
cd "${SCRIPT_DIR}"

resolve_python() {
  if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    printf '%s\n' "${REPO_ROOT}/.venv/bin/python"
    return
  fi
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return
  fi
  echo "No Python found. Expected ${REPO_ROOT}/.venv/bin/python or python3 on PATH." >&2
  exit 1
}

resolve_api_key() {
  if [[ -n "${OPENAI_API_KEY:-}" ]]; then
    printf '%s\n' "${OPENAI_API_KEY}"
    return
  fi
  if [[ -n "${GEMINI_API_KEY:-}" ]]; then
    printf '%s\n' "${GEMINI_API_KEY}"
    return
  fi
  if [[ -f "${HOME}/.gemini_api_key" ]]; then
    tr -d '\n' < "${HOME}/.gemini_api_key"
    return
  fi
  echo "Gemini API key not found. Set OPENAI_API_KEY/GEMINI_API_KEY or create ~/.gemini_api_key." >&2
  exit 1
}

export_gemini_env() {
  export OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://generativelanguage.googleapis.com/v1beta/openai/}"
  export OPENAI_API_KEY="$(resolve_api_key)"
  export PYTHONUNBUFFERED=1
}

# ---- defaults (override via flags or env vars) ----
K=8
MODEL="${GEMINI_MODEL:-gemini-3.5-flash}"
REASONING_EFFORT="${GEMINI_REASONING_EFFORT:-minimal}"
WITH_INSTRUCTION=1       # 1 = --with-instruction, 0 = --no-with-instruction
TEMPERATURE="${TEMPERATURE:-1}"
CONCURRENCY=64           # documents translated in parallel (per language, --concurrency)
JOBS=1                   # how many LANGUAGES to run in parallel (1 = sequential)
INPUT="${SCRIPT_DIR}/wmt26_genmt_blindset_filter_parse.jsonl"
PYTHON_BIN="$(resolve_python)"

LANGS=(
  arz hye_Armn bel_Cyrl zh_CN zho_Hant_TW cs_CZ et_EE de_DE is ind_Latn
  kaz_Cyrl ko_KR lld_Latn lij_Latn sme_Latn ru_RU tha_Thai
  vie_Latn ukr_Cyrl jpn_Jpan deu_Latn
)

usage() {
  cat <<EOF
Usage: $(basename "$0") [options] [-- extra args passed to sequential_scaling.py]

  -k K          sequential-scaling rounds K                 (default: ${K})
  -m MODEL      Gemini model name                           (default: ${MODEL})
  -r LEVEL      reasoning effort                            (default: ${REASONING_EFFORT})
  -f INPUT      input jsonl                                 (default: $(basename "${INPUT}"))
  -c N          concurrency (docs in parallel per language) (default: ${CONCURRENCY})
  -j N          languages run in parallel (1 = sequential)  (default: ${JOBS})
  -t TEMP       temperature                                 (default: ${TEMPERATURE})
  -i            enable  --with-instruction                  (default: on)
  -I            disable (--no-with-instruction)
  -l "a b c"    target languages to run                     (default: ${#LANGS[@]} eval langs)
  -h            show this help

Environment:
  GEMINI_MODEL             overrides default model
  GEMINI_REASONING_EFFORT  overrides default reasoning effort
  OPENAI_BASE_URL          overrides Gemini-compatible endpoint
  OPENAI_API_KEY           preferred API key source
  GEMINI_API_KEY           fallback API key source
  ~/.gemini_api_key        fallback key file

Examples:
  $(basename "$0")                                      # all default langs, Gemini defaults
  $(basename "$0") -m gemini-2.5-flash -r low           # different model / reasoning
  $(basename "$0") -j 3 -c 64                           # up to 3 langs at once, 64 docs each
  $(basename "$0") -l "zh_CN ru_RU"                     # just these two
  $(basename "$0") -l "zh_CN" -- --dry-run --limit 5    # smoke test, no API calls
EOF
}

while getopts "k:m:r:f:c:j:t:iIl:h" opt; do
  case "$opt" in
    k) K="$OPTARG" ;;
    m) MODEL="$OPTARG" ;;
    r) REASONING_EFFORT="$OPTARG" ;;
    f) INPUT="$OPTARG" ;;
    c) CONCURRENCY="$OPTARG" ;;
    j) JOBS="$OPTARG" ;;
    t) TEMPERATURE="$OPTARG" ;;
    i) WITH_INSTRUCTION=1 ;;
    I) WITH_INSTRUCTION=0 ;;
    l) read -r -a LANGS <<< "$OPTARG" ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
done
shift $((OPTIND - 1))
EXTRA=("$@")

if [[ ! -f "${PY_SCRIPT}" ]]; then
  echo "Missing sequential_scaling.py at ${PY_SCRIPT}" >&2
  exit 1
fi

if [ "${WITH_INSTRUCTION}" -eq 1 ]; then
  WI_FLAG="--with-instruction"
else
  WI_FLAG="--no-with-instruction"
fi

export_gemini_env

n=${#LANGS[@]}

echo "=================================================="
echo " input            : ${INPUT}"
echo " python           : ${PYTHON_BIN}"
echo " model            : ${MODEL}"
echo " reasoning-effort : ${REASONING_EFFORT}"
echo " base-url         : ${OPENAI_BASE_URL}"
echo " K                : ${K}"
echo " concurrency      : ${CONCURRENCY}"
echo " parallel langs   : ${JOBS}"
echo " temperature      : ${TEMPERATURE}"
echo " with-instruction : ${WI_FLAG}"
echo " resume           : on"
echo " cache            : on"
echo " target languages : ${LANGS[*]}"
[ ${#EXTRA[@]} -gt 0 ] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

build_cmd() {
  CMD=("${PYTHON_BIN}" "${PY_SCRIPT}" --input "${INPUT}" --langs "$1" --model "${MODEL}" \
       --k "${K}" --concurrency "${CONCURRENCY}" --temperature "${TEMPERATURE}" \
       --reasoning-effort "${REASONING_EFFORT}" --resume --cache "${WI_FLAG}")
  CMD+=(${EXTRA[@]+"${EXTRA[@]}"})
}

fail=()

if [ "${JOBS}" -le 1 ]; then
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
  LOGDIR="${SCRIPT_DIR}/genlogs"
  mkdir -p "${LOGDIR}"
  echo "up to ${JOBS} languages in parallel; per-language logs in ${LOGDIR}/"
  PIDS=()
  PLANG=()
  done_count=0

  reap_oldest() {
    local pid="${PIDS[0]}" lang="${PLANG[0]}" rc
    wait "${pid}"; rc=$?
    done_count=$((done_count + 1))
    if [ "${rc}" -ne 0 ]; then
      echo "[done ${done_count}/${n}] FAILED ${lang} (see ${LOGDIR}/${lang}.log)" >&2
      fail+=("${lang}")
    else
      echo "[done ${done_count}/${n}] ok ${lang}"
    fi
    PIDS=(${PIDS[@]:1+0})
    PLANG=(${PLANG[@]:1+0})
  }

  i=0
  for lang in "${LANGS[@]}"; do
    while [ "${#PIDS[@]}" -ge "${JOBS}" ]; do reap_oldest; done
    i=$((i + 1))
    build_cmd "${lang}"
    echo "[start ${i}/${n}] ${lang}  (log: ${LOGDIR}/${lang}.log)"
    ( "${CMD[@]}" > "${LOGDIR}/${lang}.log" 2>&1 ) &
    PIDS+=("$!")
    PLANG+=("${lang}")
  done
  while [ "${#PIDS[@]}" -gt 0 ]; do reap_oldest; done
fi

echo
echo "=================================================="
if [ ${#fail[@]} -eq 0 ]; then
  echo "All ${n} language(s) completed."
else
  echo "Completed with failures: ${fail[*]}"
  exit 1
fi
