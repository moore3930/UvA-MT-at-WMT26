#!/usr/bin/env python3
"""Check that submission doc_ids have the same tgt_lang as the blindset."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import iter_jsonl, preview


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUBMISSION = (
    REPO_ROOT
    / "final_submission/out/two-best/gemini-3.5-flash__gpt-final/submission.jsonl"
)
DEFAULT_BLINDSET = REPO_ROOT / "wmt26_genmt_blindset.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "For each doc_id in the submission file, verify that tgt_lang matches "
            "the value in the blindset file."
        )
    )
    parser.add_argument("--submission", type=Path, default=DEFAULT_SUBMISSION)
    parser.add_argument("--blindset", type=Path, default=DEFAULT_BLINDSET)
    parser.add_argument(
        "--show",
        type=int,
        default=20,
        help="number of missing/mismatched examples to print (default: 20)",
    )
    return parser.parse_args()


def load_doc_to_tgt_lang(path: Path) -> tuple[dict[str, str], list[str]]:
    by_doc_id: dict[str, str] = {}
    malformed: list[str] = []

    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        tgt_lang = record.get("tgt_lang")
        if not isinstance(doc_id, str) or not isinstance(tgt_lang, str):
            malformed.append(f"{path}:{line_no}: expected string doc_id and tgt_lang")
            continue
        if doc_id in by_doc_id:
            malformed.append(f"{path}:{line_no}: duplicate doc_id={doc_id}")
            continue
        by_doc_id[doc_id] = tgt_lang

    return by_doc_id, malformed


def main() -> None:
    args = parse_args()
    submission_path = args.submission.resolve()
    blindset_path = args.blindset.resolve()

    for path in (submission_path, blindset_path):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    submission, submission_malformed = load_doc_to_tgt_lang(submission_path)
    blindset, blindset_malformed = load_doc_to_tgt_lang(blindset_path)

    malformed = submission_malformed + blindset_malformed
    if malformed:
        raise SystemExit(f"malformed rows: {preview(malformed, limit=3)}")

    missing_in_blindset: list[str] = []
    mismatches: list[str] = []

    for doc_id, submission_tgt_lang in submission.items():
        blindset_tgt_lang = blindset.get(doc_id)
        if blindset_tgt_lang is None:
            missing_in_blindset.append(doc_id)
            continue
        if submission_tgt_lang != blindset_tgt_lang:
            mismatches.append(
                f"{doc_id}: submission={submission_tgt_lang!r} blindset={blindset_tgt_lang!r}"
            )

    checked = len(submission)
    same = checked - len(missing_in_blindset) - len(mismatches)

    print(f"submission: {submission_path}")
    print(f"blindset:   {blindset_path}")
    print(
        f"CHECK tgt_lang checked={checked} same={same} "
        f"mismatch={len(mismatches)} missing_in_blindset={len(missing_in_blindset)}"
    )

    if missing_in_blindset:
        print(
            f"missing doc_id(s) in blindset ({len(missing_in_blindset)}): "
            f"{preview(missing_in_blindset, limit=args.show)}"
        )
    if mismatches:
        print(
            f"tgt_lang mismatch(es) ({len(mismatches)}): "
            f"{preview(mismatches, limit=args.show)}"
        )

    raise SystemExit(0 if not missing_in_blindset and not mismatches else 1)


if __name__ == "__main__":
    main()
