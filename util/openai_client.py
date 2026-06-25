#!/usr/bin/env python3
"""openai_client.py

OpenAI GPT plumbing for the judge scripts: a drop-in replacement for the
MetaGen functions (build_client / call_metagen) that contrastive_judge.py and
pairwise_matrix.py used to import from sequential_scaling.py.

The chat `messages` shape ([{"role","content"}, ...]) and the (client, model,
messages, temperature) call signature are kept identical, so the rest of the
judge code is unchanged.

API key resolution (first hit wins):
  1) the --api-key CLI argument
  2) the OPENAI_API_KEY environment variable
  3) ~/.openai_api_key
Optionally set OPENAI_BASE_URL to point at a compatible/proxy endpoint.
"""

import os
import sys
import time
from pathlib import Path


def get_api_key(cli_key: str = "") -> str:
    """Resolve the OpenAI API key from CLI arg, env var, or key file."""
    if cli_key:
        return cli_key
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key
    key_file = Path.home() / ".openai_api_key"
    if key_file.exists():
        return key_file.read_text().strip()
    sys.exit("OpenAI API key not found. Pass --api-key, set OPENAI_API_KEY, "
             "or create ~/.openai_api_key")


def build_client(api_key: str = ""):
    """Build an OpenAI client (optionally honouring OPENAI_BASE_URL)."""
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("Missing dependency: `openai` is not installed "
                 "(pip install openai).")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    return OpenAI(api_key=get_api_key(api_key), base_url=base_url)


def call_openai(client, model, messages, max_retries=4, temperature=0.0):
    """Call OpenAI chat completions and return the response text.

    Mirrors call_metagen: same signature, same retry-with-backoff behaviour,
    just reads the OpenAI response field (resp.choices[0].message.content).
    """
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as e:  # noqa: BLE001 retry on rate limit / network / etc.
            last_err = e
            wait = 2 ** attempt
            print(f"  [warn] OpenAI call failed (attempt {attempt}): {e}; "
                  f"retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(
        f"OpenAI call still failing after {max_retries} attempts: {last_err}")
