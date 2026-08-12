#!/usr/bin/env python3
"""Sanity-check the two-best selector and print a small manual audit sample."""

import argparse
import json
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CROSS_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-3.5-flash"
    / "experiments"
    / "two-best"
    / "gemini-3.5-flash__gpt-final_rubric-v5-structured"
    / "cross-matrix"
)
DEFAULT_PRELIM = (
    REPO_ROOT
    / "final_submission"
    / "out"
    / "two-best"
    / "gemini-3.5-flash__gpt-final_rubric-v5-structured"
    / "preliminary_final.jsonl"
)
DEFAULT_SELECTION_REPORT = DEFAULT_PRELIM.parent / "reports" / "selection_report.json"
DEFAULT_MODEL_A_MATRIX_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-3.5-flash"
    / "experiments"
    / "gemini-3.5-flash_rubric-v5-structured"
    / "matrix"
)
DEFAULT_MODEL_B_MATRIX_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-3.5-flash"
    / "experiments"
    / "gpt-final_rubric-v5-structured"
    / "matrix"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Recompute two-best selector winners from cross-matrix files, verify "
            "the exported preliminary file, and print a 10-case audit sample."
        )
    )
    parser.add_argument("--cross-dir", type=Path, default=DEFAULT_CROSS_DIR)
    parser.add_argument("--prelim", type=Path, default=DEFAULT_PRELIM)
    parser.add_argument("--selection-report", type=Path, default=DEFAULT_SELECTION_REPORT)
    parser.add_argument("--model-a-matrix-dir", type=Path, default=DEFAULT_MODEL_A_MATRIX_DIR)
    parser.add_argument("--model-b-matrix-dir", type=Path, default=DEFAULT_MODEL_B_MATRIX_DIR)
    parser.add_argument("--sample-size", type=int, default=10)
    return parser.parse_args()


def iter_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_no, json.loads(line)
            except ValueError as exc:
                raise SystemExit("%s:%d: invalid JSON: %s" % (path, line_no, exc))


def suffix_strip(name, suffix):
    if not name.endswith(suffix):
        raise SystemExit("unexpected filename: %s" % name)
    return name[: -len(suffix)]


def load_cross_rows(cross_dir):
    rows = {}
    files = sorted(cross_dir.glob("*-winner-cross.jsonl"))
    if not files:
        raise SystemExit("no cross files found in %s" % cross_dir)
    for path in files:
        lang = suffix_strip(path.name, "-winner-cross.jsonl")
        for line_no, row in iter_jsonl(path):
            doc_id = row.get("doc_id")
            tgt_lang = row.get("tgt_lang")
            if not isinstance(doc_id, str) or not isinstance(tgt_lang, str):
                raise SystemExit("%s:%d: expected string doc_id/tgt_lang" % (path, line_no))
            if tgt_lang != lang:
                raise SystemExit(
                    "%s:%d: tgt_lang=%r does not match filename lang=%r"
                    % (path, line_no, tgt_lang, lang)
                )
            key = (tgt_lang, doc_id)
            if key in rows:
                raise SystemExit("duplicate cross row for %s %s" % key)
            rows[key] = row
    return rows


def load_prelim_rows(path):
    rows = {}
    for line_no, row in iter_jsonl(path):
        doc_id = row.get("doc_id")
        tgt_lang = row.get("tgt_lang")
        if not isinstance(doc_id, str) or not isinstance(tgt_lang, str):
            raise SystemExit("%s:%d: expected string doc_id/tgt_lang" % (path, line_no))
        key = (tgt_lang, doc_id)
        if key in rows:
            raise SystemExit("duplicate prelim row for %s %s" % key)
        rows[key] = row
    return rows


