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
import re
import sys
import time
from pathlib import Path


class ContentFilteredError(RuntimeError):
    """Raised when a provider blocks the request and returns no assistant text."""


_RETRY_DELAY_RE = re.compile(
    r"""retryDelay['"]?\s*[:=]\s*['"]?(?P<value>\d+(?:\.\d+)?)(?P<unit>ms|s|m)?['"]?""",
    re.IGNORECASE,
)
_PLEASE_RETRY_RE = re.compile(
    r"""Please retry in (?P<value>\d+(?:\.\d+)?)s""",
    re.IGNORECASE,
)


def _env_float(name: str):
    raw = os.getenv(name, "").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        sys.exit(f"Invalid float value for {name}: {raw!r}")


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
    timeout = _env_float("OPENAI_TIMEOUT_SECONDS")
    kwargs = {"api_key": get_api_key(api_key), "base_url": base_url}
    if timeout is not None and timeout > 0:
        kwargs["timeout"] = timeout
    return OpenAI(**kwargs)


def _response_text(resp) -> str:
    """Extract the primary assistant text from a chat completion response."""
    choice = resp.choices[0]
    message = getattr(choice, "message", None)
    if message is None or getattr(message, "content", None) is None:
        finish_reason = getattr(choice, "finish_reason", None)
        if finish_reason and str(finish_reason).startswith("content_filter"):
            raise ContentFilteredError(f"content filtered: {finish_reason}")
        raise RuntimeError("response is missing assistant message content")
    return (message.content or "").strip()


def _response_usage(resp) -> dict:
    """Extract token usage fields from a chat completion response."""
    usage = getattr(resp, "usage", None)
    if usage is None:
        return {}

    out = {}
    for field in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, field, None)
        if value is not None:
            out[field] = int(value)
    return out


def _coerce_delay_seconds(raw, unit: str | None = None):
    if raw in (None, ""):
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    if value <= 0:
        return None
    unit = (unit or "s").lower()
    if unit == "ms":
        value /= 1000.0
    elif unit == "m":
        value *= 60.0
    return value


def _headers_retry_delay(headers) -> float | None:
    if headers is None:
        return None
    for key in ("retry-after", "Retry-After"):
        value = None
        if hasattr(headers, "get"):
            value = headers.get(key)
        elif isinstance(headers, dict):
            value = headers.get(key)
        delay = _coerce_delay_seconds(value)
        if delay is not None:
            return delay
    return None


def _extract_retry_delay_seconds(err) -> float | None:
    for attr in ("retry_after", "retry_after_seconds"):
        delay = _coerce_delay_seconds(getattr(err, attr, None))
        if delay is not None:
            return delay

    delay_ms = _coerce_delay_seconds(getattr(err, "retry_after_ms", None), "ms")
    if delay_ms is not None:
        return delay_ms

    delay = _headers_retry_delay(getattr(err, "headers", None))
    if delay is not None:
        return delay

    response = getattr(err, "response", None)
    if response is not None:
        delay = _headers_retry_delay(getattr(response, "headers", None))
        if delay is not None:
            return delay

    for text in (str(err), repr(err)):
        match = _PLEASE_RETRY_RE.search(text)
        if match:
            return float(match.group("value"))
        match = _RETRY_DELAY_RE.search(text)
        if match:
            return _coerce_delay_seconds(
                match.group("value"),
                match.group("unit") or "s",
            )
    return None


def _retry_wait_seconds(err, attempt: int) -> float:
    fallback = float(2 ** attempt)
    hinted = _extract_retry_delay_seconds(err)
    if hinted is None:
        return fallback
    return max(fallback, hinted)


def call_openai_with_usage(client, model, messages, max_retries=4,
                           temperature=0.0, request_options=None):
    """Call OpenAI chat completions and return (response_text, usage_dict)."""
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            create_kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if request_options:
                for key, value in request_options.items():
                    if value is not None and value != "":
                        create_kwargs[key] = value
            resp = client.chat.completions.create(**create_kwargs)
            return _response_text(resp), _response_usage(resp)
        except ContentFilteredError:
            raise
        except Exception as e:  # noqa: BLE001 retry on rate limit / network / etc.
            last_err = e
            if attempt >= max_retries:
                break
            wait = _retry_wait_seconds(e, attempt)
            print(f"  [warn] OpenAI call failed (attempt {attempt}): {e}; "
                  f"retrying in {wait:g}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(
        f"OpenAI call still failing after {max_retries} attempts: {last_err}")


def call_openai(client, model, messages, max_retries=4, temperature=0.0,
                request_options=None):
    """Call OpenAI chat completions and return the response text.

    Mirrors call_metagen: same signature, same retry-with-backoff behaviour,
    just reads the OpenAI response field (resp.choices[0].message.content).
    """
    text, _usage = call_openai_with_usage(
        client,
        model,
        messages,
        max_retries=max_retries,
        temperature=temperature,
        request_options=request_options,
    )
    return text
