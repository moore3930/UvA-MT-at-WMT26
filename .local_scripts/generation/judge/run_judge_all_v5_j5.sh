#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
source "${SCRIPT_DIR}/lib.sh"

LANGS=(
  arz_Arab bel_Cyrl ces_Latn deu_Latn ekk_Latn hye_Armn ind_Latn isl_Latn
  jpn_Jpan kaz_Cyrl kor_Hang lij_Latn lld_Latn rus_Cyrl sme_Latn tha_Thai
  ukr_Cyrl zho_Hans zho_Hant_TW
)

RUN_NOW=0
EXTRA=()

usage() {
  cat <<'EOF'
Usage:
  .local_scripts/generation/judge/run_judge_all_v5_j5.sh [--run] [-- extra pairwise_matrix args...]

What it does:
  1. Estimates Gemini judge cost for the fixed 19-language v5 run
  2. Estimates wall time for -j 5 with per-language concurrency 32
  3. Runs the actual judge only if --run is passed

Defaults:
  SOURCE_MODEL=gpt-final
  JUDGE_MODEL=gemini-2.5-flash
  JUDGE_CONCURRENCY=32
  JUDGE_STALL_REPORT_SECONDS=20
  parallel languages (-j)=5
  rubric file=rubric/v5.txt

Examples:
  .local_scripts/generation/judge/run_judge_all_v5_j5.sh
  .local_scripts/generation/judge/run_judge_all_v5_j5.sh --run
  .local_scripts/generation/judge/run_judge_all_v5_j5.sh --run -- --limit 20
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run)
      RUN_NOW=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --)
      shift
      EXTRA=("$@")
      break
      ;;
    *)
      echo "unexpected argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

SOURCE_MODEL="${SOURCE_MODEL:-gpt-final}"
JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-32}"
JUDGE_STALL_REPORT_SECONDS="${JUDGE_STALL_REPORT_SECONDS:-20}"
EXPERIMENT_TAG="${EXPERIMENT_TAG:-rubric-v5}"
export SOURCE_MODEL JUDGE_MODEL JUDGE_CONCURRENCY JUDGE_STALL_REPORT_SECONDS EXPERIMENT_TAG

set_judge_defaults

LANGS_CSV="$(IFS=,; echo "${LANGS[*]}")"
LANGS_SPACE="$(IFS=' '; echo "${LANGS[*]}")"
SUMMARY_JSON="$(mktemp)"
trap 'rm -f "${SUMMARY_JSON}"' EXIT

echo "=================================================="
echo " source model     : ${SOURCE_MODEL}"
echo " judge model      : ${JUDGE_MODEL}"
echo " rubric file      : ${REPO_ROOT}/rubric/v5.txt"
echo " parallel langs   : 5"
echo " judge concurrency: ${JUDGE_CONCURRENCY}"
echo " stall seconds    : ${JUDGE_STALL_REPORT_SECONDS}"
echo " target languages : ${LANGS_SPACE}"
[[ ${#EXTRA[@]} -gt 0 ]] && echo " extra args       : ${EXTRA[*]}"
echo "=================================================="
echo
echo "[estimate] cost"

"${SCRIPT_DIR}/estimate_cost.sh" "${LANGS_CSV}" \
  --rubric-file "${REPO_ROOT}/rubric/v5.txt" \
  --summary-json "${SUMMARY_JSON}"

echo
echo "[estimate] wall time for -j 5 and concurrency ${JUDGE_CONCURRENCY}"

"${PYTHON_BIN}" - <<'PY' "${SUMMARY_JSON}" "${JUDGE_CONCURRENCY}"
import json
import sys
from pathlib import Path

summary_path = Path(sys.argv[1])
per_lang_concurrency = float(sys.argv[2])
data = json.loads(summary_path.read_text(encoding="utf-8"))
rows = data["per_file"]

latencies = [4, 5, 6, 8, 10]
jobs = 5

print("Assumption: average API latency per judged ordered pair")
print("| Avg latency/call | Makespan estimate |")
print("|---|---:|")
for latency in latencies:
    slots = [0.0] * jobs
    for row in rows:
        duration_seconds = (
            row["ordered_pairs_to_judge"] * latency / per_lang_concurrency
        )
        slot_idx = min(range(jobs), key=lambda i: slots[i])
        slots[slot_idx] += duration_seconds
    makespan_seconds = max(slots)
    print(
        f"| {latency}s | {makespan_seconds/3600.0:.2f} h "
        f"({makespan_seconds/60.0:.0f} min) |"
    )
PY

echo
echo "Run command:"
echo "  JUDGE_CONCURRENCY=${JUDGE_CONCURRENCY} bash ${SCRIPT_DIR}/run_judge_all_v5.sh -j 5 -l \"${LANGS_SPACE}\"${EXTRA:+ -- ${EXTRA[*]}}"

if [[ "${RUN_NOW}" != "1" ]]; then
  echo
  echo "Dry run only. Re-run with --run to start the judge."
  exit 0
fi

echo
echo "[run] starting judge"
exec bash "${SCRIPT_DIR}/run_judge_all_v5.sh" -j 5 -l "${LANGS_SPACE}" "${EXTRA[@]}"
