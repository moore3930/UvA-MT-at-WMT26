import argparse
import json
import math
from pathlib import Path
import sys


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from annotation_utils import (  # noqa: E402
    create_labelled_csv_reader,
    load_internal_records,
    match_internal_and_labelled_pairs,
    normalize_binary_choice,
    row_is_effectively_blank,
)


def empty_summary_counts():
    return {
        "model_a_wins": 0,
        "model_b_wins": 0,
        "tie": 0,
        "unclear": 0,
        "blank": 0,
    }


def proportion_standard_error(numerator, denominator):
    if denominator <= 0:
        return 0.0
    proportion = float(numerator) / float(denominator)
    return math.sqrt(proportion * (1.0 - proportion) / float(denominator))


def summarize_counts(counts, total_items):
    decisive = counts["model_a_wins"] + counts["model_b_wins"]
    labelled = decisive + counts["tie"] + counts["unclear"]
    model_a_win_rate_decisive = (
        float(counts["model_a_wins"]) / decisive if decisive else 0.0
    )
    model_b_win_rate_decisive = (
        float(counts["model_b_wins"]) / decisive if decisive else 0.0
    )
    model_a_share_all = (
        float(counts["model_a_wins"]) / total_items if total_items else 0.0
    )
    model_b_share_all = (
        float(counts["model_b_wins"]) / total_items if total_items else 0.0
    )
    tie_share_all = float(counts["tie"]) / total_items if total_items else 0.0
    unclear_share_all = (
        float(counts["unclear"]) / total_items if total_items else 0.0
    )
    return {
        "counts": dict(counts),
        "total_items": total_items,
        "labelled_items": labelled,
        "blank_items": counts["blank"],
        "decisive_items": decisive,
        "model_a_win_rate_decisive": model_a_win_rate_decisive,
        "model_b_win_rate_decisive": model_b_win_rate_decisive,
        "model_a_win_rate_decisive_sem": proportion_standard_error(
            counts["model_a_wins"], decisive
        ),
        "model_b_win_rate_decisive_sem": proportion_standard_error(
            counts["model_b_wins"], decisive
        ),
        "model_a_share_all": model_a_share_all,
        "model_b_share_all": model_b_share_all,
        "tie_share_all": tie_share_all,
        "unclear_share_all": unclear_share_all,
        "model_a_share_all_sem": proportion_standard_error(
            counts["model_a_wins"], total_items
        ),
        "model_b_share_all_sem": proportion_standard_error(
            counts["model_b_wins"], total_items
        ),
        "tie_share_all_sem": proportion_standard_error(counts["tie"], total_items),
        "unclear_share_all_sem": proportion_standard_error(
            counts["unclear"], total_items
        ),
        "decisive_margin": (
            float(counts["model_a_wins"] - counts["model_b_wins"]) / decisive
            if decisive
            else 0.0
        ),
    }


