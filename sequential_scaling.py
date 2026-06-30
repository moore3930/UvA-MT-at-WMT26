#!/usr/bin/env python3
"""sequential_scaling.py

WMT26 GenMT blindset translation pipeline (calls OpenAI GPT per item).

The LLM client/call live in util/openai_client.py (build_client / call_openai),
using the OpenAI SDK: `OpenAI(api_key=...)` and
`client.chat.completions.create(...)`. The API key is read from the
OPENAI_API_KEY env var or ~/.openai_api_key (override with --api-key).

Real per-line fields in the input file:
  doc_id, source_doc, tgt_lang, instruction,
  multimodal_instruction, multimodal_input_path

Pipeline:
  1) Read wmt26_genmt_blindset.jsonl line by line
  2) Filter the wanted target languages (exact match on the raw tgt_lang code)
  3) Map language identifiers (codes) to language names
  4) Resolve the source/target language names for the prompt templates
  5) Run k sequential-scaling rounds: round 0 produces an initial translation,
     each later round asks the model to "translate again to make it better"
     while seeing the previous `context_win` rounds as chat history
  6) Write results to results/<model>/<src>-<tgt>.jsonl, one record per line holding
     every round as hypo_0 .. hypo_{k-1} plus the final `hypothesis`, while
     keeping the input doc_id, tgt_lang and source_doc

Example:
  python sequential_scaling.py \
      --langs zh_CN --model gpt-4o --k 3 --context-win 1
"""

import argparse
import hashlib
import json
import re
import sys
import threading
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path

from results.special_output_markers import OUTPUT_BLOCKED, OUTPUT_ERROR

# LLM client/call live in util/openai_client.py (OpenAI GPT). The judge scripts
# import the same two helpers, so the whole pipeline talks to OpenAI.
from util.openai_client import (
    ContentFilteredError,
    build_client,
    call_openai_with_usage,
)


# --------------------------------------------------------------------------- #
# Language code -> language name. Covers all 45 tgt_lang codes in the data
# plus the source-side codes. Keys use the raw form from the data; lookup is
# case-insensitive.
# --------------------------------------------------------------------------- #
LANG_MAP = {
    # codes that appear on the source side
    "en": "English",
    "tr": "Turkish",
    # target languages (with region / script variants)
    "aeb": "Tunisian Arabic",
    "ar_AR": "Arabic",
    "arz": "Egyptian Arabic",
    "arz_Arab": "Egyptian Arabic",
    "bel_Cyrl": "Belarusian",
    "ces_Latn": "Czech",
    "cs": "Czech",
    "cs_CZ": "Czech",
    "de_AT": "German (Austria)",
    "de_CH": "German (Switzerland)",
    "de_DE": "German",
    "de_IT": "German (Italy)",
    "deu_Latn": "German",
    "ekk_Latn": "Estonian",
    "en_US": "English (United States)",
    "es_ES": "Spanish",
    "et_EE": "Estonian",
    "fo": "Faroese",
    "hin_Deva": "Hindi",
    "hr": "Croatian",
    "hye_Armn": "Eastern Armenian",
    "ind_Latn": "Indonesian",
    "is": "Icelandic",
    "isl_Latn": "Icelandic",
    "jpn_Jpan": "Japanese",
    "kaz_Cyrl": "Kazakh",
    "ko_KR": "Korean",
    "kor_Hang": "Korean",
    "lij_Latn": "Ligurian",
    "lld_Latn": "Ladin",
    "mni_Beng": "Manipuri (Bengali script)",
    "mni_Latn": "Manipuri (Latin script)",
    "mni_Mtei": "Manipuri (Meitei Mayek script)",
    "pl_PL": "Polish",
    "ru": "Russian",
    "ru_RU": "Russian",
    "rus_Cyrl": "Russian",
    "sme_Latn": "Northern Sami",
    "tha_Thai": "Thai",
    "ukr_Cyrl": "Ukrainian",
    "vie_Latn": "Vietnamese",
    "zh_CN": "Chinese (Simplified)",
    "zho_Hans": "Chinese (Simplified)",
    "zho_Hant_TW": "Chinese (Traditional)",
}

# case-insensitive lookup table
_LANG_MAP_LC = {k.lower(): v for k, v in LANG_MAP.items()}


def lang_name(code: str) -> str:
    """Code -> language name; return the code unchanged if not found
    (e.g. it is already 'English')."""
    if not code:
        return code
    return _LANG_MAP_LC.get(code.strip().lower(), code)


# matches "Translate from <X> to <Y>", capturing both identifiers
# (up to '.', '(', whitespace, or end of string)
_FROM_TO = re.compile(r"(Translate\s+from\s+)(\S+?)(\s+to\s+)(\S+?)(?=[\s.(]|$)",
                      re.IGNORECASE)


