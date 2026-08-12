import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Set, Tuple


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from annotation_utils import (  # noqa: E402
    ANNOTATION_COLUMNS,
    clean_text,
    empty_annotation_fields,
    load_jsonl,
    load_optional_jsonl_by_doc_id,
    rows_by_doc_id,
    select_items_stably,
    show_model_b_in_slot_a,
)


DEFAULT_STRATEGY_NAME = "best_of_8_judge_selected"


def load_excluded_doc_ids(snapshot_root, exclude_snapshot_ids, language_pair, comparison_name):
    excluded_doc_ids = set()  # type: Set[str]
    if not exclude_snapshot_ids:
        return excluded_doc_ids

    for snapshot_id in exclude_snapshot_ids:
        comparison_dir = snapshot_root / snapshot_id / language_pair / comparison_name
        if not comparison_dir.is_dir():
            raise FileNotFoundError("Exclude snapshot directory not found: {}".format(comparison_dir))
        internal_paths = sorted(comparison_dir.glob("*.internal.json"))
        if not internal_paths:
            raise FileNotFoundError(
                "No internal exports found under exclude snapshot directory: {}".format(comparison_dir)
            )
        for internal_path in internal_paths:
            payload = json.loads(internal_path.read_text(encoding="utf-8"))
            for record in payload.get("records", []):
                if isinstance(record, dict) and "doc_id" in record:
                    excluded_doc_ids.add(str(record["doc_id"]))
    return excluded_doc_ids


def candidate_payload(judged_row, model_name):
    return {
        "model_name": model_name,
        "doc_id": str(judged_row["doc_id"]),
        "judge_model": judged_row.get("judge_model"),
        "judge_source_model": judged_row.get("judge_source_model"),
        "judge_best_idx": judged_row.get("judge_best_idx"),
        "judge_best_hypo_key": judged_row.get("judge_best_hypo_key"),
        "judge_best_hypothesis": clean_text(judged_row.get("judge_best_hypothesis")),
        "judge_scores": judged_row.get("judge_scores"),
        "judge_win_rates": judged_row.get("judge_win_rates"),
        "judge_pairs_judged": judged_row.get("judge_pairs_judged"),
        "judge_identical_pairs_auto_tied": judged_row.get("judge_identical_pairs_auto_tied"),
    }


def build_internal_record(
    item_id,
    doc_id,
    language_pair,
    source_text,
    aligned_input_row,
    model_a,
    model_b,
    model_a_row,
    model_b_row,
    seed,
    snapshot_id,
    strategy_name,
):
    algorithm_a_payload = candidate_payload(model_a_row, model_name=model_a)
    algorithm_b_payload = candidate_payload(model_b_row, model_name=model_b)

    show_b_in_a = show_model_b_in_slot_a(seed=seed, doc_id=doc_id)
    if show_b_in_a:
        slot_a_label = model_b
        slot_a_payload = algorithm_b_payload
        slot_b_label = model_a
        slot_b_payload = algorithm_a_payload
    else:
        slot_a_label = model_a
        slot_a_payload = algorithm_a_payload
        slot_b_label = model_b
        slot_b_payload = algorithm_b_payload

    internal_record = {
        "item_id": item_id,
        "doc_id": doc_id,
        "language_pair": language_pair,
        "source": source_text,
        "hypothesis_A": slot_a_payload["judge_best_hypothesis"],
        "hypothesis_B": slot_b_payload["judge_best_hypothesis"],
        "A_candidate_label": slot_a_label,
        "B_candidate_label": slot_b_label,
        "A_candidate": slot_a_payload,
        "B_candidate": slot_b_payload,
        "slot_A_is_model_b": bool(show_b_in_a),
        "strategy_name": strategy_name,
        "model_a": model_a,
        "model_b": model_b,
        "model_a_candidate": algorithm_a_payload,
        "model_b_candidate": algorithm_b_payload,
        "sample_seed": seed,
        "snapshot_id": snapshot_id,
        "judge_model": model_a_row.get("judge_model") or model_b_row.get("judge_model"),
        "source_metadata": {
            "instruction": None if aligned_input_row is None else aligned_input_row.get("instruction"),
            "multimodal_instruction": None if aligned_input_row is None else aligned_input_row.get("multimodal_instruction"),
            "multimodal_input_path": None if aligned_input_row is None else aligned_input_row.get("multimodal_input_path"),
            "tgt_lang": model_a_row.get("tgt_lang") or model_b_row.get("tgt_lang"),
        },
    }

    human_row = {
        "item_id": item_id,
        "src": source_text,
        "hypo_A": slot_a_payload["judge_best_hypothesis"],
        "hypo_B": slot_b_payload["judge_best_hypothesis"],
    }
    human_row.update(empty_annotation_fields())
    return internal_record, human_row


