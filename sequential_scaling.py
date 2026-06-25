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
  6) Write results to results/<src>-<tgt>.jsonl, one record per line holding
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

# LLM client/call live in util/openai_client.py (OpenAI GPT). The judge scripts
# import the same two helpers, so the whole pipeline talks to OpenAI.
from util.openai_client import build_client, call_openai


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
class LLMCache:
    def __init__(self, path: Path, enabled: bool = True):
        self.path = path
        self.enabled = enabled
        self.mem = {}
        self.hits = 0
        self.fh = None
        self.lock = threading.Lock()  # guards mem + file writes under concurrency
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
            val = self.mem.get(key)
            if val is not None:
                self.hits += 1
            return val

    def put(self, key: str, hypothesis: str):
        if not self.enabled:
            return
        with self.lock:
            self.mem[key] = hypothesis
            self.fh.write(json.dumps({"key": key, "hypothesis": hypothesis},
                                     ensure_ascii=False) + "\n")
            self.fh.flush()

    def close(self):
        if self.fh:
            self.fh.close()


def run_rounds(client, model, src_lang, tgt_lang, source, k, context_win,
               system_prompt, temperature, cache, dry_run):
    """Run k refinement rounds for one item; return the list [hypo_0 .. hypo_{k-1}].

    Each round is cached on its full message list, so reruns reuse prior work.
    """
    hypos = []   # hypotheses from finished rounds, in order
    for _ in range(k):
        messages = build_messages(
            src_lang, tgt_lang, source, hypos, context_win, system_prompt)
        if dry_run:
            hypo = ""
        else:
            ckey = LLMCache.make_key(
                model, temperature,
                json.dumps(messages, ensure_ascii=False, sort_keys=True))
            hypo = cache.get(ckey)
            if hypo is None:
                hypo = call_openai(client, model, messages, temperature=temperature)
                cache.put(ckey, hypo)
        hypos.append(hypo)
    return hypos


def parse_args():
    p = argparse.ArgumentParser(description="WMT26 GenMT sequential translation pipeline")
    p.add_argument("--input",
                   default="/Users/diwu001/workplace/personal/wmt26/wmt26_genmt_blindset.jsonl",
                   help="input jsonl path")
    p.add_argument("--results-dir", default="results", help="output directory")
    p.add_argument("--langs", default="zh_CN",
                   help="wanted target languages (raw tgt_lang codes, comma-separated, "
                        "e.g. zh_CN,deu_Latn); default = zh_CN (Chinese); "
                        "pass 'all' to process every language")
    p.add_argument("--model", default="gpt-4o-mini",
                   help="OpenAI model name (e.g. gpt-4o, gpt-4o-mini, gpt-4.1)")
    p.add_argument("--temperature", type=float, default=0.0)
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
    return p.parse_args()


def main():
    args = parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        sys.exit(f"input file not found: {in_path}")

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    want = {x.strip() for x in args.langs.split(",") if x.strip()}
    if {"all", "*"} & {w.lower() for w in want}:  # explicit opt-out of filtering
        want = set()
    print(f"target language filter: {sorted(want)}" if want
          else "processing all target languages")

    cache_path = Path(args.cache_path) if args.cache_path else results_dir / ".gpt_cache.jsonl"
    cache = LLMCache(cache_path, enabled=not args.no_cache and not args.dry_run)
    if cache.enabled:
        print(f"cache: {cache_path} (loaded {len(cache.mem)} entries)")

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
        hypos = run_rounds(client, args.model, it["src_name"], it["tgt_name"],
                           it["source_doc"], args.k, args.context_win,
                           args.system, args.temperature, cache, args.dry_run)
        return it, hypos

    def write_result(it, hypos):
        out_rec = {"doc_id": it["doc_id"], "tgt_lang": it["tgt_lang"],
                   "source_doc": it["source_doc"]}
        for i, h in enumerate(hypos):
            out_rec[f"hypo_{i}"] = h
        out_rec["hypothesis"] = hypos[-1] if hypos else ""
        it["fh"].write(json.dumps(out_rec, ensure_ascii=False) + "\n")
        it["fh"].flush()

    n_done = n_fail = 0
    total = len(work)
    try:
        if args.concurrency <= 1 or args.dry_run:
            for it in work:
                try:
                    write_result(it, worker(it)[1])
                    n_done += 1
                except Exception as e:  # noqa: BLE001
                    n_fail += 1
                    print(f"  [error] doc_id={it['doc_id']} failed: {e}",
                          file=sys.stderr)
                if n_done and n_done % 20 == 0:
                    print(f".. {n_done}/{total} done (failed={n_fail})")
        else:
            with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
                futures = {ex.submit(worker, it): it for it in work}
                for fut in as_completed(futures):
                    it = futures[fut]
                    try:
                        write_result(it, fut.result()[1])
                        n_done += 1
                    except Exception as e:  # noqa: BLE001
                        n_fail += 1
                        print(f"  [error] doc_id={it['doc_id']} failed: {e}",
                              file=sys.stderr)
                    if n_done and n_done % 20 == 0:
                        print(f".. {n_done}/{total} done (failed={n_fail})")
    finally:
        for fh in out_handles.values():
            fh.close()
        cache.close()

    print(f"\nDone. read {n_read} lines; matched {n_kept}; written {n_done}; "
          f"failed {n_fail}; resume-skipped {n_skip}; multimodal {n_mm}; "
          f"cache hits {cache.hits}.")
    print(f"results dir: {results_dir.resolve()}")


if __name__ == "__main__":
    main()
