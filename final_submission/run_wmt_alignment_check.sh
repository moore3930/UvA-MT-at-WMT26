#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${REPO_ROOT}/.venv/bin/python}"

SOURCE=""
TRANSLATION=""
WORK_DIR=""

usage() {
  cat <<EOF
Usage:
  final_submission/run_wmt_alignment_check.sh --source FILE --translation FILE [--work-dir DIR]

Runs the vendored WMT genmt_check_alignment.py script and writes:
  - stdout to <work-dir>/wmt_alignment_stdout.txt
  - alignment.log to <work-dir>/alignment.log
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --translation) TRANSLATION="$2"; shift 2 ;;
    --work-dir) WORK_DIR="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "${SOURCE}" || -z "${TRANSLATION}" ]]; then
  echo "--source and --translation are required" >&2
  usage
  exit 1
fi

SOURCE="$(cd "$(dirname "${SOURCE}")" && pwd)/$(basename "${SOURCE}")"
TRANSLATION="$(cd "$(dirname "${TRANSLATION}")" && pwd)/$(basename "${TRANSLATION}")"

if [[ -z "${WORK_DIR}" ]]; then
  WORK_DIR="$(pwd)"
fi
WORK_DIR="$(mkdir -p "${WORK_DIR}" && cd "${WORK_DIR}" && pwd)"

(
  cd "${WORK_DIR}"
  "${PYTHON_BIN}" "${SCRIPT_DIR}/vendor/genmt_check_alignment.py" \
    --source_path "${SOURCE}" \
    --translation_path "${TRANSLATION}" \
    > "${WORK_DIR}/wmt_alignment_stdout.txt"
)

echo "wmt alignment stdout: ${WORK_DIR}/wmt_alignment_stdout.txt"
echo "wmt alignment log:    ${WORK_DIR}/alignment.log"
