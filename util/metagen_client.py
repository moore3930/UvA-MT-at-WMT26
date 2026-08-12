#!/usr/bin/env python3
"""metagen_client.py

MetaGen plumbing for the judge/generation scripts, exposing the SAME interface
as util/openai_client.py (build_client / call_openai / call_openai_with_usage /
ContentFilteredError). MetaGen is reached through the Llama API's
OpenAI-compatible endpoint, so we reuse the stock `openai` SDK and all of
openai_client's retry/parse logic -- only the client construction (base_url +
key resolution) differs.

Key resolution (first hit wins):
  1) the --api-key CLI argument
  2) the LLAMA_API_KEY environment variable
  3) ~/.llama_api_key
The key is a Llama API key starting with 'LLM|...'.

Endpoint: defaults to the experimental OpenAI-compat gateway; override with
METAGEN_BASE_URL. Requests must originate from a Meta corp IP (VPN/on-campus).
"""

import os
import sys
from pathlib import Path

# reuse the generic (client-agnostic) call + parse + retry helpers verbatim;
# they only ever touch client.chat.completions.create, so they work unchanged
# against the Llama OpenAI-compat endpoint.
from util.openai_client import (  # noqa: F401  (re-exported for callers)
    ContentFilteredError,
    call_openai,
    call_openai_with_usage,
    _env_float,
)

DEFAULT_BASE_URL = "https://api.llama.com/experimental/compat/openai/v1/"


def get_api_key(cli_key: str = "") -> str:
    """Resolve the Llama API key from CLI arg, env var, or key file."""
    if cli_key:
        return cli_key
    env_key = os.getenv("LLAMA_API_KEY")
    if env_key:
        return env_key
    key_file = Path.home() / ".llama_api_key"
    if key_file.exists():
        return key_file.read_text().strip()
    sys.exit("Llama API key not found. Pass --api-key, set LLAMA_API_KEY, "
             "or create ~/.llama_api_key (key starts with 'LLM|').")


def build_client(api_key: str = ""):
    """Build an OpenAI SDK client pointed at MetaGen's Llama compat endpoint."""
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("Missing dependency: `openai` is not installed "
                 "(pip install openai).")
    base_url = os.getenv("METAGEN_BASE_URL") or DEFAULT_BASE_URL
    timeout = _env_float("OPENAI_TIMEOUT_SECONDS")
    kwargs = {"api_key": get_api_key(api_key), "base_url": base_url}
    if timeout is not None and timeout > 0:
        kwargs["timeout"] = timeout
    return OpenAI(**kwargs)
