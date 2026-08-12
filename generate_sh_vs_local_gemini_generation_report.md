# `generate.sh` vs `.local_scripts/gemini/generation`

## Short take

`generate.sh` is a broad, generic wrapper around `sequential_scaling.py`, while `.local_scripts/gemini/generation` is a narrower Gemini-specific workflow built to reproduce and validate a GPT-aligned subset.

The most important prompt-level finding is that the two paths do **not** use different Gemini prompt templates. The old Gemini workflow imports `build_messages` from `sequential_scaling.py`, so for the same input record and the same flags, the actual chat messages are the same.

The biggest practical differences are around:

- input selection and ordering
- Gemini environment setup
- multimodal handling
- resumability and logging
- compatibility with the current checkout

## Scope difference

`generate.sh`:

- defaults to `wmt26_genmt_blindset_filter_parse.jsonl` and 21 target-language codes in `LANGS` (`generate.sh:17-35`)
- relies on the filtered file's `src_lang` field (`generate.sh:23`, `sequential_scaling.py:909-947`)
- is generic by default: model `gpt-4o-mini`, concurrency `64`, no Gemini-specific env setup (`generate.sh:17-23`, `generate.sh:107-113`)

Old Gemini workflow:

- defaults to the original `wmt26_genmt_blindset.jsonl` (`.local_scripts/gemini/generation/common.py:22`)
- only supports `ar_AR`, `ru_RU`, `zh_CN` (`.local_scripts/gemini/generation/common.py:26`, `.local_scripts/gemini/generation/lib.sh:52-60`)
- first prepares per-language aligned inputs from `results/gpt-5.5/en-*.jsonl` order (`.local_scripts/gemini/generation/prepare_aligned_inputs.py:42-64`)
- skips multimodal examples while preparing those aligned inputs (`.local_scripts/gemini/generation/common.py:66-75`)
- runs Gemini through the OpenAI-compatible Google endpoint and resolves a Gemini key automatically (`.local_scripts/gemini/generation/lib.sh:11-31`)

Derived counts from the current files:

- `wmt26_genmt_blindset.jsonl`: 47,159 records, 45 target-language codes
- `wmt26_genmt_blindset_filter_parse.jsonl`: 18,317 records, 33 target-language codes
- old Gemini target set size from GPT results: `150 + 917 + 747 = 1,814` records
- new default `LANGS` set size: `11,533` records

## Prompt construction

Both paths use the same prompt builder from `sequential_scaling.py`:

- prompt templates: `sequential_scaling.py:177-246`
- instruction folding into the system message: `sequential_scaling.py:156-168`
- old Gemini workflow imports that shared logic: `.local_scripts/gemini/generation/common.py:15-20`

### Exact round-0 Gemini prompt for one overlapping sample

Sample record: `doc_id=46038-zh_CN`, source text `I won't find out until Monday.`

This is the exact message list produced by both paths for that sample:

```json
[
  {
    "role": "system",
    "content": "You are a professional translator. Follow the instruction and output only the translation, with no explanations."
  },
  {
    "role": "user",
    "content": "Please translate the following text from English to Chinese (Simplified). Provide only one translation on the first line and do not output anything else after that.\n\nEnglish: I won't find out until Monday.\nChinese (Simplified):"
  }
]
```

### Exact refinement-round Gemini prompt shape for the same sample

If round 0 had produced `我要到星期一才会知道。`, both paths would send:

```json
[
  {
    "role": "system",
    "content": "You are a professional translator. Follow the instruction and output only the translation, with no explanations."
  },
  {
    "role": "user",
    "content": "Please translate the following text from English to Chinese (Simplified). Provide only one translation on the first line and do not output anything else after that.\n\nEnglish: I won't find out until Monday.\nChinese (Simplified):"
  },
  {
    "role": "assistant",
    "content": "我要到星期一才会知道。"
  },
  {
    "role": "user",
    "content": "Please again translate the following text from English to Chinese (Simplified) to make it better. Provide only one translation on the first line and do not output anything else after that.\n\nEnglish: I won't find out until Monday.\nChinese (Simplified):"
  }
]
```

### Prompt differences

For this overlapping sample, there is **no prompt text difference**.

Why:

- the old Gemini workflow reuses `build_messages` from `sequential_scaling.py`
- this sample has a trivial `Translate from en to zh_CN.` instruction, and trivial instructions are intentionally **not** injected into the system prompt (`sequential_scaling.py:163-168`)
- `generate.sh` gets the source language from `src_lang`, while the old workflow gets it by parsing the instruction, but both resolve to `English` for this sample (`sequential_scaling.py:909-947`)

So the prompt-level difference is not "different wording"; it is mostly "different records, different run flags, different orchestration."

## Runtime / workflow differences

`generate.sh`:

- invokes `sequential_scaling.py` directly once per target language (`generate.sh:107-126`)
- does not set `--resume`
- does not set `--write-order input`
- does not set usage/failure/cost log paths
- does not set `--reasoning-effort`
- does not skip multimodal inputs unless the caller passes that explicitly after `--`