def export_language(
    language_code,
    judged_root,
    aligned_inputs_root,
    snapshot_root,
    snapshot_id,
    sample_size,
    seed,
    model_a,
    model_b,
    strategy_name,
    exclude_snapshot_ids,
):
    language_pair = "en-{}".format(language_code)
    model_a_path = judged_root / model_a / "{}.jsonl".format(language_pair)
    model_b_path = judged_root / model_b / "{}.jsonl".format(language_pair)
    if not model_a_path.is_file():
        raise FileNotFoundError("Missing judged file for model A: {}".format(model_a_path))
    if not model_b_path.is_file():
        raise FileNotFoundError("Missing judged file for model B: {}".format(model_b_path))

    aligned_inputs_path = None if aligned_inputs_root is None else aligned_inputs_root / "{}.jsonl".format(language_pair)
    aligned_by_doc_id = load_optional_jsonl_by_doc_id(aligned_inputs_path)

    rows_a_by_doc_id = rows_by_doc_id(load_jsonl(model_a_path))
    rows_b_by_doc_id = rows_by_doc_id(load_jsonl(model_b_path))
    common_doc_ids = sorted(set(rows_a_by_doc_id) & set(rows_b_by_doc_id))
    if not common_doc_ids:
        raise ValueError("No shared doc_ids between {} and {}".format(model_a_path, model_b_path))

    comparison_name = "{}_vs_{}".format(model_a, model_b)
    excluded_doc_ids = load_excluded_doc_ids(
        snapshot_root=snapshot_root,
        exclude_snapshot_ids=exclude_snapshot_ids,
        language_pair=language_pair,
        comparison_name=comparison_name,
    )
    eligible_doc_ids = [doc_id for doc_id in common_doc_ids if doc_id not in excluded_doc_ids]
    selected_doc_ids = select_items_stably(
        eligible_doc_ids,
        sample_size=sample_size,
        seed=seed,
    )
    if sample_size is not None and len(selected_doc_ids) < sample_size:
        raise ValueError(
            "Requested sample_size={}, but only {} eligible docs remain after excluding {} docs.".format(
                sample_size,
                len(selected_doc_ids),
                len(excluded_doc_ids),
            )
        )

    output_dir = snapshot_root / snapshot_id / language_pair / comparison_name
    output_dir.mkdir(parents=True, exist_ok=True)
    internal_path = output_dir / "{}.internal.json".format(strategy_name)
    human_path = output_dir / "{}_human.csv".format(strategy_name)

    internal_records = []  # type: List[Dict[str, Any]]
    human_rows = []  # type: List[Dict[str, str]]
    for item_number, doc_id in enumerate(selected_doc_ids, start=1):
        row_a = rows_a_by_doc_id[doc_id]
        row_b = rows_b_by_doc_id[doc_id]
        source_text = clean_text(row_a.get("source_doc") or row_b.get("source_doc"))
        aligned_row = aligned_by_doc_id.get(doc_id)
        item_id = "item_{:04d}".format(item_number)
        internal_record, human_row = build_internal_record(
            item_id=item_id,
            doc_id=doc_id,
            language_pair=language_pair,
            source_text=source_text,
            aligned_input_row=aligned_row,
            model_a=model_a,
            model_b=model_b,
            model_a_row=row_a,
            model_b_row=row_b,
            seed=seed,
            snapshot_id=snapshot_id,
            strategy_name=strategy_name,
        )
        internal_records.append(internal_record)
        human_rows.append(human_row)

    export_payload = {
        "schema_version": "judge_best_forced_choice_human_export_v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": snapshot_id,
        "strategy_name": strategy_name,
        "comparison_name": comparison_name,
        "language_pair": language_pair,
        "model_a": model_a,
        "model_b": model_b,
        "judged_root": str(judged_root),
        "aligned_inputs_path": str(aligned_inputs_path) if aligned_inputs_path is not None else None,
        "seed": seed,
        "randomization_scheme": "sha256(seed, namespace, doc_id)",
        "requested_sample_size": sample_size,
        "exported_sample_size": len(internal_records),
        "exclude_snapshot_ids": exclude_snapshot_ids,
        "excluded_doc_ids_count": len(excluded_doc_ids),
        "records": internal_records,
    }
    internal_path.write_text(
        json.dumps(export_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with human_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["item_id", "src", "hypo_A", "hypo_B"] + ANNOTATION_COLUMNS,
        )
        writer.writeheader()
        writer.writerows(human_rows)

    print(
        "Wrote {} blinded rows for {} to {} and {}".format(
            len(human_rows),
            language_pair,
            internal_path,
            human_path,
        )
    )
    return [internal_path, human_path]


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Export blinded pairwise human-annotation CSVs comparing judge-selected best hypotheses "
            "from two judged model output sets."
        )
    )
    parser.add_argument("--lang", required=True, help="Target language code suffix, e.g. ar_AR, ru_RU, zh_CN.")
    parser.add_argument(
        "--judged-root",
        type=Path,
        default=Path("results/gemini-2.5-flash/judged"),
        help="Root containing nested judged exports by source model.",
    )
    parser.add_argument(
        "--aligned-inputs-root",
        type=Path,
        default=Path("results/gemini-3.5-flash/aligned_inputs"),
        help="Optional root containing aligned input jsonl files.",
    )
    parser.add_argument(
        "--snapshot-root",
        type=Path,
        default=Path("results/human_annotation/snapshots"),
        help="Root directory where snapshot exports are written.",
    )
    parser.add_argument("--snapshot-id", type=str, required=True, help="Snapshot id.")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Number of shared docs to export. Omit to export all shared docs in shuffled order.",
    )
    parser.add_argument("--seed", type=int, default=20260630, help="Seed used for doc sampling and slot shuffling.")
    parser.add_argument("--model-a", type=str, default="gemini-3.5-flash", help="Source model label for side A.")
    parser.add_argument("--model-b", type=str, default="gpt-5.5", help="Source model label for side B.")
    parser.add_argument("--strategy-name", type=str, default=DEFAULT_STRATEGY_NAME, help="Output strategy name.")
    parser.add_argument(
        "--exclude-snapshot-id",
        action="append",
        default=[],
        help="Snapshot id whose exported doc_ids should be excluded. May be repeated.",
    )
    args = parser.parse_args()
    if args.sample_size is not None and args.sample_size <= 0:
        parser.error("--sample-size must be a positive integer when provided.")
    return args


def main():
    args = parse_args()
    export_language(
        language_code=args.lang,
        judged_root=args.judged_root,
        aligned_inputs_root=args.aligned_inputs_root,
        snapshot_root=args.snapshot_root,
        snapshot_id=args.snapshot_id,
        sample_size=args.sample_size,
        seed=args.seed,
        model_a=args.model_a,
        model_b=args.model_b,
        strategy_name=args.strategy_name,
        exclude_snapshot_ids=args.exclude_snapshot_id,
    )


if __name__ == "__main__":
    main()
