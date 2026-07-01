#!/usr/bin/env python3
"""
step1-filter.py -- keep only records whose `tgt_lang` is in an allow-list.

Reads a blindset JSONL and a newline-separated list of target-language codes
(tgt_lang_filter.txt), and writes out only the records whose `tgt_lang` appears
in that list.  Filtering is on `tgt_lang` alone (source / src_lang is ignored).

Usage:
    python step1-filter.py
    python step1-filter.py -i IN.jsonl -l tgt_lang_filter.txt -o OUT.jsonl
"""

import argparse
import json
import sys
from collections import Counter

DEFAULT_IN = "wmt26_genmt_blindset.jsonl"
DEFAULT_LIST = "tgt_lang_filter.txt"
DEFAULT_OUT = "wmt26_genmt_blindset_filter.jsonl"


def load_allowlist(path):
    with open(path, encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default=DEFAULT_IN, help=f"input jsonl (default: {DEFAULT_IN})")
    ap.add_argument("-l", "--list", default=DEFAULT_LIST, help=f"tgt_lang allow-list (default: {DEFAULT_LIST})")
    ap.add_argument("-o", "--output", default=DEFAULT_OUT, help=f"output jsonl (default: {DEFAULT_OUT})")
    args = ap.parse_args()

    keep = load_allowlist(args.list)

    seen = kept = 0
    kept_by_tgt = Counter()

    with open(args.input, encoding="utf-8") as fin, \
         open(args.output, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            seen += 1
            rec = json.loads(line)
            if rec.get("tgt_lang") in keep:
                fout.write(line if line.endswith("\n") else line + "\n")
                kept += 1
                kept_by_tgt[rec["tgt_lang"]] += 1

    print(f"read {seen} -> kept {kept} -> {args.output}", file=sys.stderr)
    print(f"  tgt_lang kept ({len(kept_by_tgt)}):", file=sys.stderr)
    for tgt in sorted(kept_by_tgt):
        print(f"    {tgt:14} {kept_by_tgt[tgt]}", file=sys.stderr)
    missing = keep - set(kept_by_tgt)
    if missing:
        print(f"  WARNING: in allow-list but not found in data: {sorted(missing)}", file=sys.stderr)


if __name__ == "__main__":
    main()
