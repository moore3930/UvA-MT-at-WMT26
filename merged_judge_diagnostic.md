# Merged Judge Diagnostic

## Scope
- Target merged dir:
  `results/merged/gemini-3.5-flash__gpt-final`
- Judge setup:
  - model: `gemini-2.5-flash`
  - reasoning effort: `none`
  - temperature: `0.0`
  - prompt mode: `--json-only`
  - concurrency: `64`
- Diagnostic LP:
  - `arz`
  - full `16` hypotheses per row

## Implemented Runner/Estimator Changes
- Shared judge helpers now support both:
  - `en-<lang>.jsonl`
  - `<lang>.jsonl`
- Added merged low-thinking wrappers:
  - [.local_scripts/generation/judge/run_merged_lowthink_all.sh](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/run_merged_lowthink_all.sh)
  - [.local_scripts/generation/judge/run_merged_lowthink_lang.sh](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/run_merged_lowthink_lang.sh)
  - [.local_scripts/generation/judge/estimate_merged_lowthink_cost.sh](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/estimate_merged_lowthink_cost.sh)
- Extended estimator:
  - supports merged filename layout via empty `RESULT_FILE_PREFIX`
  - supports `--max-hypos N` for `8` vs `16`

## Exact Static Cost Estimates
- Saved machine-readable summaries:
  - [cost_k8_cpt365.json](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/diagnostics/merged/gemini-3.5-flash__gpt-final/cost_k8_cpt365.json)
  - [cost_k16_cpt365.json](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/diagnostics/merged/gemini-3.5-flash__gpt-final/cost_k16_cpt365.json)
  - [arz_cost_k16_cpt365.json](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/diagnostics/merged/gemini-3.5-flash__gpt-final/arz_cost_k16_cpt365.json)
- Assumptions:
  - prompt chars/token: `3.65`
  - visible output tokens/call: `20`
  - thinking tokens/call: `0`

## Cost Methodology

### Static full-dataset cost estimate
- Source data:
  - the real merged input dir
    `results/merged/gemini-3.5-flash__gpt-final`
- Script used:
  - [.local_scripts/generation/judge/estimate_merged_lowthink_cost.sh](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/estimate_merged_lowthink_cost.sh)
  - which calls
    [.local_scripts/generation/judge/estimate_judge_cost.py](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/estimate_judge_cost.py)
- Method:
  1. Read each real merged JSONL row.
  2. Extract the first `N` hypotheses per row, where `N` is `8` or `16`.
  3. Enumerate every ordered pair `(i, j)` with `i != j`.
  4. Skip pairs where `hypo_i == hypo_j`, because `pairwise_matrix.py` auto-ties them with no API call.
  5. For each remaining pair, build the exact judge prompt locally with `build_judge_messages(...)`, using the same rubric and JSON-only mode as the intended run.
  6. Sum the prompt character counts across all non-identical ordered pairs.
  7. Convert prompt characters to estimated prompt tokens using a fixed chars/token assumption.
  8. Estimate billed visible output tokens as:
     - `non_identical_ordered_pairs * 20`
  9. Set thinking tokens to `0`, because the intended judge mode is:
     - `reasoning_effort=none`
  10. Apply the `gemini-2.5-flash` pricing rates from `sequential_scaling.py`:
      - input: `$0.30 / 1M`
      - output: `$2.50 / 1M`

### Why this is trustworthy
- Exact, not guessed:
  - number of docs
  - number of hypotheses used (`8` or `16`)
  - ordered-pair count
  - identical-pair auto-tie count
  - prompt text shape, because prompts are built with the real local prompt builder
- Assumed, not exact:
  - prompt chars to prompt tokens conversion
  - visible output tokens per judged pair
- Chosen assumptions:
  - prompt chars/token: `3.65`
    - this matches the earlier low-thinking estimator
  - visible output tokens/call: `20`
    - same as the earlier low-thinking estimator
  - thinking tokens/call: `0`
    - aligned with `reasoning_effort=none`

