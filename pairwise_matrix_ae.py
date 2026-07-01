import argparse
import json
import re
import sys
from pathlib import Path
import os
from pairwise_matrix import _Tee
from metric_predict import MetricxPredictor, CometQEPredictor, RemedyQEPredictor

_HYPO_RE = re.compile(r"^hypo_(\d+)$")

def parse_args():
    p = argparse.ArgumentParser(
        description="Build a K x K directed win/loss matrix per doc from hypo pairs")
    p.add_argument("--in", dest="inp", required=True,
                   help="sequential_scaling output jsonl (with hypo_0..hypo_{K-1})")
    p.add_argument("--out", default="",
                   help="output jsonl (default <in_dir>/<model>/<exp>/<stem>-metricx-matrix.jsonl)")
    p.add_argument("--exp", default="",
                   help="experiment name; outputs go to <in_dir>/<model>/<exp>/ "
                        "(use to separate different judge prompts under a model)")
    p.add_argument("--metric_params", default={}, help="dict contains the parameters for the metric predictor")
    p.add_argument("--ae-metric",default="cometqe",choices=["metricx-24","cometqe","remedyqe"],help="which metric to use for pairwise scoring")
    p.add_argument("--scores-cache",help="json file to cache pointwise scores (default: no caching)")
    p.add_argument("--src-lang", default="English")
    p.add_argument("--tgt-lang", default="",
                   help="target language name (default: inferred from tgt_lang field)")
    p.add_argument("--thrs", default=0.1, type=float,
                   help="score difference threshold for win/loss/tie (default 0.1)")
    p.add_argument("--no-log", action="store_true",
                   help="do not tee console output to <out_dir>/log/<stem>.log")
    return p.parse_args()




def extract_hypos(rec: dict):
    """Return the ordered list of hypo texts [hypo_0, hypo_1, ...] from a row."""
    idx = sorted(int(m.group(1)) for k in rec for m in [_HYPO_RE.match(k)] if m)
    return [rec[f"hypo_{i}"] for i in idx]


def main():
    args = parse_args()

    in_path = Path(args.inp)
    if not in_path.exists():
        sys.exit(f"--in not found: {in_path}")

    if args.out:
        out_path = Path(args.out)
    else:
        # outputs nest under <in_dir>/<model>/<exp>/ (exp under the model name)
        out_dir = in_path.parent
        if args.ae_metric:
            out_dir = out_dir / args.ae_metric.replace("/", "_")
        if args.exp:
            out_dir = out_dir / args.exp
        out_path = out_dir / f"{in_path.stem}-{args.ae_metric}-matrix.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    #tee all console output to a log/ subfolder next to the output
    if not args.no_log:
        log_path = out_path.parent / "log" / f"{out_path.stem}.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_fh = open(log_path, "w", encoding="utf-8")
        sys.stdout = _Tee(sys.stdout, log_fh)
        sys.stderr = _Tee(sys.stderr, log_fh)
        print(f"log: {log_path}")

    #load model for evaluation
    predictor = None
    metric_params = args.metric_params if isinstance(args.metric_params, dict) else json.loads(args.metric_params)
    print(f"loading predictor for {args.ae_metric} with params: {metric_params}")
    if args.ae_metric == "metricx-24":
        predictor = MetricxPredictor(metric_params)
    if args.ae_metric == "cometqe":
        predictor = CometQEPredictor(metric_params)
    if args.ae_metric == "remedyqe":
        predictor = RemedyQEPredictor(metric_params)


    # ---- phase 1: load docs and enumerate every ORDERED pair to judge ----
    docs = {}        # doc_id -> {"hypos","tgt","source","K","mat"}

    n_doc = 0
    to_score = []
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
            tgt = rec.get("tgt_lang")
            source = rec.get("source_doc") or ""
            K = len(hypos)
            source_lang = doc_id.split("#")[0].split("-")[0]
            to_score.extend([{"source": source,"hypothesis": x,"doc_id": doc_id,"src_lang": source_lang,"tgt_lang": tgt[:2]} for x in hypos])
            
            
            mat = [[0] * K for _ in range(K)]   # diagonal + identical -> 0
            docs[doc_id] = {"hypos": hypos, "tgt": tgt, "source": source,
                            "K": K, "mat": mat}
            
            n_doc += 1
    print(f"processed {n_doc} docs")
    pointwise_scores = predictor.predict(to_score)

    for ex in pointwise_scores:
        docs[ex["doc_id"]].setdefault("scores", []).append(ex["prediction"])
    
    for doc_id, d in docs.items():
        mat, K = d["mat"], d["K"]
        for i in range(K):
            for j in range(K):
                if i==j:
                    continue
                ratio = d["scores"][i]/d["scores"][j]
                if ratio > 1.0+args.thrs:
                    mat[i][j] = 1
                elif ratio < 1.0-args.thrs:
                    mat[i][j] = -1
                else:
                    mat[i][j] = 0
                    

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
                "source_doc": d["source"],
                "hypos": d["hypos"],
                "scores": d["scores"]
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
