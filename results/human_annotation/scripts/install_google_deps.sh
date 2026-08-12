#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib.sh"

set_human_annotation_defaults

PY_VERSION="$("${PYTHON_BIN}" - <<'PY'
import sys
print("{}.{}.{}".format(*sys.version_info[:3]))
PY
)"

echo "Using interpreter: ${PYTHON_BIN} (${PY_VERSION})"

if ! "${PYTHON_BIN}" -m pip --version >/dev/null 2>&1; then
  echo "pip is missing for ${PYTHON_BIN}; attempting to bootstrap it with ensurepip."
  "${PYTHON_BIN}" -m ensurepip --upgrade
fi

if ! "${PYTHON_BIN}" -m pip --version >/dev/null 2>&1; then
  echo "Could not bootstrap pip for ${PYTHON_BIN}." >&2
  echo "Try one of these manually:" >&2
  echo "  ${PYTHON_BIN} -m ensurepip --upgrade" >&2
  echo "  conda install pip" >&2
  exit 1
fi

PKGS=()
if "${PYTHON_BIN}" - <<'PY'
import sys
sys.exit(0 if sys.version_info >= (3, 8) else 1)
PY
then
  PKGS=(
    "google-api-python-client"
    "google-auth"
    "google-auth-oauthlib"
  )
else
  echo "Detected Python < 3.8; installing older Google client packages for compatibility."
  PKGS=(
    "google-api-python-client<2"
    "google-auth<2"
    "google-auth-oauthlib<1"
  )
fi

"${PYTHON_BIN}" -m pip install "${PKGS[@]}"

echo "Installed Google Sheets/Drive dependencies for ${PYTHON_BIN}"
