#!/usr/bin/env python3
"""Report best-hypothesis percentages for merged judged results."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Read merged judged JSONL and report how often each merged hypo key "
            "wins, mapped back to (model_name, original_hypo_id) via merge_meta."
        )
    )
    parser.add_argument(
        "input",
        help=(
            "Merged judged JSONL file or directory of JSONL files, e.g. "
            "results/gemini-2.5-flash/judged/merged/gemini-3.5-flash__gpt-final"
        ),
    )
    parser.add_argument(
        "--per-file",
        action="store_true",
        help="also print a separate summary for each JSONL file",
    )
    parser.add_argument(
        "--sort-by",
        choices=("hypo", "pct", "count", "model"),
        default="hypo",
        help="row sort order for printed summaries",
    )
    return parser.parse_args()


def resolve_path(path_str: str) -> Path:
    path = Path(path_str)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path.resolve()


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}")


def input_files(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix != ".jsonl":
            raise SystemExit(f"Expected a .jsonl file, got: {path}")
        return [path]
    if path.is_dir():
        files = sorted(
            child for child in path.glob("*.jsonl") if child.is_file() and not child.name.startswith(".")
        )
        if not files:
            raise SystemExit(f"No top-level .jsonl files found in {path}")
        return files
    raise SystemExit(f"Missing input path: {path}")


def hypo_sort_key(hypo_key: str):
    try:
        return int(hypo_key.split("_", 1)[1])
    except Exception:
        return hypo_key


class Summary:
    def __init__(self):
        self.total_docs = 0
        self.best_counts = Counter()
        self.model_best_counts = Counter()
        self.mapping_doc_counts = Counter()
        self.mapping_winrate_sums = defaultdict(float)

    def add_record(self, record: dict, source_name: str):
        merge_meta = record.get("merge_meta")
        best_key = record.get("judge_best_hypo_key")
        win_rates = record.get("judge_win_rates")

        if not isinstance(merge_meta, dict):
            raise SystemExit(f"{source_name}: missing or invalid merge_meta for doc_id={record.get('doc_id')}")
        if not isinstance(best_key, str):
            raise SystemExit(
                f"{source_name}: missing or invalid judge_best_hypo_key for doc_id={record.get('doc_id')}"
            )
        if not isinstance(win_rates, list):
            raise SystemExit(f"{source_name}: missing or invalid judge_win_rates for doc_id={record.get('doc_id')}")

        self.total_docs += 1

        for hypo_key, origin in merge_meta.items():
            if not (isinstance(origin, list) and len(origin) == 2):
                raise SystemExit(
                    f"{source_name}: invalid merge_meta[{hypo_key}] for doc_id={record.get('doc_id')}: {origin!r}"
                )
            model_name, original_hypo_key = origin
            idx = hypo_sort_key(hypo_key)
            if not isinstance(idx, int):
                raise SystemExit(
                    f"{source_name}: unsupported hypo key {hypo_key!r} for doc_id={record.get('doc_id')}"
                )
            if idx >= len(win_rates):
                raise SystemExit(
                    f"{source_name}: judge_win_rates too short for {hypo_key} in doc_id={record.get('doc_id')}"
                )
            mapping_key = (hypo_key, str(model_name), str(original_hypo_key))
            self.mapping_doc_counts[mapping_key] += 1
            self.mapping_winrate_sums[mapping_key] += float(win_rates[idx])

        if best_key not in merge_meta:
            raise SystemExit(
                f"{source_name}: judge_best_hypo_key={best_key} missing from merge_meta for doc_id={record.get('doc_id')}"
            )

        best_origin = merge_meta[best_key]
        self.best_counts[(best_key, str(best_origin[0]), str(best_origin[1]))] += 1
        self.model_best_counts[str(best_origin[0])] += 1

    def rows(self):
        rows = []
        for mapping_key, seen_docs in self.mapping_doc_counts.items():
            best_count = self.best_counts.get(mapping_key, 0)
            avg_win_rate = self.mapping_winrate_sums[mapping_key] / seen_docs if seen_docs else 0.0
            rows.append(
                {
                    "hypo_key": mapping_key[0],
                    "model_name": mapping_key[1],
                    "original_hypo_key": mapping_key[2],
                    "docs_seen": seen_docs,
                    "best_count": best_count,
                    "best_pct": 100.0 * best_count / seen_docs if seen_docs else 0.0,
                    "avg_win_rate_pct": 100.0 * avg_win_rate,
                }
            )
        return rows


def sort_rows(rows: list[dict], sort_by: str) -> list[dict]:
    if sort_by == "pct":
        key_fn = lambda row: (-row["best_pct"], -row["best_count"], hypo_sort_key(row["hypo_key"]))
    elif sort_by == "count":
        key_fn = lambda row: (-row["best_count"], -row["best_pct"], hypo_sort_key(row["hypo_key"]))
    elif sort_by == "model":
        key_fn = lambda row: (row["model_name"], row["original_hypo_key"], hypo_sort_key(row["hypo_key"]))
    else:
        key_fn = lambda row: hypo_sort_key(row["hypo_key"])
    return sorted(rows, key=key_fn)


def print_summary(title: str, summary: Summary, sort_by: str):
    print(title)
    print(f"docs: {summary.total_docs}")
    print("hypo_key\tmodel\toriginal_hypo\tbest_count\tbest_pct\tavg_win_rate_pct")
    for row in sort_rows(summary.rows(), sort_by):
        print(
            f"{row['hypo_key']}\t{row['model_name']}\t{row['original_hypo_key']}\t"
            f"{row['best_count']}\t{row['best_pct']:.2f}\t{row['avg_win_rate_pct']:.2f}"
        )

    if summary.model_best_counts:
        print("model_totals")
        print("model\tbest_count\tbest_pct")
        for model_name, best_count in sorted(
            summary.model_best_counts.items(),
            key=lambda item: (-item[1], item[0]),
        ):
            best_pct = 100.0 * best_count / summary.total_docs if summary.total_docs else 0.0
            print(f"{model_name}\t{best_count}\t{best_pct:.2f}")
    print()


def main():
    args = parse_args()
    path = resolve_path(args.input)
    files = input_files(path)

    overall = Summary()

    for file_path in files:
        file_summary = Summary()
        for record in iter_jsonl(file_path):
            file_summary.add_record(record, str(file_path))
            overall.add_record(record, str(file_path))
        if args.per_file:
            print_summary(f"[{file_path.name}]", file_summary, args.sort_by)

    if len(files) > 1:
        print_summary("[overall]", overall, args.sort_by)
    elif not args.per_file:
        print_summary(f"[{files[0].name}]", overall, args.sort_by)


if __name__ == "__main__":
    main()
