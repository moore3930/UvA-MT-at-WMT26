#!/usr/bin/env python3
"""Static cost estimator for full round-robin judge runs."""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sequential_scaling import PRICING_PROFILES, lang_name  # noqa: E402
from util.contrastive_judge import (  # noqa: E402
    DEFAULT_RUBRIC,
    build_judge_messages,
    render_rubric,
)

HYPO_RE = re.compile(r"^hypo_(\d+)$")


def parse_args():
    p = argparse.ArgumentParser(
        description="Estimate full round-robin Gemini judge cost without API calls.")
    p.add_argument(
        "--input-dir",
        required=True,
        help="directory containing generated result jsonl files (e.g. results/gemini-3.5-flash)",
    )
    p.add_argument(
        "--model",
        default="gemini-2.5-flash",
        choices=sorted(PRICING_PROFILES),
        help="pricing profile to use",
    )
    p.add_argument(
        "--langs",
        default="all",
        help="comma-separated target languages (e.g. ar_AR,ru_RU) or 'all'",
    )
    p.add_argument(
        "--result-file-prefix",
        default="",
        help="filename prefix before <lang>.jsonl (default: empty)",
    )
    p.add_argument(
        "--src-lang",
        default="English",
        help="source language name used in judge prompts",
    )
    p.add_argument(
        "--rubric-file",
        default="",
        help="optional rubric file to match the intended judge prompt",
    )
    p.add_argument(
        "--json-only",
        action="store_true",
        help="estimate for JSON-only verdict prompts with no free-form explanation",
    )
    p.add_argument(
        "--prompt-chars-per-token",
        type=float,
        default=2.0,
        help="static chars/token approximation for prompt token estimation",
    )
    p.add_argument(
        "--visible-output-tokens-per-call",
        type=float,
        default=20.0,
        help="assumed visible output tokens per judged ordered pair",
    )
    p.add_argument(
        "--thinking-tokens-per-call",
        type=float,
        default=0.0,
        help="assumed thinking tokens per judged ordered pair",
    )
    p.add_argument(
        "--max-hypos",
        type=int,
        default=0,
        help="use only the first N hypotheses per row (0 = all available)",
    )
    p.add_argument(
        "--summary-json",
        default="",
        help="optional JSON summary output path",
    )
    return p.parse_args()


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def extract_hypos(rec: dict, max_hypos: int = 0) -> list[str]:
    idx = sorted(int(m.group(1)) for k in rec for m in [HYPO_RE.match(k)] if m)
    if max_hypos > 0:
        idx = idx[:max_hypos]
    return [rec[f"hypo_{i}"] for i in idx]


def wanted_files(input_dir: Path, langs_arg: str, result_file_prefix: str) -> list[Path]:
    if langs_arg.strip().lower() in {"all", "*"}:
        return sorted(input_dir.glob(f"{result_file_prefix}*.jsonl"))
    langs = [x.strip() for x in langs_arg.split(",") if x.strip()]
    return [input_dir / f"{result_file_prefix}{lang}.jsonl" for lang in langs]


def compute_stats(path: Path, src_lang: str, rubric_text: str, json_only: bool,
                  prompt_chars_per_token: float,
                  visible_output_tokens_per_call: float,
                  thinking_tokens_per_call: float,
                  model: str,
                  max_hypos: int) -> dict:
    docs = 0
    ordered_pairs = 0
    identical_pairs = 0
    prompt_chars_total = 0

    for rec in iter_jsonl(path):
        docs += 1
        hypos = extract_hypos(rec, max_hypos=max_hypos)
        tgt_lang = lang_name(rec.get("tgt_lang") or "")
        source = rec.get("source_doc") or ""
        for i in range(len(hypos)):
            for j in range(len(hypos)):
                if i == j:
                    continue
                if hypos[i] == hypos[j]:
                    identical_pairs += 1
                    continue
                msgs = build_judge_messages(
                    source,
                    hypos[i],
                    hypos[j],
                    src_lang,
                    tgt_lang,
                    rubric_text,
                    require_reason=not json_only,
                )
                prompt_chars_total += (
                    len(msgs[0]["content"]) + len(msgs[1]["content"])
                )
                ordered_pairs += 1

    prompt_tokens_est = prompt_chars_total / prompt_chars_per_token
    visible_output_tokens_est = ordered_pairs * visible_output_tokens_per_call
    thinking_tokens_est = ordered_pairs * thinking_tokens_per_call
    billed_output_tokens_est = visible_output_tokens_est + thinking_tokens_est
    rates = PRICING_PROFILES[model]
    input_cost_usd = (
        prompt_tokens_est / 1_000_000.0 * rates["input_per_million_usd"]
    )
    visible_output_cost_usd = (
        visible_output_tokens_est / 1_000_000.0 * rates["output_per_million_usd"]
    )
    thinking_cost_usd = (
        thinking_tokens_est / 1_000_000.0 * rates["output_per_million_usd"]
    )
    total_cost_usd = input_cost_usd + visible_output_cost_usd + thinking_cost_usd

    return {
        "file": path.name,
        "docs": docs,
        "hypotheses_per_doc": max_hypos if max_hypos > 0 else None,
        "ordered_pairs_to_judge": ordered_pairs,
        "identical_pairs_auto_tied": identical_pairs,
        "prompt_chars_total": prompt_chars_total,
        "avg_prompt_chars_per_call": (
            prompt_chars_total / ordered_pairs if ordered_pairs else 0.0
        ),
        "prompt_tokens_est": prompt_tokens_est,
        "visible_output_tokens_est": visible_output_tokens_est,
        "thinking_tokens_est": thinking_tokens_est,
        "billed_output_tokens_est": billed_output_tokens_est,
        "input_cost_usd": input_cost_usd,
        "visible_output_cost_usd": visible_output_cost_usd,
        "thinking_cost_usd": thinking_cost_usd,
        "total_cost_usd": total_cost_usd,
    }


