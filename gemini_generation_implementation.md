# Gemini Generation Implementation

## Implemented Changes
- Extended [util/openai_client.py](/home/stroshi/UvA-MT-at-WMT26/util/openai_client.py) with a usage-aware call helper and fast-fail handling for Gemini content-filter responses.
- Extended [sequential_scaling.py](/home/stroshi/UvA-MT-at-WMT26/sequential_scaling.py) with:
  - `--reasoning-effort`
  - `--write-order`
  - `--usage-log`
  - `--cost-summary`
  - `--pricing-profile`
  - per-call token logging and estimated-cost aggregation
- Added Gemini generation helpers under [.local_scripts/gemini/generation](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/gemini/generation):
  - `common.py`
  - `estimate_cost.py`
  - `check_api.py`
  - `prepare_aligned_inputs.py`
  - `run_generation.sh`
  - `validate_results.py`
- Extended [.local_scripts/gemini/test_gemini_no_code_path.py](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/gemini/test_gemini_no_code_path.py) to cover usage capture, request-option forwarding, and fast-fail content filtering.

## Verification
- Unit tests passed with `.venv/bin/python`.
- Smoke run succeeded end-to-end:
  - outputs in [results/smoke/gemini-3.5-flash](/home/stroshi/UvA-MT-at-WMT26/results/smoke/gemini-3.5-flash)
  - aggregate usage summary in [aggregate_summary.json](/home/stroshi/UvA-MT-at-WMT26/results/smoke/gemini-3.5-flash/usage/aggregate_summary.json)
- Full run artifacts currently present:
  - [en-ar_AR.jsonl](/home/stroshi/UvA-MT-at-WMT26/results/gemini-3.5-flash/en-ar_AR.jsonl): 150 rows complete
  - [en-ru_RU.jsonl](/home/stroshi/UvA-MT-at-WMT26/results/gemini-3.5-flash/en-ru_RU.jsonl): 570 rows complete before stop
  - [aligned_inputs](/home/stroshi/UvA-MT-at-WMT26/results/gemini-3.5-flash/aligned_inputs/manifest.json): GPT-ordered inputs prepared for all three languages

## Blocker
- Gemini 3.5 Flash hard-blocks some source texts whose content asks for prohibited help, even when the task is only translation.
- The OpenAI-compatible endpoint returns `finish_reason=content_filter:*` and no assistant `message`, so those docs cannot be completed with this model/path without changing the provider/model strategy.

## Recommended Next Step
- Either accept partial Gemini 3.5 Flash coverage and keep the blocker list, or choose a fallback model/provider specifically for the hard-blocked documents.
