#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

SOURCE="${REPO_ROOT}/wmt26_genmt_blindset_filter_parse.jsonl"
MATRIX_DIR=""
WORK_DIR=""
LANGS="all"
MATRIX_LANG_PREFIX=""
COPY_FIELDS=""
MAX_FIXES="20"

usage() {
  cat <<EOF
Usage:
  final_submission/run_final_submission_pipeline.sh --matrix-dir DIR [options]

Builds:
  1. a structural alignment mask over all judged hypotheses
  2. an audit-friendly final file with mask-aware fallback selection
  3. a thin WMT submission file
  4. small reports, including the WMT alignment check

Options:
  --matrix-dir DIR         directory with *-llm-matrix.jsonl files
  --work-dir DIR           output working directory
                           default: final_submission/out/<matrix-dir-name>
  --source FILE            source jsonl
                           default: ${SOURCE}
  --langs CSV              comma-separated langs or "all" (default: all)
  --matrix-lang-prefix P   optional prefix before <lang>-llm-matrix.jsonl
  --copy-fields CSV        extra fields to keep in thin submission (e.g. thinking)
  --max-fixes N            hard limit for structurally fixed samples (default: 20)
  -h, --help               show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --matrix-dir) MATRIX_DIR="$2"; shift 2 ;;
    --work-dir) WORK_DIR="$2"; shift 2 ;;
    --source) SOURCE="$2"; shift 2 ;;
    --langs) LANGS="$2"; shift 2 ;;
    --matrix-lang-prefix) MATRIX_LANG_PREFIX="$2"; shift 2 ;;
    --copy-fields) COPY_FIELDS="$2"; shift 2 ;;
    --max-fixes) MAX_FIXES="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${MATRIX_DIR}" ]]; then
  echo "--matrix-dir is required" >&2
  usage
  exit 1
fi

MATRIX_DIR="$(cd "${MATRIX_DIR}" && pwd)"
SOURCE="$(cd "$(dirname "${SOURCE}")" && pwd)/$(basename "${SOURCE}")"

if [[ -z "${WORK_DIR}" ]]; then
  WORK_DIR="${REPO_ROOT}/final_submission/out/$(basename "${MATRIX_DIR}")"
fi
WORK_DIR="$(mkdir -p "${WORK_DIR}" && cd "${WORK_DIR}" && pwd)"
REPORT_DIR="${WORK_DIR}/reports"
mkdir -p "${REPORT_DIR}"

MASK_OUT="${WORK_DIR}/alignment_mask.jsonl"
PRELIM_OUT="${WORK_DIR}/preliminary_final.jsonl"
SUBMISSION_OUT="${WORK_DIR}/submission.jsonl"
MASK_REPORT_JSON="${REPORT_DIR}/alignment_mask_report.json"
MASK_STDOUT="${REPORT_DIR}/alignment_mask_stdout.txt"
SELECTION_REPORT_JSON="${REPORT_DIR}/selection_report.json"
SELECTION_STDOUT="${REPORT_DIR}/selection_stdout.txt"
FIXES_JSONL="${REPORT_DIR}/fixed_samples.jsonl"
SUBMISSION_STDOUT="${REPORT_DIR}/submission_stdout.txt"
WMT_STDOUT="${REPORT_DIR}/wmt_alignment_stdout.txt"
SUMMARY_MD="${REPORT_DIR}/pipeline_summary.md"

echo "=================================================="
echo " matrix dir       : ${MATRIX_DIR}"
echo " source           : ${SOURCE}"
echo " work dir         : ${WORK_DIR}"
echo " python           : ${PYTHON_BIN}"
echo " langs            : ${LANGS}"
echo " matrix prefix    : ${MATRIX_LANG_PREFIX:-<empty>}"
echo " copy fields      : ${COPY_FIELDS:-<none>}"
echo " max fixes        : ${MAX_FIXES}"
echo "=================================================="

"${PYTHON_BIN}" "${SCRIPT_DIR}/build_alignment_mask.py" \
  --matrix-dir "${MATRIX_DIR}" \
  --source "${SOURCE}" \
  --out "${MASK_OUT}" \
  --report-json "${MASK_REPORT_JSON}" \
  --matrix-lang-prefix "${MATRIX_LANG_PREFIX}" \
  --langs "${LANGS}" \
  > "${MASK_STDOUT}"

