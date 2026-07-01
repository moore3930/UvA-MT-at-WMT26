#!/usr/bin/env python3
"""
filter.py -- keep only the WMT26 evaluation records, filtering by `tgt_lang`.

The 23 official directions listed below collapse to 20 unique target languages.
A record is kept iff its `tgt_lang` is one of those 20 FLORES codes (source /
src_lang is NOT used for filtering, per request).

    Czech    -> German                        deu_Latn
    Czech    -> Ukrainian                      ukr_Cyrl
    Czech    -> Vietnamese                     vie_Latn
    Chinese, Simplified -> Japanese           jpn_Jpan
    English  -> Arabic, Egyptian               arz_Arab
    English  -> Eastern Armenian               hye_Armn
    English  -> Belarusian                     bel_Cyrl
    English  -> Chinese, Simplified            zho_Hans
    English  -> Chinese, Traditional Taiwan    zho_Hant_TW
    English  -> Czech                          ces_Latn
    English  -> Estonian                       ekk_Latn
    English  -> German                         deu_Latn
    English  -> Icelandic                      isl_Latn
    English  -> Indonesian                     ind_Latn
    English  -> Japanese                       jpn_Jpan
    English  -> Kazakh                         kaz_Cyrl
    English  -> Korean                         kor_Hang
    English  -> Ladin (Val Badia), Italy       lld_Latn
    English  -> Ligurian, Italy                lij_Latn
    English  -> Northern Sami                  sme_Latn
    English  -> Russian                        rus_Cyrl
    English  -> Thai                           tha_Thai
    English  -> Ukrainian                      ukr_Cyrl

Usage:
    python filter.py                 # in/out use the defaults below
    python filter.py -i IN -o OUT
"""

import argparse
import json
import sys
from collections import Counter

DEFAULT_IN = "wmt26_genmt_blindset_parse.jsonl"
DEFAULT_OUT = "wmt26_genmt_blindset_filter.jsonl"

# 20 unique target languages of the 23 evaluation directions.
TARGET_LANGS = {
    "deu_Latn", "ukr_Cyrl", "vie_Latn", "jpn_Jpan", "arz_Arab", "hye_Armn",
    "bel_Cyrl", "zho_Hans", "zho_Hant_TW", "ces_Latn", "ekk_Latn", "isl_Latn",
    "ind_Latn", "kaz_Cyrl", "kor_Hang", "lld_Latn", "lij_Latn", "sme_Latn",
    "rus_Cyrl", "tha_Thai",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default=DEFAULT_IN, help=f"input jsonl (default: {DEFAULT_IN})")
    ap.add_argument("-o", "--output", default=DEFAULT_OUT, help=f"output jsonl (default: {DEFAULT_OUT})")
    args = ap.parse_args()

    seen = kept = 0
    kept_by_tgt = Counter()
    dropped_by_tgt = Counter()

    with open(args.input, encoding="utf-8") as fin, \
         open(args.output, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            seen += 1
            rec = json.loads(line)
            tgt = rec.get("tgt_lang")
            if tgt in TARGET_LANGS:
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                kept += 1
                kept_by_tgt[tgt] += 1
            else:
                dropped_by_tgt[tgt] += 1

    print(f"read {seen} -> kept {kept} -> {args.output}", file=sys.stderr)
    print(f"  kept tgt_lang ({len(kept_by_tgt)}):", file=sys.stderr)
    for tgt in sorted(kept_by_tgt):
        print(f"    {tgt:14} {kept_by_tgt[tgt]}", file=sys.stderr)
    missing = TARGET_LANGS - set(kept_by_tgt)
    if missing:
        print(f"  WARNING: expected but absent: {sorted(missing)}", file=sys.stderr)
    print(f"  dropped tgt_lang: {dict(dropped_by_tgt.most_common())}", file=sys.stderr)


if __name__ == "__main__":
    main()
