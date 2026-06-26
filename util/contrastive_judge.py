#!/usr/bin/env python3
"""contrastive_judge.py

Pairwise (contrastive) MT judge: given a source text and TWO candidate
translations, decide which one is better (A / B / tie) according to a rubric.

It reuses the MetaGen access, cache and concurrency from sequential_scaling.py.

Typical uses
------------
Compare two systems' outputs (joined on doc_id):
    python util/contrastive_judge.py --a sysX.jsonl --b sysY.jsonl

Check whether refinement helped, within one file (round 0 vs round 7):
    python util/contrastive_judge.py --a results/en-zh_CN.jsonl \
        --a-field hypo_0 --b-field hypo_7

Position bias
-------------
LLM pairwise judges tend to favour whichever candidate is shown first. By
default each pair is judged TWICE (A,B and B,A); a side only "wins" if it wins
both orders, otherwise the verdict is a tie and flagged inconsistent. Disable
with --no-swap (one call per pair, faster, biased).

Rubric
------
The judging criteria live in DEFAULT_RUBRIC below (edit it directly), or pass
--rubric-file to supply your own free-form rubric text.
"""

import argparse
import json
import os
import re
import sys
import threading
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path

# This module lives in util/ but imports sequential_scaling from the repo root.
# Put the repo root on sys.path so `python util/contrastive_judge.py` works as a
# script too (harmless no-op when imported as the util.contrastive_judge module).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Reuse the provider-agnostic plumbing (language map + prompt cache) from
# sequential_scaling.py, but get the LLM client/call from util/openai_client.py
# so the judge talks to OpenAI GPT instead of MetaGen.
from sequential_scaling import lang_name, LLMCache
from util.openai_client import build_client, call_openai


# ===========================================================================
# RUBRIC  -- customise this.
# Each entry is (name, description). Listed most-important-first; the judge is
# told to weigh earlier criteria more heavily. Replace/extend freely, or pass
# --rubric-file to override the whole block with your own text.
# ===========================================================================
DEFAULT_RUBRIC = [
    ("Accuracy / adequacy",
     "Faithfully conveys the full meaning of the source. No mistranslation, "
     "no hallucinated/added content, no omissions."),
    ("Fluency / naturalness",
     "Reads naturally and grammatically in the target language, as if written "
     "by an educated native speaker."),
    ("Terminology & named entities",
     "Correct, consistent, domain-appropriate terms; names, numbers and codes "
     "rendered correctly."),
    ("Style & register",
     "Matches the tone, formality and style of the source (e.g. casual vs "
     "formal, marketing vs technical)."),
    ("Locale & formatting",
     "Correct script, punctuation, and number/date conventions for the target "
     "locale."),
]


def render_rubric(rubric) -> str:
    """Turn the (name, description) list into a numbered prompt block."""
    return "\n".join(f"{i}. {name}: {desc}"
                     for i, (name, desc) in enumerate(rubric, 1))


# ===========================================================================
# Prompt assembly
# ===========================================================================
JUDGE_SYSTEM = (
    "You are an expert, impartial bilingual translation evaluator. You compare "
    "two candidate translations of the same source and decide which is better. "
    "Judge strictly on quality; ignore which candidate is labelled A or B and "
    "ignore their order or length."
)

JUDGE_TEMPLATE = (
    "Compare two candidate translations and decide which is better.\n\n"
    "Source language: {src_lang}\n"
    "Target language: {tgt_lang}\n\n"
    "Judge against this rubric (earlier criteria matter more):\n{rubric}\n\n"
    "=== SOURCE ===\n{source}\n\n"
    "=== TRANSLATION A ===\n{trans_a}\n\n"
    "=== TRANSLATION B ===\n{trans_b}\n\n"
    "Briefly reason which is better and why, then end with a single JSON object "
    "on the last line and nothing after it:\n"
    '{{"winner": "A" | "B" | "tie", "reason": "<short justification>"}}'
)


def build_judge_messages(source, trans_a, trans_b, src_lang, tgt_lang,
                         rubric_text):
    """Assemble the [system, user] messages for one A-vs-B comparison."""
    user = JUDGE_TEMPLATE.format(
        src_lang=src_lang, tgt_lang=tgt_lang, rubric=rubric_text,
        source=source, trans_a=trans_a, trans_b=trans_b)
    return [{"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": user}]


