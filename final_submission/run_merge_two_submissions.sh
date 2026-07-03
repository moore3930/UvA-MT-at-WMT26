#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

SOURCE="${REPO_ROOT}/wmt26_genmt_blindset_filter_parse.jsonl"
PAIR_NAME="gemini-3.5-flash__gpt-final"
EXPERIMENT_TAG="rubric-v5-structured"
SELECTED_INPUT="${REPO_ROOT}/final_submission/out/two-best/${PAIR_NAME}_${EXPERIMENT_TAG}/preliminary_final.jsonl"
OLDER_INPUT="${REPO_ROOT}/final_submission/out/two-best/${PAIR_NAME}/preliminary_final.jsonl"
OLDER_MERGED_DIR="${REPO_ROOT}/results/merged/${PAIR_NAME}"
WORK_DIR=""
COPY_FIELDS=""
SELECTED_LANGS="arz_Arab,bel_Cyrl,ces_Latn,deu_Latn,ekk_Latn,hye_Armn,ind_Latn,isl_Latn,jpn_Jpan,kaz_Cyrl,kor_Hang,lij_Latn,lld_Latn,rus_Cyrl,sme_Latn,tha_Thai,ukr_Cyrl,zho_Hans,zho_Hant_TW"
OLDER_LANGS="arz,cs,cs_CZ,de_AT,de_CH,de_DE,de_IT,et_EE,is,ko_KR,ru,ru_RU,vie_Latn,zh_CN"

usage() {
  cat <<EOF
Usage:
  final_submission/run_merge_two_submissions.sh [options]

Merges:
  1. the selected-language two-best preliminary output
  2. the older per-language merged results for the remaining languages
  3. writes a full merged preliminary file, split per-language artifacts, and submission

Options:
  --selected-input FILE   default: ${SELECTED_INPUT}
  --older-input FILE      default: ${OLDER_INPUT}
  --older-merged-dir DIR  fallback only, default: ${OLDER_MERGED_DIR}
  --source FILE           default: ${SOURCE}
  --pair-name NAME        default: ${PAIR_NAME}
  --experiment-tag NAME   default: ${EXPERIMENT_TAG}
  --work-dir DIR          default: final_submission/out/merge_two_submissions/<pair-name>_<experiment-tag>
  --selected-langs CSV    default: built-in 19-language set
  --older-langs CSV       default: built-in 14-language remainder
  --copy-fields CSV       extra fields to keep in thin submission
  -h, --help              show this help
EOF
}

