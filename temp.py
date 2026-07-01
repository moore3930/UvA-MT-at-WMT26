#!/usr/bin/env python3
"""temp.py -- backfill the src_lang field into existing result files.

Existing sequential_scaling.py outputs were written before src_lang was saved.
This script recovers it WITHOUT re-running any translation: it builds a
doc_id -> src_lang map from the source dataset (which carries src_lang) and
inserts that field (right after doc_id) into each result record, matched by
doc_id. Records already carrying src_lang are refreshed from the map.

Usage:
  # preview (no writes)
  python temp.py --dry-run
  # apply in place to results/gpt-4o-mini/*.jsonl (default)
  python temp.py --apply
  # specific files / dirs
  python temp.py --apply results/gpt-4o-mini/de_DE.jsonl results/gpt-5.5
"""

import argparse
import json
import os
import sys
from pathlib import Path


def build_src_map(src_path: Path) -> dict:
    m = {}
    with src_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            did = d.get("doc_id")
            if did is not None:
                m[did] = d.get("src_lang", "")
    return m


def with_src_lang(rec: dict, src_lang: str) -> dict:
    """Return rec with src_lang inserted right after doc_id (order preserved)."""
    out = {}
    for k, v in rec.items():
        if k == "src_lang":
            continue  # drop any existing one; we re-insert in the right spot
        out[k] = v
        if k == "doc_id":
            out["src_lang"] = src_lang
    if "doc_id" not in rec:  # no doc_id: just put it up front
        out = {"src_lang": src_lang, **out}
    return out


def process_file(path: Path, src_map: dict, apply: bool) -> dict:
    updated = missing = total = deduped = 0
    seen = set()
    out_lines = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                out_lines.append(line)
                continue
            total += 1
            try:
                rec = json.loads(s)
            except json.JSONDecodeError:
                out_lines.append(line)  # keep malformed lines untouched
                continue
            did = rec.get("doc_id")
            if did is not None and did in seen:
                deduped += 1          # duplicate doc_id -> drop (keep first)
                continue
            if did is not None:
                seen.add(did)
            if did in src_map:
                rec = with_src_lang(rec, src_map[did])
                updated += 1
            else:
                missing += 1
            out_lines.append(json.dumps(rec, ensure_ascii=False) + "\n")

    if apply and (updated or deduped):
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            f.writelines(out_lines)
        os.replace(tmp, path)
    return {"file": str(path), "total": total, "updated": updated,
            "missing": missing, "deduped": deduped}


def collect_files(paths) -> list:
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files.extend(sorted(p.glob("*.jsonl")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"  [warn] not found: {p}", file=sys.stderr)
    return files


def parse_args():
    ap = argparse.ArgumentParser(description="Backfill src_lang into result files")
    ap.add_argument("targets", nargs="*", default=["results/gpt-4o-mini"],
                    help="result files or dirs (default: results/gpt-4o-mini)")
    ap.add_argument("--src",
                    default="wmt26_genmt_blindset_filter_parse.jsonl",
                    help="dataset jsonl that carries src_lang (the doc_id source)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--apply", action="store_true", help="write changes in place")
    g.add_argument("--dry-run", action="store_true",
                   help="only report what would change (default)")
    return ap.parse_args()


def main():
    args = parse_args()
    apply = args.apply  # default (neither / --dry-run) = preview only

    src_path = Path(args.src)
    if not src_path.exists():
        sys.exit(f"src dataset not found: {src_path}")
    src_map = build_src_map(src_path)
    print(f"src map: {len(src_map)} doc_id -> src_lang from {src_path.name}")

    files = collect_files(args.targets)
    if not files:
        sys.exit("no target files found")

    print(f"mode: {'APPLY (in place)' if apply else 'DRY-RUN (no writes)'}\n")
    tot_u = tot_m = tot_d = 0
    for path in files:
        r = process_file(path, src_map, apply)
        tot_u += r["updated"]
        tot_m += r["missing"]
        tot_d += r["deduped"]
        flags = []
        if r["missing"]:
            flags.append(f"{r['missing']} doc_id not in map")
        if r["deduped"]:
            flags.append(f"dropped {r['deduped']} duplicate(s)")
        flag = ("  <-- " + "; ".join(flags)) if flags else ""
        print(f"  {r['file']}: {r['updated']}/{r['total']} set{flag}")

    print(f"\ntotal: updated {tot_u}, missing {tot_m}, deduped {tot_d} "
          f"across {len(files)} file(s)")
    if not apply:
        print("(dry-run; re-run with --apply to write)")


if __name__ == "__main__":
    main()