Old Gemini workflow:

- invokes `sequential_scaling.py` on prepared aligned inputs (`.local_scripts/gemini/generation/generate_lang.sh:73-91`)
- sets `--resume`
- sets `--no-cache`
- sets `--write-order input`
- sets usage, failure, and cost logs
- sets `--reasoning-effort "${REASONING_EFFORT}"`, defaulting to `minimal` (`.local_scripts/gemini/generation/lib.sh:34-49`)

## Issues found

### 1. `generate.sh` is not runnable as-is in the current environment

`generate.sh` hardcodes `python` (`generate.sh:109`), but this machine currently has no `python` on `PATH`. The old Gemini scripts handle this more safely by preferring `.venv/bin/python` and then falling back to `python3` (`.local_scripts/gemini/generation/lib.sh:3-9`).

There is a second compatibility wrinkle here: the system `python3` is `3.6.8`, and current `sequential_scaling.py` uses `argparse.BooleanOptionalAction` (`sequential_scaling.py:713-718`, `sequential_scaling.py:723-733`), which is not available there.

Impact:

- `generate.sh` will fail immediately here unless `python` is added to `PATH` or the script is changed.
- changing it blindly to `python3` would still fail in this environment; using the repo venv is the safer fix.

### 2. `generate.sh` is not a drop-in Gemini replacement

It defaults to `gpt-4o-mini` (`generate.sh:18`) and does not export Gemini's OpenAI-compatible base URL or resolve `GEMINI_API_KEY` / `~/.gemini_api_key`. The old workflow does (`.local_scripts/gemini/generation/lib.sh:11-31`).

Impact:

- if someone expects `generate.sh` to replace the previous Gemini workflow, they still need to set Gemini env vars manually and override the model

### 3. `generate.sh` will include multimodal rows by default

`sequential_scaling.py` only skips multimodal records when `--skip-multimodal` is passed (`sequential_scaling.py:723-728`, `sequential_scaling.py:902-906`). `generate.sh` does not pass that flag.

In the current filtered file, the default `LANGS` cover `11,533` records total, including `2,586` multimodal records.

Impact:

- those records will be translated from `source_doc` text only, while the referenced media is ignored
- this is materially different from the old Gemini pipeline, which removed multimodal examples at input-preparation time

### 4. `generate.sh` will append duplicates on rerun

`sequential_scaling.py` opens output files in append mode and only skips finished `doc_id`s when `--resume` is enabled (`sequential_scaling.py:721-722`, `sequential_scaling.py:869-875`, `sequential_scaling.py:928-930`). `generate.sh` does not pass `--resume`.

Impact:

- rerunning the same language will append duplicate records to the same output file

### 5. `generate.sh` loses the old pipeline's stable ordering and audit trail

`sequential_scaling.py` defaults to `--write-order completion` (`sequential_scaling.py:736-738`). The old Gemini wrapper forces `--write-order input` and writes per-language usage/cost/failure logs (`.local_scripts/gemini/generation/generate_lang.sh:83-90`).

Impact:

- output order can vary with concurrency
- simple line-by-line comparison against reference files becomes harder
- blocked/error analysis is less reproducible unless extra flags are supplied manually

### 6. The old Gemini wrapper is likely stale against the current `sequential_scaling.py`

The old Gemini helper and validator assume filenames like `en-zh_CN.jsonl` (`.local_scripts/gemini/generation/common.py:33-35`, `.local_scripts/gemini/generation/validate_results.py:147-152`), but current `sequential_scaling.py` writes files named only by target language, e.g. `zh_CN.jsonl` (`sequential_scaling.py:258-269`).

I confirmed this with a dry run using the current checkout: it wrote:

```text
/tmp/.../gemini-3.5-flash/zh_CN.jsonl
```

Impact:

- the old validation flow will not match current output filenames unless something else renames them
- existing `results/gemini-3.5-flash/en-*.jsonl` files were likely produced before this naming change or by an extra post-step

### 7. Parallel language execution in `generate.sh` can underutilize slots

When `-j > 1`, `generate.sh` waits on the oldest running language job rather than whichever finishes first (`generate.sh:142-166`).

Impact:

- if an older language is slow and a newer one finishes early, that completed slot is not reused immediately
- this is a throughput issue, not a correctness issue

### 8. `generate.sh` carries unused language lists

`LANGS2` and `LANGS3` are defined but never used (`generate.sh:27-43`).

Impact:

- easy to misread which language set is actually active

## Bottom line

If the question is "does `generate.sh` send different Gemini prompts than the old Gemini workflow?", the answer is mostly no: the prompt templates are shared.

If the question is "does `generate.sh` behave like the old Gemini generation strategy?", the answer is definitely no. The main differences are input curation, multimodal handling, Gemini setup, resumability, output ordering, and validation compatibility.
