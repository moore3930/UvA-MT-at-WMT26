#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

# Reuse the shared Gemini/OpenAI-compatible env helpers from generation.
source "${REPO_ROOT}/.local_scripts/gemini/generation/lib.sh"

pair_filename() {
  printf '%s%s.jsonl\n' "${RESULT_FILE_PREFIX}" "${1}"
}

lang_from_result_file() {
  local base
  base="$(basename "${1}")"
  base="${base%.jsonl}"
  if [[ -n "${RESULT_FILE_PREFIX}" ]]; then
    base="${base#${RESULT_FILE_PREFIX}}"
  fi
  printf '%s\n' "${base}"
}

set_judge_defaults() {
  PYTHON_BIN="$(resolve_python)"
  SOURCE_MODEL="${SOURCE_MODEL:-gemini-3.5-flash}"
  JUDGE_MODEL="${JUDGE_MODEL:-gemini-2.5-flash}"
  JUDGE_REASONING_EFFORT="${JUDGE_REASONING_EFFORT:-none}"
  JUDGE_TEMPERATURE="${JUDGE_TEMPERATURE:-0.0}"
  JUDGE_CONCURRENCY="${JUDGE_CONCURRENCY:-32}"
  JUDGE_JSON_ONLY="${JUDGE_JSON_ONLY:-1}"
  JUDGE_STRUCTURED_OUTPUT="${JUDGE_STRUCTURED_OUTPUT:-0}"
  JUDGE_REQUEST_TIMEOUT="${JUDGE_REQUEST_TIMEOUT:-180}"
  JUDGE_STALL_REPORT_SECONDS="${JUDGE_STALL_REPORT_SECONDS:-60}"
  RESULT_FILE_PREFIX="${RESULT_FILE_PREFIX-}"
  RESULTS_ROOT="${RESULTS_ROOT:-results}"
  JUDGE_CACHE_ROOT="${JUDGE_CACHE_ROOT:-/fnwi_fs/ivi/irlab/personal/stroshi/wmt2026_cache}"
  JUDGE_CACHE_SOURCE_MODEL="${JUDGE_CACHE_SOURCE_MODEL:-}"
  if [[ -z "${JUDGE_CACHE_SOURCE_MODEL}" ]]; then
    case "${SOURCE_MODEL}" in
      gpt-final|gemini-3.5-flash)
        JUDGE_CACHE_SOURCE_MODEL="merged/gemini-3.5-flash__gpt-final"
        ;;
      *)
        JUDGE_CACHE_SOURCE_MODEL="${SOURCE_MODEL}"
        ;;
    esac
  fi
  INPUT_RESULTS_DIR="${INPUT_RESULTS_DIR:-${REPO_ROOT}/${RESULTS_ROOT}/${SOURCE_MODEL}}"
  ARTIFACT_ROOT="${ARTIFACT_ROOT:-${REPO_ROOT}/${RESULTS_ROOT}/${JUDGE_MODEL}/artifacts/${SOURCE_MODEL}}"
  CACHE_ARTIFACT_ROOT="${CACHE_ARTIFACT_ROOT:-${JUDGE_CACHE_ROOT}/${JUDGE_MODEL}/artifacts/${JUDGE_CACHE_SOURCE_MODEL}}"
  JUDGED_ROOT="${JUDGED_ROOT:-${REPO_ROOT}/${RESULTS_ROOT}/${JUDGE_MODEL}/judged/${SOURCE_MODEL}}"
  COST_PROMPT_CHARS_PER_TOKEN="${COST_PROMPT_CHARS_PER_TOKEN:-2.0}"
  COST_VISIBLE_OUTPUT_TOKENS="${COST_VISIBLE_OUTPUT_TOKENS:-20}"
  COST_THINKING_TOKENS="${COST_THINKING_TOKENS:-0}"
}

require_structured_output() {
  if [[ "${JUDGE_STRUCTURED_OUTPUT:-0}" != "1" ]]; then
    echo "Structured output is required for this workflow. Set JUDGE_STRUCTURED_OUTPUT=1." >&2
    exit 1
  fi
}

result_glob_pattern() {
  printf '%s*.jsonl\n' "${RESULT_FILE_PREFIX}"
}

input_result_path() {
  printf '%s/%s\n' "${INPUT_RESULTS_DIR}" "$(pair_filename "$1")"
}

matrix_output_path() {
  printf '%s/matrix/%s-llm-matrix.jsonl\n' "${ARTIFACT_ROOT}" "${1}"
}

cache_output_path() {
  printf '%s/cache/%s-llm-matrix.cache.jsonl\n' "${CACHE_ARTIFACT_ROOT}" "${1}"
}

judged_output_path() {
  printf '%s/%s\n' "${JUDGED_ROOT}" "$(pair_filename "$1")"
}

ensure_judge_dirs() {
  mkdir -p "${ARTIFACT_ROOT}/matrix" "${CACHE_ARTIFACT_ROOT}/cache" "${JUDGED_ROOT}"
}

validate_input_result() {
  local path="$1"
  if [[ ! -f "${path}" ]]; then
    echo "Input results file not found: ${path}" >&2
    exit 1
  fi
}

validate_judge_lang() {
  local lang="$1"
  local path
  path="$(input_result_path "${lang}")"
  validate_input_result "${path}"
}
