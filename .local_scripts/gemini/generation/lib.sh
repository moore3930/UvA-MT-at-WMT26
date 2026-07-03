#!/usr/bin/env bash
#
# Shared Gemini/OpenAI-compatible env helpers.
#
# Provides the Python-resolution and API-key/endpoint setup used by the
# generation and judge scripts. Mirrors the inline copies in generate_gemini.sh.

# Repo root: default to three levels up from this file
# (.local_scripts/gemini/generation/lib.sh -> repo root), unless already set.
if [[ -z "${REPO_ROOT:-}" ]]; then
  _LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  REPO_ROOT="$(cd "${_LIB_DIR}/../../.." && pwd)"
fi

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
