#!/usr/bin/env python3
"""llm_client.py

Single dispatch point for the LLM backend, so the whole pipeline can switch
between MetaGen and a personal OpenAI API with one environment variable instead
of editing imports.

    LLM_BACKEND=metagen   (default)  -> util.metagen_client  (Llama compat endpoint)
    LLM_BACKEND=openai               -> util.openai_client   (OpenAI / OPENAI_BASE_URL)

Both backends expose the identical interface (build_client / call_openai /
call_openai_with_usage / ContentFilteredError / get_api_key), so every caller
just does `from util.llm_client import ...` and stays backend-agnostic.

Key resolution is delegated to whichever backend is selected:
  - metagen: LLAMA_API_KEY  or  ~/.llama_api_key   (+ METAGEN_BASE_URL)
  - openai : OPENAI_API_KEY or  ~/.openai_api_key   (+ OPENAI_BASE_URL)
"""

import os

BACKEND = os.getenv("LLM_BACKEND", "metagen").strip().lower()

if BACKEND in ("openai", "gpt", "personal"):
    BACKEND = "openai"
    from util.openai_client import (  # noqa: F401  (re-exported)
        ContentFilteredError,
        build_client,
        call_openai,
        call_openai_with_usage,
        get_api_key,
    )
elif BACKEND in ("metagen", "", "llama"):
    BACKEND = "metagen"
    from util.metagen_client import (  # noqa: F401  (re-exported)
        ContentFilteredError,
        build_client,
        call_openai,
        call_openai_with_usage,
        get_api_key,
    )
else:
    raise ValueError(
        f"Unknown LLM_BACKEND={BACKEND!r}; expected 'metagen' or 'openai'."
    )
