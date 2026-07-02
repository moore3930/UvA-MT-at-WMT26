#!/usr/bin/env python3
"""cook_for_submission.py

Assemble a WMT26 GenMT submission file.

  1) Read a blindset jsonl (same structure as wmt26_genmt_blindset.jsonl:
     doc_id, source_doc, tgt_lang, instruction, ...).
  2) Read EVERY *.jsonl under a results folder and build a doc_id -> hypothesis
     map from their `hypothesis` field.
  3) For each blindset sample, append the matching `hypothesis` (by doc_id) and
     write it out, preserving the blindset's order.
  4) Write the result to UvA_submission.jsonl.

Blindset samples with no matching hypothesis get "" (and are counted/warned).

Example:
  python cook_for_submission.py \
      --blindset wmt26_genmt_blindset.jsonl \
      --results-dir results/gpt-4o-mini \
      --out UvA_submission.jsonl
"""

import argparse
import json
import sys
from pathlib import Path


def build_hypothesis_map(results_dir: Path, recursive: bool) -> dict:
    """doc_id -> hypothesis, gathered from every *.jsonl under results_dir.

    Only records that actually carry a `hypothesis` field contribute, so files
    without it (e.g. judge/matrix outputs) are ignored naturally.
    """
    pattern = "**/*.jsonl" if recursive else "*.jsonl"
    files = sorted(results_dir.glob(pattern))
    hypo = {}
    collisions = 0
    for fp in files:
        with fp.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "hypothesis" not in rec:
                    continue
                did = rec.get("doc_id")
                if did is None:
                    continue
                if did in hypo and hypo[did] != rec["hypothesis"]:
                    collisions += 1
                hypo[did] = rec["hypothesis"]
    return hypo, files, collisions


def parse_args():
    ap = argparse.ArgumentParser(description="Cook a WMT26 GenMT submission jsonl")
    ap.add_argument("--blindset", default="wmt26_genmt_blindset.jsonl",
                    help="blindset jsonl (doc_id, source_doc, tgt_lang, ...)")
    ap.add_argument("--results-dir", default="results/gpt-4o-mini",
                    help="folder whose *.jsonl carry doc_id + hypothesis")
    ap.add_argument("--out", default="UvA_submission.jsonl",
                    help="output submission jsonl")
    ap.add_argument("--recursive", action="store_true",
                    help="also read *.jsonl in subfolders of --results-dir")
    ap.add_argument("--field", default="hypothesis",
                    help="name of the appended field in the output "
                         "(default: hypothesis)")
    ap.add_argument("--drop-missing", action="store_true",
                    help="skip blindset samples with no hypothesis instead of "
                         "writing an empty one")
    return ap.parse_args()


def main():
    args = parse_args()

    blind_path = Path(args.blindset)
    results_dir = Path(args.results_dir)
    out_path = Path(args.out)
    if not blind_path.exists():
        sys.exit(f"blindset not found: {blind_path}")
    if not results_dir.is_dir():
        sys.exit(f"results dir not found: {results_dir}")

    hypo, files, collisions = build_hypothesis_map(results_dir, args.recursive)
    print(f"read {len(files)} jsonl file(s) from {results_dir}")
    print(f"hypothesis map: {len(hypo)} doc_id -> hypothesis"
          + (f" ({collisions} conflicting duplicate(s), kept last)"
             if collisions else ""))

    n = matched = missing = written = 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with blind_path.open("r", encoding="utf-8") as fin, \
            out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            n += 1
            rec = json.loads(line)
            did = rec.get("doc_id")
            if did in hypo:
                rec[args.field] = hypo[did]
                matched += 1
            else:
                missing += 1
                if args.drop_missing:
                    continue
                rec[args.field] = ""
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
            written += 1

    print(f"\nblindset samples: {n}")
    print(f"  matched (hypothesis filled): {matched}")
    print(f"  missing (no hypothesis):     {missing}"
          + (" -> dropped" if args.drop_missing else ' -> written with ""'))
    print(f"written {written} lines to {out_path.resolve()}")


if __name__ == "__main__":
    main()
