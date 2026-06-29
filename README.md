# LLM-judge vs. Human Coherency Evaluation

This repo uses **WMT25 human evaluation data** as the gold standard to measure how well an **LLM pairwise judge** agrees with human ratings.

> 中文版见 [`README.md`](README.md).

---

## Installation

This project includes a `pyproject.toml` for [`uv`](https://docs.astral.sh/uv/). It requires **Python >= 3.10**.

```bash
# 1) Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2) Enter the project
cd /path/to/UvA-MT-at-WMT26

# 3) Install a compatible Python (recommended)
uv python install 3.11

# 4) Create/update .venv, resolve dependencies, and install the project
uv sync
```

> If you prefer a lower-level pip-style install, `uv pip install -r pyproject.toml` also works, but `uv sync` is the recommended project workflow.

## Tests

Run the local quick integrity tests with:

```bash
.local_scripts/gemini/run_tests.sh
```

These are fast local checks for the judge/parser path and do not call the API.

---

## 0. Goal

> **Getting the data:** download the WMT25 evaluation set from <https://github.com/wmt-conference/wmt25-general-mt> and put `wmt25-genmt-humeval.jsonl` at the repo root. The file is git-ignored (it exceeds GitHub's 100 MB limit), so it is not in this repo — `dev/extract_dev.py` reads it to build the dev set.

**Core goal: tune the llm-as-a-judge so its verdicts match human ratings as closely as possible.**

We treat the judge as a tunable system with two main knobs:

1. **Model** (`--model`): swap in different MetaGen models as the judge;
2. **Rubric / prompt** (`--rubric-file`): swap in different grading criteria and prompts.

**The evaluation is pairwise / contrastive** — we never ask the judge for an absolute score on a single translation. Instead the judge only answers "is A or B better?"; we collect every ordered pair into a win/loss matrix and align it against the human ratings. Two reasons for going contrastive rather than pointwise:

1. **It matches this year's WMT human evaluation** — WMT's human protocol is itself comparison-based, so the judge should use the same paradigm to stay on the same footing as the gold standard;
2. **Pairwise is more accurate than pointwise** — a head-to-head comparison gives the model an explicit reference point (judging A *against* B) instead of conjuring an absolute score for a lone translation, which makes verdicts more stable and reliable.

**How we choose:** each (model × rubric) combo is one **experiment** (stored under `dev/<model>/<exp>/`). `coherency_eval.py` quantifies its agreement with the human scores (`dir_both`, Kendall/Spearman, Best@k, …). **Higher agreement = better judge.** We compare experiments side by side and pick the best combo.

**End application:** plug the tuned judge into **`sequential_scaling.py`** — during multi-round translation it judges/selects the refinement candidates (picking the better translation to drive the next round), so generation quality tracks human preference more closely.

> In one line: **this repo picks/tunes a "human-like" scorer for `sequential_scaling.py`**; the coherency evaluation on the dev set is the selection criterion, not the end goal.

---

## 1. Pipeline & scripts

| Script | What it does | Main output |
|---|---|---|
| `extract_dev.py` | From `wmt25-genmt-humeval.jsonl`, sample en-zh / en-ru; per item take 8 random systems' translations + their human scores (mean over annotators) | `dev/<pair>.jsonl` |
| `pairwise_matrix.py` | LLM judge does a **pairwise** verdict over each item's 8 translations, producing a directed K×K win/loss matrix (both directions judged independently, exposing position bias) | `dev/<model>/<exp>/<pair>-llm-matrix.jsonl` |
| `coherency_eval.py` | Compares the LLM matrix against a human matrix rebuilt from `score_i`; prints agreement metrics + a threshold sweep, and exports tables | `dev/<model>/<exp>/coherency.jsonl`, `coherency_sweep.{csv,tsv}` |

> The human win/loss matrix is **not persisted**: `coherency_eval.py` rebuilds it on the fly from the `score_i` in `dev/<pair>.jsonl` at any threshold, so saving it would just be a redundant artifact.

### Directory convention (experiment isolation)

```
dev/                              ← shared gold (experiment-independent, stored once)
  en-zh.jsonl  en-ru.jsonl                  translations + human scores (score_i)
dev/<model>/<exp>/                ← experiment dir: a model-name level + an experiment-name level
  en-zh-llm-matrix.jsonl  en-ru-llm-matrix.jsonl
  coherency.jsonl  coherency_sweep.csv  coherency_sweep.tsv
  cache/                          ← judge-call cache (reused for resume)
    en-zh-llm-matrix.cache.jsonl  en-ru-llm-matrix.cache.jsonl
  log/                            ← run logs (pairwise_matrix.py tees automatically)
    en-zh-llm-matrix.log  en-ru-llm-matrix.log
```

For example `dev/gpt-4o-mini/v1/` (model `gpt-4o-mini`, experiment `v1`).

> `pairwise_matrix.py` tees console output to `<model>/<exp>/log/<stem>.log` (disable with `--no-log`) and writes the cache to `<model>/<exp>/cache/`; both dirs are created automatically.

- **The dev set is shared**: different experiments judge the **same translations**, which is what makes them comparable.
- `--model` sets the model-name level, `--exp` sets the experiment-name level beneath it; both only affect the **llm-matrix and coherency** outputs.

```bash
# 1) Build the dev set (experiment-independent, run once; the script lives in dev/ and is cwd-independent)
python3 dev/extract_dev.py

# 2) Run a judge experiment (output goes to dev/<model>/<exp>/)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model <model> --exp <exp> [--rubric-file <prompt>]
python3 pairwise_matrix.py --in dev/en-ru.jsonl --model <model> --exp <exp>

# 3) Coherency evaluation (auto reads/writes that experiment folder)
python3 coherency_eval.py --model <model> --exp <exp>
```

---

## 2. Script usage

### `sequential_scaling.py` — translation generation (sequential scaling)

Translates source text into the target language with a MetaGen model; `-k` sets the number of rounds (round 0 translates, later rounds refine), stored as `hypo_0..hypo_{k-1}`. This is upstream of `pairwise_matrix.py` (it produces the candidates to be judged).

```bash
# Simplest: use the default input (a hardcoded absolute path to wmt26_genmt_blindset.jsonl), translate to Chinese, single round
python3 sequential_scaling.py --input wmt26_genmt_blindset.jsonl --model gpt-4o-mini --langs zh_CN

# 8 rounds of sequential scaling, 8-way concurrency, en->ru
python3 sequential_scaling.py --input wmt26_genmt_blindset.jsonl \
  --results-dir results --langs ru_RU --model gpt-4o-mini -k 8 --concurrency 8

# Debug: only 5 items, and don't call the model (build prompts only)
python3 sequential_scaling.py --langs zh_CN --limit 5 --dry-run
```

Common flags: `--input` (input jsonl; defaults to a hardcoded absolute path to `wmt26_genmt_blindset.jsonl`, so pass it explicitly), `--results-dir` (output dir, default `results`), `--langs` (target langs, comma-separated or `all`), `--model`, `-k` (rounds), `--context-win` (how many prior rounds to look back when refining), `--concurrency`, `--resume` (skip already-done doc_ids), `--limit`, `--dry-run`, `--no-cache`.
Output: `results/<src>-<tgt>.jsonl` (e.g. `results/en-zh_CN.jsonl`), each line with `hypo_0..hypo_{k-1}`.

### `pairwise_matrix.py` — LLM pairwise judge → win/loss matrix

Reads a jsonl with `hypo_0..hypo_{K-1}`, has the LLM judge every **ordered pair** of an item's translations, and writes a directed K×K matrix (both directions judged independently, exposing position bias).

```bash
# Simplest: judge one dev language pair (model defaults to gpt-4o-mini)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp v1

# Swap the judge's prompt (rubric), under a new experiment name
python3 pairwise_matrix.py --in dev/en-ru.jsonl --model gpt-4o-mini --exp v2 \
  --rubric-file my_rubric.txt

# Reuse a cache from elsewhere (full hit / zero API when model/prompt/translations match)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp v2 \
  --cache-path dev/gpt-4o-mini/v1/cache/en-zh-llm-matrix.cache.jsonl

# Debug: only the first 3 items (note: without --out this overwrites the experiment's
# real output, so for debugging pass an explicit --out)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp tmp --limit 3
```

Common flags: `--in` (required, jsonl with hypos), `--model`, `--exp`, `--rubric-file` (swap judge prompt), `--concurrency` (default 32), `--cache-path`, `--no-cache`, `--no-log`, `--limit`.
Default outputs: `<in_dir>/<model>/<exp>/<pair>-llm-matrix.jsonl`, cache under `cache/`, logs under `log/` (both auto-created).

### `coherency_eval.py` — LLM matrix vs. human scores

**How it works** (each language pair handled independently):

1. **Load & align**: the directed LLM matrix `*-llm-matrix.jsonl` (one K×K `winloss` per doc) + the shared dev raw human scores `score_i`, joined on `doc_id`.
2. **Symmetrize the LLM matrix (handling position bias)**: the LLM judge tends to prefer whichever candidate is shown *first*, so the matrix is **directed** — each pair {i,j} is judged twice (i-first and j-first), and the two often **disagree** (~20% of pairs flip with order, tracked as `position_disagreements`). Symmetrization rule: both orders say i wins → i wins; both say j wins → j wins; **the two disagree → tie**. So the LLM's tie rate (~20%) comes mostly from position bias, not from genuine ties; the human matrix is antisymmetric by construction and has no such issue.
3. **Rebuild the human verdict**: from `score_i - score_j` and threshold `t` (`diff>t` win, `diff<-t` loss, else tie).
4. **Pairwise comparison** of LLM vs. human → `agreement_3way` + a 3×3 confusion matrix + `dir_strict` / `dir_both`.
5. **Rank correlation**: per doc, human raw scores vs. LLM net score (row sums) → Kendall τ-b / Spearman ρ, then averaged across docs.
6. **Best@k**: whether the argmax of the LLM net score falls in the human top-1 / top-2.
7. **Threshold sweep**: step 4 (threshold-dependent) is recomputed for each `t`; steps 5–6 are threshold-independent and computed once.

> The human matrix is rebuilt in memory per threshold; `*-human-matrix.jsonl` is not read (it is no longer persisted).

```bash
# Simplest: evaluate an experiment (auto-reads matrices in dev/<model>/<exp>/, exports back there)
python3 coherency_eval.py --model gpt-4o-mini --exp v1

# Custom threshold sweep (the first one is the primary threshold)
python3 coherency_eval.py --model gpt-4o-mini --exp v1 --thresholds 0,5,10,15,20,25,30,40,50

# A single language pair only
python3 coherency_eval.py --model gpt-4o-mini --exp v1 --pairs en-zh

# Explicit files + export path (bypass the model/exp convention)
python3 coherency_eval.py --dev dev/en-zh.jsonl \
  --llm dev/gpt-4o-mini/v1/en-zh-llm-matrix.jsonl --csv /tmp/out.csv
```

Common flags: `--model`, `--exp`, `--pairs` (default `en-zh,en-ru`), `--thresholds`, `--dir` (shared-gold dir, defaults to the `dev/` next to the script), `--dump/--csv/--tsv` (explicit paths override the auto-export).
Default outputs: `dev/<model>/<exp>/coherency.jsonl` + `coherency_sweep.{csv,tsv}`, plus metrics and the threshold sweep printed to the console.

---

## 3. Metrics at a glance

| Metric | Meaning | Threshold-sensitive? |
|---|---|---|
| `agreement_3way` | Per-pair 3-way (win-i / tie / win-j) exact-match rate; **both-tie also counts as agreement** | Yes |
| `dir_strict` | Among pairs where humans call a winner, fraction where the LLM agrees on direction (**LLM tie = wrong**) | Yes |
| `dir_both` | Among pairs where **both** call a winner, fraction agreeing on direction (the purest "direction" metric) | Yes |
| `kendall_mean` / `spearman_mean` | Per-doc rank correlation (human raw scores vs. LLM net score), averaged across docs | **No** (depends on score order) |
| `best1` / `best2` | Is the LLM's top pick the human-best / within the human top-2 | **No** (depends on score extrema) |

> The threshold `t` (`win_k=loss_n=t`) only decides "how big a gap counts as a win"; it **does not change the order/extrema of the scores**, so Kendall/Spearman/best are threshold-independent.

---

## 4. How this differs from traditional MT metric meta-evaluation ⭐

> "Computing the Spearman / agreement between two matrices" here is **not** the same thing as the **metric meta-evaluation** of the WMT Metrics Shared Task. In short: **what we do is closer to per-source segment-level ranking agreement, whereas the traditional focus is system-level + global segment-level, and the metric paradigm has moved from correlation coefficients to pairwise accuracy.**

### 4.1 Different level of analysis (the key one)

| | Traditional metric meta-eval | This repo |
|---|---|---|
| Primary level | **system-level**: aggregate each system's scores over the whole test set into one value, then correlate the ranking of the N systems | none (each doc's 8 translations come from different systems but cover only one sentence) |
| Secondary level | **segment-level**: **pool** every segment's (metric, human) pair into one big correlation | **per-doc ranking of K=8**, one correlation per doc, then **averaged across docs** |