"${PYTHON_BIN}" "${SCRIPT_DIR}/select_final_hypotheses.py" \
  --matrix-dir "${MATRIX_DIR}" \
  --mask "${MASK_OUT}" \
  --source "${SOURCE}" \
  --out "${PRELIM_OUT}" \
  --report-json "${SELECTION_REPORT_JSON}" \
  --fixes-jsonl "${FIXES_JSONL}" \
  --matrix-lang-prefix "${MATRIX_LANG_PREFIX}" \
  --langs "${LANGS}" \
  --max-fixes "${MAX_FIXES}" \
  > "${SELECTION_STDOUT}"

"${PYTHON_BIN}" "${SCRIPT_DIR}/make_submission_jsonl.py" \
  --input "${PRELIM_OUT}" \
  --out "${SUBMISSION_OUT}" \
  --copy-fields "${COPY_FIELDS}" \
  > "${SUBMISSION_STDOUT}"

(
  bash "${SCRIPT_DIR}/run_wmt_alignment_check.sh" \
    --source "${SOURCE}" \
    --translation "${SUBMISSION_OUT}" \
    --work-dir "${REPORT_DIR}" \
    > /dev/null
)

MASK_ROWS="$(wc -l < "${MASK_OUT}")"
PRELIM_ROWS="$(wc -l < "${PRELIM_OUT}")"
SUBMISSION_ROWS="$(wc -l < "${SUBMISSION_OUT}")"
WMT_SUMMARY="$(grep 'checked, .* aligned, .* misaligned' "${WMT_STDOUT}" | tail -n 1 || true)"
SELECTION_COUNTS="$("${PYTHON_BIN}" - "${SELECTION_REPORT_JSON}" <<'PY'
import json
import sys
from pathlib import Path

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(report.get("kept_count", 0))
print(report.get("fixed_count", 0))
print(report.get("unfixable_count", 0))
print(report.get("missing_matrix_row_count", 0))
print(report.get("missing_mask_row_count", 0))
PY
)"
readarray -t SELECTION_COUNT_LINES <<< "${SELECTION_COUNTS}"
KEPT_COUNT="${SELECTION_COUNT_LINES[0]:-0}"
FIXED_COUNT="${SELECTION_COUNT_LINES[1]:-0}"
UNFIXABLE_COUNT="${SELECTION_COUNT_LINES[2]:-0}"
MISSING_MATRIX_COUNT="${SELECTION_COUNT_LINES[3]:-0}"
MISSING_MASK_COUNT="${SELECTION_COUNT_LINES[4]:-0}"

cat > "${SUMMARY_MD}" <<EOF
# Final Submission Pipeline Report

- Matrix dir: \`${MATRIX_DIR}\`
- Source: \`${SOURCE}\`
- Alignment mask: \`${MASK_OUT}\`
- Preliminary final: \`${PRELIM_OUT}\`
- Submission: \`${SUBMISSION_OUT}\`
- Mask rows: \`${MASK_ROWS}\`
- Preliminary rows: \`${PRELIM_ROWS}\`
- Submission rows: \`${SUBMISSION_ROWS}\`
- Kept judged best: \`${KEPT_COUNT}\`
- Structurally fixed samples: \`${FIXED_COUNT}\`
- Unfixable samples: \`${UNFIXABLE_COUNT}\`
- Missing matrix rows: \`${MISSING_MATRIX_COUNT}\`
- Missing mask rows: \`${MISSING_MASK_COUNT}\`
- Max fixes limit: \`${MAX_FIXES}\`
- WMT alignment summary: \`${WMT_SUMMARY}\`

## Reports

- Alignment mask stdout: \`${MASK_STDOUT}\`
- Alignment mask JSON: \`${MASK_REPORT_JSON}\`
- Selection stdout: \`${SELECTION_STDOUT}\`
- Selection JSON: \`${SELECTION_REPORT_JSON}\`
- Fixed samples JSONL: \`${FIXES_JSONL}\`
- Submission stdout: \`${SUBMISSION_STDOUT}\`
- WMT alignment stdout: \`${WMT_STDOUT}\`
- WMT alignment log: \`${REPORT_DIR}/alignment.log\`
EOF

echo
echo "Pipeline completed."
echo "  alignment mask    : ${MASK_OUT}"
echo "  preliminary final : ${PRELIM_OUT}"
echo "  submission        : ${SUBMISSION_OUT}"
echo "  summary           : ${SUMMARY_MD}"
