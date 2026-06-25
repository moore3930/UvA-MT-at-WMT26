#!/usr/bin/env python3
"""pairwise_matrix.py

Read a sequential_scaling output (e.g. results/en-zh_CN.jsonl) where each row
has K candidate translations hypo_0 .. hypo_{K-1}, and for every document judge
every ORDERED pair of hypos to build a K x K win/loss matrix.

Output (one row per doc) goes to a new jsonl, with the matrix as a 2D array
`winloss`, where the verdict is recorded by SHOWN POSITION:

    winloss[i][j] = +1  -> with hypo_i shown FIRST (A) and hypo_j SECOND (B),
                           the judge preferred hypo_i
                  = -1  -> the judge preferred hypo_j
                  =  0  -> tie  (and i == j; the diagonal is always 0)

Both directions are judged independently -- winloss[i][j] and winloss[j][i] are
SEPARATE calls, NOT mirrors, so the matrix exposes any position-order effect
(if the judge had no position bias, winloss[i][j] would equal -winloss[j][i]).

Identical hypos (common once refinement converges) are scored 0 without any API
call, in both directions.

Example:
    python pairwise_matrix.py --in results/en-zh_CN.jsonl
    python pairwise_matrix.py --in results/en-zh_CN.jsonl --limit 50

On caching / speed
------------------
The MetaGen chat API exposes no explicit KV / prefix-cache knob (checked), so
there is nothing to "turn on". Speed comes from:
  1) skipping pairs whose two hypos are byte-identical (no call at all) -- the
     big win, since hypo_i often converge and repeat;
  2) the prompt-level result cache (LLMCache) -> identical judge calls reuse.
Each cell is judged on its own (no mirroring), since position order can matter.
Server-side prompt caching (GPT models) is automatic but only helps long
(>~1k token) prompts; these judge prompts are short, so it is negligible.
"""

import argparse
import json
import re
import sys
import threading
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path

from sequential_scaling import lang_name, LLMCache
from util.openai_client import build_client
from util.contrastive_judge import DEFAULT_RUBRIC, judge_pair, render_rubric


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


def extract_hypos(rec: dict):
    """Return the ordered list of hypo texts [hypo_0, hypo_1, ...] from a row."""
    idx = sorted(int(m.group(1)) for k in rec for m in [_HYPO_RE.match(k)] if m)
    return [rec[f"hypo_{i}"] for i in idx]


def parse_args():
    p = argparse.ArgumentParser(
        description="Build a K x K directed win/loss matrix per doc from hypo pairs")
    p.add_argument("--in", dest="inp", required=True,
                   help="sequential_scaling output jsonl (with hypo_0..hypo_{K-1})")
    p.add_argument("--out", default="",
                   help="output jsonl (default <in_dir>/<model>/<exp>/<stem>-llm-matrix.jsonl)")
    p.add_argument("--exp", default="",
                   help="experiment name; outputs go to <in_dir>/<model>/<exp>/ "
                        "(use to separate different judge prompts under a model)")
    p.add_argument("--model", default="gpt-4o-mini", help="OpenAI judge model")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--src-lang", default="English")
    p.add_argument("--tgt-lang", default="",
                   help="target language name (default: inferred from tgt_lang field)")
    p.add_argument("--rubric-file", default="",
                   help="file whose text replaces the default rubric block")
    p.add_argument("--concurrency", type=int, default=32)
    p.add_argument("--limit", type=int, default=0, help="max docs (0=all)")
    p.add_argument("--api-key", default="")
    p.add_argument("--cache-path", default="",
                   help="default <out_dir>/cache/<stem>.cache.jsonl")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--no-log", action="store_true",
                   help="do not tee console output to <out_dir>/log/<stem>.log")
    return p.parse_args()


