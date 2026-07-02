#!/usr/bin/env python3
"""Select final hypotheses using judge scores plus structural-alignment masks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from common import iter_jsonl, load_matrix_rows, load_source_rows, preview, wanted_langs


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "wmt26_genmt_blindset_filter_parse.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Select final hypotheses in source order, keeping the judged best "
            "when structurally valid and otherwise falling back to the "
            "best-scoring valid hypothesis."
        )
    )
    parser.add_argument("--matrix-dir", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--report-json", type=Path, default=None)
    parser.add_argument("--fixes-jsonl", type=Path, default=None)
    parser.add_argument("--matrix-lang-prefix", default="")
    parser.add_argument("--langs", default="all")
    parser.add_argument("--max-fixes", type=int, default=20)
    parser.add_argument(
        "--strict",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="fail on missing rows or fix-limit violations (default: true)",
    )
    return parser.parse_args()


def load_masks(mask_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    masks: dict[tuple[str, str], dict[str, Any]] = {}
    duplicates: list[str] = []
    for line_no, record in iter_jsonl(mask_path):
        doc_id = record.get("doc_id")
        lang = record.get("tgt_lang")
        if not isinstance(doc_id, str) or not isinstance(lang, str):
            raise SystemExit(f"{mask_path}:{line_no}: expected string doc_id and tgt_lang")
        key = (lang, doc_id)
        if key in masks:
            duplicates.append(f"{lang}:{doc_id}")
            continue
        masks[key] = record
    if duplicates:
        raise SystemExit(f"duplicate mask rows: {preview(sorted(duplicates), limit=10)}")
    return masks


def choose_best_valid(record: dict[str, Any], valid_indices: list[int]) -> int:
    scores = record.get("score")
    hypos = record.get("hypos")
    if not isinstance(scores, list) or not isinstance(hypos, list) or len(scores) != len(hypos):
        raise SystemExit(
            f"{record.get('doc_id')}: missing or malformed score vector for fallback selection"
        )
    for score in scores:
        if not isinstance(score, (int, float)):
            raise SystemExit(f"{record.get('doc_id')}: non-numeric score in score vector")
    return max(valid_indices, key=lambda idx: (scores[idx], -idx))


def build_output_row(
    source_row: dict[str, Any],
    matrix_info: dict[str, Any],
    selected_idx: int,
    mask_info: dict[str, Any],
    fixed: bool,
    unfixable: bool,
) -> dict[str, Any]:
    record = matrix_info["record"]
    hypos = matrix_info["hypos"]
    out = dict(source_row)
    out["hypothesis"] = hypos[selected_idx]
    out["judge_best_idx"] = selected_idx
    out["judge_best_hypothesis"] = hypos[selected_idx]
    out["judge_original_best_idx"] = matrix_info["best_idx"]
    out["judge_original_best_hypothesis"] = hypos[matrix_info["best_idx"]]
    out["judge_scores"] = record.get("score")
    out["judge_position_disagreements"] = record.get("position_disagreements")
    out["judge_pairs_judged"] = record.get("pairwise_comparisons")
    out["judge_identical_pairs_auto_tied"] = record.get("identical_shortcuts")
    out["judge_matrix_file"] = matrix_info["path"].name
    out["judge_alignment_check_kind"] = mask_info.get("check_kind")
    out["judge_alignment_mask"] = mask_info.get("alignment_mask")
    out["judge_alignment_valid_hypothesis_indices"] = mask_info.get("valid_hypothesis_indices")
    out["judge_alignment_source_metric"] = mask_info.get("source_metric")
    out["judge_alignment_hypothesis_metrics"] = mask_info.get("hypothesis_metrics")
    out["judge_alignment_fixed"] = fixed
    out["judge_alignment_unfixable"] = unfixable
    return out


def main() -> None:
    args = parse_args()
    source_path = args.source.resolve()
    matrix_dir = args.matrix_dir.resolve()
    mask_path = args.mask.resolve()
    out_path = args.out.resolve()
    langs = wanted_langs(args.langs)

    if not source_path.is_file():
        raise SystemExit(f"missing source file: {source_path}")
    if not matrix_dir.is_dir():
        raise SystemExit(f"missing matrix dir: {matrix_dir}")
    if not mask_path.is_file():
        raise SystemExit(f"missing mask file: {mask_path}")

    source_rows, _expected_by_lang = load_source_rows(source_path, langs)
    matrix_by_lang, malformed = load_matrix_rows(matrix_dir, args.matrix_lang_prefix, langs)
    if malformed:
        raise SystemExit(f"malformed matrix data: {preview(malformed, limit=3)}")
    masks = load_masks(mask_path)

    output_rows: list[dict[str, Any]] = []
    fixes: list[dict[str, Any]] = []
    unfixable: list[str] = []
    missing_masks: list[str] = []
    missing_matrix_rows: list[str] = []
    fixed_count = kept_count = unfixable_count = 0

    for source_row in source_rows:
        lang = source_row["tgt_lang"]
        doc_id = source_row["doc_id"]
        key = (lang, doc_id)

        matrix_info = matrix_by_lang.get(lang, {}).get(doc_id)
        if matrix_info is None:
            missing_matrix_rows.append(f"{lang}:{doc_id}")
            continue
        mask_info = masks.get(key)
        if mask_info is None:
            missing_masks.append(f"{lang}:{doc_id}")
            continue

        mask = mask_info.get("alignment_mask")
        valid_indices = mask_info.get("valid_hypothesis_indices")
        if not isinstance(mask, list) or not isinstance(valid_indices, list):
            raise SystemExit(f"{lang}:{doc_id}: malformed alignment mask row")
        if len(mask) != len(matrix_info["hypos"]):
            raise SystemExit(f"{lang}:{doc_id}: mask length does not match hypothesis count")

        original_best = matrix_info["best_idx"]
        if mask[original_best] == 1:
            selected_idx = original_best
            kept_count += 1
            fixed = False
            is_unfixable = False
        else:
            if not valid_indices:
                selected_idx = original_best
                fixed = False
                is_unfixable = True
                unfixable_count += 1
                unfixable.append(f"{lang}:{doc_id}")
            else:
                selected_idx = choose_best_valid(matrix_info["record"], list(valid_indices))
                fixed = True
                is_unfixable = False
                fixed_count += 1
                fixes.append(
                    {
                        "doc_id": doc_id,
                        "tgt_lang": lang,
                        "matrix_file": matrix_info["path"].name,
                        "original_best_idx": original_best,
                        "replacement_best_idx": selected_idx,
                        "alignment_mask": mask,
                        "valid_hypothesis_indices": valid_indices,
                        "scores": matrix_info["record"].get("score"),
                        "check_kind": mask_info.get("check_kind"),
                        "source_metric": mask_info.get("source_metric"),
                        "hypothesis_metrics": mask_info.get("hypothesis_metrics"),
                    }
                )

        output_rows.append(
            build_output_row(
                source_row,
                matrix_info,
                selected_idx,
                mask_info,
                fixed,
                is_unfixable,
            )
        )

    failures = []
    if missing_matrix_rows:
        failures.append(
            f"missing matrix rows ({len(missing_matrix_rows)}): "
            f"{preview(missing_matrix_rows, limit=10)}"
        )
    if missing_masks:
        failures.append(
            f"missing mask rows ({len(missing_masks)}): "
            f"{preview(missing_masks, limit=10)}"
        )
    if fixed_count > args.max_fixes:
        failures.append(
            f"fixed_count={fixed_count} exceeds hard limit max_fixes={args.max_fixes}"
        )

    report = {
        "source": str(source_path),
        "matrix_dir": str(matrix_dir),
        "mask": str(mask_path),
        "output": str(out_path),
        "strict": args.strict,
        "max_fixes": args.max_fixes,
        "total_rows": len(source_rows),
        "written_rows": len(output_rows),
        "kept_count": kept_count,
        "fixed_count": fixed_count,
        "unfixable_count": unfixable_count,
        "missing_matrix_row_count": len(missing_matrix_rows),
        "missing_mask_row_count": len(missing_masks),
        "unfixable_rows_preview": unfixable[:20],
        "failures": failures,
        "fix_preview": fixes[:20],
    }

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

    print(f"source: {source_path}")
    print(f"matrix:  {matrix_dir}")
    print(f"mask:    {mask_path}")
    print(f"output:  {out_path}")
    print(
        "SELECTION "
        f"total={len(source_rows)} kept={kept_count} fixed={fixed_count} "
        f"unfixable={unfixable_count} missing_matrix={len(missing_matrix_rows)} "
        f"missing_mask={len(missing_masks)}"
    )

    if unfixable:
        print(f"WARN unfixable rows ({len(unfixable)}): {preview(unfixable, limit=10)}")

    if failures and args.strict:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"wrote {len(output_rows)} final rows to {out_path}")


if __name__ == "__main__":
    main()
