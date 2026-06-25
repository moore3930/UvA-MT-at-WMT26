#!/usr/bin/env python3
"""Extract a dev set from the WMT25 human-eval data.

For every en-zh and en-ru sample in wmt25-genmt-humeval.jsonl we keep:
  - doc_id
  - tgt_lang        (derived from doc_id, e.g. "zh_CN", "ru_RU")
  - source_doc      (the source text, i.e. src_text)
  - hypo_0..hypo_7  8 translations from 8 randomly picked systems
  - score_0..score_7
                    the mean human-eval score of the system behind hypo_i
                    (a system may be scored by several annotators -> mean)

Output structure mirrors results_gpt54_k8_100/en-zh_CN.jsonl, with the
extra score_i fields holding the averaged scores.

The human win/loss matrix is NOT written here: coherency_eval.py rebuilds it
on the fly from these raw score_i (at any threshold), so persisting it would
just be a redundant artifact.

This script lives in dev/; paths are resolved relative to its location, so it
can be run from anywhere:
    python3 dev/extract_dev.py
"""

import json
import os
import random
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent          # .../wmt26/dev
REPO_ROOT = SCRIPT_DIR.parent                         # .../wmt26
SRC_FILE = REPO_ROOT / "wmt25-genmt-humeval.jsonl"    # input lives at repo root
OUT_DIR = SCRIPT_DIR                                   # outputs go into dev/
N_HYPO = 8
SEED = 42

# language-pair prefix in doc_id  ->  dev filename
PAIRS = {
    "en-zh": "en-zh.jsonl",
    "en-ru": "en-ru.jsonl",
}


def tgt_lang_from_doc_id(doc_id):
    """'en-zh_CN_#_...'  ->  'zh_CN'."""
    lp = doc_id.split("_#_", 1)[0]      # 'en-zh_CN'
    return lp.split("-", 1)[1]          # 'zh_CN'


def mean_score(entries):
    """Average the 'score' field over all annotation entries for a system."""
    scores = [e["score"] for e in entries if e.get("score") is not None]
    if not scores:
        return None
    return sum(scores) / len(scores)


def build_record(d, rng):
    # systems that have BOTH a translation and at least one score (drop refA reference)
    eligible = sorted((set(d["tgt_text"]) & set(d["scores"])) - {"refA"})
    k = min(N_HYPO, len(eligible))
    chosen = rng.sample(eligible, k)

    rec = {
        "doc_id": d["doc_id"],
        "tgt_lang": tgt_lang_from_doc_id(d["doc_id"]),
        "source_doc": d["src_text"],
    }
    for i, sys_name in enumerate(chosen):
        rec[f"hypo_{i}"] = d["tgt_text"][sys_name]
        rec[f"score_{i}"] = mean_score(d["scores"][sys_name])
    return rec


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = random.Random(SEED)

    writers = {p: open(os.path.join(OUT_DIR, fn), "w", encoding="utf-8")
               for p, fn in PAIRS.items()}
    counts = {p: 0 for p in PAIRS}

    try:
        with open(SRC_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                doc_id = d["doc_id"]
                for prefix in PAIRS:
                    if doc_id.startswith(prefix):
                        rec = build_record(d, rng)
                        writers[prefix].write(
                            json.dumps(rec, ensure_ascii=False) + "\n")
                        counts[prefix] += 1
                        break
    finally:
        for w in writers.values():
            w.close()

    for p, fn in PAIRS.items():
        print(f"{os.path.join(OUT_DIR, fn)}: {counts[p]} samples")


if __name__ == "__main__":
    main()