def load_matrix_rows(matrix_dir):
    rows = {}
    files = sorted(matrix_dir.glob("*-llm-matrix.jsonl"))
    if not files:
        raise SystemExit("no matrix files found in %s" % matrix_dir)
    for path in files:
        lang = suffix_strip(path.name, "-llm-matrix.jsonl")
        for line_no, row in iter_jsonl(path):
            doc_id = row.get("doc_id")
            best = row.get("best")
            hypos = row.get("hypos")
            score = row.get("score")
            if not isinstance(doc_id, str):
                raise SystemExit("%s:%d: expected string doc_id" % (path, line_no))
            if not isinstance(best, int):
                raise SystemExit("%s:%d: expected int best" % (path, line_no))
            if not isinstance(hypos, list) or not hypos or any(not isinstance(x, str) for x in hypos):
                raise SystemExit("%s:%d: expected non-empty string hypos list" % (path, line_no))
            if not isinstance(score, list) or len(score) != len(hypos):
                raise SystemExit("%s:%d: expected score list aligned with hypos" % (path, line_no))
            if any(not isinstance(x, (int, float)) for x in score):
                raise SystemExit("%s:%d: score values must be numeric" % (path, line_no))
            key = (lang, doc_id)
            if key in rows:
                raise SystemExit("duplicate matrix row for %s %s" % key)
            rows[key] = {
                "best_idx": best,
                "hypos": hypos,
                "score": score,
            }
    return rows


def bool_int(value):
    return 1 if value else 0


