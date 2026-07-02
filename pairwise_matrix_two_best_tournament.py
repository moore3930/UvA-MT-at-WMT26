#!/usr/bin/env python3
"""Judge only the cross-model winner-vs-opposite-pool pairs needed for merge."""

from __future__ import annotations

import argparse
import json
import re
import sys
import threading
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any

from sequential_scaling import LLMCache, lang_name
from util.openai_client import build_client
from util.contrastive_judge import (
    DEFAULT_RUBRIC,
    instruction_for_record,
    judge_pair,
    render_rubric,
    src_lang_for_record,
)


_HYPO_RE = re.compile(r"^hypo_(\d+)$")


class _Tee:
    """Write to several streams at once (console + log file)."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)

    def flush(self):
        for st in self.streams:
            st.flush()


def extract_hypos(rec: dict[str, Any]) -> list[str]:
    idx = sorted(int(m.group(1)) for k in rec for m in [_HYPO_RE.match(k)] if m)
    return [rec[f"hypo_{i}"] for i in idx]


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc


def load_rows(path: Path, limit: int = 0) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    ordered: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        if not isinstance(doc_id, str):
            raise SystemExit(f"{path}:{line_no}: expected string doc_id")
        if doc_id in by_id:
            raise SystemExit(f"{path}:{line_no}: duplicate doc_id={doc_id}")
        ordered.append(record)
        by_id[doc_id] = record
        if limit and len(ordered) >= limit:
            break
    return ordered, by_id


def load_matrix_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line_no, record in iter_jsonl(path):
        doc_id = record.get("doc_id")
        best = record.get("best")
        hypos = record.get("hypos")
        if not isinstance(doc_id, str):
            raise SystemExit(f"{path}:{line_no}: expected string doc_id")
        if doc_id in rows:
            raise SystemExit(f"{path}:{line_no}: duplicate doc_id={doc_id}")
        if not isinstance(best, int):
            raise SystemExit(f"{path}:{line_no}: missing integer best")
        if not isinstance(hypos, list) or not hypos or any(not isinstance(x, str) for x in hypos):
            raise SystemExit(f"{path}:{line_no}: missing non-empty string hypos list")
        if best < 0 or best >= len(hypos):
            raise SystemExit(f"{path}:{line_no}: best={best} out of range for {len(hypos)} hypos")
        rows[doc_id] = {
            "record": record,
            "best_idx": best,
            "hypos": hypos,
        }
    return rows


def comparable_fields(record: dict[str, Any]) -> list[str]:
    return sorted(
        key for key in record
        if not _HYPO_RE.match(key) and key not in {"hypothesis", "merge_meta"}
    )


def validate_rows_match(
    path_a: Path,
    row_a: dict[str, Any],
    path_b: Path,
    row_b: dict[str, Any],
) -> None:
    fields_a = comparable_fields(row_a)
    fields_b = comparable_fields(row_b)
    if fields_a != fields_b:
        raise SystemExit(
            f"Non-hypothesis fields differ for doc_id={row_a.get('doc_id')} "
            f"between {path_a} and {path_b}: {fields_a} vs {fields_b}"
        )
    for field in fields_a:
        if row_a.get(field) != row_b.get(field):
            raise SystemExit(
                f"Field mismatch for doc_id={row_a.get('doc_id')} field={field} "
                f"between {path_a} and {path_b}"
            )


def parse_args():
    p = argparse.ArgumentParser(
        description=(
            "Judge only the raw best-vs-opposite-pool cross-model pairs needed "
            "to replace a full merged 16x16 run."
        )
    )
    p.add_argument("--model-a-input", required=True, help="results/<model-a>/<lang>.jsonl")
    p.add_argument("--model-b-input", required=True, help="results/<model-b>/<lang>.jsonl")
    p.add_argument("--model-a-matrix", required=True, help="matrix jsonl for model A")
    p.add_argument("--model-b-matrix", required=True, help="matrix jsonl for model B")
    p.add_argument("--model-a-name", required=True, help="label for model A")
    p.add_argument("--model-b-name", required=True, help="label for model B")
    p.add_argument(
        "--tie-winner-default",
        default="model_b",
        help=(
            "winner to select on exact total-score ties: "
            "model_a/model_b/a/b or a model name (default: model_b)"
        ),
    )
    p.add_argument("--out", required=True, help="output jsonl path")
    p.add_argument("--cache-path", default="", help="judge cache jsonl path")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI-compatible judge model")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--src-lang", default="", help="fallback source language name")
    p.add_argument("--tgt-lang", default="", help="optional override target language name")
    p.add_argument("--rubric-file", default="", help="optional rubric override")
    p.add_argument("--concurrency", type=int, default=32)
    p.add_argument("--limit", type=int, default=0, help="max docs (0=all)")
    p.add_argument("--api-key", default="")
    p.add_argument("--reasoning-effort", default="", help="optional reasoning effort")
    p.add_argument(
        "--with-instruction",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="inject each record's task-specific instruction into the judge prompt",
    )
    p.add_argument(
        "--json-only",
        action="store_true",
        help="request only the JSON winner verdict with no free-form reason",
    )
    p.add_argument(
        "--structured-output-winner-only",
        action="store_true",
        help=(
            "request schema-constrained JSON output with only "
            '{"winner": "A" | "B" | "tie"}'
        ),
    )
    p.add_argument(
        "--request-timeout",
        type=float,
        default=180.0,
        help="per-request timeout in seconds for judge API calls",
    )
    p.add_argument(
        "--stall-report-seconds",
        type=float,
        default=60.0,
        help="emit a warning if no futures finish for this many seconds",
    )
    p.add_argument("--no-cache", action="store_true")
    p.add_argument(
        "--no-log",
        action="store_true",
        help="do not tee console output to <out_dir>/log/<stem>.log",
    )
    return p.parse_args()


def main():
    args = parse_args()

    path_a = Path(args.model_a_input)
    path_b = Path(args.model_b_input)
    matrix_a_path = Path(args.model_a_matrix)
    matrix_b_path = Path(args.model_b_matrix)
    out_path = Path(args.out)

    for path in (path_a, path_b, matrix_a_path, matrix_b_path):
        if not path.exists():
            sys.exit(f"missing input: {path}")

    tie_default_raw = (args.tie_winner_default or "").strip()
    tie_default_norm = tie_default_raw.lower()
    if tie_default_norm in {"model_a", "a"}:
        tie_default_side = "model_a"
    elif tie_default_norm in {"model_b", "b"}:
        tie_default_side = "model_b"
    elif tie_default_raw == args.model_a_name:
        tie_default_side = "model_a"
    elif tie_default_raw == args.model_b_name:
        tie_default_side = "model_b"
    else:
        raise SystemExit(
            "--tie-winner-default must be one of model_a/model_b/a/b or exactly "
            f"match one of the model names ({args.model_a_name}, {args.model_b_name}); "
            f"got: {args.tie_winner_default!r}"
        )

    rubric_text = (
        Path(args.rubric_file).read_text(encoding="utf-8").strip()
        if args.rubric_file
        else render_rubric(DEFAULT_RUBRIC)
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not args.no_log:
        log_path = out_path.parent / "log" / f"{out_path.stem}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(log_path, "w", encoding="utf-8")
        sys.stdout = _Tee(sys.stdout, log_fh)
        sys.stderr = _Tee(sys.stderr, log_fh)
        print(f"log: {log_path}")

    cache_path = (
        Path(args.cache_path)
        if args.cache_path
        else out_path.parent / "cache" / f"{out_path.stem}.cache.jsonl"
    )
    cache = LLMCache(cache_path, enabled=not args.no_cache)
    if cache.enabled:
        print(f"cache: {cache_path} (loaded {cache.loaded_entries} entries)")

    request_options = {}
    if args.reasoning_effort:
        request_options["reasoning_effort"] = args.reasoning_effort
    if args.structured_output_winner_only:
        request_options["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "judge_winner",
                "schema": {
                    "type": "object",
                    "properties": {
                        "winner": {
                            "type": "string",
                            "enum": ["A", "B", "tie"],
                        }
                    },
                    "required": ["winner"],
                    "additionalProperties": False,
                },
            },
        }
    if args.request_timeout and args.request_timeout > 0:
        request_options["timeout"] = args.request_timeout
    if not request_options:
        request_options = None

    rows_a, rows_a_by_id = load_rows(path_a, limit=args.limit)
    _rows_b, rows_b_by_id = load_rows(path_b)
    matrix_a = load_matrix_rows(matrix_a_path)
    matrix_b = load_matrix_rows(matrix_b_path)

    docs: dict[str, dict[str, Any]] = {}
    task_slots: dict[tuple[str, str, int, str, int], dict[str, Any]] = {}
    unique_auto_ties = 0
    duplicate_task_references = 0

    def fill_ref(doc_id: str, field_name: str, idx: int, value: int) -> None:
        docs[doc_id][field_name][idx] = value

    def verdict_to_score(winner: str) -> int:
        if winner == "A":
            return 1
        if winner == "B":
            return -1
        return 0

    def is_content_filter_error(exc: Exception) -> bool:
        msg = str(exc)
        needles = (
            "content filtered",
            "content_filter",
            "PROHIBITED_CONTENT",
        )
        return any(needle in msg for needle in needles)

    def register_task(
        key: tuple[str, str, int, str, int],
        first_text: str,
        second_text: str,
        ref: tuple[str, str, int],
    ) -> None:
        nonlocal unique_auto_ties, duplicate_task_references
        slot = task_slots.get(key)
        if slot is None:
            slot = {
                "first_text": first_text,
                "second_text": second_text,
                "refs": [],
                "auto_tie": first_text == second_text,
            }
            task_slots[key] = slot
            if slot["auto_tie"]:
                unique_auto_ties += 1
        else:
            duplicate_task_references += 1
        slot["refs"].append(ref)

    for row_a in rows_a:
        doc_id = row_a["doc_id"]
        row_b = rows_b_by_id.get(doc_id)
        if row_b is None:
            raise SystemExit(f"missing doc_id={doc_id} in {path_b}")
        validate_rows_match(path_a, row_a, path_b, row_b)

        matrix_a_info = matrix_a.get(doc_id)
        matrix_b_info = matrix_b.get(doc_id)
        if matrix_a_info is None:
            raise SystemExit(f"missing doc_id={doc_id} in {matrix_a_path}")
        if matrix_b_info is None:
            raise SystemExit(f"missing doc_id={doc_id} in {matrix_b_path}")

        hypos_a = matrix_a_info["hypos"]
        hypos_b = matrix_b_info["hypos"]
        if extract_hypos(row_a) != hypos_a:
            raise SystemExit(f"hypothesis mismatch for doc_id={doc_id} in {path_a}")
        if extract_hypos(row_b) != hypos_b:
            raise SystemExit(f"hypothesis mismatch for doc_id={doc_id} in {path_b}")

        best_a = matrix_a_info["best_idx"]
        best_b = matrix_b_info["best_idx"]
        score_a = matrix_a_info["record"].get("score")
        score_b = matrix_b_info["record"].get("score")
        tgt_lang_code = row_a.get("tgt_lang") or ""

        docs[doc_id] = {
            "doc_id": doc_id,
            "source": row_a.get("source_doc") or "",
            "src": src_lang_for_record(row_a, args.src_lang),
            "instr": instruction_for_record(row_a, args.with_instruction),
            "tgt_lang": tgt_lang_code,
            "tgt_language": args.tgt_lang or lang_name(tgt_lang_code),
            "model_a_name": args.model_a_name,
            "model_b_name": args.model_b_name,
            "model_a_hypos": hypos_a,
            "model_b_hypos": hypos_b,
            "model_a_best_idx": best_a,
            "model_b_best_idx": best_b,
            "model_a_best_hypothesis": hypos_a[best_a],
            "model_b_best_hypothesis": hypos_b[best_b],
            "model_a_intra_score": score_a[best_a] if isinstance(score_a, list) else None,
            "model_b_intra_score": score_b[best_b] if isinstance(score_b, list) else None,
            "model_a_matrix_file": matrix_a_path.name,
            "model_b_matrix_file": matrix_b_path.name,
            "model_a_best_vs_model_b_pool": [None] * len(hypos_b),
            "model_b_pool_vs_model_a_best": [None] * len(hypos_b),
            "model_b_best_vs_model_a_pool": [None] * len(hypos_a),
            "model_a_pool_vs_model_b_best": [None] * len(hypos_a),
            "content_filter_ties": 0,
        }

        for j, hypo_b in enumerate(hypos_b):
            register_task(
                (doc_id, "a", best_a, "b", j),
                hypos_a[best_a],
                hypo_b,
                (doc_id, "model_a_best_vs_model_b_pool", j),
            )
            register_task(
                (doc_id, "b", j, "a", best_a),
                hypo_b,
                hypos_a[best_a],
                (doc_id, "model_b_pool_vs_model_a_best", j),
            )

        for i, hypo_a in enumerate(hypos_a):
            register_task(
                (doc_id, "b", best_b, "a", i),
                hypos_b[best_b],
                hypo_a,
                (doc_id, "model_b_best_vs_model_a_pool", i),
            )
            register_task(
                (doc_id, "a", i, "b", best_b),
                hypo_a,
                hypos_b[best_b],
                (doc_id, "model_a_pool_vs_model_b_best", i),
            )

    tasks: list[tuple[str, str, int, str, int]] = []
    for key, slot in task_slots.items():
        if slot["auto_tie"]:
            for doc_id, field_name, idx in slot["refs"]:
                fill_ref(doc_id, field_name, idx, 0)
            continue
        tasks.append(key)

    print(
        f"docs={len(docs)}; unique ordered pairs to judge={len(tasks)}; "
        f"identical unique pairs auto-tied={unique_auto_ties}; "
        f"duplicate task references={duplicate_task_references}; model={args.model}"
    )

    tlocal = threading.local()

    def client_for_thread():
        client = getattr(tlocal, "client", None)
        if client is None:
            client = build_client(args.api_key)
            tlocal.client = client
        return client

    def text_for(doc: dict[str, Any], side: str, idx: int) -> str:
        if side == "a":
            return doc["model_a_hypos"][idx]
        return doc["model_b_hypos"][idx]

    def worker(task: tuple[str, str, int, str, int]):
        doc_id, first_side, first_idx, second_side, second_idx = task
        doc = docs[doc_id]
        first_text = text_for(doc, first_side, first_idx)
        second_text = text_for(doc, second_side, second_idx)
        verdict = judge_pair(
            client_for_thread(),
            args.model,
            doc["source"],
            first_text,
            second_text,
            doc["src"],
            doc["tgt_language"],
            rubric_text,
            args.temperature,
            cache,
            swap=False,
            request_options=request_options,
            require_reason=not args.json_only,
            instruction=doc["instr"],
        )
        return task, verdict["winner"]

    n_done = 0
    n_fail = 0
    n_content_filtered = 0
    if tasks:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(worker, t): t for t in tasks}
            pending = set(futures)
            while pending:
                done, pending = wait(
                    pending,
                    timeout=args.stall_report_seconds,
                    return_when=FIRST_COMPLETED,
                )
                if not done:
                    if cache.enabled:
                        stats = cache.stats()
                        print(
                            f"  [stall] no completions for "
                            f"{args.stall_report_seconds:g}s; pending={len(pending)} "
                            f"(cache hits={stats['hits']}/{stats['lookups']}, new={stats['writes']})"
                        )
                    else:
                        print(
                            f"  [stall] no completions for "
                            f"{args.stall_report_seconds:g}s; pending={len(pending)}"
                        )
                    continue
                for fut in done:
                    try:
                        task, winner = fut.result()
                    except Exception as e:  # noqa: BLE001
                        task = futures[fut]
                        if is_content_filter_error(e):
                            slot = task_slots[task]
                            for doc_id, field_name, idx in slot["refs"]:
                                fill_ref(doc_id, field_name, idx, 0)
                                docs[doc_id]["content_filter_ties"] += 1
                            n_content_filtered += 1
                            n_done += 1
                            print(f"  [content-filter->tie] {task}: {e}", file=sys.stderr)
                            continue
                        n_fail += 1
                        print(f"  [error] {task}: {e}", file=sys.stderr)
                        continue
                    slot = task_slots[task]
                    score = verdict_to_score(winner)
                    for doc_id, field_name, idx in slot["refs"]:
                        fill_ref(doc_id, field_name, idx, score)
                    n_done += 1
                    if n_done % 50 == 0:
                        if cache.enabled:
                            stats = cache.stats()
                            print(
                                f".. {n_done}/{len(tasks)} ordered pairs judged "
                                f"(cache hits={stats['hits']}/{stats['lookups']}, new={stats['writes']})"
                            )
                        else:
                            print(f".. {n_done}/{len(tasks)} ordered pairs judged")

    print(f"content-filtered unique ordered pairs treated as tie={n_content_filtered}")

    if n_fail:
        raise SystemExit(f"{n_fail} judge task(s) failed; output not written")

    with out_path.open("w", encoding="utf-8") as fout:
        for doc in docs.values():
            arrays = (
                "model_a_best_vs_model_b_pool",
                "model_b_pool_vs_model_a_best",
                "model_b_best_vs_model_a_pool",
                "model_a_pool_vs_model_b_best",
            )
            for name in arrays:
                if any(v is None for v in doc[name]):
                    raise SystemExit(f"incomplete results for doc_id={doc['doc_id']} field={name}")

            a_cross = sum(doc["model_a_best_vs_model_b_pool"]) - sum(doc["model_b_pool_vs_model_a_best"])
            b_cross = sum(doc["model_b_best_vs_model_a_pool"]) - sum(doc["model_a_pool_vs_model_b_best"])
            a_total = None
            b_total = None
            if doc["model_a_intra_score"] is not None:
                a_total = doc["model_a_intra_score"] + a_cross
            if doc["model_b_intra_score"] is not None:
                b_total = doc["model_b_intra_score"] + b_cross

            selected_side = None
            tie_resolved = False
            if a_total is not None and b_total is not None:
                if a_total > b_total:
                    selected_side = "model_a"
                elif b_total > a_total:
                    selected_side = "model_b"
                else:
                    selected_side = tie_default_side
                    tie_resolved = True

            result = {
                "doc_id": doc["doc_id"],
                "tgt_lang": doc["tgt_lang"],
                "tgt_language": doc["tgt_language"],
                "source_doc": doc["source"],
                "model_a_name": doc["model_a_name"],
                "model_b_name": doc["model_b_name"],
                "model_a_matrix_file": doc["model_a_matrix_file"],
                "model_b_matrix_file": doc["model_b_matrix_file"],
                "model_a_hypos": doc["model_a_hypos"],
                "model_b_hypos": doc["model_b_hypos"],
                "model_a_best_idx": doc["model_a_best_idx"],
                "model_b_best_idx": doc["model_b_best_idx"],
                "model_a_best_hypothesis": doc["model_a_best_hypothesis"],
                "model_b_best_hypothesis": doc["model_b_best_hypothesis"],
                "model_a_intra_score": doc["model_a_intra_score"],
                "model_b_intra_score": doc["model_b_intra_score"],
                "model_a_best_vs_model_b_pool": doc["model_a_best_vs_model_b_pool"],
                "model_b_pool_vs_model_a_best": doc["model_b_pool_vs_model_a_best"],
                "model_b_best_vs_model_a_pool": doc["model_b_best_vs_model_a_pool"],
                "model_a_pool_vs_model_b_best": doc["model_a_pool_vs_model_b_best"],
                "model_a_cross_score": a_cross,
                "model_b_cross_score": b_cross,
                "model_a_total_score": a_total,
                "model_b_total_score": b_total,
                "tie_winner_default": tie_default_side,
                "tie_was_resolved_by_default": tie_resolved,
                "selected_model_side": selected_side,
                "selected_model_name": (
                    doc["model_a_name"] if selected_side == "model_a"
                    else doc["model_b_name"] if selected_side == "model_b"
                    else None
                ),
                "selected_best_idx": (
                    doc["model_a_best_idx"] if selected_side == "model_a"
                    else doc["model_b_best_idx"] if selected_side == "model_b"
                    else None
                ),
                "selected_best_hypothesis": (
                    doc["model_a_best_hypothesis"] if selected_side == "model_a"
                    else doc["model_b_best_hypothesis"] if selected_side == "model_b"
                    else None
                ),
                "score_delta_model_a_minus_model_b": (
                    a_total - b_total if a_total is not None and b_total is not None else None
                ),
                "pairwise_comparisons": sum(len(slot["refs"]) > 0 and not slot["auto_tie"] and key[0] == doc["doc_id"]
                                             for key, slot in task_slots.items()),
                "identical_shortcuts": sum(slot["auto_tie"] and key[0] == doc["doc_id"]
                                           for key, slot in task_slots.items()),
                "content_filter_ties": doc["content_filter_ties"],
                "duplicate_task_references": sum(max(0, len(slot["refs"]) - 1)
                                                 for key, slot in task_slots.items()
                                                 if key[0] == doc["doc_id"]),
            }
            fout.write(json.dumps(result, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
