#!/usr/bin/env python3
"""Verify merged submission rows exactly match two-best final hypotheses."""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def load_jsonl(path: Path) -> List[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    return rows


def build_submission_index(rows: List[dict], path: Path) -> Dict[Tuple[str, str], dict]:
    index = {}
    for i, row in enumerate(rows, start=1):
        key = (row.get("doc_id"), row.get("tgt_lang"))
        if not all(isinstance(part, str) for part in key):
            raise SystemExit(f"{path}:{i}: expected string doc_id and tgt_lang")
        if key in index:
            raise SystemExit(f"{path}:{i}: duplicate submission key {key}")
        index[key] = row
    return index


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check that each final two-best hypothesis selected for the cached "
            "languages is present verbatim in a merged submission."
        )
    )
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--two-best-prelim", type=Path, required=True)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument(
        "--print-limit",
        type=int,
        default=0,
        help="print at most this many matching rows; 0 means print none",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    suffix = "-winner-cross.cache.jsonl"
    cache_langs = set()
    for path in args.cache_dir.glob("*-winner-cross.cache.jsonl"):
        name = path.name
        if not name.endswith(suffix):
            continue
        cache_langs.add(name[: -len(suffix)])
    if not cache_langs:
        raise SystemExit(f"no cache files found in {args.cache_dir}")

    prelim_rows = load_jsonl(args.two_best_prelim)
    submission_rows = load_jsonl(args.submission)
    submission_index = build_submission_index(submission_rows, args.submission)

    matches = []
    mismatches = []
    missing_langs = sorted(cache_langs.difference({row.get("tgt_lang") for row in prelim_rows}))

    for row_no, row in enumerate(prelim_rows, start=1):
        doc_id = row.get("doc_id")
        tgt_lang = row.get("tgt_lang")
        expected = row.get("two_best_final_hypothesis")

        if tgt_lang not in cache_langs:
            continue
        if not isinstance(doc_id, str) or not isinstance(tgt_lang, str):
            mismatches.append(
                f"{args.two_best_prelim}:{row_no}: invalid doc_id/tgt_lang types"
            )
            continue
        if not isinstance(expected, str):
            mismatches.append(
                f"{args.two_best_prelim}:{row_no}: missing two_best_final_hypothesis for "
                f"{doc_id} {tgt_lang}"
            )
            continue

        key = (doc_id, tgt_lang)
        submission_row = submission_index.get(key)
        if submission_row is None:
            mismatches.append(f"MISSING submission row for {doc_id} {tgt_lang}")
            continue

        actual = submission_row.get("hypothesis")
        if actual != expected:
            mismatches.append(
                f"TEXT MISMATCH for {doc_id} {tgt_lang}: "
                f"expected_len={len(expected)} actual_len={len(actual) if isinstance(actual, str) else 'non-string'}"
            )
            continue

        matches.append((doc_id, tgt_lang, expected))

    print(
        f"cache_langs={len(cache_langs)} "
        f"prelim_rows={len(prelim_rows)} "
        f"submission_rows={len(submission_rows)} "
        f"checked_matches={len(matches)} "
        f"mismatches={len(mismatches)}"
    )

    if missing_langs:
        print("LANGS MISSING FROM TWO-BEST PRELIM:")
        for lang in missing_langs:
            print(f"  {lang}")

    if args.print_limit > 0:
        print("MATCHES:")
        for doc_id, tgt_lang, text in matches[: args.print_limit]:
            print(
                json.dumps(
                    {"doc_id": doc_id, "tgt_lang": tgt_lang, "hypothesis": text},
                    ensure_ascii=False,
                )
            )

    if mismatches:
        print("MISMATCHES:")
        for item in mismatches:
            print(item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
