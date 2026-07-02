#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

SOURCE="${REPO_ROOT}/wmt26_genmt_blindset_filter_parse.jsonl"
MODEL_A="gemini-3.5-flash"
MODEL_B="gpt-final"
JUDGE_MODEL="gemini-2.5-flash"
PAIR_NAME=""
WORK_DIR=""
LANGS="all"
COPY_FIELDS=""

usage() {
  cat <<EOF
Usage:
  final_submission/run_two_best_submission_pipeline.sh [options]

Builds:
  1. a merged two-best alignment mask over both 8-hypothesis pools
  2. an audit-friendly merged final file in source order
  3. a thin WMT submission file
  4. small reports, including the WMT alignment check

Options:
  --model-a NAME          default: ${MODEL_A}
  --model-b NAME          default: ${MODEL_B}
  --judge-model NAME      default: ${JUDGE_MODEL}
  --pair-name NAME        default: <model-a>__<model-b>
  --work-dir DIR          output working directory
                          default: final_submission/out/two-best/<pair-name>
  --source FILE           source jsonl
                          default: ${SOURCE}
  --langs CSV             comma-separated langs or "all" (default: all)
  --copy-fields CSV       extra fields to keep in thin submission
  -h, --help              show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model-a) MODEL_A="$2"; shift 2 ;;
    --model-b) MODEL_B="$2"; shift 2 ;;
    --judge-model) JUDGE_MODEL="$2"; shift 2 ;;
    --pair-name) PAIR_NAME="$2"; shift 2 ;;
    --work-dir) WORK_DIR="$2"; shift 2 ;;
    --source) SOURCE="$2"; shift 2 ;;
    --langs) LANGS="$2"; shift 2 ;;
    --copy-fields) COPY_FIELDS="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${PAIR_NAME}" ]]; then
  PAIR_NAME="${MODEL_A}__${MODEL_B}"
fi

SOURCE="$(cd "$(dirname "${SOURCE}")" && pwd)/$(basename "${SOURCE}")"
CROSS_DIR="${REPO_ROOT}/results/${JUDGE_MODEL}/artifacts/two-best/${PAIR_NAME}/cross-matrix"
MODEL_A_RESULTS_DIR="${REPO_ROOT}/results/${MODEL_A}"
MODEL_B_RESULTS_DIR="${REPO_ROOT}/results/${MODEL_B}"
MODEL_A_MATRIX_DIR="${REPO_ROOT}/results/${JUDGE_MODEL}/artifacts/${MODEL_A}/matrix"
MODEL_B_MATRIX_DIR="${REPO_ROOT}/results/${JUDGE_MODEL}/artifacts/${MODEL_B}/matrix"

if [[ -z "${WORK_DIR}" ]]; then
  WORK_DIR="${REPO_ROOT}/final_submission/out/two-best/${PAIR_NAME}"
fi
WORK_DIR="$(mkdir -p "${WORK_DIR}" && cd "${WORK_DIR}" && pwd)"
REPORT_DIR="${WORK_DIR}/reports"
mkdir -p "${REPORT_DIR}"

MASK_OUT="${WORK_DIR}/alignment_mask.jsonl"
FILTERED_SOURCE_OUT="${WORK_DIR}/source.filtered.jsonl"
PRELIM_OUT="${WORK_DIR}/preliminary_final.jsonl"
SUBMISSION_OUT="${WORK_DIR}/submission.jsonl"
EXPORT_REPORT_JSON="${REPORT_DIR}/selection_report.json"
EXPORT_STDOUT="${REPORT_DIR}/selection_stdout.txt"
FIXES_JSONL="${REPORT_DIR}/fixed_samples.jsonl"
SUBMISSION_STDOUT="${REPORT_DIR}/submission_stdout.txt"
WMT_STDOUT="${REPORT_DIR}/wmt_alignment_stdout.txt"
SUMMARY_MD="${REPORT_DIR}/pipeline_summary.md"

echo "=================================================="
echo " model A         : ${MODEL_A}"
echo " model B         : ${MODEL_B}"
echo " judge model     : ${JUDGE_MODEL}"
echo " pair name       : ${PAIR_NAME}"
echo " cross dir       : ${CROSS_DIR}"
echo " model A results : ${MODEL_A_RESULTS_DIR}"
echo " model B results : ${MODEL_B_RESULTS_DIR}"
echo " model A matrix  : ${MODEL_A_MATRIX_DIR}"
echo " model B matrix  : ${MODEL_B_MATRIX_DIR}"
echo " source          : ${SOURCE}"
echo " work dir        : ${WORK_DIR}"
echo " python          : ${PYTHON_BIN}"
echo " langs           : ${LANGS}"
echo " copy fields     : ${COPY_FIELDS:-<none>}"
echo "=================================================="