_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_verdict(text: str) -> dict:
    """Extract {"winner","reason"} from the model output; winner in {A,B,tie}."""
    m = _JSON_RE.search(text or "")
    if m:
        try:
            obj = json.loads(m.group(0))
            w = str(obj.get("winner", "")).strip().lower()
            winner = {"a": "A", "b": "B", "tie": "tie"}.get(w, "tie")
            return {"winner": winner, "reason": str(obj.get("reason", ""))[:500]}
        except json.JSONDecodeError:
            pass
    return {"winner": "tie", "reason": "<unparseable judge output>"}


# ===========================================================================
# One pairwise judgement (with optional position-bias swap)
# ===========================================================================
def _judge_once(client, model, source, cand_a, cand_b, src_lang, tgt_lang,
                rubric_text, temperature, cache):
    """Judge with a fixed A/B assignment; return parsed verdict dict."""
    messages = build_judge_messages(source, cand_a, cand_b, src_lang, tgt_lang,
                                    rubric_text)
    key = LLMCache.make_key(
        model, temperature,
        "JUDGE\x00" + json.dumps(messages, ensure_ascii=False, sort_keys=True))
    if cache:
        raw = cache.get_or_compute(
            key,
            lambda: call_openai(client, model, messages, temperature=temperature),
        )
    else:
        raw = call_openai(client, model, messages, temperature=temperature)
    v = parse_verdict(raw)
    v["raw"] = raw
    return v


def judge_pair(client, model, source, trans_a, trans_b, src_lang, tgt_lang,
               rubric_text, temperature, cache, swap=True):
    """Compare trans_a vs trans_b; return a normalized verdict.

    With swap=True, judge both orders (A,B) and (B,A) to cancel position bias:
    a side wins only if it wins both orders; disagreement -> tie (inconsistent).
    Returned winner is relative to the ORIGINAL inputs: "A"=trans_a, "B"=trans_b.
    """
    # order 1: A=trans_a, B=trans_b  -> verdict already in original terms
    v1 = _judge_once(client, model, source, trans_a, trans_b,
                     src_lang, tgt_lang, rubric_text, temperature, cache)
    votes = {"order_ab": v1["winner"]}
    reasons = {"order_ab": v1["reason"]}

    if not swap:
        return {"winner": v1["winner"], "consistent": None,
                "votes": votes, "reasons": reasons}

    # order 2: A=trans_b, B=trans_a  -> remap result back to original terms
    v2 = _judge_once(client, model, source, trans_b, trans_a,
                     src_lang, tgt_lang, rubric_text, temperature, cache)
    remap = {"A": "B", "B": "A", "tie": "tie"}  # swapped -> original
    v2_norm = remap[v2["winner"]]
    votes["order_ba"] = v2_norm
    reasons["order_ba"] = v2["reason"]

    if v1["winner"] == v2_norm:
        winner, consistent = v1["winner"], True
    else:
        winner, consistent = "tie", False  # order-dependent -> no clear winner
    return {"winner": winner, "consistent": consistent,
            "votes": votes, "reasons": reasons}


# ===========================================================================
# Data loading
# ===========================================================================
def load_jsonl_by_id(path: Path) -> dict:
    rows = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "doc_id" in d:
                rows[d["doc_id"]] = d
    return rows