abspath_loose() {
  case "$1" in
    /*) printf '%s\n' "$1" ;;
    *) printf '%s\n' "$(pwd)/$1" ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --selected-input) SELECTED_INPUT="$2"; shift 2 ;;
    --older-input) OLDER_INPUT="$2"; shift 2 ;;
    --older-merged-dir) OLDER_MERGED_DIR="$2"; shift 2 ;;
    --source) SOURCE="$2"; shift 2 ;;
    --pair-name) PAIR_NAME="$2"; shift 2 ;;
    --experiment-tag) EXPERIMENT_TAG="$2"; shift 2 ;;
    --work-dir) WORK_DIR="$2"; shift 2 ;;
    --selected-langs) SELECTED_LANGS="$2"; shift 2 ;;
    --older-langs) OLDER_LANGS="$2"; shift 2 ;;
    --copy-fields) COPY_FIELDS="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

SOURCE="$(abspath_loose "${SOURCE}")"
SELECTED_INPUT="$(abspath_loose "${SELECTED_INPUT}")"
OLDER_INPUT="$(abspath_loose "${OLDER_INPUT}")"
OLDER_MERGED_DIR="$(abspath_loose "${OLDER_MERGED_DIR}")"

if [[ -f "${OLDER_INPUT}" ]]; then
  OLDER_MODE="older preliminary input"
  OLDER_ARGS=(--older-input "${OLDER_INPUT}")
else
  OLDER_MODE="older merged dir fallback"
  OLDER_ARGS=(--older-merged-dir "${OLDER_MERGED_DIR}")
fi

if [[ -z "${WORK_DIR}" ]]; then
  if [[ -n "${EXPERIMENT_TAG}" ]]; then
    WORK_DIR="${REPO_ROOT}/final_submission/out/merge_two_submissions/${PAIR_NAME}_${EXPERIMENT_TAG}"
  else
    WORK_DIR="${REPO_ROOT}/final_submission/out/merge_two_submissions/${PAIR_NAME}"
  fi
fi
WORK_DIR="$(mkdir -p "${WORK_DIR}" && cd "${WORK_DIR}" && pwd)"
REPORT_DIR="${WORK_DIR}/reports"
PER_LANG_DIR="${WORK_DIR}/per_language"
mkdir -p "${REPORT_DIR}" "${PER_LANG_DIR}"

FILTERED_SOURCE_OUT="${WORK_DIR}/source.filtered.jsonl"
PRELIM_OUT="${WORK_DIR}/preliminary_final.jsonl"
SUBMISSION_OUT="${WORK_DIR}/submission.jsonl"
MERGE_REPORT_JSON="${REPORT_DIR}/merge_report.json"
MERGE_STDOUT="${REPORT_DIR}/merge_stdout.txt"
SUBMISSION_STDOUT="${REPORT_DIR}/submission_stdout.txt"
WMT_STDOUT="${REPORT_DIR}/wmt_alignment_stdout.txt"
SUMMARY_MD="${REPORT_DIR}/pipeline_summary.md"

echo "=================================================="
echo " selected input   : ${SELECTED_INPUT}"
echo " older mode       : ${OLDER_MODE}"
echo " older input      : ${OLDER_INPUT}"
echo " older merged dir : ${OLDER_MERGED_DIR}"
echo " source           : ${SOURCE}"
echo " work dir         : ${WORK_DIR}"
echo " python           : ${PYTHON_BIN}"
echo " selected langs   : ${SELECTED_LANGS}"
echo " older langs      : ${OLDER_LANGS}"
echo " copy fields      : ${COPY_FIELDS:-<none>}"
echo "=================================================="

"${PYTHON_BIN}" "${SCRIPT_DIR}/merge_two_submissions.py" \
  --selected-input "${SELECTED_INPUT}" \
  "${OLDER_ARGS[@]}" \
  --source "${SOURCE}" \
  --out "${PRELIM_OUT}" \
  --filtered-source-out "${FILTERED_SOURCE_OUT}" \
  --per-lang-dir "${PER_LANG_DIR}" \
  --report-json "${MERGE_REPORT_JSON}" \
  --selected-langs "${SELECTED_LANGS}" \
  --older-langs "${OLDER_LANGS}" \
  > "${MERGE_STDOUT}"

"${PYTHON_BIN}" "${SCRIPT_DIR}/make_submission_jsonl.py" \
  --input "${PRELIM_OUT}" \
  --out "${SUBMISSION_OUT}" \
  --copy-fields "${COPY_FIELDS}" \
  > "${SUBMISSION_STDOUT}"

(
  bash "${SCRIPT_DIR}/run_wmt_alignment_check.sh" \
    --source "${FILTERED_SOURCE_OUT}" \
    --translation "${SUBMISSION_OUT}" \
    --work-dir "${REPORT_DIR}" \
    > /dev/null
)

PRELIM_ROWS="$(wc -l < "${PRELIM_OUT}")"
SUBMISSION_ROWS="$(wc -l < "${SUBMISSION_OUT}")"
PER_LANG_COUNT="$(find "${PER_LANG_DIR}" -maxdepth 1 -type f -name '*.jsonl' | wc -l)"
if [[ "${PER_LANG_COUNT}" -ne 33 ]]; then
  echo "expected 33 per-language merged files, found ${PER_LANG_COUNT}" >&2
  exit 1
fi
WMT_SUMMARY="$(grep 'checked, .* aligned, .* misaligned' "${WMT_STDOUT}" | tail -n 1 || true)"
MERGE_COUNTS="$("${PYTHON_BIN}" - "${MERGE_REPORT_JSON}" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(report.get("selected_lang_count", 0))
print(report.get("older_lang_count", 0))
print(report.get("merged_lang_count", 0))
print(report.get("selected_rows", 0))
print(report.get("older_rows", 0))
print(report.get("merged_rows", 0))
PY
)"
readarray -t MERGE_COUNT_LINES <<< "${MERGE_COUNTS}"
SELECTED_LANG_COUNT="${MERGE_COUNT_LINES[0]:-0}"
OLDER_LANG_COUNT="${MERGE_COUNT_LINES[1]:-0}"
MERGED_LANG_COUNT="${MERGE_COUNT_LINES[2]:-0}"
SELECTED_ROWS="${MERGE_COUNT_LINES[3]:-0}"
OLDER_ROWS="${MERGE_COUNT_LINES[4]:-0}"
MERGED_ROWS="${MERGE_COUNT_LINES[5]:-0}"

cat > "${SUMMARY_MD}" <<EOF
# Merge Two Submissions Report

- Selected input: \`${SELECTED_INPUT}\`
- Older merged dir: \`${OLDER_MERGED_DIR}\`
- Source: \`${FILTERED_SOURCE_OUT}\`
- Preliminary final: \`${PRELIM_OUT}\`
- Submission: \`${SUBMISSION_OUT}\`
- Per-language dir: \`${PER_LANG_DIR}\`
- Selected languages: \`${SELECTED_LANG_COUNT}\`
- Older languages: \`${OLDER_LANG_COUNT}\`
- Merged languages: \`${MERGED_LANG_COUNT}\`
- Per-language files: \`${PER_LANG_COUNT}\`
- Selected rows: \`${SELECTED_ROWS}\`
- Older rows: \`${OLDER_ROWS}\`
- Merged rows: \`${MERGED_ROWS}\`
- Preliminary rows: \`${PRELIM_ROWS}\`
- Submission rows: \`${SUBMISSION_ROWS}\`
- WMT alignment summary: \`${WMT_SUMMARY}\`

## Reports

- Merge stdout: \`${MERGE_STDOUT}\`
- Merge JSON: \`${MERGE_REPORT_JSON}\`
- Submission stdout: \`${SUBMISSION_STDOUT}\`
- WMT alignment stdout: \`${WMT_STDOUT}\`
EOF

echo "summary: ${SUMMARY_MD}"