What we compute is neither classic system-level nor classic global segment-level — it's the ability to **rank the 8 candidates for each source sentence** (item-level ranking), then averaged.

### 4.2 Different output shape of the thing being evaluated

- Traditional metrics (BLEU / COMET / BLEURT) are **scalar functions**; meta-eval correlates the scalar directly against human scalars/rankings.
- Our LLM judge is inherently a **pairwise comparison** (directed, with position bias). To even compute Spearman we first **symmetrize** it, then aggregate into a **Borda-style net score**. That step **loses/reconstructs information** — the scalar is reverse-engineered from pairwise verdicts, not the judge's native output.

### 4.3 Different aggregation → different estimand (easy to overlook)

- Traditional global segment-level is **one pooled correlation** (thousands of points): stable, but **contaminated by per-sentence difficulty** — a 90 on doc A and a 90 on doc B aren't comparable in quality, and pooling mixes in cross-sentence scale.
- This repo computes **per-doc (grouped) then averages**, which **naturally controls for source difficulty** (only comparing 8 candidates within the same source). This mirrors the recent **"group-by-item" vs "no-grouping" Kendall** discussion (Deutsch et al. 2023 show global pooling inflates correlation). So it's a **deliberate refinement**, but its numbers are **not directly comparable to older papers**.

