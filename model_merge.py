#!/usr/bin/env python3
"""Merge result directories by doc_id, concatenating hypothesis fields."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
RESULTS_ROOT = REPO_ROOT / "results"
MERGED_ROOT = RESULTS_ROOT / "merged"
ALIGNMENT_CHECK = REPO_ROOT / ".final_checks" / "check_results_set_alignment.py"
_HYPO_RE = re.compile(r"^hypo_(\d+)$")


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Merge one or more results directories by doc_id, keeping shared "
            "metadata and concatenating hypo_* fields."
        )
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="input result dirs like results/gemini-3.5-flash results/gpt-final",
    )
    parser.add_argument(
        "--name",
        default="",
        help=(
            "output subdir name under results/merged/ "
            "(default: joined input dir basenames)"
        ),
    )
    parser.add_argument(
        "--out-dir",
        default="",
        help="explicit output directory (overrides --name)",
    )
    parser.add_argument(
        "--skip-set-check",
        action="store_true",
        help="skip running .final_checks/check_results_set_alignment.py first",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and summarize without writing merged JSONL files",
    )
    return parser.parse_args()


def resolve_dir(path_str):
    path = Path(path_str)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def iter_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit("%s:%d: invalid JSON: %s" % (path, line_no, exc))


def load_jsonl(path):
    return [record for _, record in iter_jsonl(path)]


def top_level_jsonl_files(results_dir):
    return sorted(
        path.name
        for path in results_dir.glob("*.jsonl")
        if path.is_file() and not path.name.startswith(".")
    )


def run_set_alignment_check(results_dir):
    cmd = [sys.executable, str(ALIGNMENT_CHECK), str(results_dir)]
    print("set-check:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def canonical_output_name(input_dirs):
    return "__".join(path.name for path in input_dirs)


def extract_hypo_keys(record):
    idx = sorted(
        int(match.group(1))
        for key in record
        for match in [_HYPO_RE.match(key)]
        if match
    )
    expected = list(range(len(idx)))
    if idx != expected:
        raise SystemExit(
            "Non-contiguous hypo fields for doc_id %s: found %s, expected %s"
            % (record.get("doc_id"), idx, expected)
        )
    return ["hypo_%d" % i for i in idx]


def comparable_fields(record):
    return [
        key
        for key in record
        if not _HYPO_RE.match(key) and key not in ("hypothesis", "merge_meta")
    ]


def ensure_same_language_files(input_dirs):
    expected = top_level_jsonl_files(input_dirs[0])
    for results_dir in input_dirs[1:]:
        actual = top_level_jsonl_files(results_dir)
        if actual != expected:
            raise SystemExit(
                "Top-level language files differ for %s\nexpected: %s\nactual:   %s"
                % (results_dir, expected, actual)
            )
    return expected


def ensure_same_doc_id_sets(lang_filename, rows_by_dir):
    reference_dir = next(iter(rows_by_dir))
    reference_ids = set(row["doc_id"] for row in rows_by_dir[reference_dir])
    for results_dir, rows in rows_by_dir.items():
        actual_ids = set(row["doc_id"] for row in rows)
        if actual_ids != reference_ids:
            missing = sorted(reference_ids - actual_ids)
            extra = sorted(actual_ids - reference_ids)
            raise SystemExit(
                "%s in %s is not doc_id-aligned with %s\nmissing: %s\nextra: %s"
                % (
                    lang_filename,
                    results_dir,
                    reference_dir,
                    missing[:5],
                    extra[:5],
                )
            )


def merged_origin(model_name, row, old_hypo_key):
    merge_meta = row.get("merge_meta")
    if isinstance(merge_meta, dict) and old_hypo_key in merge_meta:
        return merge_meta[old_hypo_key]
    return [model_name, old_hypo_key]


def merge_language(lang_filename, input_dirs):
    rows_by_dir = {}
    for results_dir in input_dirs:
        rows_by_dir[results_dir] = load_jsonl(results_dir / lang_filename)

    ensure_same_doc_id_sets(lang_filename, rows_by_dir)

    base_dir = input_dirs[0]
    base_rows = rows_by_dir[base_dir]
    by_dir_and_id = {
        results_dir: {row["doc_id"]: row for row in rows}
        for results_dir, rows in rows_by_dir.items()
    }

    merged_rows = []
    total_hypos = 0

    for base_row in base_rows:
        doc_id = base_row["doc_id"]
        merged_row = {}

        base_fields = comparable_fields(base_row)
        base_field_set = set(base_fields)
        for results_dir in input_dirs[1:]:
            other_row = by_dir_and_id[results_dir][doc_id]
            other_fields = comparable_fields(other_row)
            if set(other_fields) != base_field_set:
                raise SystemExit(
                    "Non-hypothesis fields differ for doc_id %s between %s and %s\n"
                    "base:  %s\nother: %s"
                    % (doc_id, base_dir, results_dir, base_fields, other_fields)
                )
            for field in base_fields:
                if other_row[field] != base_row[field]:
                    raise SystemExit(
                        "Field mismatch for doc_id %s field %s between %s and %s"
                        % (doc_id, field, base_dir, results_dir)
                    )

        for field in base_fields:
            merged_row[field] = base_row[field]

        next_hypo_idx = 0
        merge_meta = {}
        for results_dir in input_dirs:
            row = by_dir_and_id[results_dir][doc_id]
            model_name = results_dir.name
            hypo_keys = extract_hypo_keys(row)
            for old_hypo_key in hypo_keys:
                new_hypo_key = "hypo_%d" % next_hypo_idx
                merged_row[new_hypo_key] = row[old_hypo_key]
                merge_meta[new_hypo_key] = merged_origin(
                    model_name=model_name,
                    row=row,
                    old_hypo_key=old_hypo_key,
                )
                next_hypo_idx += 1

        if next_hypo_idx == 0:
            raise SystemExit("No hypo_* fields found for doc_id %s" % doc_id)

        merged_row["hypothesis"] = merged_row["hypo_%d" % (next_hypo_idx - 1)]
        merged_row["merge_meta"] = merge_meta
        merged_rows.append(merged_row)
        total_hypos += next_hypo_idx

    return merged_rows, total_hypos


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")


def main():
    args = parse_args()
    input_dirs = [resolve_dir(path_str) for path_str in args.inputs]

    if len(input_dirs) < 2:
        raise SystemExit("Need at least two input result directories")
    for results_dir in input_dirs:
        if not results_dir.is_dir():
            raise SystemExit("Missing input directory: %s" % results_dir)
    if len(set(input_dirs)) != len(input_dirs):
        raise SystemExit("Duplicate input directories are not allowed")
    if not ALIGNMENT_CHECK.is_file():
        raise SystemExit("Missing alignment checker: %s" % ALIGNMENT_CHECK)

    if args.out_dir:
        output_dir = resolve_dir(args.out_dir)
    else:
        merge_name = args.name or canonical_output_name(input_dirs)
        output_dir = (MERGED_ROOT / merge_name).resolve()

    if output_dir.exists() and not output_dir.is_dir():
        raise SystemExit("Output path exists and is not a directory: %s" % output_dir)

    if not args.skip_set_check:
        for results_dir in input_dirs:
            run_set_alignment_check(results_dir)

    lang_filenames = ensure_same_language_files(input_dirs)

    total_docs = 0
    total_hypos = 0

    print("inputs:")
    for results_dir in input_dirs:
        print("  - %s" % results_dir)
    print("output: %s" % output_dir)
    if args.dry_run:
        print("mode: dry-run")

    for lang_filename in lang_filenames:
        merged_rows, lang_hypo_total = merge_language(lang_filename, input_dirs)
        total_docs += len(merged_rows)
        total_hypos += lang_hypo_total
        if not args.dry_run:
            write_jsonl(output_dir / lang_filename, merged_rows)
        avg_hypos = (
            float(lang_hypo_total) / float(len(merged_rows))
            if merged_rows else 0.0
        )
        print(
            "%s: docs=%d total_hypos=%d avg_hypos_per_doc=%.2f"
            % (lang_filename, len(merged_rows), lang_hypo_total, avg_hypos)
        )

    avg_hypos = float(total_hypos) / float(total_docs) if total_docs else 0.0
    print(
        "TOTAL: files=%d docs=%d total_hypos=%d avg_hypos_per_doc=%.2f"
        % (len(lang_filenames), total_docs, total_hypos, avg_hypos)
    )
    if args.dry_run:
        print("Dry run complete; no files written.")


if __name__ == "__main__":
    main()