def transform_instruction(instruction: str):
    """Replace the language codes in 'from X to Y' with language names.

    Returns (new_instruction, parsed_source_code_or_name).
    For instructions already written with names ('from English to Faroese')
    or detailed guidance templates, lang_name leaves unknown tokens as-is,
    so nothing changes.
    """
    if not instruction:
        return instruction, None

    src_holder = {"src": None}

    def _repl(m):
        src_holder["src"] = m.group(2)
        return f"{m.group(1)}{lang_name(m.group(2))}{m.group(3)}{lang_name(m.group(4))}"

    new = _FROM_TO.sub(_repl, instruction, count=1)
    return new, src_holder["src"]


# --------------------------------------------------------------------------- #
# Multi-round (sequential-scaling) prompting
#   round 0 : an initial translation (STEP1)
#   round i : "translate again to make it better" (STEP2), shown the previous
#             `context_win` rounds as conversation history
# --------------------------------------------------------------------------- #
STEP1_PROMPT = (
    "Please translate the following text from {src_lang} to {tgt_lang}. "
    "Provide only one translation on the first line and do not output anything "
    "else after that.\n\n{src_lang}: {source}\n{tgt_lang}:"
)

STEP2_PROMPT = (
    "Please again translate the following text from {src_lang} to {tgt_lang} "
    "to make it better. Provide only one translation on the first line and do "
    "not output anything else after that.\n\n{src_lang}: {source}\n{tgt_lang}:"
)


def turn_prompt(is_first: bool, src_lang: str, tgt_lang: str, source: str) -> str:
    """User prompt for one conversation turn.

    The FIRST turn uses STEP1 ('please translate'); any later turn uses STEP2
    ('please again translate ... to make it better').
    """
    template = STEP1_PROMPT if is_first else STEP2_PROMPT
    return template.format(src_lang=src_lang, tgt_lang=tgt_lang, source=source)


