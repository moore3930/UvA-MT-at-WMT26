#!/usr/bin/env python3
"""Filter WMT26 blindset JSONL down to the required official directions.

This utility keeps only the target-language codes that correspond to the
official WMT26 directions discussed in the project notes. The blindset mixes
those official directions with extra test-suite-only directions; this script
removes the extras and writes a new JSONL.

Usage:
    python3 filter_required_directions.py
    python3 filter_required_directions.py \
        --input wmt26_genmt_blindset.jsonl \
        --output wmt26_genmt_required_only.jsonl
"""

import argparse
import json
from collections import Counter
from pathlib import Path


# Raw tgt_lang codes present in wmt26_genmt_blindset.jsonl that map to the
# official directions we want to keep.
REQUIRED_TGT_LANGS = {
    "arz",
    "arz_Arab",
    "bel_Cyrl",
    "ces_Latn",
    "cs",
    "cs_CZ",
    "de_DE",
    "deu_Latn",
    "ekk_Latn",
    "et_EE",
    "hye_Armn",
    "ind_Latn",
    "is",
    "isl_Latn",
    "jpn_Jpan",
    "kaz_Cyrl",
    "ko_KR",
    "kor_Hang",
    "lij_Latn",
    "lld_Latn",
    "ru",
    "ru_RU",
    "rus_Cyrl",
    "sme_Latn",
    "tha_Thai",
    "ukr_Cyrl",
    "vie_Latn",
    "zh_CN",
    "zho_Hans",
    "zho_Hant_TW",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Keep only the required official directions from a blindset JSONL."
    )
    parser.add_argument(
        "--input",
        default="wmt26_genmt_blindset.jsonl",
        help="Input JSONL path (default: wmt26_genmt_blindset.jsonl).",
    )
    parser.add_argument(
        "--output",
        default="wmt26_genmt_required_only.jsonl",
        help="Output JSONL path (default: wmt26_genmt_required_only.jsonl).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    kept_counts = Counter()
    dropped_counts = Counter()
    kept_lines = 0
    dropped_lines = 0

    with input_path.open("r", encoding="utf-8") as fin, output_path.open(
        "w", encoding="utf-8"
    ) as fout:
        for line_no, line in enumerate(fin, 1):
            line = line.rstrip("\n")
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_no}: {exc}") from exc

            tgt_lang = obj.get("tgt_lang")
            if tgt_lang in REQUIRED_TGT_LANGS:
                fout.write(line + "\n")
                kept_counts[tgt_lang] += 1
                kept_lines += 1
            else:
                dropped_counts[tgt_lang] += 1
                dropped_lines += 1

    print(f"input:   {input_path}")
    print(f"output:  {output_path}")
    print(f"kept:    {kept_lines}")
    print(f"dropped: {dropped_lines}")
    print("kept tgt_lang counts:")
    for lang in sorted(kept_counts):
        print(f"  {lang}: {kept_counts[lang]}")

    if dropped_counts:
        print("dropped tgt_lang counts:")
        for lang in sorted(dropped_counts):
            print(f"  {lang}: {dropped_counts[lang]}")


if __name__ == "__main__":
    main()
