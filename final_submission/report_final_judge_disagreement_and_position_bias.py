#!/usr/bin/env python3
"""Report AB-vs-BA disagreement and A/B position counts for the final submission."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from common import iter_jsonl


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FINAL_PRELIM = (
    REPO_ROOT
    / "final_submission"
    / "out"
    / "merge_two_submissions"
    / "gemini-3.5-flash__gpt-final_rubric-v5-structured"
    / "preliminary_final.jsonl"
)
DEFAULT_NEW_CROSS_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-3.5-flash"
    / "experiments"
    / "two-best"
    / "gemini-3.5-flash__gpt-final_rubric-v5-structured"
    / "cross-matrix"
)
DEFAULT_OLD_CROSS_DIR = (
    REPO_ROOT
    / "results"
    / "gemini-2.5-flash"
    / "artifacts"
    / "two-best"
    / "gemini-3.5-flash__gpt-final"
    / "cross-matrix"
)
DEFAULT_OUT = DEFAULT_FINAL_PRELIM.parent / "reports" / "final_judge_disagreement_and_position_bias.md"
DEFAULT_JSON = DEFAULT_FINAL_PRELIM.parent / "reports" / "final_judge_disagreement_and_position_bias.json"
DEFAULT_SELECTED_LANGS = (
    "arz_Arab,bel_Cyrl,ces_Latn,deu_Latn,ekk_Latn,hye_Armn,ind_Latn,isl_Latn,"
    "jpn_Jpan,kaz_Cyrl,kor_Hang,lij_Latn,lld_Latn,rus_Cyrl,sme_Latn,tha_Thai,"
    "ukr_Cyrl,zho_Hans,zho_Hant_TW"
)


@dataclass
class LangStats:
    docs: int = 0
    unique_pairs: int = 0
    ab_ba_disagreements: int = 0
    position_a_wins: int = 0
    position_b_wins: int = 0
    ties: int = 0

    @property
    def disagreement_pct(self) -> float:
        if self.unique_pairs == 0:
            return 0.0
        return 100.0 * self.ab_ba_disagreements / self.unique_pairs

    @property
    def position_a_pct(self) -> float:
        total = self.position_a_wins + self.position_b_wins + self.ties
        if total == 0:
            return 0.0
        return 100.0 * self.position_a_wins / total

    @property
    def position_b_pct(self) -> float:
        total = self.position_a_wins + self.position_b_wins + self.ties
        if total == 0:
            return 0.0
        return 100.0 * self.position_b_wins / total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a report of AB-vs-BA disagreement and A/B position counts "
            "for the final merged submission."
        )
    )
    parser.add_argument("--final-prelim", type=Path, default=DEFAULT_FINAL_PRELIM)
    parser.add_argument("--new-cross-dir", type=Path, default=DEFAULT_NEW_CROSS_DIR)
    parser.add_argument("--old-cross-dir", type=Path, default=DEFAULT_OLD_CROSS_DIR)
    parser.add_argument("--selected-langs", default=DEFAULT_SELECTED_LANGS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    return parser.parse_args()


def parse_langs(csv: str) -> set[str]:
    return {part.strip() for part in csv.split(",") if part.strip()}


def language_from_path(path: Path) -> str:
    suffix = "-winner-cross"
    stem = path.stem
    if not stem.endswith(suffix):
        raise SystemExit(f"unexpected cross filename: {path.name}")
    return stem[: -len(suffix)]


def score_counts(values: list[int]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for value in values:
        if value == 1:
            counts["a"] += 1
        elif value == -1:
            counts["b"] += 1
        elif value == 0:
            counts["tie"] += 1
        else:
            raise SystemExit(f"unexpected score value: {value!r}")
    return counts


def pair_disagreement(forward: int, reverse: int) -> bool:
    return forward != -reverse


def load_final_langs(path: Path) -> list[str]:
    langs: list[str] = []
    seen: set[str] = set()
    for line_no, row in iter_jsonl(path):
        lang = row.get("tgt_lang")
        if not isinstance(lang, str):
            raise SystemExit(f"{path}:{line_no}: expected string tgt_lang")
        if lang not in seen:
            seen.add(lang)
            langs.append(lang)
    return langs


def summarize_cross_file(path: Path) -> tuple[LangStats, dict[str, str]]:
    stats = LangStats()
    model_names: dict[str, str] = {}
    for line_no, row in iter_jsonl(path):
        stats.docs += 1

        model_a_name = row.get("model_a_name")
        model_b_name = row.get("model_b_name")
        if not isinstance(model_a_name, str) or not isinstance(model_b_name, str):
            raise SystemExit(f"{path}:{line_no}: expected model_a_name/model_b_name strings")
        model_names["model_a_name"] = model_a_name
        model_names["model_b_name"] = model_b_name

        arrays = {}
        for key in (
            "model_a_best_vs_model_b_pool",
            "model_b_pool_vs_model_a_best",
            "model_b_best_vs_model_a_pool",
            "model_a_pool_vs_model_b_best",
        ):
            value = row.get(key)
            if not isinstance(value, list) or not all(isinstance(v, int) for v in value):
                raise SystemExit(f"{path}:{line_no}: expected integer list for {key}")
            arrays[key] = value

        counts = Counter()
        for key in arrays:
            counts.update(score_counts(arrays[key]))
        stats.position_a_wins += counts["a"]
        stats.position_b_wins += counts["b"]
        stats.ties += counts["tie"]

        best_a = row.get("model_a_best_idx")
        best_b = row.get("model_b_best_idx")
        if not isinstance(best_a, int) or not isinstance(best_b, int):
            raise SystemExit(f"{path}:{line_no}: expected integer best indices")

        forward_a = arrays["model_a_best_vs_model_b_pool"]
        reverse_a = arrays["model_b_pool_vs_model_a_best"]
        if len(forward_a) != len(reverse_a):
            raise SystemExit(f"{path}:{line_no}: mismatched A/B pool lengths")
        for j in range(len(forward_a)):
            stats.unique_pairs += 1
            if pair_disagreement(forward_a[j], reverse_a[j]):
                stats.ab_ba_disagreements += 1

        forward_b = arrays["model_a_pool_vs_model_b_best"]
        reverse_b = arrays["model_b_best_vs_model_a_pool"]
        if len(forward_b) != len(reverse_b):
            raise SystemExit(f"{path}:{line_no}: mismatched B/A pool lengths")
        for i in range(len(forward_b)):
            if i == best_a:
                continue
            stats.unique_pairs += 1
            if pair_disagreement(forward_b[i], reverse_b[i]):
                stats.ab_ba_disagreements += 1

    return stats, model_names


def main() -> None:
    args = parse_args()
    final_prelim = args.final_prelim.resolve()
    new_cross_dir = args.new_cross_dir.resolve()
    old_cross_dir = args.old_cross_dir.resolve()
    out_path = args.out.resolve()
    json_path = args.json_out.resolve()
    selected_langs = parse_langs(args.selected_langs)

    for path in (final_prelim, new_cross_dir, old_cross_dir):
        if not path.exists():
            raise SystemExit(f"missing path: {path}")

    langs = load_final_langs(final_prelim)
    per_lang: dict[str, LangStats] = {}
    totals = LangStats()
    model_names: dict[str, str] | None = None
    source_dirs: dict[str, str] = {}

    for lang in langs:
        cross_dir = new_cross_dir if lang in selected_langs else old_cross_dir
        source_dirs[lang] = str(cross_dir)
        path = cross_dir / f"{lang}-winner-cross.jsonl"
        if not path.is_file():
            raise SystemExit(f"missing cross file for {lang}: {path}")

        stats, names = summarize_cross_file(path)
        if model_names is None:
            model_names = names
        elif names != model_names:
            raise SystemExit(f"{lang}: model names differ across cross files")

        per_lang[lang] = stats
        totals.docs += stats.docs
        totals.unique_pairs += stats.unique_pairs
        totals.ab_ba_disagreements += stats.ab_ba_disagreements
        totals.position_a_wins += stats.position_a_wins
        totals.position_b_wins += stats.position_b_wins
        totals.ties += stats.ties

    assert model_names is not None
    md_lines = [
        "# Final Judge Disagreement And Position Bias",
        "",
        f"- Final preliminary input: `{final_prelim}`",
        f"- Selected-language cross dir: `{new_cross_dir}`",
        f"- Older-language cross dir: `{old_cross_dir}`",
        f"- Model A: `{model_names['model_a_name']}`",
        f"- Model B: `{model_names['model_b_name']}`",
        "- `A/B disagreement` means the judge gave inconsistent results for the same unordered pair when the prompt order was swapped.",
        "- `position A` / `position B` count wins for the first vs second hypothesis position in the judged prompt, not the underlying model identity.",
        "",
        "| lang | docs | unique pairs | A/B disagreements | disagreement % | pos A wins | pos B wins | ties | pos A % | pos B % |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| ALL | {totals.docs} | {totals.unique_pairs} | {totals.ab_ba_disagreements} | "
            f"{totals.disagreement_pct:.2f}% | {totals.position_a_wins} | {totals.position_b_wins} | "
            f"{totals.ties} | {totals.position_a_pct:.2f}% | {totals.position_b_pct:.2f}% |"
        ),
    ]

    rows_json = []
    for lang in langs:
        stats = per_lang[lang]
        md_lines.append(
            f"| {lang} | {stats.docs} | {stats.unique_pairs} | {stats.ab_ba_disagreements} | "
            f"{stats.disagreement_pct:.2f}% | {stats.position_a_wins} | {stats.position_b_wins} | "
            f"{stats.ties} | {stats.position_a_pct:.2f}% | {stats.position_b_pct:.2f}% |"
        )
        rows_json.append(
            {
                "lang": lang,
                "docs": stats.docs,
                "unique_pairs": stats.unique_pairs,
                "ab_ba_disagreements": stats.ab_ba_disagreements,
                "disagreement_pct": round(stats.disagreement_pct, 6),
                "position_a_wins": stats.position_a_wins,
                "position_b_wins": stats.position_b_wins,
                "ties": stats.ties,
                "position_a_pct": round(stats.position_a_pct, 6),
                "position_b_pct": round(stats.position_b_pct, 6),
                "cross_dir": source_dirs[lang],
            }
        )

    report = {
        "final_prelim": str(final_prelim),
        "new_cross_dir": str(new_cross_dir),
        "old_cross_dir": str(old_cross_dir),
        "selected_langs": sorted(selected_langs),
        "model_names": model_names,
        "totals": {
            "docs": totals.docs,
            "unique_pairs": totals.unique_pairs,
            "ab_ba_disagreements": totals.ab_ba_disagreements,
            "disagreement_pct": totals.disagreement_pct,
            "position_a_wins": totals.position_a_wins,
            "position_b_wins": totals.position_b_wins,
            "ties": totals.ties,
            "position_a_pct": totals.position_a_pct,
            "position_b_pct": totals.position_b_pct,
        },
        "rows": rows_json,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"final_prelim: {final_prelim}")
    print(f"markdown: {out_path}")
    print(f"json: {json_path}")
    print(
        "totals: docs=%d unique_pairs=%d disagreements=%d posA=%d posB=%d ties=%d"
        % (
            totals.docs,
            totals.unique_pairs,
            totals.ab_ba_disagreements,
            totals.position_a_wins,
            totals.position_b_wins,
            totals.ties,
        )
    )


if __name__ == "__main__":
    main()