def parse_args():
    p = argparse.ArgumentParser(description="Contrastive (pairwise) MT judge")
    p.add_argument("--a", required=True, help="jsonl with candidate A (and source)")
    p.add_argument("--b", default="",
                   help="jsonl with candidate B (default: same file as --a)")
    p.add_argument("--a-field", default="hypothesis", help="translation field in --a")
    p.add_argument("--b-field", default="hypothesis", help="translation field in --b")
    p.add_argument("--source-field", default="source_doc", help="source text field")
    p.add_argument("--out", default="", help="output jsonl (default <a>.judge.jsonl)")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI judge model")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--src-lang", default="English", help="source language name")
    p.add_argument("--tgt-lang", default="",
                   help="target language name (default: inferred from tgt_lang field)")
    p.add_argument("--rubric-file", default="",
                   help="file whose text replaces the default rubric block")
    p.add_argument("--no-swap", action="store_true",
                   help="judge each pair once (faster, but position-biased)")
    p.add_argument("--concurrency", type=int, default=16)
    p.add_argument("--limit", type=int, default=0, help="max pairs (0=all)")
    p.add_argument("--api-key", default="")
    p.add_argument("--cache-path", default="", help="default <out>.cache.jsonl")
    p.add_argument("--no-cache", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()

    a_path = Path(args.a)
    b_path = Path(args.b) if args.b else a_path
    if not a_path.exists():
        sys.exit(f"--a not found: {a_path}")
    if not b_path.exists():
        sys.exit(f"--b not found: {b_path}")
    if a_path == b_path and args.a_field == args.b_field:
        sys.exit("--a-field and --b-field are identical on the same file; "
                 "nothing to compare.")

    rubric_text = (Path(args.rubric_file).read_text(encoding="utf-8").strip()
                   if args.rubric_file else render_rubric(DEFAULT_RUBRIC))

    rows_a = load_jsonl_by_id(a_path)
    rows_b = load_jsonl_by_id(b_path)
    common = [d for d in rows_a if d in rows_b]
    print(f"A={a_path.name}({args.a_field})  B={b_path.name}({args.b_field})  "
          f"common doc_ids={len(common)}  swap={not args.no_swap}  "
          f"model={args.model}")

    out_path = Path(args.out) if args.out else a_path.with_suffix(".judge.jsonl")
    cache_path = (Path(args.cache_path) if args.cache_path
                  else out_path.with_suffix(".cache.jsonl"))
    cache = LLMCache(cache_path, enabled=not args.no_cache)
    if cache.enabled:
        print(f"cache: {cache_path} (loaded {len(cache.mem)} entries)")

    # build the work list of (source, trans_a, trans_b) triples
    work = []
    for doc_id in common:
        ra, rb = rows_a[doc_id], rows_b[doc_id]
        ta, tb = ra.get(args.a_field), rb.get(args.b_field)
        if not ta or not tb:
            continue
        source = ra.get(args.source_field) or rb.get(args.source_field) or ""
        tgt = args.tgt_lang or lang_name(ra.get("tgt_lang") or "")
        work.append({"doc_id": doc_id, "source": source, "trans_a": ta,
                     "trans_b": tb, "tgt_lang": tgt})
        if args.limit and len(work) >= args.limit:
            break
    print(f"to judge: {len(work)} pairs")

    tlocal = threading.local()

    def client_for_thread():
        c = getattr(tlocal, "client", None)
        if c is None:
            c = build_client(args.api_key)
            tlocal.client = c
        return c

    def worker(it):
        verdict = judge_pair(
            client_for_thread(), args.model, it["source"], it["trans_a"],
            it["trans_b"], args.src_lang, it["tgt_lang"], rubric_text,
            args.temperature, cache, swap=not args.no_swap)
        return it, verdict

    counts = {"A": 0, "B": 0, "tie": 0}
    n_inconsistent = n_done = n_fail = 0
    fout = out_path.open("w", encoding="utf-8")
    try:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(worker, it): it for it in work}
            for fut in as_completed(futures):
                it = futures[fut]
                try:
                    _, v = fut.result()
                except Exception as e:  # noqa: BLE001
                    n_fail += 1
                    print(f"  [error] doc_id={it['doc_id']}: {e}", file=sys.stderr)
                    continue
                counts[v["winner"]] += 1
                if v.get("consistent") is False:
                    n_inconsistent += 1
                rec = {"doc_id": it["doc_id"], "winner": v["winner"],
                       "consistent": v["consistent"], "votes": v["votes"],
                       "source_doc": it["source"], "trans_a": it["trans_a"],
                       "trans_b": it["trans_b"], "reasons": v["reasons"]}
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fout.flush()
                n_done += 1
                if n_done % 20 == 0:
                    print(f".. {n_done}/{len(work)} judged")
    finally:
        fout.close()
        cache.close()

    total = max(1, n_done)
    print(f"\nDone. judged {n_done} pairs (failed {n_fail}).")
    print(f"  A ({args.a_field}) wins: {counts['A']} ({100*counts['A']/total:.1f}%)")
    print(f"  B ({args.b_field}) wins: {counts['B']} ({100*counts['B']/total:.1f}%)")
    print(f"  ties:            {counts['tie']} ({100*counts['tie']/total:.1f}%)")
    if not args.no_swap:
        print(f"  order-inconsistent (counted as tie): {n_inconsistent} "
              f"({100*n_inconsistent/total:.1f}%)")
    print(f"output: {out_path.resolve()}")


if __name__ == "__main__":
    main()