def main():
    args = parse_args()

    in_path = Path(args.inp)
    if not in_path.exists():
        sys.exit(f"--in not found: {in_path}")

    rubric_text = (Path(args.rubric_file).read_text(encoding="utf-8").strip()
                   if args.rubric_file else render_rubric(DEFAULT_RUBRIC))

    if args.out:
        out_path = Path(args.out)
    else:
        # outputs nest under <in_dir>/<model>/<exp>/ (exp under the model name)
        out_dir = in_path.parent
        if args.model:
            out_dir = out_dir / args.model.replace("/", "_")
        if args.exp:
            out_dir = out_dir / args.exp
        out_path = out_dir / f"{in_path.stem}-llm-matrix.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # tee all console output to a log/ subfolder next to the output
    if not args.no_log:
        log_path = out_path.parent / "log" / f"{out_path.stem}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(log_path, "w", encoding="utf-8")
        sys.stdout = _Tee(sys.stdout, log_fh)
        sys.stderr = _Tee(sys.stderr, log_fh)
        print(f"log: {log_path}")

    # cache lives in a dedicated cache/ subfolder next to the output
    cache_path = (Path(args.cache_path) if args.cache_path
                  else out_path.parent / "cache" / f"{out_path.stem}.cache.jsonl")
    cache = LLMCache(cache_path, enabled=not args.no_cache)
    if cache.enabled:
        print(f"cache: {cache_path} (loaded {len(cache.mem)} entries)")

    # ---- phase 1: load docs and enumerate every ORDERED pair to judge ----
    docs = {}        # doc_id -> {"hypos","tgt","source","K","mat"}
    tasks = []       # (doc_id, i, j) ordered pairs (i != j) to judge
    n_doc = n_skip_identical = 0
    with in_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            hypos = extract_hypos(rec)
            if len(hypos) < 2:
                continue
            doc_id = rec.get("doc_id")
            tgt = args.tgt_lang or lang_name(rec.get("tgt_lang") or "")
            source = rec.get("source_doc") or ""
            K = len(hypos)
            mat = [[0] * K for _ in range(K)]   # diagonal + identical -> 0
            docs[doc_id] = {"hypos": hypos, "tgt": tgt, "source": source,
                            "K": K, "mat": mat}
            for i in range(K):
                for j in range(K):
                    if i == j:
                        continue
                    if hypos[i] == hypos[j]:
                        n_skip_identical += 1          # tie, no API call
                    else:
                        tasks.append((doc_id, i, j))
            n_doc += 1
            if args.limit and n_doc >= args.limit:
                break

    print(f"docs={n_doc}; ordered pairs to judge={len(tasks)}; "
          f"identical pairs auto-tied={n_skip_identical}; model={args.model}")

    # ---- phase 2: judge every ordered pair concurrently (single order each) ----
    tlocal = threading.local()

    def client_for_thread():
        c = getattr(tlocal, "client", None)
        if c is None:
            c = build_client(args.api_key)
            tlocal.client = c
        return c

    def worker(task):
        doc_id, i, j = task
        d = docs[doc_id]
        # swap=False -> ONE call, with hypo_i as A (shown first), hypo_j as B
        v = judge_pair(client_for_thread(), args.model, d["source"],
                       d["hypos"][i], d["hypos"][j], args.src_lang, d["tgt"],
                       rubric_text, args.temperature, cache, swap=False)
        return task, v["winner"]

    n_done = n_fail = 0
    if tasks:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(worker, t): t for t in tasks}
            for fut in as_completed(futures):
                try:
                    (doc_id, i, j), winner = fut.result()
                except Exception as e:  # noqa: BLE001
                    n_fail += 1
                    print(f"  [error] {futures[fut]}: {e}", file=sys.stderr)
                    continue
                mat = docs[doc_id]["mat"]
                mat[i][j] = 1 if winner == "A" else -1 if winner == "B" else 0
                n_done += 1
                if n_done % 50 == 0:
                    print(f".. {n_done}/{len(tasks)} ordered pairs judged")

    # ---- phase 3: write per-doc matrices (+ direction-aware aggregates) ----
    def disagreements(mat, K):
        # unordered pairs where the two orders don't agree (position effect)
        return sum(1 for i in range(K) for j in range(i + 1, K)
                   if mat[i][j] != -mat[j][i])

    with out_path.open("w", encoding="utf-8") as fout:
        for doc_id, d in docs.items():
            mat, K = d["mat"], d["K"]
            # combined score uses BOTH directions: how much i wins as the first
            # candidate (row) plus how much it wins as the second (neg column)
            score = [sum(mat[i]) - sum(mat[r][i] for r in range(K))
                     for i in range(K)]
            best = max(range(K), key=lambda i: (score[i], -i))
            rec = {
                "doc_id": doc_id,
                "tgt_lang": d["tgt"],
                "k": K,
                "winloss": mat,           # winloss[i][j]: i shown first vs j second
                "score": score,           # both-direction net score per hypo
                "best": best,
                "position_disagreements": disagreements(mat, K),
                "source_doc": d["source"],
                "hypos": d["hypos"],
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # aggregate: avg combined score per hypo index + overall position-bias rate
    maxK = max((d["K"] for d in docs.values()), default=0)
    agg = [0.0] * maxK
    cnt = [0] * maxK
    total_pairs = total_disagree = 0
    for d in docs.values():
        mat, K = d["mat"], d["K"]
        for i in range(K):
            agg[i] += sum(mat[i]) - sum(mat[r][i] for r in range(K))
            cnt[i] += 1
        total_pairs += K * (K - 1) // 2
        total_disagree += disagreements(mat, K)

    print(f"\nDone. wrote {len(docs)} matrices (judged {n_done} ordered pairs, "
          f"failed {n_fail}).")
    print("avg combined win-score per hypo index (higher = preferred more):")
    for i in range(maxK):
        if cnt[i]:
            print(f"  hypo_{i}: {agg[i] / cnt[i]:+.2f}")
    if total_pairs:
        print(f"position-order disagreements: {total_disagree}/{total_pairs} "
              f"pairs ({100 * total_disagree / total_pairs:.1f}%) "
              f"-> judge position sensitivity")
    print(f"output: {out_path.resolve()}")


if __name__ == "__main__":
    main()