def build_messages(src_lang, tgt_lang, source, history_hypos,
                   context_win, system_prompt):
    """Assemble the chat messages for the next round.

    history_hypos: hypotheses from finished rounds, in order. Only the last
    `context_win` are shown back to the model. The conversation always OPENS
    with a STEP1 'translate' request; every later user turn (including the
    current one, when there is history) uses STEP2 'translate again'. So even
    when the window has dropped the original round 0, the shown conversation
    still starts with a plain translate request, then refines.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    window = history_hypos[-context_win:] if context_win > 0 else []
    for turn_idx, past_hypo in enumerate(window):
        messages.append({"role": "user",
                         "content": turn_prompt(turn_idx == 0, src_lang, tgt_lang, source)})
        messages.append({"role": "assistant", "content": past_hypo})

    # current request: STEP1 only when it is the very first turn (no history)
    messages.append({"role": "user",
                     "content": turn_prompt(not window, src_lang, tgt_lang, source)})
    return messages


def normalize(code: str) -> str:
    return code.strip().lower() if code else code


# the source side may be written as a code or a language name; canonicalize it
# to a single short code so the same language pair is not split into files
_SRC_CANON = {
    "en": "en", "eng": "en", "english": "en",
    "tr": "tr", "tur": "tr", "turkish": "tr",
    "ko": "ko", "kor": "ko", "korean": "ko",
}


def canon_src(src: str) -> str:
    if not src:
        return "en"
    key = src.strip().lower()
    if key in _SRC_CANON:
        return _SRC_CANON[key]
    if key in _LANG_MAP_LC:  # already a known code
        return key
    return safe_name(key)


def safe_name(s: str) -> str:
    """Make a string safe to use in a filename."""
    return re.sub(r"[^0-9A-Za-z._-]+", "_", s) if s else s


def pair_filename(src_code: str, tgt_lang: str) -> str:
    s = safe_name(src_code) or "src"
    t = safe_name(tgt_lang) or "tgt"
    return f"{s}-{t}.jsonl"


PRICING_PROFILES = {
    "gemini-3.5-flash": {
        "input_per_million_usd": 1.50,
        "output_per_million_usd": 9.00,
    },
    "gemini-2.5-pro": {
        "input_per_million_usd": 1.25,
        "output_per_million_usd": 10.00,
    },
    "gemini-2.5-flash": {
        "input_per_million_usd": 0.30,
        "output_per_million_usd": 2.50,
    },
    "gemini-3.1-flash-lite": {
        "input_per_million_usd": 0.25,
        "output_per_million_usd": 1.50,
    },
    "gemini-2.5-flash-lite": {
        "input_per_million_usd": 0.10,
        "output_per_million_usd": 0.40,
    },
}


def usage_log_record(doc_id: str, tgt_lang: str, model: str, round_idx: int,
                     usage: dict, pricing_profile: str = "",
                     cache_hit: bool = False) -> dict:
    """Build one per-call usage record and attach an estimated cost."""
    prompt_tokens = int((usage or {}).get("prompt_tokens") or 0)
    completion_tokens = int((usage or {}).get("completion_tokens") or 0)
    total_tokens = int((usage or {}).get("total_tokens") or 0)
    inferred_thinking_tokens = max(
        total_tokens - prompt_tokens - completion_tokens, 0)
    billed_output_tokens = max(total_tokens - prompt_tokens, 0)
    cost_usd = None
    rates = PRICING_PROFILES.get(pricing_profile) if pricing_profile else None
    if rates is not None:
        cost_usd = round(
            (prompt_tokens / 1_000_000.0) * rates["input_per_million_usd"]
            + (billed_output_tokens / 1_000_000.0)
            * rates["output_per_million_usd"],
            10,
        )
    return {
        "doc_id": doc_id,
        "tgt_lang": tgt_lang,
        "model": model,
        "round": round_idx,
        "cache_hit": cache_hit,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "inferred_thinking_tokens": inferred_thinking_tokens,
        "estimated_cost_usd": cost_usd,
    }


def empty_usage_bucket() -> dict:
    return {
        "calls": 0,
        "cache_hits": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "inferred_thinking_tokens": 0,
        "estimated_cost_usd": 0.0,
    }


def accumulate_usage(bucket: dict, record: dict):
    """Accumulate one usage record into a summary bucket."""
    bucket["calls"] += 1
    bucket["cache_hits"] += 1 if record.get("cache_hit") else 0
    bucket["prompt_tokens"] += record["prompt_tokens"]
    bucket["completion_tokens"] += record["completion_tokens"]
    bucket["total_tokens"] += record["total_tokens"]
    bucket["inferred_thinking_tokens"] += record["inferred_thinking_tokens"]
    if record.get("estimated_cost_usd") is not None:
        bucket["estimated_cost_usd"] = round(
            bucket["estimated_cost_usd"] + record["estimated_cost_usd"], 10)


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def classify_failure(err: Exception) -> str:
    """Map an exception to a stable failure kind."""
    if isinstance(err, ContentFilteredError):
        return "blocked"
    return "error"


def is_counted_failure_kind(kind: str) -> bool:
    return kind in {"blocked", "error"}


def load_done_ids(path: Path) -> set:
    done = set()
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    done.add(json.loads(line).get("doc_id"))
                except json.JSONDecodeError:
                    continue
    return done


# --------------------------------------------------------------------------- #
# Prompt-level persistent cache
#   key = sha256(model + temperature + prompt)
#   stored as an append-only jsonl ({"key":..., "hypothesis":...} per line),
#   plus an in-memory dict for lookups. Identical prompts are reused, which
#   survives reruns, changed filters, and changed output filenames.
# --------------------------------------------------------------------------- #
class _PendingValue:
    """One in-flight cache fill that other threads can wait on."""

    def __init__(self):
        self.event = threading.Event()
        self.error = None


class LLMCache:
    def __init__(self, path: Path, enabled: bool = True):
        self.path = path
        self.enabled = enabled
        self.mem = {}
        self.loaded_entries = 0
        self.lookups = 0
        self.hits = 0
        self.writes = 0
        self.fh = None
        self.lock = threading.Lock()  # guards mem + file writes under concurrency
        self.inflight = {}
        if not enabled:
            return
        # load existing cache
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        self.mem[rec["key"]] = rec["hypothesis"]
                    except (json.JSONDecodeError, KeyError):
                        continue
        self.loaded_entries = len(self.mem)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = path.open("a", encoding="utf-8")

    @staticmethod
    def make_key(model: str, temperature: float, prompt: str) -> str:
        h = hashlib.sha256()
        h.update(f"{model}\x00{temperature}\x00".encode("utf-8"))
        h.update(prompt.encode("utf-8"))
        return h.hexdigest()

    def get(self, key: str):
        if not self.enabled:
            return None
        with self.lock:
            self.lookups += 1
            val = self.mem.get(key)
            if val is not None:
                self.hits += 1
            return val

    def put(self, key: str, hypothesis: str):
        if not self.enabled:
            return
        with self.lock:
            if key in self.mem:
                return
            self.mem[key] = hypothesis
            self.fh.write(json.dumps({"key": key, "hypothesis": hypothesis},
                                     ensure_ascii=False) + "\n")
            self.fh.flush()
            self.writes += 1

    def get_or_compute(self, key: str, compute_fn):
        """Return a cached value or compute it once across concurrent threads."""
        if not self.enabled:
            return compute_fn()

        while True:
            with self.lock:
                self.lookups += 1
                val = self.mem.get(key)
                if val is not None:
                    self.hits += 1
                    return val

                pending = self.inflight.get(key)
                if pending is None:
                    pending = _PendingValue()
                    self.inflight[key] = pending
                    owner = True
                else:
                    owner = False

            if owner:
                try:
                    value = compute_fn()
                except Exception as e:  # noqa: BLE001
                    with self.lock:
                        self.inflight.pop(key, None)
                    pending.error = e
                    pending.event.set()
                    raise

                with self.lock:
                    if key not in self.mem:
                        self.mem[key] = value
                        self.fh.write(json.dumps({"key": key, "hypothesis": value},
                                                 ensure_ascii=False) + "\n")
                        self.fh.flush()
                        self.writes += 1
                    self.inflight.pop(key, None)
                pending.event.set()
                return value

            pending.event.wait()
            if pending.error is not None:
                raise pending.error

            with self.lock:
                val = self.mem.get(key)
                if val is not None:
                    self.hits += 1
                    return val
            raise RuntimeError(
                f"Cache waiter woke up for missing key {key}; expected cached value")

    def get_or_compute_payload(self, key: str, compute_fn, value_fn):
        """Return (value, payload_or_none, cache_hit) with single-flight semantics."""
        if not self.enabled:
            payload = compute_fn()
            return value_fn(payload), payload, False

        while True:
            with self.lock:
                self.lookups += 1
                val = self.mem.get(key)
                if val is not None:
                    self.hits += 1
                    return val, None, True

                pending = self.inflight.get(key)
                if pending is None:
                    pending = _PendingValue()
                    self.inflight[key] = pending
                    owner = True
                else:
                    owner = False

            if owner:
                try:
                    payload = compute_fn()
                    value = value_fn(payload)
                except Exception as e:  # noqa: BLE001
                    with self.lock:
                        self.inflight.pop(key, None)
                    pending.error = e
                    pending.event.set()
                    raise

                with self.lock:
                    if key not in self.mem:
                        self.mem[key] = value
                        self.fh.write(json.dumps({"key": key, "hypothesis": value},
                                                 ensure_ascii=False) + "\n")
                        self.fh.flush()
                        self.writes += 1
                    self.inflight.pop(key, None)
                pending.event.set()
                return value, payload, False

            pending.event.wait()
            if pending.error is not None:
                raise pending.error

            with self.lock:
                val = self.mem.get(key)
                if val is not None:
                    self.hits += 1
                    return val, None, True
            raise RuntimeError(
                f"Cache waiter woke up for missing key {key}; expected cached value")

    def stats(self) -> dict:
        """Return a thread-safe snapshot of cache activity."""
        with self.lock:
            lookups = self.lookups
            hits = self.hits
            writes = self.writes
            total_entries = len(self.mem)
            loaded_entries = self.loaded_entries
            inflight = len(self.inflight)
        return {
            "enabled": self.enabled,
            "loaded_entries": loaded_entries,
            "lookups": lookups,
            "hits": hits,
            "misses": lookups - hits,
            "writes": writes,
            "total_entries": total_entries,
            "inflight": inflight,
            "hit_rate": (hits / lookups) if lookups else None,
        }

    def close(self):
        if self.fh:
            self.fh.close()


def run_rounds(client, model, src_lang, tgt_lang, source, k, context_win,
               system_prompt, temperature, cache, dry_run,
               request_options=None):
    """Run k refinement rounds for one item.

    Returns (hypos, round_usage_records, terminal_error, terminal_kind).
    Blocked/error rows keep any completed earlier rounds and fill the
    blocked/unattempted tail with a marker so the output file stays aligned
    with the reference set.
    """
    hypos = []   # hypotheses from finished rounds, in order
    round_usage = []
    terminal_error = None
    terminal_kind = None
    for round_idx in range(k):
        messages = build_messages(
            src_lang, tgt_lang, source, hypos, context_win, system_prompt)
        if dry_run:
            hypo = ""
            usage = {}
            cache_hit = False
        else:
            ckey = LLMCache.make_key(
                model, temperature,
                json.dumps(messages, ensure_ascii=False, sort_keys=True))
            try:
                hypo, payload, cache_hit = cache.get_or_compute_payload(
                    ckey,
                    lambda: call_openai_with_usage(
                        client,
                        model,
                        messages,
                        temperature=temperature,
                        request_options=request_options,
                    ),
                    lambda payload: payload[0],
                )
            except ContentFilteredError as err:
                terminal_error = err
                terminal_kind = "blocked"
                hypos.extend([OUTPUT_BLOCKED] * (k - len(hypos)))
                round_usage.append({
                    "round": round_idx,
                    "cache_hit": False,
                    "usage": {},
                    "blocked": True,
                    "error": False,
                })
                break
            except Exception as err:  # noqa: BLE001
                terminal_error = err
                terminal_kind = "error"
                hypos.extend([OUTPUT_ERROR] * (k - len(hypos)))
                round_usage.append({
                    "round": round_idx,
                    "cache_hit": False,
                    "usage": {},
                    "blocked": False,
                    "error": True,
                })
                break
            usage = payload[1] if payload is not None else {}
        hypos.append(hypo)
        round_usage.append({
            "round": round_idx,
            "cache_hit": cache_hit,
            "usage": usage,
            "blocked": False,
            "error": False,
        })
    return hypos, round_usage, terminal_error, terminal_kind


def parse_args():
    p = argparse.ArgumentParser(description="WMT26 GenMT sequential translation pipeline")
    p.add_argument("--input",
                   default="/Users/diwu001/workplace/personal/wmt26/wmt26_genmt_blindset.jsonl",
                   help="input jsonl path")
    p.add_argument("--results-dir", default="results",
                   help="output directory; results are written under a per-model "
                        "subdir <results-dir>/<model>/<src>-<tgt>.jsonl")
    p.add_argument("--langs", default="zh_CN",
                   help="wanted target languages (raw tgt_lang codes, comma-separated, "
                        "e.g. zh_CN,deu_Latn); default = zh_CN (Chinese); "
                        "pass 'all' to process every language")
    p.add_argument("--model", default="gpt-4o-mini",
                   help="OpenAI model name (e.g. gpt-4o, gpt-4o-mini, gpt-4.1)")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--reasoning-effort", default="",
                   help="optional reasoning control for compatible providers "
                        "(e.g. minimal, low, medium, high)")
    p.add_argument("-k", "--k", type=int, default=1,
                   help="number of translation rounds (sequential scaling); "
                        "round 0 translates, later rounds refine. Stored as "
                        "hypo_0 .. hypo_{k-1}")
    p.add_argument("--context-win", type=int, default=1,
                   help="how many previous rounds the model sees when refining "
                        "(default 1 = only the last round)")
    p.add_argument("--concurrency", type=int, default=16,
                   help="number of documents translated in parallel (threads). "
                        "Each doc's k rounds stay sequential; only different docs "
                        "run concurrently. 1 = fully sequential")
    p.add_argument("--api-key", default="",
                   help="OpenAI API key; defaults to OPENAI_API_KEY env "
                        "or ~/.openai_api_key")
    p.add_argument("--system", default="You are a professional translator. "
                   "Follow the instruction and output only the translation, "
                   "with no explanations.",
                   help="system prompt (empty string = no system message)")
    p.add_argument("--limit", type=int, default=0,
                   help="max items to process (0 = no limit, for debugging)")
    p.add_argument("--resume", action="store_true",
                   help="skip doc_id values already present in the output files")
    p.add_argument("--skip-multimodal", action="store_true", default=True,
                   help="skip multimodal samples (on by default; v1 is text-only)")
    p.add_argument("--dry-run", action="store_true",
                   help="only parse and build prompts, do not call GPT (hypothesis empty)")
    p.add_argument("--cache-path", default="",
                   help="prompt-level cache file (default <results-dir>/.gpt_cache.jsonl)")
    p.add_argument("--no-cache", action="store_true", help="disable the prompt-level cache")
    p.add_argument("--write-order", choices=("completion", "input"),
                   default="completion",
                   help="write finished docs as they complete or preserve input order")
    p.add_argument("--usage-log", default="",
                   help="jsonl path for per-call token usage (default "
                        "<results-dir>/usage/<input_stem>.usage.jsonl when tracking)")
    p.add_argument("--cost-summary", default="",
                   help="json path for aggregated token usage and estimated cost "
                        "(default <results-dir>/usage/<input_stem>.summary.json "
                        "when tracking)")
    p.add_argument("--failure-log", default="",
                   help="jsonl path for per-doc failures (default "
                        "<results-dir>/usage/<input_stem>.failures.jsonl when tracking)")
    p.add_argument("--failure-summary", default="",
                   help="json path for aggregated failure counts (default "
                        "<results-dir>/usage/<input_stem>.failures.summary.json "
                        "when tracking)")
    p.add_argument("--pricing-profile", default="",
                   choices=sorted(PRICING_PROFILES),
                   help="pricing profile for estimated cost reporting")
    return p.parse_args()


def main():
    args = parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        sys.exit(f"input file not found: {in_path}")

    # scope outputs by model so different models never share/clobber files:
    # <results-dir>/<model>/<src>-<tgt>.jsonl (default cache lives here too)
    results_dir = Path(args.results_dir) / safe_name(args.model)
    results_dir.mkdir(parents=True, exist_ok=True)

    want = {x.strip() for x in args.langs.split(",") if x.strip()}
    if {"all", "*"} & {w.lower() for w in want}:  # explicit opt-out of filtering
        want = set()
    print(f"target language filter: {sorted(want)}" if want
          else "processing all target languages")

    request_options = {}
    if args.reasoning_effort:
        request_options["reasoning_effort"] = args.reasoning_effort
    if not request_options:
        request_options = None

    track_usage = (not args.dry_run and bool(
        args.usage_log or args.cost_summary or args.pricing_profile))
    usage_log_path = None
    cost_summary_path = None
    failure_log_path = None
    failure_summary_path = None
    usage_fh = None
    failure_fh = None
    usage_totals = empty_usage_bucket()
    per_language_usage = {}
    docs_written_by_lang = {}
    loaded_usage_records = 0
    failure_counts = {"blocked": 0, "error": 0}
    per_language_failures = {}
    latest_failures = {}
    loaded_failure_records = 0

    def load_existing_usage(path: Path):
        totals = empty_usage_bucket()
        per_lang = {}
        loaded = 0
        if not path.exists():
            return totals, per_lang, loaded
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                accumulate_usage(totals, record)
                lang_bucket = per_lang.setdefault(
                    record.get("tgt_lang", ""), empty_usage_bucket())
                accumulate_usage(lang_bucket, record)
                loaded += 1
        return totals, per_lang, loaded

    if track_usage:
        usage_dir = results_dir / "usage"
        usage_log_path = (Path(args.usage_log) if args.usage_log
                          else usage_dir / f"{in_path.stem}.usage.jsonl")
        cost_summary_path = (Path(args.cost_summary) if args.cost_summary
                             else usage_dir / f"{in_path.stem}.summary.json")
        failure_log_path = (Path(args.failure_log) if args.failure_log
                            else usage_dir / f"{in_path.stem}.failures.jsonl")
        failure_summary_path = (Path(args.failure_summary) if args.failure_summary
                                else usage_dir / f"{in_path.stem}.failures.summary.json")
        usage_log_path.parent.mkdir(parents=True, exist_ok=True)
        usage_totals, per_language_usage, loaded_usage_records = (
            load_existing_usage(usage_log_path))
        usage_fh = usage_log_path.open("a", encoding="utf-8")

        if failure_log_path.exists():
            with failure_log_path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    doc_id = record.get("doc_id")
                    if doc_id:
                        latest_failures[doc_id] = record
                        loaded_failure_records += 1
        for record in latest_failures.values():
            kind = record.get("kind", "error")
            if not is_counted_failure_kind(kind):
                continue
            failure_counts[kind] = failure_counts.get(kind, 0) + 1
            lang_bucket = per_language_failures.setdefault(
                record.get("tgt_lang", ""), {"blocked": 0, "error": 0})
            lang_bucket[kind] = lang_bucket.get(kind, 0) + 1
        failure_fh = failure_log_path.open("a", encoding="utf-8")

    cache_path = Path(args.cache_path) if args.cache_path else results_dir / ".gpt_cache.jsonl"
    cache = LLMCache(cache_path, enabled=not args.no_cache and not args.dry_run)
    if cache.enabled:
        print(f"cache: {cache_path} (loaded {cache.loaded_entries} entries)")

    out_handles = {}
    done_ids = {}

    def get_handle(src_code, tgt_lang):
        fname = pair_filename(src_code, tgt_lang)
        if fname not in out_handles:
            fpath = results_dir / fname
            if args.resume:
                done_ids[fname] = load_done_ids(fpath)
            out_handles[fname] = fpath.open("a", encoding="utf-8")
        return fname, out_handles[fname]

    # ---- phase 1: build the work list (sequential file I/O, main thread) ----
    work = []
    n_read = n_kept = n_skip = n_mm = 0
    with in_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_read += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"  [warn] skipping malformed line: {e}", file=sys.stderr)
                continue

            tgt_lang = item.get("tgt_lang")
            doc_id = item.get("doc_id")
            instruction = item.get("instruction") or ""
            source_doc = item.get("source_doc") or ""

            # 2) filter target languages (exact match on the raw code)
            if want and tgt_lang not in want:
                continue
            # multimodal samples: skipped in v1
            if args.skip_multimodal and (item.get("multimodal_instruction")
                                         or item.get("multimodal_input_path")):
                n_mm += 1
                continue
            n_kept += 1

            # 3)+4) resolve source/target language names for the prompts
            _, src_raw = transform_instruction(instruction)
            src_code = canon_src(src_raw)  # source is overwhelmingly en
            fname, fh = get_handle(src_code, tgt_lang)
            if args.resume and doc_id in done_ids.get(fname, set()):
                n_skip += 1
                continue

            work.append({
                "work_idx": len(work),
                "doc_id": doc_id, "tgt_lang": tgt_lang, "source_doc": source_doc,
                "src_name": lang_name(src_code), "tgt_name": lang_name(tgt_lang),
                "fh": fh,
            })
            if args.limit and len(work) >= args.limit:
                break

    print(f"to translate: {len(work)} docs (matched {n_kept}, "
          f"resume-skipped {n_skip}, multimodal {n_mm}); "
          f"k={args.k} context_win={args.context_win} concurrency={args.concurrency}")

    # ---- phase 2: translate, concurrent over docs (k rounds stay sequential) ----
    # One client per worker thread (mirrors test.py's per-path client). Only the
    # main thread writes output, so no output lock is needed; the cache is locked.
    tlocal = threading.local()

    def thread_client():
        c = getattr(tlocal, "client", None)
        if c is None:
            c = build_client(args.api_key)
            tlocal.client = c
        return c

    def worker(it):
        client = None if args.dry_run else thread_client()
        hypos, round_usage, terminal_error, terminal_kind = run_rounds(
            client,
            args.model,
            it["src_name"],
            it["tgt_name"],
            it["source_doc"],
            args.k,
            args.context_win,
            args.system,
            args.temperature,
            cache,
            args.dry_run,
            request_options=request_options,
        )
        return it, hypos, round_usage, terminal_error, terminal_kind

    def write_result(it, hypos):
        out_rec = {"doc_id": it["doc_id"], "tgt_lang": it["tgt_lang"],
                   "source_doc": it["source_doc"]}
        for i, h in enumerate(hypos):
            out_rec[f"hypo_{i}"] = h
        out_rec["hypothesis"] = hypos[-1] if hypos else ""
        it["fh"].write(json.dumps(out_rec, ensure_ascii=False) + "\n")
        it["fh"].flush()

    def write_usage_records(it, round_usage):
        if not track_usage:
            return
        for round_info in round_usage:
            record = usage_log_record(
                it["doc_id"],
                it["tgt_lang"],
                args.model,
                round_info["round"],
                round_info["usage"],
                pricing_profile=args.pricing_profile,
                cache_hit=round_info["cache_hit"],
            )
            usage_fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            usage_fh.flush()
            accumulate_usage(usage_totals, record)
            lang_bucket = per_language_usage.setdefault(
                it["tgt_lang"], empty_usage_bucket())
            accumulate_usage(lang_bucket, record)

    n_done = n_blocked = n_error_rows = n_fail = 0
    last_reported = 0
    total = len(work)

    def maybe_report_progress():
        nonlocal last_reported
        processed = n_done + n_fail
        if not processed or processed - last_reported < 20:
            return
        last_reported = processed
        if cache.enabled:
            stats = cache.stats()
            print(f".. {processed}/{total} processed (written={n_done}; "
                  f"error_rows={n_error_rows}; failed={n_fail}; "
                  f"cache hits={stats['hits']}/{stats['lookups']}, "
                  f"new={stats['writes']})")
        else:
            print(f".. {processed}/{total} processed (written={n_done}; "
                  f"error_rows={n_error_rows}; failed={n_fail})")

    def record_failure(it, err):
        kind = classify_failure(err)
        if not track_usage:
            return kind
        record = {
            "doc_id": it["doc_id"],
            "tgt_lang": it["tgt_lang"],
            "model": args.model,
            "kind": kind,
            "error": str(err),
        }
        failure_fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        failure_fh.flush()

        prev = latest_failures.get(it["doc_id"])
        if prev is not None:
            prev_kind = prev.get("kind", "error")
            if is_counted_failure_kind(prev_kind):
                failure_counts[prev_kind] = max(
                    failure_counts.get(prev_kind, 0) - 1, 0)
                prev_bucket = per_language_failures.setdefault(
                    prev.get("tgt_lang", ""), {"blocked": 0, "error": 0})
                prev_bucket[prev_kind] = max(prev_bucket.get(prev_kind, 0) - 1, 0)
        latest_failures[it["doc_id"]] = record
        failure_counts[kind] = failure_counts.get(kind, 0) + 1
        lang_bucket = per_language_failures.setdefault(
            it["tgt_lang"], {"blocked": 0, "error": 0})
        lang_bucket[kind] = lang_bucket.get(kind, 0) + 1
        return kind

    def resolve_failure_if_needed(it):
        if not track_usage:
            return
        prev = latest_failures.get(it["doc_id"])
        if prev is None:
            return
        prev_kind = prev.get("kind", "error")
        if not is_counted_failure_kind(prev_kind):
            return
        record = {
            "doc_id": it["doc_id"],
            "tgt_lang": it["tgt_lang"],
            "model": args.model,
            "kind": "resolved",
            "error": None,
        }
        failure_fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        failure_fh.flush()
        latest_failures[it["doc_id"]] = record
        failure_counts[prev_kind] = max(failure_counts.get(prev_kind, 0) - 1, 0)
        lang_bucket = per_language_failures.setdefault(
            it["tgt_lang"], {"blocked": 0, "error": 0})
        lang_bucket[prev_kind] = max(lang_bucket.get(prev_kind, 0) - 1, 0)

    def commit_success(it, hypos, round_usage):
        nonlocal n_done
        write_result(it, hypos)
        write_usage_records(it, round_usage)
        resolve_failure_if_needed(it)
        docs_written_by_lang[it["tgt_lang"]] = (
            docs_written_by_lang.get(it["tgt_lang"], 0) + 1)
        n_done += 1
        maybe_report_progress()

    def commit_terminal_marker(it, hypos, round_usage, err, kind):
        nonlocal n_done, n_blocked, n_error_rows
        write_result(it, hypos)
        write_usage_records(it, round_usage)
        docs_written_by_lang[it["tgt_lang"]] = (
            docs_written_by_lang.get(it["tgt_lang"], 0) + 1)
        record_failure(it, err)
        n_done += 1
        if kind == "blocked":
            n_blocked += 1
            print(f"  [blocked] doc_id={it['doc_id']}: {err}", file=sys.stderr)
        else:
            n_error_rows += 1
            print(f"  [error-row] doc_id={it['doc_id']}: {err}", file=sys.stderr)
        maybe_report_progress()

    def commit_failure(it, err):
        nonlocal n_fail
        n_fail += 1
        record_failure(it, err)
        print(f"  [error] doc_id={it['doc_id']} failed: {err}", file=sys.stderr)
        maybe_report_progress()

    try:
        if args.concurrency <= 1 or args.dry_run:
            for it in work:
                try:
                    _, hypos, round_usage, terminal_error, terminal_kind = worker(it)
                    if terminal_error is not None:
                        commit_terminal_marker(
                            it, hypos, round_usage, terminal_error, terminal_kind)
                    else:
                        commit_success(it, hypos, round_usage)
                except Exception as e:  # noqa: BLE001
                    commit_failure(it, e)
        else:
            with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
                futures = {ex.submit(worker, it): it for it in work}
                pending = {}
                next_write_idx = 0
                for fut in as_completed(futures):
                    it = futures[fut]
                    try:
                        outcome = ("ok",) + fut.result()
                    except Exception as e:  # noqa: BLE001
                        outcome = ("error", it, e)

                    if args.write_order == "completion":
                        if outcome[0] == "ok":
                            (_tag, done_it, hypos, round_usage,
                             terminal_error, terminal_kind) = outcome
                            if terminal_error is not None:
                                commit_terminal_marker(
                                    done_it, hypos, round_usage,
                                    terminal_error, terminal_kind)
                            else:
                                commit_success(done_it, hypos, round_usage)
                        else:
                            _tag, done_it, err = outcome
                            commit_failure(done_it, err)
                        continue

                    pending[it["work_idx"]] = outcome
                    while next_write_idx in pending:
                        queued = pending.pop(next_write_idx)
                        if queued[0] == "ok":
                            (_tag, done_it, hypos, round_usage,
                             terminal_error, terminal_kind) = queued
                            if terminal_error is not None:
                                commit_terminal_marker(
                                    done_it, hypos, round_usage,
                                    terminal_error, terminal_kind)
                            else:
                                commit_success(done_it, hypos, round_usage)
                        else:
                            _tag, done_it, err = queued
                            commit_failure(done_it, err)
                        next_write_idx += 1
    finally:
        for fh in out_handles.values():
            fh.close()
        if usage_fh is not None:
            usage_fh.close()
        if failure_fh is not None:
            failure_fh.close()
        cache.close()

    print(f"\nDone. read {n_read} lines; matched {n_kept}; written {n_done}; "
          f"blocked {n_blocked}; error-marked {n_error_rows}; failed {n_fail}; "
          f"resume-skipped {n_skip}; "
          f"multimodal {n_mm}.")
    if cache.enabled:
        stats = cache.stats()
        hit_rate = (f"{100 * stats['hit_rate']:.1f}%"
                    if stats["hit_rate"] is not None else "n/a")
        print(f"cache activity: hits={stats['hits']}/{stats['lookups']} "
              f"({hit_rate}), new entries={stats['writes']}, "
              f"total entries={stats['total_entries']}")
    if track_usage and cost_summary_path is not None:
        summary = {
            "model": args.model,
            "pricing_profile": args.pricing_profile or None,
            "pricing_rates": PRICING_PROFILES.get(args.pricing_profile),
            "input_path": str(in_path.resolve()),
            "results_dir": str(results_dir.resolve()),
            "usage_log_path": str(usage_log_path.resolve()),
            "temperature": args.temperature,
            "reasoning_effort": args.reasoning_effort or None,
            "k": args.k,
            "context_win": args.context_win,
            "write_order": args.write_order,
            "loaded_usage_records": loaded_usage_records,
            "loaded_failure_records": loaded_failure_records,
            "documents_written_this_run": n_done,
            "documents_blocked_this_run": n_blocked,
            "documents_error_this_run": n_error_rows + n_fail,
            "documents_failed_this_run": n_blocked + n_error_rows + n_fail,
            "resume_skipped_this_run": n_skip,
            "totals": usage_totals,
            "per_language": {},
        }
        for lang, bucket in sorted(per_language_usage.items()):
            lang_summary = dict(bucket)
            lang_summary["documents_written_this_run"] = docs_written_by_lang.get(lang, 0)
            summary["per_language"][lang] = lang_summary
        write_json(cost_summary_path, summary)
        failure_summary = {
            "model": args.model,
            "input_path": str(in_path.resolve()),
            "failure_log_path": (str(failure_log_path.resolve())
                                  if failure_log_path is not None else None),
            "documents_written_this_run": n_done,
            "documents_blocked_this_run": n_blocked,
            "documents_error_this_run": n_error_rows + n_fail,
            "documents_failed_this_run": n_blocked + n_error_rows + n_fail,
            "loaded_failure_records": loaded_failure_records,
            "totals": failure_counts,
            "per_language": {},
            "latest_failures": sorted(latest_failures.values(), key=lambda rec: rec["doc_id"]),
        }
        for lang, bucket in sorted(per_language_failures.items()):
            failure_summary["per_language"][lang] = {
                "blocked": bucket.get("blocked", 0),
                "error": bucket.get("error", 0),
            }
        write_json(failure_summary_path, failure_summary)
        print(f"usage log: {usage_log_path.resolve()}")
        print(f"cost summary: {cost_summary_path.resolve()}")
        print(f"failure log: {failure_log_path.resolve()}")
        print(f"failure summary: {failure_summary_path.resolve()}")
        if args.pricing_profile:
            print(f"estimated cost so far: ${usage_totals['estimated_cost_usd']:.4f}")
    print(f"results dir: {results_dir.resolve()}")


if __name__ == "__main__":
    main()
