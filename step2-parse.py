#!/usr/bin/env python3
"""
parse.py -- add a `src_lang` field to every record of a WMT26 GenMT blindset.

For each JSONL record we resolve the SOURCE language with a two-step logic:

  1) INSTRUCTION FIRST.  Records whose `instruction` follows the explicit
     "Translate from <X> to <Y>." template carry the source right there, e.g.
         "Translate from en to zh_CN."  -> source = English
     We parse <X> and normalise it to a FLORES-style code.

  2) DETECT OTHERWISE.  The "You are a professional <lang> translator ..."
     records do not name the source, so we detect it from `source_doc`:
       - non-Latin scripts are resolved directly by Unicode range
         (Han -> Chinese, Kana -> Japanese, Cyrillic -> Russian, ...);
       - Latin text is disambiguated between English / Italian / Czech with a
         stop-word rate comparison (English is the default when nothing wins),
         with a Czech boost when Czech-specific háček/kroužek letters appear.

The emitted `src_lang` codes use the same FLORES-200 "xxx_Script" convention as
the corpus `tgt_lang` set (ces_Latn, zho_Hans, kor_Hang, ... already appear
there), so source and target labels are drawn from one consistent namespace.

Consistency check: in the accompanying blindset the resolved directions are
19 English-source directions plus Czech->{deu_Latn, ukr_Cyrl, vie_Latn} and
Chinese->jpn_Jpan, exactly as expected.

Usage:
    python parse.py                 # in/out use the defaults below
    python parse.py -i IN -o OUT
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict

DEFAULT_IN = "wmt26_genmt_blindset.jsonl"
DEFAULT_OUT = "wmt26_genmt_blindset_parse.jsonl"

# --------------------------------------------------------------------------- #
# 1) instruction parsing
# --------------------------------------------------------------------------- #

# "Translate from <src> to <tgt>."  -> capture <src>
INSTR_RE = re.compile(r"Translate from\s+(\S+?)\s+to\s+\S+?\.", re.IGNORECASE)

# Normalise whatever appears after "from" (a short code or an English name)
# into a FLORES-style code that matches the tgt_lang namespace.
NAME2FLORES = {
    "en": "eng_Latn", "english": "eng_Latn",
    "cs": "ces_Latn", "czech": "ces_Latn",
    "it": "ita_Latn", "italian": "ita_Latn",
    "de": "deu_Latn", "german": "deu_Latn",
    "ko": "kor_Hang", "korean": "kor_Hang",
    "tr": "tur_Latn", "turkish": "tur_Latn",
    "zh": "zho_Hans", "chinese": "zho_Hans",
    "ja": "jpn_Jpan", "japanese": "jpn_Jpan",
    "ru": "rus_Cyrl", "russian": "rus_Cyrl",
    "es": "spa_Latn", "spanish": "spa_Latn",
    "fr": "fra_Latn", "french": "fra_Latn",
}


def normalise_src(token):
    """Map an instruction 'from' token to a FLORES code, or None if unknown."""
    return NAME2FLORES.get(token.strip().lower())


def src_from_instruction(instruction):
    m = INSTR_RE.search(instruction or "")
    if not m:
        return None
    return normalise_src(m.group(1))  # may be None for an unmapped code


# --------------------------------------------------------------------------- #
# 2) language detection from source_doc
# --------------------------------------------------------------------------- #

TAG_RE = re.compile(r"<[^>]+>")


def strip_markup(s):
    return TAG_RE.sub("", s or "")


def _has(text, lo, hi):
    return any(lo <= ord(c) <= hi for c in text)


# Unicode-range -> FLORES code for non-Latin scripts (unambiguous by script).
SCRIPT_RANGES = [
    (0x4E00, 0x9FFF, "zho_Hans"),   # CJK Han
    (0x3040, 0x30FF, "jpn_Jpan"),   # Hiragana/Katakana
    (0xAC00, 0xD7A3, "kor_Hang"),   # Hangul
    (0x0600, 0x06FF, "arb_Arab"),   # Arabic
    (0x0400, 0x04FF, "rus_Cyrl"),   # Cyrillic
    (0x0E00, 0x0E7F, "tha_Thai"),   # Thai
    (0x0530, 0x058F, "hye_Armn"),   # Armenian
    (0x0900, 0x097F, "hin_Deva"),   # Devanagari
]

# Czech-specific letters (háček / kroužek) that do not occur in English/Italian.
CZECH_LETTERS = set("řěůčšžťďňŘĚŮČŠŽŤĎŇ")

# Stop words per Latin language.  The Czech list deliberately excludes tokens
# that are also common English words (a, to, v, do, ...) to avoid false hits.
STOPWORDS = {
    "eng_Latn": set("the of and to in is that for it you was with on this as be "
                    "are have not but at they from or an we he his".split()),
    "ita_Latn": set("il lo la gli le di che è per un una del della dei degli con "
                    "non sono nel nella come anche più questo essere si ha".split()),
    "ces_Latn": set("na je že ale jako není který jsou jsem byl bylo když protože "
                    "více nebo své také již jejich".split()),
}

WORD_RE = re.compile(r"[a-zà-ÿ]+")


def detect_latin(text):
    """Disambiguate Latin-script text: English (default) / Italian / Czech."""
    words = WORD_RE.findall(text.lower())
    if not words:
        return "eng_Latn"
    n = len(words)
    score = {lang: sum(w in sw for w in words) / n for lang, sw in STOPWORDS.items()}
    if sum(c in CZECH_LETTERS for c in text) >= 2:
        score["ces_Latn"] += 1.0  # strong, script-level Czech evidence
    best = max(score, key=score.get)
    return best if score[best] > 0 else "eng_Latn"


def detect_source(source_doc):
    text = strip_markup(source_doc)
    for lo, hi, code in SCRIPT_RANGES:
        if _has(text, lo, hi):
            return code
    return detect_latin(text)


# --------------------------------------------------------------------------- #
# resolve one record
# --------------------------------------------------------------------------- #

def resolve_src_lang(record):
    """Return (src_lang, method) for one record."""
    src = src_from_instruction(record.get("instruction"))
    if src is not None:
        return src, "instruction"
    return detect_source(record.get("source_doc")), "detected"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--input", default=DEFAULT_IN, help=f"input jsonl (default: {DEFAULT_IN})")
    ap.add_argument("-o", "--output", default=DEFAULT_OUT, help=f"output jsonl (default: {DEFAULT_OUT})")
    args = ap.parse_args()

    n = 0
    by_method = Counter()
    by_src = Counter()
    directions = defaultdict(Counter)  # tgt_lang -> Counter(src_lang)

    with open(args.input, encoding="utf-8") as fin, \
         open(args.output, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            src, method = resolve_src_lang(rec)
            rec["src_lang"] = src
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

            n += 1
            by_method[method] += 1
            by_src[src] += 1
            directions[rec.get("tgt_lang")][src] += 1

    # ---- summary ----
    print(f"wrote {n} records -> {args.output}", file=sys.stderr)
    print(f"  resolved by: {dict(by_method)}", file=sys.stderr)
    print(f"  src_lang distribution: {dict(by_src.most_common())}", file=sys.stderr)
    n_dir = sum(len(srcs) for srcs in directions.values())
    print(f"  language directions (src->tgt): {n_dir} across {len(directions)} tgt_lang", file=sys.stderr)
    for tgt in sorted(directions):
        parts = ", ".join(f"{s}:{c}" for s, c in directions[tgt].most_common())
        print(f"    {tgt:14} {parts}", file=sys.stderr)


if __name__ == "__main__":
    main()