def preview(text, limit):
    text = text.replace("\n", " / ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def verify_equal(actual, expected, label, mismatches, key):
    if actual != expected:
        mismatches.append("%s %s: expected=%r actual=%r" % (key[0], key[1], expected, actual))


def choose_manual_cases(case_rows, sample_size):
    if sample_size <= 0 or not case_rows:
        return []

    fixed = [row for row in case_rows if row["alignment_fixed"]]
    kept = [row for row in case_rows if not row["alignment_fixed"]]

    by_abs_delta_asc = sorted(kept, key=lambda row: (abs(row["score_delta"]), row["tgt_lang"], row["doc_id"]))
    by_abs_delta_desc = sorted(
        kept,
        key=lambda row: (-abs(row["score_delta"]), row["tgt_lang"], row["doc_id"]),
    )

    picked = []
    seen = set()

    def add_rows(rows):
        for row in rows:
            key = (row["tgt_lang"], row["doc_id"])
            if key in seen:
                continue
            seen.add(key)
            picked.append(row)
            if len(picked) >= sample_size:
                return

    add_rows(fixed)
    if len(picked) < sample_size:
        near_count = max(0, min(len(by_abs_delta_asc), (sample_size - len(picked) + 1) // 2))
        add_rows(by_abs_delta_asc[:near_count])
    if len(picked) < sample_size:
        far_count = sample_size - len(picked)
        add_rows(by_abs_delta_desc[:far_count])
    if len(picked) < sample_size:
        add_rows(by_abs_delta_asc)
    return picked[:sample_size]


def main():
    args = parse_args()
    cross_rows = load_cross_rows(args.cross_dir.resolve())
    prelim_rows = load_prelim_rows(args.prelim.resolve())
    matrix_a_rows = load_matrix_rows(args.model_a_matrix_dir.resolve())
    matrix_b_rows = load_matrix_rows(args.model_b_matrix_dir.resolve())

    selection_report = None
    if args.selection_report.is_file():
        selection_report = json.loads(args.selection_report.read_text(encoding="utf-8"))

    raw_selected_counts = Counter()
    final_counts = Counter()
    selector_mismatches = []
    prelim_selected_mismatches = []
    final_mismatches = []
    missing_prelim = []
    case_rows = []
    selected_invalid_count = 0
    fixed_count = 0
    cross_model_fix_count = 0
    unfixable_count = 0

    for key in sorted(cross_rows):
        cross_row = cross_rows[key]
        prelim_row = prelim_rows.get(key)
        if prelim_row is None:
            missing_prelim.append("%s %s" % key)
            continue

        matrix_a = matrix_a_rows.get(key)
        matrix_b = matrix_b_rows.get(key)
        if matrix_a is None or matrix_b is None:
            raise SystemExit("missing matrix rows for %s %s" % key)

        hypos_a = cross_row.get("model_a_hypos")
        hypos_b = cross_row.get("model_b_hypos")
        if hypos_a != matrix_a["hypos"]:
            raise SystemExit("model_a_hypos mismatch for %s %s" % key)
        if hypos_b != matrix_b["hypos"]:
            raise SystemExit("model_b_hypos mismatch for %s %s" % key)

        best_a = cross_row.get("model_a_best_idx")
        best_b = cross_row.get("model_b_best_idx")
        if best_a != matrix_a["best_idx"] or best_b != matrix_b["best_idx"]:
            raise SystemExit("best_idx mismatch for %s %s" % key)

        a_cross = (
            sum(cross_row["model_a_best_vs_model_b_pool"])
            - sum(cross_row["model_b_pool_vs_model_a_best"])
        )
        b_cross = (
            sum(cross_row["model_b_best_vs_model_a_pool"])
            - sum(cross_row["model_a_pool_vs_model_b_best"])
        )
        a_total = matrix_a["score"][best_a] + a_cross
        b_total = matrix_b["score"][best_b] + b_cross
        tie_default = cross_row.get("tie_winner_default")

        if a_total > b_total:
            expected_selected_side = "model_a"
            tie_resolved = False
        elif b_total > a_total:
            expected_selected_side = "model_b"
            tie_resolved = False
        else:
            expected_selected_side = tie_default
            tie_resolved = True

        expected_selected_name = (
            cross_row.get("model_a_name")
            if expected_selected_side == "model_a"
            else cross_row.get("model_b_name")
        )
        expected_selected_idx = best_a if expected_selected_side == "model_a" else best_b
        expected_selected_text = (
            hypos_a[best_a] if expected_selected_side == "model_a" else hypos_b[best_b]
        )

        key_label = "%s %s" % key
        verify_equal(cross_row.get("model_a_cross_score"), a_cross, "model_a_cross_score", selector_mismatches, key)
        verify_equal(cross_row.get("model_b_cross_score"), b_cross, "model_b_cross_score", selector_mismatches, key)
        verify_equal(cross_row.get("model_a_total_score"), a_total, "model_a_total_score", selector_mismatches, key)
        verify_equal(cross_row.get("model_b_total_score"), b_total, "model_b_total_score", selector_mismatches, key)
        verify_equal(
            cross_row.get("selected_model_side"),
            expected_selected_side,
            "selected_model_side",
            selector_mismatches,
            key,
        )
        verify_equal(
            cross_row.get("selected_model_name"),
            expected_selected_name,
            "selected_model_name",
            selector_mismatches,
            key,
        )
        verify_equal(
            cross_row.get("selected_best_idx"),
            expected_selected_idx,
            "selected_best_idx",
            selector_mismatches,
            key,
        )
        verify_equal(
            cross_row.get("selected_best_hypothesis"),
            expected_selected_text,
            "selected_best_hypothesis",
            selector_mismatches,
            key,
        )
        verify_equal(
            cross_row.get("tie_was_resolved_by_default"),
            tie_resolved,
            "tie_was_resolved_by_default",
            selector_mismatches,
            key,
        )

        raw_selected_counts[expected_selected_name] += 1

        verify_equal(
            prelim_row.get("two_best_selected_model_name"),
            expected_selected_name,
            "two_best_selected_model_name",
            prelim_selected_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_selected_model_side"),
            expected_selected_side,
            "two_best_selected_model_side",
            prelim_selected_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_selected_best_idx"),
            expected_selected_idx,
            "two_best_selected_best_idx",
            prelim_selected_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_selected_best_hypothesis"),
            expected_selected_text,
            "two_best_selected_best_hypothesis",
            prelim_selected_mismatches,
            key,
        )

        mask_a = prelim_row.get("two_best_alignment_model_a_mask")
        mask_b = prelim_row.get("two_best_alignment_model_b_mask")
        if (
            not isinstance(mask_a, list)
            or not isinstance(mask_b, list)
            or len(mask_a) != len(hypos_a)
            or len(mask_b) != len(hypos_b)
        ):
            raise SystemExit("bad alignment mask lengths for %s" % key_label)

        selected_passed = bool(
            (mask_a if expected_selected_side == "model_a" else mask_b)[expected_selected_idx]
        )
        if not selected_passed:
            selected_invalid_count += 1

        candidates = []
        for idx, text in enumerate(hypos_a):
            intra_score = float(matrix_a["score"][idx])
            candidates.append(
                {
                    "side": "model_a",
                    "model_name": cross_row.get("model_a_name"),
                    "idx": idx,
                    "hypo_key": "hypo_%d" % idx,
                    "text": text,
                    "passed": bool(mask_a[idx]),
                    "intra_score": intra_score,
                    "cross_score": float(a_cross),
                    "model_total_score": float(a_total),
                    "proxy_total_score": float(a_cross) + intra_score,
                }
            )
        for idx, text in enumerate(hypos_b):
            intra_score = float(matrix_b["score"][idx])
            candidates.append(
                {
                    "side": "model_b",
                    "model_name": cross_row.get("model_b_name"),
                    "idx": idx,
                    "hypo_key": "hypo_%d" % idx,
                    "text": text,
                    "passed": bool(mask_b[idx]),
                    "intra_score": intra_score,
                    "cross_score": float(b_cross),
                    "model_total_score": float(b_total),
                    "proxy_total_score": float(b_cross) + intra_score,
                }
            )

        if selected_passed:
            expected_final = None
            for candidate in candidates:
                if candidate["side"] == expected_selected_side and candidate["idx"] == expected_selected_idx:
                    expected_final = candidate
                    break
            expected_fixed = False
            expected_unfixable = False
            expected_reason = "selected_passed_alignment"
        else:
            valid_candidates = [candidate for candidate in candidates if candidate["passed"]]
            if not valid_candidates:
                expected_final = None
                for candidate in candidates:
                    if candidate["side"] == expected_selected_side and candidate["idx"] == expected_selected_idx:
                        expected_final = candidate
                        break
                expected_fixed = False
                expected_unfixable = True
                expected_reason = "no_valid_candidate_keep_selected"
                unfixable_count += 1
            else:
                expected_final = max(
                    valid_candidates,
                    key=lambda candidate: (
                        candidate["proxy_total_score"],
                        bool_int(candidate["model_name"] == expected_selected_name),
                        candidate["model_total_score"],
                        candidate["intra_score"],
                        bool_int(candidate["side"] == tie_default),
                        -candidate["idx"],
                    ),
                )
                expected_fixed = True
                expected_unfixable = False
                expected_reason = "combined_valid_fallback"
                fixed_count += 1
                if expected_final["model_name"] != expected_selected_name:
                    cross_model_fix_count += 1

        verify_equal(
            prelim_row.get("two_best_selected_best_passed_alignment"),
            selected_passed,
            "two_best_selected_best_passed_alignment",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_alignment_fixed"),
            expected_fixed,
            "two_best_alignment_fixed",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_alignment_unfixable"),
            expected_unfixable,
            "two_best_alignment_unfixable",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_alignment_fix_reason"),
            expected_reason,
            "two_best_alignment_fix_reason",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_model_name"),
            expected_final["model_name"],
            "two_best_final_model_name",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_model_side"),
            expected_final["side"],
            "two_best_final_model_side",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_hypo_key"),
            expected_final["hypo_key"],
            "two_best_final_hypo_key",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_hypothesis"),
            expected_final["text"],
            "two_best_final_hypothesis",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_intra_score"),
            expected_final["intra_score"],
            "two_best_final_intra_score",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_cross_score_proxy"),
            expected_final["cross_score"],
            "two_best_final_cross_score_proxy",
            final_mismatches,
            key,
        )
        verify_equal(
            prelim_row.get("two_best_final_proxy_total_score"),
            expected_final["proxy_total_score"],
            "two_best_final_proxy_total_score",
            final_mismatches,
            key,
        )

        final_counts[expected_final["model_name"]] += 1

        case_rows.append(
            {
                "doc_id": key[1],
                "tgt_lang": key[0],
                "selected_model_name": expected_selected_name,
                "selected_model_side": expected_selected_side,
                "selected_best_idx": expected_selected_idx,
                "selected_best_hypothesis": expected_selected_text,
                "final_model_name": expected_final["model_name"],
                "final_model_side": expected_final["side"],
                "final_hypo_key": expected_final["hypo_key"],
                "final_hypothesis": expected_final["text"],
                "alignment_fixed": expected_fixed,
                "selected_passed": selected_passed,
                "a_total": a_total,
                "b_total": b_total,
                "a_cross": a_cross,
                "b_cross": b_cross,
                "a_best_idx": best_a,
                "b_best_idx": best_b,
                "a_best_hypothesis": hypos_a[best_a],
                "b_best_hypothesis": hypos_b[best_b],
                "score_delta": a_total - b_total,
                "tie_resolved": tie_resolved,
                "source_doc": cross_row.get("source_doc", ""),
            }
        )

    if missing_prelim:
        raise SystemExit("missing prelim rows: %s" % ", ".join(missing_prelim[:10]))

    if selection_report is not None:
        report_checks = [
            ("written_rows", len(cross_rows)),
            ("kept_count", len(cross_rows) - fixed_count - unfixable_count),
            ("selected_invalid_count", selected_invalid_count),
            ("fixed_count", fixed_count),
            ("cross_model_fix_count", cross_model_fix_count),
            ("unfixable_count", unfixable_count),
        ]
        for field, expected in report_checks:
            actual = selection_report.get(field)
            if actual != expected:
                final_mismatches.append(
                    "selection_report %s: expected=%r actual=%r" % (field, expected, actual)
                )

    print("rows=%d" % len(cross_rows))
    print(
        "raw_selected_wins gemini-3.5-flash=%d gpt-final=%d"
        % (
            raw_selected_counts.get("gemini-3.5-flash", 0),
            raw_selected_counts.get("gpt-final", 0),
        )
    )
    print(
        "final_wins_after_alignment gemini-3.5-flash=%d gpt-final=%d"
        % (
            final_counts.get("gemini-3.5-flash", 0),
            final_counts.get("gpt-final", 0),
        )
    )
    print(
        "selected_invalid=%d fixed=%d cross_model_fix=%d unfixable=%d"
        % (selected_invalid_count, fixed_count, cross_model_fix_count, unfixable_count)
    )
    print(
        "mismatches selector=%d prelim_selected=%d final=%d"
        % (len(selector_mismatches), len(prelim_selected_mismatches), len(final_mismatches))
    )

    manual_cases = choose_manual_cases(case_rows, args.sample_size)
    if manual_cases:
        print("manual_cases=%d" % len(manual_cases))
        for idx, row in enumerate(manual_cases, start=1):
            print(
                "[case %d] %s %s delta=%+d selected=%s/%s final=%s/%s fixed=%s selected_passed=%s tie=%s"
                % (
                    idx,
                    row["tgt_lang"],
                    row["doc_id"],
                    int(row["score_delta"]),
                    row["selected_model_name"],
                    "hypo_%d" % row["selected_best_idx"],
                    row["final_model_name"],
                    row["final_hypo_key"],
                    row["alignment_fixed"],
                    row["selected_passed"],
                    row["tie_resolved"],
                )
            )
            print(
                "  totals: model_a=%+d (cross=%+d) model_b=%+d (cross=%+d)"
                % (int(row["a_total"]), int(row["a_cross"]), int(row["b_total"]), int(row["b_cross"]))
            )
            print("  source: %s" % preview(row["source_doc"], 180))
            print(
                "  model_a_best: hypo_%d | %s"
                % (row["a_best_idx"], preview(row["a_best_hypothesis"], 180))
            )
            print(
                "  model_b_best: hypo_%d | %s"
                % (row["b_best_idx"], preview(row["b_best_hypothesis"], 180))
            )
            print("  final: %s" % preview(row["final_hypothesis"], 180))

    all_mismatches = selector_mismatches + prelim_selected_mismatches + final_mismatches
    if all_mismatches:
        print("MISMATCH PREVIEW:")
        for item in all_mismatches[:20]:
            print("  %s" % item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