def summarize_snapshot(snapshot_root, labelled_root):
    pairs = match_internal_and_labelled_pairs(
        snapshot_root=snapshot_root,
        labelled_root=labelled_root,
    )
    recovered_rows = []
    language_summaries = {}
    overall_counts = empty_summary_counts()
    overall_total_items = 0
    model_a_name = None
    model_b_name = None

    for internal_json_path, labelled_csv_path in pairs:
        payload, records_by_item_id = load_internal_records(internal_json_path)
        language_pair = str(payload.get("language_pair") or internal_json_path.parent.parent.name)
        model_a = str(payload.get("model_a"))
        model_b = str(payload.get("model_b"))
        if model_a_name is None:
            model_a_name = model_a
        if model_b_name is None:
            model_b_name = model_b
        if model_a != model_a_name or model_b != model_b_name:
            raise ValueError(
                "Mixed model comparison families are not supported in one summary run: "
                "expected {} vs {}, got {} vs {}".format(
                    model_a_name,
                    model_b_name,
                    model_a,
                    model_b,
                )
            )

        counts = empty_summary_counts()
        total_items = len(records_by_item_id)
        overall_total_items += total_items

        with labelled_csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = create_labelled_csv_reader(handle)
            for row in reader:
                if row_is_effectively_blank(row):
                    continue
                item_id = str(row["item_id"])
                if item_id not in records_by_item_id:
                    raise ValueError("Missing item_id={!r} in {}".format(item_id, internal_json_path))
                record = records_by_item_id[item_id]
                choice = normalize_binary_choice(row.get("label", ""))
                preferred_model = None
                if choice is None:
                    counts["blank"] += 1
                elif choice == "A":
                    preferred_model = str(record["A_candidate_label"])
                    if preferred_model == model_a:
                        counts["model_a_wins"] += 1
                    elif preferred_model == model_b:
                        counts["model_b_wins"] += 1
                    else:
                        raise ValueError("Unknown preferred model for choice A: {}".format(preferred_model))
                elif choice == "B":
                    preferred_model = str(record["B_candidate_label"])
                    if preferred_model == model_a:
                        counts["model_a_wins"] += 1
                    elif preferred_model == model_b:
                        counts["model_b_wins"] += 1
                    else:
                        raise ValueError("Unknown preferred model for choice B: {}".format(preferred_model))
                elif choice == "tie":
                    counts["tie"] += 1
                elif choice == "unclear":
                    counts["unclear"] += 1
                else:
                    raise ValueError("Unexpected normalized choice: {}".format(choice))

                recovered_rows.append(
                    {
                        "snapshot_id": payload.get("snapshot_id"),
                        "language_pair": language_pair,
                        "item_id": item_id,
                        "doc_id": record.get("doc_id"),
                        "model_a": model_a,
                        "model_b": model_b,
                        "A_candidate_label": record.get("A_candidate_label"),
                        "B_candidate_label": record.get("B_candidate_label"),
                        "choice": choice,
                        "preferred_model": preferred_model,
                        "source": record.get("source"),
                        "hypothesis_A": record.get("hypothesis_A"),
                        "hypothesis_B": record.get("hypothesis_B"),
                    }
                )

        for key, value in counts.items():
            overall_counts[key] += value

        language_summaries[language_pair] = {
            "language_pair": language_pair,
            "comparison_name": payload.get("comparison_name"),
            "model_a": model_a,
            "model_b": model_b,
            "summary": summarize_counts(counts, total_items=total_items),
            "paths": {
                "internal_json_path": str(internal_json_path),
                "labelled_csv_path": str(labelled_csv_path),
            },
        }

    summary_payload = {
        "schema_version": "human_label_summary_v3",
        "label_space": ["A", "B", "tie", "unclear"],
        "model_a": model_a_name,
        "model_b": model_b_name,
        "languages": language_summaries,
        "overall": summarize_counts(overall_counts, total_items=overall_total_items),
    }
    return summary_payload, recovered_rows


def write_outputs(output_dir, summary_payload, recovered_rows):
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path = output_dir / "manual_label_raw_statistics_all_languages.json"
    recovered_path = output_dir / "recovered_votes_all_languages.jsonl"
    summary_path.write_text(
        json.dumps(summary_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with recovered_path.open("w", encoding="utf-8") as handle:
        for row in recovered_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return [summary_path, recovered_path]


def print_summary(summary_payload):
    model_a = summary_payload["model_a"]
    model_b = summary_payload["model_b"]
    print("Comparison: {} vs {}".format(model_a, model_b))
    for language_pair, payload in sorted(summary_payload["languages"].items()):
        summary = payload["summary"]
        counts = summary["counts"]
        print(
            "{}: {}={}, {}={}, tie={}, unclear={}, blank={}, decisive_margin={:.3f}".format(
                language_pair,
                model_a,
                counts["model_a_wins"],
                model_b,
                counts["model_b_wins"],
                counts["tie"],
                counts["unclear"],
                counts["blank"],
                summary["decisive_margin"],
            )
        )
    overall = summary_payload["overall"]
    counts = overall["counts"]
    print(
        "overall: {}={}, {}={}, tie={}, unclear={}, blank={}, decisive_margin={:.3f}".format(
            model_a,
            counts["model_a_wins"],
            model_b,
            counts["model_b_wins"],
            counts["tie"],
            counts["unclear"],
            counts["blank"],
            overall["decisive_margin"],
        )
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Recover blinded human labels by matching labelled CSVs back to their internal exports "
            "and write per-language and overall summary statistics."
        )
    )
    parser.add_argument("--snapshot-id", type=str, required=True, help="Snapshot id.")
    parser.add_argument(
        "--snapshot-root",
        type=Path,
        default=Path("results/human_annotation/snapshots"),
        help="Root directory containing original snapshot exports.",
    )
    parser.add_argument(
        "--labelled-root",
        type=Path,
        default=Path("results/human_annotation/labelled_snapshot"),
        help="Root directory containing downloaded labelled snapshot CSVs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory where summary JSON and recovered JSONL should be written.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    snapshot_root = args.snapshot_root / args.snapshot_id
    labelled_root = args.labelled_root / args.snapshot_id
    output_dir = args.output_dir or Path("results/human_annotation/plots") / args.snapshot_id

    summary_payload, recovered_rows = summarize_snapshot(
        snapshot_root=snapshot_root,
        labelled_root=labelled_root,
    )
    written = write_outputs(
        output_dir=output_dir,
        summary_payload=summary_payload,
        recovered_rows=recovered_rows,
    )
    print_summary(summary_payload)
    for path in written:
        print("wrote: {}".format(path))


if __name__ == "__main__":
    main()
