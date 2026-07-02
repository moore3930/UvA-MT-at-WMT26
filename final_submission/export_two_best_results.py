#!/usr/bin/env python3
"""Export final merged results from two-best cross-model judge outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import iter_jsonl, load_matrix_rows, load_source_rows, preview, wanted_langs
from structure_alignment import check_structure


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "wmt26_genmt_blindset_filter_parse.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a final merged JSONL from two-best cross-model outputs, "
            "keeping the selected winner when structurally valid and otherwise "
            "falling back over valid candidates from both models."
        )
    )
    parser.add_argument("--cross-dir", type=Path, required=True)
    parser.add_argument("--model-a-results-dir", type=Path, required=True)
    parser.add_argument("--model-b-results-dir", type=Path, required=True)
    parser.add_argument("--model-a-matrix-dir", type=Path, required=True)
    parser.add_argument("--model-b-matrix-dir", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--mask-out", type=Path, default=None)
    parser.add_argument("--filtered-source-out", type=Path, default=None)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument("--fixes-jsonl", type=Path, default=None)
    parser.add_argument("--langs", default="all")
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail on missing rows or malformed data (default: true)",
    )
    return parser.parse_args()


def extract_hypos(rec: dict[str, Any]) -> list[str]:
    out: list[tuple[int, str]] = []
    for key, value in rec.items():
        if not key.startswith("hypo_"):
            continue
        try:
            idx = int(key.split("_", 1)[1])
        except ValueError as exc:
            raise SystemExit(f"{rec.get('doc_id')}: bad hypo key {key!r}") from exc
        if not isinstance(value, str):
            raise SystemExit(f"{rec.get('doc_id')}: expected string value for {key}")
        out.append((idx, value))
    out.sort()
    expected = list(range(len(out)))
    actual = [idx for idx, _value in out]
    if actual != expected:
        raise SystemExit(
            f"{rec.get('doc_id')}: non-contiguous hypo ids {actual}, expected {expected}"
        )
    return [value for _idx, value in out]


def language_from_cross_path(path: Path) -> str:
    stem = path.stem
    suffix = "-winner-cross"
    if not stem.endswith(suffix):
        raise SystemExit(f"unexpected cross filename: {path.name}")
    return stem[: -len(suffix)]


def load_cross_rows(cross_dir: Path, langs: set[str] | None):
    files = sorted(cross_dir.glob("*-winner-cross.jsonl"))
    if not files:
        raise SystemExit(f"no *-winner-cross.jsonl files found in {cross_dir}")

    by_lang: dict[str, dict[str, dict[str, Any]]] = {}
    malformed: list[str] = []
    for path in files:
        lang = language_from_cross_path(path)
        if langs is not None and lang not in langs:
            continue
        rows_for_lang: dict[str, dict[str, Any]] = {}
        duplicates: list[str] = []
        for line_no, record in iter_jsonl(path):
            doc_id = record.get("doc_id")
            if not isinstance(doc_id, str):
                malformed.append(f"{path}:{line_no}: expected string doc_id")
                continue
            if doc_id in rows_for_lang:
                duplicates.append(doc_id)
                continue
            rows_for_lang[doc_id] = record
        if duplicates:
            malformed.append(
                f"{path}: duplicate doc_id(s): {preview(sorted(duplicates), limit=10)}"
            )
        by_lang[lang] = rows_for_lang
    return by_lang, malformed


def load_result_rows(results_dir: Path, expected_langs: set[str]):
    files = sorted(
        path
        for path in results_dir.glob("*.jsonl")
        if not path.name.startswith(".") and path.stem in expected_langs
    )
    if not files:
        raise SystemExit(f"no *.jsonl files found in {results_dir}")

    by_lang: dict[str, dict[str, dict[str, Any]]] = {}
    malformed: list[str] = []
    for path in files:
        lang = path.stem
        rows_for_lang: dict[str, dict[str, Any]] = {}
        duplicates: list[str] = []
        for line_no, record in iter_jsonl(path):
            doc_id = record.get("doc_id")
            if not isinstance(doc_id, str):
                malformed.append(f"{path}:{line_no}: expected string doc_id")
                continue
            if doc_id in rows_for_lang:
                duplicates.append(doc_id)
                continue
            rows_for_lang[doc_id] = record
        if duplicates:
            malformed.append(
                f"{path}: duplicate doc_id(s): {preview(sorted(duplicates), limit=10)}"
            )
        by_lang[lang] = rows_for_lang
    return by_lang, malformed


def compare_fields(
    source_row: dict[str, Any],
    row_a: dict[str, Any],
    row_b: dict[str, Any],
) -> None:
    source_fields = ("doc_id", "src_lang", "tgt_lang", "source_doc")
    for field in source_fields:
        base = source_row.get(field)
        if row_a.get(field) != base:
            raise SystemExit(
                f"{source_row.get('tgt_lang')}:{source_row.get('doc_id')}: "
                f"model A field mismatch for {field}"
            )
        if row_b.get(field) != base:
            raise SystemExit(
                f"{source_row.get('tgt_lang')}:{source_row.get('doc_id')}: "
                f"model B field mismatch for {field}"
            )

    row_fields = ("instruction", "multimodal_instruction", "multimodal_input_path")
    for field in row_fields:
        if row_a.get(field) != row_b.get(field):
            raise SystemExit(
                f"{source_row.get('tgt_lang')}:{source_row.get('doc_id')}: "
                f"model A/B field mismatch for {field}"
            )


def bool_int(value: bool) -> int:
    return 1 if value else 0


def main() -> None:
    args = parse_args()
    source_path = args.source.resolve()
    cross_dir = args.cross_dir.resolve()
    model_a_results_dir = args.model_a_results_dir.resolve()
    model_b_results_dir = args.model_b_results_dir.resolve()
    model_a_matrix_dir = args.model_a_matrix_dir.resolve()
    model_b_matrix_dir = args.model_b_matrix_dir.resolve()
    out_path = args.out.resolve()
    langs = wanted_langs(args.langs)

    for path in (
        source_path,
        cross_dir,
        model_a_results_dir,
        model_b_results_dir,
        model_a_matrix_dir,
        model_b_matrix_dir,
    ):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    source_rows, expected_by_lang = load_source_rows(source_path, langs)
    cross_by_lang, cross_malformed = load_cross_rows(cross_dir, langs)
    if cross_malformed:
        raise SystemExit(f"malformed cross rows: {preview(cross_malformed, limit=3)}")
    expected_langs = set(expected_by_lang)
    model_a_rows, model_a_malformed = load_result_rows(model_a_results_dir, expected_langs)
    model_b_rows, model_b_malformed = load_result_rows(model_b_results_dir, expected_langs)
    if model_a_malformed:
        raise SystemExit(f"malformed model A rows: {preview(model_a_malformed, limit=3)}")
    if model_b_malformed:
        raise SystemExit(f"malformed model B rows: {preview(model_b_malformed, limit=3)}")
    model_a_matrix, matrix_a_malformed = load_matrix_rows(model_a_matrix_dir, "", langs)
    model_b_matrix, matrix_b_malformed = load_matrix_rows(model_b_matrix_dir, "", langs)
    if matrix_a_malformed:
        raise SystemExit(f"malformed model A matrix rows: {preview(matrix_a_malformed, limit=3)}")
    if matrix_b_malformed:
        raise SystemExit(f"malformed model B matrix rows: {preview(matrix_b_malformed, limit=3)}")

    output_rows: list[dict[str, Any]] = []
    mask_rows: list[dict[str, Any]] = []
    filtered_source_rows: list[dict[str, Any]] = []
    fixes: list[dict[str, Any]] = []
    failures: list[str] = []
    kept_count = 0
    fixed_count = 0
    cross_model_fix_count = 0
    unfixable_count = 0
    selected_invalid_count = 0
    no_valid_count = 0
    kind_counts = {"html": 0, "json": 0, "unstructured": 0}

    for source_row in source_rows:
        lang = source_row["tgt_lang"]
        doc_id = source_row["doc_id"]

        cross_row = cross_by_lang.get(lang, {}).get(doc_id)
        row_a = model_a_rows.get(lang, {}).get(doc_id)
        row_b = model_b_rows.get(lang, {}).get(doc_id)
        matrix_a = model_a_matrix.get(lang, {}).get(doc_id)
        matrix_b = model_b_matrix.get(lang, {}).get(doc_id)

        if cross_row is None:
            failures.append(f"missing cross row: {lang}:{doc_id}")
            continue
        if row_a is None:
            failures.append(f"missing model A row: {lang}:{doc_id}")
            continue
        if row_b is None:
            failures.append(f"missing model B row: {lang}:{doc_id}")
            continue
        if matrix_a is None:
            failures.append(f"missing model A matrix row: {lang}:{doc_id}")
            continue
        if matrix_b is None:
            failures.append(f"missing model B matrix row: {lang}:{doc_id}")
            continue

        compare_fields(source_row, row_a, row_b)

        hypos_a = extract_hypos(row_a)
        hypos_b = extract_hypos(row_b)
        if hypos_a != matrix_a["hypos"]:
            raise SystemExit(f"{lang}:{doc_id}: model A hypos do not match matrix hypos")
        if hypos_b != matrix_b["hypos"]:
            raise SystemExit(f"{lang}:{doc_id}: model B hypos do not match matrix hypos")
        if hypos_a != cross_row.get("model_a_hypos"):
            raise SystemExit(f"{lang}:{doc_id}: model A hypos do not match cross hypos")
        if hypos_b != cross_row.get("model_b_hypos"):
            raise SystemExit(f"{lang}:{doc_id}: model B hypos do not match cross hypos")

        score_a = matrix_a["record"].get("score")
        score_b = matrix_b["record"].get("score")
        if (
            not isinstance(score_a, list)
            or len(score_a) != len(hypos_a)
            or any(not isinstance(x, (int, float)) for x in score_a)
        ):
            raise SystemExit(f"{lang}:{doc_id}: malformed model A score vector")
        if (
            not isinstance(score_b, list)
            or len(score_b) != len(hypos_b)
            or any(not isinstance(x, (int, float)) for x in score_b)
        ):
            raise SystemExit(f"{lang}:{doc_id}: malformed model B score vector")

        checks_a = [check_structure(source_row.get("source_doc", ""), hypo) for hypo in hypos_a]
        checks_b = [check_structure(source_row.get("source_doc", ""), hypo) for hypo in hypos_b]
        kind = checks_a[0]["kind"] if checks_a else "unstructured"
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        source_metric = checks_a[0]["source_metric"] if checks_a else None
        mask_a = [1 if check["passed"] else 0 for check in checks_a]
        mask_b = [1 if check["passed"] else 0 for check in checks_b]
        valid_a = [idx for idx, bit in enumerate(mask_a) if bit == 1]
        valid_b = [idx for idx, bit in enumerate(mask_b) if bit == 1]

        selected_side = cross_row.get("selected_model_side")
        selected_name = cross_row.get("selected_model_name")
        selected_idx = cross_row.get("selected_best_idx")
        if selected_side not in {"model_a", "model_b"}:
            raise SystemExit(f"{lang}:{doc_id}: invalid selected_model_side={selected_side!r}")
        if not isinstance(selected_idx, int):
            raise SystemExit(f"{lang}:{doc_id}: invalid selected_best_idx={selected_idx!r}")

        model_infos = {
            "model_a": {
                "name": cross_row.get("model_a_name"),
                "hypos": hypos_a,
                "scores": score_a,
                "mask": mask_a,
                "valid_indices": valid_a,
                "cross_score": cross_row.get("model_a_cross_score"),
                "total_score": cross_row.get("model_a_total_score"),
            },
            "model_b": {
                "name": cross_row.get("model_b_name"),
                "hypos": hypos_b,
                "scores": score_b,
                "mask": mask_b,
                "valid_indices": valid_b,
                "cross_score": cross_row.get("model_b_cross_score"),
                "total_score": cross_row.get("model_b_total_score"),
            },
        }
        if selected_name != model_infos[selected_side]["name"]:
            raise SystemExit(
                f"{lang}:{doc_id}: selected_model_name does not match selected_model_side"
            )

        for side in ("model_a", "model_b"):
            if not isinstance(model_infos[side]["cross_score"], (int, float)):
                raise SystemExit(f"{lang}:{doc_id}: invalid {side} cross score")
            if not isinstance(model_infos[side]["total_score"], (int, float)):
                raise SystemExit(f"{lang}:{doc_id}: invalid {side} total score")

        selected_text = model_infos[selected_side]["hypos"][selected_idx]
        selected_passed = bool(model_infos[selected_side]["mask"][selected_idx])
        tie_default_side = cross_row.get("tie_winner_default")

        candidates: list[dict[str, Any]] = []
        for side in ("model_a", "model_b"):
            info = model_infos[side]
            for idx, hypo in enumerate(info["hypos"]):
                intra_score = float(info["scores"][idx])
                cross_score = float(info["cross_score"])
                total_proxy = cross_score + intra_score
                candidates.append(
                    {
                        "side": side,
                        "model_name": info["name"],
                        "idx": idx,
                        "hypo_key": f"hypo_{idx}",
                        "text": hypo,
                        "passed": bool(info["mask"][idx]),
                        "intra_score": intra_score,
                        "cross_score": cross_score,
                        "model_total_score": float(info["total_score"]),
                        "proxy_total_score": total_proxy,
                    }
                )

        if selected_passed:
            final_candidate = next(
                c for c in candidates if c["side"] == selected_side and c["idx"] == selected_idx
            )
            fixed = False
            unfixable = False
            fix_reason = "selected_passed_alignment"
            kept_count += 1
        else:
            selected_invalid_count += 1
            valid_candidates = [candidate for candidate in candidates if candidate["passed"]]
            if not valid_candidates:
                no_valid_count += 1
                unfixable_count += 1
                final_candidate = next(
                    c for c in candidates if c["side"] == selected_side and c["idx"] == selected_idx
                )
                fixed = False
                unfixable = True
                fix_reason = "no_valid_candidate_keep_selected"
            else:
                final_candidate = max(
                    valid_candidates,
                    key=lambda candidate: (
                        candidate["proxy_total_score"],
                        bool_int(candidate["model_name"] == selected_name),
                        candidate["model_total_score"],
                        candidate["intra_score"],
                        bool_int(candidate["side"] == tie_default_side),
                        -candidate["idx"],
                    ),
                )
                fixed = True
                unfixable = False
                fix_reason = "combined_valid_fallback"
                fixed_count += 1
                if final_candidate["model_name"] != selected_name:
                    cross_model_fix_count += 1
                fixes.append(
                    {
                        "doc_id": doc_id,
                        "tgt_lang": lang,
                        "selected_model_name": selected_name,
                        "selected_model_side": selected_side,
                        "selected_best_idx": selected_idx,
                        "selected_best_hypothesis": selected_text,
                        "replacement_model_name": final_candidate["model_name"],
                        "replacement_model_side": final_candidate["side"],
                        "replacement_hypo_key": final_candidate["hypo_key"],
                        "replacement_hypothesis": final_candidate["text"],
                        "replacement_intra_score": final_candidate["intra_score"],
                        "replacement_proxy_total_score": final_candidate["proxy_total_score"],
                        "model_a_mask": mask_a,
                        "model_b_mask": mask_b,
                        "model_a_scores": score_a,
                        "model_b_scores": score_b,
                    }
                )

        output_row = dict(source_row)
        output_row.update(
            {
                "hypothesis": final_candidate["text"],
                "two_best_model_a_name": model_infos["model_a"]["name"],
                "two_best_model_b_name": model_infos["model_b"]["name"],
                "two_best_model_a_total_score": cross_row.get("model_a_total_score"),
                "two_best_model_b_total_score": cross_row.get("model_b_total_score"),
                "two_best_model_a_cross_score": cross_row.get("model_a_cross_score"),
                "two_best_model_b_cross_score": cross_row.get("model_b_cross_score"),
                "two_best_selected_model_name": selected_name,
                "two_best_selected_model_side": selected_side,
                "two_best_selected_best_idx": selected_idx,
                "two_best_selected_best_hypothesis": selected_text,
                "two_best_selected_best_passed_alignment": selected_passed,
                "two_best_tie_winner_default": cross_row.get("tie_winner_default"),
                "two_best_tie_was_resolved_by_default": cross_row.get(
                    "tie_was_resolved_by_default"
                ),
                "two_best_final_model_name": final_candidate["model_name"],
                "two_best_final_model_side": final_candidate["side"],
                "two_best_final_hypo_key": final_candidate["hypo_key"],
                "two_best_final_hypothesis": final_candidate["text"],
                "two_best_final_intra_score": final_candidate["intra_score"],
                "two_best_final_cross_score_proxy": final_candidate["cross_score"],
                "two_best_final_proxy_total_score": final_candidate["proxy_total_score"],
                "two_best_alignment_check_kind": kind,
                "two_best_alignment_source_metric": source_metric,
                "two_best_alignment_model_a_mask": mask_a,
                "two_best_alignment_model_b_mask": mask_b,
                "two_best_alignment_model_a_valid_hypothesis_indices": valid_a,
                "two_best_alignment_model_b_valid_hypothesis_indices": valid_b,
                "two_best_alignment_model_a_hypothesis_metrics": [
                    check["hypothesis_metric"] for check in checks_a
                ],
                "two_best_alignment_model_b_hypothesis_metrics": [
                    check["hypothesis_metric"] for check in checks_b
                ],
                "two_best_alignment_fixed": fixed,
                "two_best_alignment_unfixable": unfixable,
                "two_best_alignment_fix_reason": fix_reason,
                "two_best_pairwise_comparisons": cross_row.get("pairwise_comparisons"),
                "two_best_identical_shortcuts": cross_row.get("identical_shortcuts"),
                "two_best_content_filter_ties": cross_row.get("content_filter_ties"),
                "two_best_duplicate_task_references": cross_row.get(
                    "duplicate_task_references"
                ),
            }
        )
        output_rows.append(output_row)
        filtered_source_rows.append(source_row)
        mask_rows.append(
            {
                "doc_id": doc_id,
                "tgt_lang": lang,
                "cross_file": f"{lang}-winner-cross.jsonl",
                "check_kind": kind,
                "source_metric": source_metric,
                "model_a_name": model_infos["model_a"]["name"],
                "model_b_name": model_infos["model_b"]["name"],
                "selected_model_name": selected_name,
                "selected_model_side": selected_side,
                "selected_best_idx": selected_idx,
                "selected_best_passed": selected_passed,
                "model_a_alignment_mask": mask_a,
                "model_b_alignment_mask": mask_b,
                "model_a_valid_hypothesis_indices": valid_a,
                "model_b_valid_hypothesis_indices": valid_b,
                "model_a_hypothesis_metrics": [check["hypothesis_metric"] for check in checks_a],
                "model_b_hypothesis_metrics": [check["hypothesis_metric"] for check in checks_b],
                "fixed": fixed,
                "unfixable": unfixable,
                "fix_reason": fix_reason,
                "final_model_name": final_candidate["model_name"],
                "final_model_side": final_candidate["side"],
                "final_hypo_key": final_candidate["hypo_key"],
            }
        )

    report = {
        "source": str(source_path),
        "cross_dir": str(cross_dir),
        "model_a_results_dir": str(model_a_results_dir),
        "model_b_results_dir": str(model_b_results_dir),
        "model_a_matrix_dir": str(model_a_matrix_dir),
        "model_b_matrix_dir": str(model_b_matrix_dir),
        "output": str(out_path),
        "strict": args.strict,
        "langs": args.langs,
        "total_source_rows": len(source_rows),
        "written_rows": len(output_rows),
        "kept_count": kept_count,
        "selected_invalid_count": selected_invalid_count,
        "fixed_count": fixed_count,
        "cross_model_fix_count": cross_model_fix_count,
        "unfixable_count": unfixable_count,
        "no_valid_count": no_valid_count,
        "failure_count": len(failures),
        "failures_preview": failures[:50],
        "kind_counts": kind_counts,
        "fix_preview": fixes[:20],
    }

    if args.strict and failures:
        if args.report_json is not None:
            args.report_json.parent.mkdir(parents=True, exist_ok=True)
            args.report_json.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        raise SystemExit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.mask_out is not None:
        args.mask_out.parent.mkdir(parents=True, exist_ok=True)
        with args.mask_out.open("w", encoding="utf-8") as handle:
            for row in mask_rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.filtered_source_out is not None:
        args.filtered_source_out.parent.mkdir(parents=True, exist_ok=True)
        with args.filtered_source_out.open("w", encoding="utf-8") as handle:
            for row in filtered_source_rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.fixes_jsonl is not None:
        args.fixes_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with args.fixes_jsonl.open("w", encoding="utf-8") as handle:
            for row in fixes:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    if args.report_json is not None:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    print(f"source:  {source_path}")
    print(f"cross:   {cross_dir}")
    print(f"output:  {out_path}")
    if args.mask_out is not None:
        print(f"mask:    {args.mask_out.resolve()}")
    if args.filtered_source_out is not None:
        print(f"source-filtered: {args.filtered_source_out.resolve()}")
    print(
        "TWO-BEST EXPORT "
        f"total={len(source_rows)} written={len(output_rows)} kept={kept_count} "
        f"selected_invalid={selected_invalid_count} fixed={fixed_count} "
        f"cross_model_fix={cross_model_fix_count} unfixable={unfixable_count} "
        f"no_valid={no_valid_count} failures={len(failures)}"
    )
    if failures:
        print(f"WARN failures ({len(failures)}): {preview(failures, limit=10)}")


if __name__ == "__main__":
    main()