### 4.4 Small-sample noise

- Global segment-level: n is large, so a single correlation is stable.
- This repo: each correlation comes from only **8 points**, so a single doc is very noisy; stability comes from averaging over ~200 docs. That's the price of grouping.

### 4.5 The metric paradigm has shifted

Modern WMT metrics meta-eval (Kocmi et al. 2021; Freitag et al.) primarily uses **pairwise ranking accuracy + tie calibration** (Deutsch et al. 2023), not Spearman/Pearson — correlation coefficients are sensitive to ties and scale and are less task-aligned.
- This repo's **`dir_both` / `agreement` are closer to modern pairwise accuracy**;
- **Spearman is, by contrast, the more "old-school" display metric.**

### 4.6 Setup details

- Our judge is **QE-style** (given source + candidates, no reference); traditional BLEU/COMET are mostly reference-based (COMET also has a QE variant). The human gold is **MQM-derived scores**, in line with modern WMT.
- This repo **does not yet do significance testing** (traditionally one uses bootstrap / permutation / the Williams test to check whether two metrics' correlations differ significantly).

### Summary

- **The differences, in essence**: level (per-source ranking), object (pairwise rather than scalar), aggregation (grouped-average rather than global pooling), metric (correlation coefficient vs. pairwise accuracy).
- To **align with modern metric meta-eval**:
  1. Use **pairwise accuracy (≈ `dir_both`) + tie calibration** as the primary metric, Spearman as a reference only;
  2. Add a **system-level** view (aggregate each system over many sentences, then rank) — what WMT cares about most; the current matrices have dropped system names, so this needs rebuilding from the raw `wmt25` data;
  3. Add **bootstrap confidence intervals / significance testing**.
