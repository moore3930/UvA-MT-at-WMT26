#!/usr/bin/env bash
#
# generate.sh -- run sequential_scaling.py over a list of target languages.
#
# Enumerates each target language and calls sequential_scaling.py once per
# language, forwarding K, model, temperature and --with-instruction. The input
# file carries a per-record src_lang field, so the source language is resolved
# automatically -- no per-group source handling is needed.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${SCRIPT_DIR}/sequential_scaling.py"
cd "${SCRIPT_DIR}"   # so results/ and the util/results imports resolve here

# ---- defaults (override via flags) ----
K=8
MODEL="gpt-4o-mini"
WITH_INSTRUCTION=1       # 1 = --with-instruction, 0 = --no-with-instruction
TEMPERATURE=1
CONCURRENCY=64           # documents translated in parallel (per language, --concurrency)
JOBS=1                   # how many LANGUAGES to run in parallel (1 = sequential)
INPUT="${SCRIPT_DIR}/wmt26_genmt_blindset_filter_parse.jsonl"   # carries a src_lang field

# Target languages to run (the unique tgt_lang codes of the WMT26 eval set).

LANGS2=(
  bel_Cyrl zh_CN zho_Hant_TW cs_CZ et_EE de_DE is ind_Latn
)

LANGS=(
  arz hye_Armn bel_Cyrl zh_CN zho_Hant_TW cs_CZ et_EE de_DE is ind_Latn
  kaz_Cyrl ko_KR lld_Latn lij_Latn sme_Latn ru_RU tha_Thai
  vie_Latn ukr_Cyrl jpn_Jpan deu_Latn
)

# Full tgt_lang set from tgt_lang_filter.txt (all 33 codes in the filter file).
LANGS3=(
  arz arz_Arab bel_Cyrl ces_Latn cs cs_CZ de_AT de_CH de_DE
  de_IT deu_Latn ekk_Latn et_EE hye_Armn ind_Latn is isl_Latn jpn_Jpan
  kaz_Cyrl ko_KR kor_Hang lij_Latn lld_Latn ru ru_RU rus_Cyrl sme_Latn
  tha_Thai ukr_Cyrl vie_Latn zh_CN zho_Hans zho_Hant_TW
)

usage() {
  cat <<EOF
Usage: $(basename "$0") [options] [-- extra args passed to sequential_scaling.py]

  -k K          sequential-scaling rounds K                 (default: ${K})
  -m MODEL      model name                                  (default: ${MODEL})
  -f INPUT      input jsonl                                 (default: $(basename "${INPUT}"))
  -c N          concurrency (docs in parallel per language) (default: ${CONCURRENCY})
  -j N          languages run in parallel (1 = sequential)  (default: ${JOBS})
  -t TEMP       temperature                                 (default: ${TEMPERATURE})
  -i            enable  --with-instruction                  (default: on)
  -I            disable (--no-with-instruction)
  -l "a b c"    target languages to run                     (default: ${#LANGS[@]} eval langs)
  -h            show this help

Examples:
  $(basename "$0")                                     # all eval langs, defaults
  $(basename "$0") -m gpt-5.5 -k 4                     # different model / rounds
  $(basename "$0") -j 3 -c 64                          # up to 3 langs at once, 64 docs each
  $(basename "$0") -l "zh_CN cs_CZ"                    # just these two
  $(basename "$0") -l "pl_PL" -- --dry-run --limit 5   # smoke test, no API calls
EOF
}

while getopts "k:m:f:c:j:t:iIl:h" opt; do
  case "$opt" in
    k) K="$OPTARG" ;;
    m) MODEL="$OPTARG" ;;
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
EXTRA=("$@")   # anything after `--` is forwarded verbatim

if [ "${WITH_INSTRUCTION}" -eq 1 ]; then
  WI_FLAG="--with-instruction"
else
  WI_FLAG="--no-with-instruction"
fi

n=${#LANGS[@]}

echo "=================================================="
echo " input            : ${INPUT}"
echo " model            : ${MODEL}"
echo " K                : ${K}"
echo " concurrency      : ${CONCURRENCY}"
echo " parallel langs   : ${JOBS}"
echo " temperature      : ${TEMPERATURE}"
echo " with-instruction : ${WI_FLAG}"
echo " target languages : ${LANGS[*]}"
[ ${#EXTRA[@]} -gt 0 ] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="

# build the python command for one language
build_cmd() {   # $1 = lang; result in global CMD array
  CMD=(python "${PY}" --input "${INPUT}" --langs "$1" --model "${MODEL}" \
       --k "${K}" --concurrency "${CONCURRENCY}" --temperature "${TEMPERATURE}" \
       "${WI_FLAG}")
  CMD+=(${EXTRA[@]+"${EXTRA[@]}"})   # 3.2-safe empty-array expansion
}

fail=()

if [ "${JOBS}" -le 1 ]; then
  # ---- sequential: one language at a time, live output ----
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
  # ---- parallel: keep at most JOBS languages running (FIFO rolling pool) ----
  # Each language runs its own process (with its own --concurrency); per-language
  # output goes to genlogs/<lang>.log to keep the console readable.
  LOGDIR="${SCRIPT_DIR}/genlogs"
  mkdir -p "${LOGDIR}"
  echo "up to ${JOBS} languages in parallel; per-language logs in ${LOGDIR}/"
  PIDS=()      # active child pids, oldest first
  PLANG=()     # parallel: the language for each pid
  done_count=0

  reap_oldest() {   # block on the oldest job, record its result, drop it
    local pid="${PIDS[0]}" lang="${PLANG[0]}" rc
    wait "${pid}"; rc=$?
    done_count=$((done_count + 1))
    if [ "${rc}" -ne 0 ]; then
      echo "[done ${done_count}/${n}] FAILED ${lang} (see ${LOGDIR}/${lang}.log)" >&2
      fail+=("${lang}")
    else
      echo "[done ${done_count}/${n}] ok ${lang}"
    fi
    PIDS=(${PIDS[@]:1+0})     # drop index 0 (empty-safe)
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
