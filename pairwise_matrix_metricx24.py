import argparse
import json
import re
import sys
import threading
from concurrent.futures import as_completed, ThreadPoolExecutor
from pathlib import Path
import datasets
import torch
import transformers
import metricx.metricx24.models as models
import os
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
    p.add_argument("--metricx_param", default={"model_name_or_path":"google/metricx-24-hybrid-xl-v2p6","tokenizer":"google/mt5-xl"}, help="MetricX params to use")
    p.add_argument("--model",default="metricx-24")
    p.add_argument("--scores-cache",help="json file to cache pointwise scores (default: no caching)")
    p.add_argument("--src-lang", default="English")
    p.add_argument("--tgt-lang", default="",
                   help="target language name (default: inferred from tgt_lang field)")
    p.add_argument("--thrs", default=0.1, type=float,
                   help="score difference threshold for win/loss/tie (default 0.1)")
    p.add_argument("--no-log", action="store_true",
                   help="do not tee console output to <out_dir>/log/<stem>.log")
    return p.parse_args()


def get_dataset(
    input_file: str, tokenizer, max_input_length: int, device
):
  """Gets the test dataset for prediction.

  If `is_qe` is true, the input data must have "hypothesis" and "source" fields.
  If it is false, there must be "hypothesis" and "reference" fields.

  Args:
    input_file: The path to the jsonl input file.
    tokenizer: The tokenizer to use.
    max_input_length: The maximum input sequence length.
    device: The ID of the device to put the PyTorch tensors on.
    is_qe: Indicates whether the metric is a QE metric or not.

  Returns:
    The dataset.
  """

  def _make_input(example):
    example["input"] = (
        "source: "
        + example["source"]
        + " candidate: "
        + example["hypothesis"]
    )
    return example
   

  def _tokenize(example):
    return tokenizer(
        example["input"],
        max_length=max_input_length,
        truncation=True,
        padding=False,
    )

  def _remove_eos(example):
    example["input_ids"] = example["input_ids"][:-1]
    example["attention_mask"] = example["attention_mask"][:-1]
    return example

   
  ds = datasets.load_dataset("json",data_files={"test": input_file})

  ds = ds.map(_make_input)
  ds = ds.map(_tokenize)
  ds = ds.map(_remove_eos)
  ds.set_format(
      type="torch",
      columns=["input_ids", "attention_mask"],
      device=device,
      output_all_columns=True,
  )
  return ds

def metricx_init(model_name_or_path, tokenizer):
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    tokenizer = transformers.AutoTokenizer.from_pretrained(tokenizer)

    model = models.MT5ForRegression.from_pretrained(
        model_name_or_path, torch_dtype="auto"
    )

    model.to(device)
    model.eval()
    
    return model, tokenizer, device

def metricx_predict(examples, model, tokenizer, device):
   
    max_input_length = 1536
    batch_size = 1
    ds = get_dataset(
        examples,
        tokenizer,
        max_input_length,
        device,
    )

    os.makedirs("metricx-24",exist_ok=True)
    training_args = transformers.TrainingArguments(
        output_dir="metricx-24",
        per_device_eval_batch_size=batch_size,
        dataloader_pin_memory=False,
    )
    trainer = transformers.Trainer(
        model=model,
        args=training_args,
    )
    predictions, _, _ = trainer.predict(test_dataset=ds["test"])
    results = []
    for pred, example in zip(predictions, ds["test"]):
        example["prediction"] = float(pred)
        del example["input"]
        del example["input_ids"]
        del example["attention_mask"]
        results.append(example)
    
    return results

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
        if args.model:
            out_dir = out_dir / args.model.replace("/", "_")
        if args.exp:
            out_dir = out_dir / args.exp
        out_path = out_dir / f"{in_path.stem}-metricx-matrix.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # tee all console output to a log/ subfolder next to the output
    # if not args.no_log:
    #     log_path = out_path.parent / "log" / f"{out_path.stem}.log"
    #     log_path.parent.mkdir(parents=True, exist_ok=True)
    #     log_fh = open(log_path, "w", encoding="utf-8")
    #     sys.stdout = _Tee(sys.stdout, log_fh)
    #     sys.stderr = _Tee(sys.stderr, log_fh)
    #     print(f"log: {log_path}")

    #load model for evaluation
    model, tokenizer, device = metricx_init(**args.metricx_param)
    # ---- phase 1: load docs and enumerate every ORDERED pair to judge ----
    docs = {}        # doc_id -> {"hypos","tgt","source","K","mat"}

    n_doc = n_skip_identical = 0
    cached_scores = {}
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
            to_score = [{"source": source,"hypothesis": x} for x in hypos]
            with open("temp_toscore.jsonl","w") as tmpjs:
                json.dump(to_score,tmpjs)
            if args.scores_cache and os.path.exists(args.scores_cache):
                with open(args.scores_cache,"r") as f:
                    cached_scores = json.load(f)
                if doc_id in cached_scores:
                    pointwise_scores = cached_scores[doc_id]
                else:
                    pointwise_scores = metricx_predict("temp_toscore.jsonl",model, tokenizer, device)
                    cached_scores[doc_id] = pointwise_scores
                    with open(args.scores_cache,"w") as f:
                        json.dump(cached_scores,f)
            else:
                pointwise_scores = metricx_predict("temp_toscore.jsonl",model, tokenizer, device)
                cached_scores[doc_id] = pointwise_scores
                with open(args.scores_cache,"w") as f:
                    json.dump(cached_scores,f)
            
            def _validate_order_and_extract(pointwise_scores,hypos):
                scores = []
                for h in hypos:
                    for ps in pointwise_scores:
                        if ps["hypothesis"] == h:
                            scores.append(ps["prediction"])
                            break
                assert len(scores) == len(hypos), f"Mismatch in scores and hypos for doc_id {doc_id}, hypos: {hypos}, scores: {scores}"      
                return scores
            
         
            scores = _validate_order_and_extract(pointwise_scores,hypos)
            
            mat = [[0] * K for _ in range(K)]   # diagonal + identical -> 0
            docs[doc_id] = {"hypos": hypos, "tgt": tgt, "source": source,
                            "K": K, "mat": mat}
            
            for i in range(K):
                for j in range(K):
                    if i == j:
                        mat[i][j]=0
                    if hypos[i] == hypos[j]:
                        mat[i][j]=0
                        n_skip_identical += 1          
                    else:
                        score_diff = scores[i]-scores[j]
                        mat[i][j]= 1 if score_diff > args.thrs else -1 if score_diff < -args.thrs else 0
            n_doc += 1
    print(f"processed {n_doc} docs")

    os.remove("temp_toscore.jsonl")
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
            }
            fout.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