"${PYTHON_BIN}" "${SCRIPT_DIR}/export_two_best_results.py" \
  --cross-dir "${CROSS_DIR}" \
  --model-a-results-dir "${MODEL_A_RESULTS_DIR}" \
  --model-b-results-dir "${MODEL_B_RESULTS_DIR}" \
  --model-a-matrix-dir "${MODEL_A_MATRIX_DIR}" \
  --model-b-matrix-dir "${MODEL_B_MATRIX_DIR}" \
  --source "${SOURCE}" \
  --langs "${LANGS}" \
  --mask-out "${MASK_OUT}" \
  --filtered-source-out "${FILTERED_SOURCE_OUT}" \
  --out "${PRELIM_OUT}" \
  --report-json "${EXPORT_REPORT_JSON}" \
  --fixes-jsonl "${FIXES_JSONL}" \
  > "${EXPORT_STDOUT}"

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

MASK_ROWS="$(wc -l < "${MASK_OUT}")"
PRELIM_ROWS="$(wc -l < "${PRELIM_OUT}")"
SUBMISSION_ROWS="$(wc -l < "${SUBMISSION_OUT}")"
WMT_SUMMARY="$(grep 'checked, .* aligned, .* misaligned' "${WMT_STDOUT}" | tail -n 1 || true)"
SELECTION_COUNTS="$("${PYTHON_BIN}" - "${EXPORT_REPORT_JSON}" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(report.get("kept_count", 0))
print(report.get("selected_invalid_count", 0))
print(report.get("fixed_count", 0))
print(report.get("cross_model_fix_count", 0))
print(report.get("unfixable_count", 0))
print(report.get("failure_count", 0))
PY
)"
readarray -t SELECTION_COUNT_LINES <<< "${SELECTION_COUNTS}"
KEPT_COUNT="${SELECTION_COUNT_LINES[0]:-0}"
SELECTED_INVALID_COUNT="${SELECTION_COUNT_LINES[1]:-0}"
FIXED_COUNT="${SELECTION_COUNT_LINES[2]:-0}"
CROSS_MODEL_FIX_COUNT="${SELECTION_COUNT_LINES[3]:-0}"
UNFIXABLE_COUNT="${SELECTION_COUNT_LINES[4]:-0}"
FAILURE_COUNT="${SELECTION_COUNT_LINES[5]:-0}"

cat > "${SUMMARY_MD}" <<EOF
# Two-Best Submission Pipeline Report

- Model A: \`${MODEL_A}\`
- Model B: \`${MODEL_B}\`
- Judge model: \`${JUDGE_MODEL}\`
- Pair name: \`${PAIR_NAME}\`
- Cross dir: \`${CROSS_DIR}\`
- Source: \`${FILTERED_SOURCE_OUT}\`
- Alignment mask: \`${MASK_OUT}\`
- Preliminary final: \`${PRELIM_OUT}\`
- Submission: \`${SUBMISSION_OUT}\`
- Mask rows: \`${MASK_ROWS}\`
- Preliminary rows: \`${PRELIM_ROWS}\`
- Submission rows: \`${SUBMISSION_ROWS}\`
- Kept selected winner: \`${KEPT_COUNT}\`
- Selected winner failed alignment: \`${SELECTED_INVALID_COUNT}\`
- Structurally fixed samples: \`${FIXED_COUNT}\`
- Cross-model fixes: \`${CROSS_MODEL_FIX_COUNT}\`
- Unfixable samples: \`${UNFIXABLE_COUNT}\`
- Export failures: \`${FAILURE_COUNT}\`
- WMT alignment summary: \`${WMT_SUMMARY}\`

## Reports

- Export stdout: \`${EXPORT_STDOUT}\`
- Export JSON: \`${EXPORT_REPORT_JSON}\`
- Fixed samples JSONL: \`${FIXES_JSONL}\`
- Submission stdout: \`${SUBMISSION_STDOUT}\`
- WMT alignment stdout: \`${WMT_STDOUT}\`
EOF

echo "summary: ${SUMMARY_MD}"