def main():
    args = parse_args()
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        raise SystemExit(f"input dir not found: {input_dir}")

    rubric_text = (
        Path(args.rubric_file).read_text(encoding="utf-8").strip()
        if args.rubric_file
        else render_rubric(DEFAULT_RUBRIC)
    )

    files = wanted_files(input_dir, args.langs, args.result_file_prefix)
    if not files:
        raise SystemExit(f"no matching result files under {input_dir}")

    summaries = []
    for path in files:
        if not path.exists():
            raise SystemExit(f"result file not found: {path}")
        summaries.append(
            compute_stats(
                path,
                args.src_lang,
                rubric_text,
                args.json_only,
                args.prompt_chars_per_token,
                args.visible_output_tokens_per_call,
                args.thinking_tokens_per_call,
                args.model,
                args.max_hypos,
            )
        )

    totals = {
        "docs": sum(x["docs"] for x in summaries),
        "ordered_pairs_to_judge": sum(x["ordered_pairs_to_judge"] for x in summaries),
        "identical_pairs_auto_tied": sum(x["identical_pairs_auto_tied"] for x in summaries),
        "prompt_chars_total": sum(x["prompt_chars_total"] for x in summaries),
        "prompt_tokens_est": sum(x["prompt_tokens_est"] for x in summaries),
        "visible_output_tokens_est": sum(x["visible_output_tokens_est"] for x in summaries),
        "thinking_tokens_est": sum(x["thinking_tokens_est"] for x in summaries),
        "billed_output_tokens_est": sum(x["billed_output_tokens_est"] for x in summaries),
        "input_cost_usd": sum(x["input_cost_usd"] for x in summaries),
        "visible_output_cost_usd": sum(x["visible_output_cost_usd"] for x in summaries),
        "thinking_cost_usd": sum(x["thinking_cost_usd"] for x in summaries),
        "total_cost_usd": sum(x["total_cost_usd"] for x in summaries),
    }

    print(f"Judge model: {args.model}")
    print(f"Input dir: {input_dir}")
    print(f"Prompt mode: {'json-only' if args.json_only else 'reason+json'}")
    print(f"Result file prefix: {args.result_file_prefix!r}")
    print(f"Max hypos: {args.max_hypos or 'all'}")
    print(f"Prompt chars/token assumption: {args.prompt_chars_per_token}")
    print(f"Visible output tokens/call assumption: {args.visible_output_tokens_per_call}")
    print(f"Thinking tokens/call assumption: {args.thinking_tokens_per_call}")
    print()
    print("| File | Docs | Ordered pairs | Identical auto-tied | Prompt tokens est | Visible output est | Thinking est | Total est $ |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    for row in summaries:
        print(
            f"| `{row['file']}` | {row['docs']:,} | {row['ordered_pairs_to_judge']:,} | "
            f"{row['identical_pairs_auto_tied']:,} | {round(row['prompt_tokens_est']):,} | "
            f"{round(row['visible_output_tokens_est']):,} | {round(row['thinking_tokens_est']):,} | "
            f"{row['total_cost_usd']:.2f} |"
        )
    print(
        f"| **Total** | **{totals['docs']:,}** | **{totals['ordered_pairs_to_judge']:,}** | "
        f"**{totals['identical_pairs_auto_tied']:,}** | **{round(totals['prompt_tokens_est']):,}** | "
        f"**{round(totals['visible_output_tokens_est']):,}** | **{round(totals['thinking_tokens_est']):,}** | "
        f"**{totals['total_cost_usd']:.2f}** |"
    )

    if args.summary_json:
        out = {
            "model": args.model,
            "input_dir": str(input_dir.resolve()),
            "prompt_mode": "json-only" if args.json_only else "reason+json",
            "result_file_prefix": args.result_file_prefix,
            "max_hypos": args.max_hypos or None,
            "assumptions": {
                "prompt_chars_per_token": args.prompt_chars_per_token,
                "visible_output_tokens_per_call": args.visible_output_tokens_per_call,
                "thinking_tokens_per_call": args.thinking_tokens_per_call,
            },
            "per_file": summaries,
            "totals": totals,
        }
        out_path = Path(args.summary_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