### Small-LP extrapolated cost estimate
- Real run used:
  - `arz`, full `16` hypotheses
- Method:
  1. Compute the exact static `arz` cost with the same estimator.
  2. Divide that small-LP cost by its judged ordered-pair count to get an average cost per judged ordered pair for `arz`.
  3. Multiply by the full-dataset judged ordered-pair count.
- Purpose:
  - useful as a diagnostic lower-side estimate
- Limitation:
  - it underestimates the true full-dataset cost if the sampled LP has shorter-than-average prompts
  - that is exactly what happened here, so the full static estimate is the number to use for budgeting

### Full merged dataset
- `8` hypotheses:
  - ordered pairs to judge: `717,036`
  - identical auto-tied: `308,716`
  - exact static cost estimate: `$192.47`
- `16` hypotheses:
  - ordered pairs to judge: `3,896,400`
  - identical auto-tied: `499,680`
  - exact static cost estimate: `$1008.77`

### Small-LP diagnostic (`arz`, 16 hypotheses)
- docs: `150`
- ordered pairs to judge: `34,448`
- identical auto-tied: `1,552`
- exact static cost estimate: `$5.98`

## Real Diagnostic Run
- Command path used:
  [.local_scripts/generation/judge/run_merged_lowthink_lang.sh](/home/stroshi/UvA-MT-at-WMT26/.local_scripts/generation/judge/run_merged_lowthink_lang.sh)
- Output artifacts:
  - matrix: [arz-llm-matrix.jsonl](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/artifacts/merged_diag/gemini-3.5-flash__gpt-final/matrix/arz-llm-matrix.jsonl)
  - cache: [arz-llm-matrix.cache.jsonl](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/artifacts/merged_diag/gemini-3.5-flash__gpt-final/cache/arz-llm-matrix.cache.jsonl)
  - log: [arz-llm-matrix.log](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/artifacts/merged_diag/gemini-3.5-flash__gpt-final/matrix/log/arz-llm-matrix.log)
  - judged export: [arz.jsonl](/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/judged/merged_diag/gemini-3.5-flash__gpt-final/arz.jsonl)

### Measured runtime
- wall time: `246.667 s`
- docs: `150`
- ordered pairs judged: `34,448`
- observed throughput:
  - `139.65` ordered pairs / second
- observed cache activity:
  - cache hits: `9,612 / 34,448` = `27.9%`
  - new cache entries: `24,836`
  - effective new-result throughput: `100.69` new entries / second

## Extrapolation From The Small LP

### Time
- Using the observed `arz` wall-clock throughput and scaling by judged ordered pairs:
  - extrapolated `8`-hypothesis full run:
    - `5,134.38 s`
    - about `1.43 h`
  - extrapolated `16`-hypothesis full run:
    - `27,900.41 s`
    - about `7.75 h`

### Cost
- Using the `arz` average cost per judged ordered pair and scaling by judged ordered pairs:
  - extrapolated `8`-hypothesis full run:
    - `$124.52`
  - extrapolated `16`-hypothesis full run:
    - `$676.66`

## Interpretation
- The `arz`-based time extrapolation is useful because it comes from the real merged low-thinking runner with the real cache behavior and the full `16`-hypothesis workload.
- The `arz`-based cost extrapolation is less trustworthy than the exact whole-dataset static estimator:
  - extrapolated `16`-hypothesis cost from `arz`: `$676.66`
  - exact full static `16`-hypothesis estimate: `$1008.77`
- That gap means `arz` is cheaper than the dataset average, likely because its prompts are shorter than many other language pairs.

## Recommended Numbers To Use
- For planning the actual full run:
  - runtime budget: about `7.75 h` for full `16`-hypothesis judging
  - cost budget:
    - use the exact static full estimate: `$1008.77`
    - treat the `arz` extrapolated `$676.66` as an optimistic lower-side diagnostic, not the planning budget
