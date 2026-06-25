# LLM-judge vs Human 一致性评估

本仓库用 **WMT25 人工评测数据** 作为金标,衡量 **LLM 成对裁判(pairwise judge)** 与人工打分的一致性。

> English version: [`README.en.md`](README.en.md).

---

## 0. 实验目的

**核心目标:调优 llm-as-a-judge,使其判定尽可能贴近人工评分。**

我们把 judge 当作可调系统,主要调两个旋钮:

1. **模型**(`--model`):换不同 MetaGen 模型作裁判;
2. **Rubric / prompt**(`--rubric-file`):换不同的评判标准与提示词。

**评估范式是 pairwise / contrastive(成对对比),而非给单条译文打绝对分。** judge 每次只回答"A 和 B 哪个更好",我们把所有有序对的结果汇成 win/loss 矩阵,再与人工分对齐。选 contrastive 而非 pointwise 有两个原因:

1. **对齐今年 WMT 的人工评估** —— 今年 WMT 人工评测本身就是**对比式**的,judge 用同样范式才与金标口径一致;
2. **pairwise 比 pointwise 更准** —— 成对比较给了模型一个**明确的参照基准**(拿 A 比着 B 判),而非凭空给单条译文打绝对分,判定更稳、更可靠。

**怎么选:** 每组(模型 × rubric)= 一个**实验**(放在 `dev/<model>/<exp>/`),用 `coherency_eval.py` 量化它与人工分的一致性(`dir_both`、Kendall/Spearman、Best@k 等)。**一致性越高 = judge 越好**;横向对比多组实验,选出最优组合。

**最终应用:** 把调优后的 judge 接入 **`sequential_scaling.py`** —— 在多轮翻译里用它评判/挑选 refine 候选(选出更优译文驱动下一轮),让生成质量更贴近人工偏好。

> 一句话:**本仓库是给 `sequential_scaling.py` 选/调一个"像人"的打分器**;dev 集上的一致性评估是选择依据,不是最终目的。

---

## 1. 流程与脚本

| 脚本 | 作用 | 主要产物 |
|---|---|---|
| `extract_dev.py` | 从 `wmt25-genmt-humeval.jsonl` 抽 en-zh / en-ru,每条取随机 8 个系统的译文 + 人工分(多标注取均值) | `dev/<pair>.jsonl` |
| `pairwise_matrix.py` | 用 LLM judge 对每条样本的 8 条译文做**逐对**判定,输出有向 K×K win/loss 矩阵(双向独立判,暴露位置偏置) | `dev/<model>/<exp>/<pair>-llm-matrix.jsonl` |
| `coherency_eval.py` | 对比 LLM 矩阵与从 `score_i` 重建的人工矩阵,输出一致性指标 + 阈值扫描 + 导出 | `dev/<model>/<exp>/coherency.jsonl`、`coherency_sweep.{csv,tsv}` |

> 人工 win/loss 矩阵**不落盘**:`coherency_eval.py` 直接从 `dev/<pair>.jsonl` 的 `score_i` 按任意阈值即时重建,持久化它只会是冗余产物。

### 目录约定(实验隔离)

```
dev/                              ← 共享真值(实验无关,不重复存)
  en-zh.jsonl  en-ru.jsonl                  译文 + 人工分(score_i)
dev/<model>/<exp>/                ← 实验目录:模型名一层 + 实验名一层
  en-zh-llm-matrix.jsonl  en-ru-llm-matrix.jsonl
  coherency.jsonl  coherency_sweep.csv  coherency_sweep.tsv
  cache/                          ← judge 调用缓存(断点续跑复用)
    en-zh-llm-matrix.cache.jsonl  en-ru-llm-matrix.cache.jsonl
  log/                            ← 运行日志(pairwise_matrix.py 自动 tee)
    en-zh-llm-matrix.log  en-ru-llm-matrix.log
```

例如 `dev/gpt-4o-mini/v1/`(模型 `gpt-4o-mini`、实验 `v1`)。

> `pairwise_matrix.py` 把控制台输出同时写入 `<model>/<exp>/log/<stem>.log`(`--no-log` 关闭),缓存写入 `<model>/<exp>/cache/`,均自动建目录。

- **dev 集共享**:不同实验判的是**同一批译文**,才可比。
- `--model` 决定模型名一层,`--exp` 决定其下实验名一层;两者只影响 **llm-matrix 与 coherency**。

```bash
# 1) 抽 dev 集(实验无关,只需跑一次;脚本在 dev/ 下,路径与 cwd 无关)
python3 dev/extract_dev.py

# 2) 跑某个实验的 judge(输出到 dev/<model>/<exp>/)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model <model> --exp <exp> [--rubric-file <prompt>]
python3 pairwise_matrix.py --in dev/en-ru.jsonl --model <model> --exp <exp>

# 3) 一致性评估(自动读/写该实验文件夹)
python3 coherency_eval.py --model <model> --exp <exp>
```

---

## 2. 脚本用法详解

### `sequential_scaling.py` — 翻译生成(sequential scaling)

用 MetaGen 模型把源文翻译成目标语;`-k` 控制轮数(round 0 先翻,之后每轮 refine),结果存成 `hypo_0..hypo_{k-1}`。这是 `pairwise_matrix.py` 的上游(产出待判定的多条候选)。

```bash
# 最简:用默认输入(硬编码的 wmt26_genmt_blindset.jsonl 绝对路径),翻成中文,单轮
python3 sequential_scaling.py --input wmt26_genmt_blindset.jsonl --model gpt-4o-mini --langs zh_CN

# k=8 轮 sequential scaling,8 路并发,en->ru
python3 sequential_scaling.py --input wmt26_genmt_blindset.jsonl \
  --results-dir results --langs ru_RU --model gpt-4o-mini -k 8 --concurrency 8

# 调试:只跑 5 条、且不调用模型(只构建 prompt)
python3 sequential_scaling.py --langs zh_CN --limit 5 --dry-run
```

常用参数:`--input`(输入 jsonl,默认是硬编码的 `wmt26_genmt_blindset.jsonl` 绝对路径,建议显式传入)、`--results-dir`(输出目录,默认 `results`)、`--langs`(目标语,逗号分隔或 `all`)、`--model`、`-k`(轮数)、`--context-win`(refine 时回看几轮)、`--concurrency`、`--resume`(跳过已完成 doc_id)、`--limit`、`--dry-run`、`--no-cache`。
输出:`results/<src>-<tgt>.jsonl`(如 `results/en-zh_CN.jsonl`),每行含 `hypo_0..hypo_{k-1}`。

### `pairwise_matrix.py` — LLM 逐对裁判 → win/loss 矩阵

读含 `hypo_0..hypo_{K-1}` 的 jsonl,对每条样本的所有**有序对**用 LLM judge 判优劣,输出有向 K×K 矩阵(两方向独立判,暴露位置偏置)。

```bash
# 最简:判 dev 的一个语言对(model 默认 gpt-4o-mini)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp v1

# 换 judge 的 prompt(rubric),开新实验名
python3 pairwise_matrix.py --in dev/en-ru.jsonl --model gpt-4o-mini --exp v2 \
  --rubric-file my_rubric.txt

# 复用别处的缓存(同 model/prompt/译文时全命中,零 API)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp v2 \
  --cache-path dev/gpt-4o-mini/v1/cache/en-zh-llm-matrix.cache.jsonl

# 调试:只跑前 3 条(注意:不带 --out 会写进该实验正式输出,debug 建议加 --out)
python3 pairwise_matrix.py --in dev/en-zh.jsonl --model gpt-4o-mini --exp tmp --limit 3
```

常用参数:`--in`(必填,带 hypo 的 jsonl)、`--model`、`--exp`、`--rubric-file`(换 judge prompt)、`--concurrency`(默认 32)、`--cache-path`、`--no-cache`、`--no-log`、`--limit`。
默认产物:`<in_dir>/<model>/<exp>/<pair>-llm-matrix.jsonl`,缓存在 `cache/`,日志在 `log/`(均自动建目录)。

### `coherency_eval.py` — LLM 矩阵 vs 人工分一致性

**逻辑简述**(每个语言对独立处理):

1. **读入**:LLM 有向矩阵 `*-llm-matrix.jsonl`(每 doc 一个 K×K `winloss`)+ 共享 dev 的原始人工分 `score_i`,按 `doc_id` 对齐。
2. **LLM 对称化(处理位置偏置)**:LLM judge 倾向于偏好"先出现"的那条,所以矩阵是**有向**的——对 {i,j} 会分别判 (i 在前) 和 (j 在前) 两次,二者常**不一致**(实测约 20% 的对会随顺序翻转,见 `position_disagreements`)。对称化规则:两个方向都判 i 赢→ i 赢、都判 j 赢→ j 赢、**方向矛盾→ tie**。因此 LLM 的 tie 率(~20%)主要来自位置偏置,而非真的判平;人工矩阵则天生反对称、无此问题。
3. **重建人工裁决**:由 `score_i - score_j` 与阈值 `t` 得 win/tie/loss(`diff>t` 赢、`diff<-t` 输、否则平)。
4. **逐对比对** LLM vs 人工 → `agreement_3way` + 3×3 混淆矩阵 + `dir_strict` / `dir_both`。
5. **排序相关**:每 doc 用人工原始分 vs LLM 净分(行和)算 Kendall τ-b / Spearman ρ,再跨 doc 平均。
6. **Best@k**:LLM 净分 argmax 是否落在人工分的 top-1 / top-2。
7. **阈值扫描**:对每个 `t` 重算 4(阈值相关项),5–6 阈值无关只算一次。

> 人工矩阵在内存里按阈值即时重建,不读 `*-human-matrix.jsonl`(后者已不落盘)。

```bash
# 最简:评估某实验(自动读 dev/<model>/<exp>/ 的矩阵,导出回同目录)
python3 coherency_eval.py --model gpt-4o-mini --exp v1

# 自定义阈值扫描(首个为主阈值)
python3 coherency_eval.py --model gpt-4o-mini --exp v1 --thresholds 0,5,10,15,20,25,30,40,50

# 只评一个语言对
python3 coherency_eval.py --model gpt-4o-mini --exp v1 --pairs en-zh

# 显式指定文件 + 导出路径(绕过 model/exp 约定)
python3 coherency_eval.py --dev dev/en-zh.jsonl \
  --llm dev/gpt-4o-mini/v1/en-zh-llm-matrix.jsonl --csv /tmp/out.csv
```

常用参数:`--model`、`--exp`、`--pairs`(默认 `en-zh,en-ru`)、`--thresholds`、`--dir`(共享真值目录,默认脚本旁 `dev/`)、`--dump/--csv/--tsv`(显式则覆盖自动导出)。
默认产物:`dev/<model>/<exp>/coherency.jsonl` + `coherency_sweep.{csv,tsv}`,并在终端打印指标与阈值扫描。

---

## 3. 一致性指标速览

| 指标 | 含义 | 受阈值影响? |
|---|---|---|
| `agreement_3way` | 逐对三分类(win-i / tie / win-j)完全一致率;**都判平也算一致** | 是 |
| `dir_strict` | 人工判了胜负的对中,LLM 方向一致比例(**LLM 判平算错**) | 是 |
| `dir_both` | **两边都判胜负**的对中方向一致比例(最纯的"方向"指标) | 是 |
| `kendall_mean` / `spearman_mean` | per-doc 排序相关(人工原始分 vs LLM 净分),再跨 doc 平均 | **否**(看原始分顺序) |
| `best1` / `best2` | LLM 选的最佳是否=人工最佳 / 落在人工前二 | **否**(看原始分极值) |

> 阈值 `t`(`win_k=loss_n=t`)只决定"分差多大才算胜负",**不改变分数顺序/极值**,故 Kendall/Spearman/best 与阈值无关。

---

## 4. 与传统 MT metric meta-eval 的区别 ⭐

> 这里"算两个矩阵的 Spearman / 一致性",和 WMT Metrics Shared Task 那套 **metric meta-evaluation** 不是一回事。核心:**我们做的更接近"分源(per-source)的 segment-level 排序一致性",而传统主战场是 system-level + 全局 segment-level,且度量范式已从相关系数转向 pairwise accuracy。**

### 4.1 评测层级不同(最关键)

| | 传统 metric meta-eval | 本仓库 |
|---|---|---|
| 主层级 | **system-level**:每个系统在整个测试集上聚合成一个分,再对 N 个系统排序求相关 | 无(每个 doc 的 8 条来自不同系统,但只覆盖一句) |
| 次层级 | **segment-level**:把**所有** segment 的(metric, human)对**池化**成一个大相关 | **per-doc 内 K=8 排序**,每 doc 一个相关,再**跨 doc 平均** |

我们算的既不是经典 system-level,也不是经典全局 segment-level,而是**"对每个源句把 8 个候选排序"的能力**(item-level ranking),再平均。

### 4.2 被测对象的输出形态不同

- 传统 metric(BLEU / COMET / BLEURT)是**标量函数**,meta-eval 直接拿标量与人工标量/排序求相关。
- 本仓库的 LLM judge 本质是**成对比较**(有向、有位置偏置),要先**对称化**、再 **Borda 式聚合成净分**才能算 Spearman。这一步**有信息损失/重构**——标量是从 pairwise 反推的,不是 judge 原生输出。

### 4.3 聚合方式 → 估计量不同(易被忽略)

- 传统全局 segment-level 是**一个池化相关**(几千个点):稳,但会被**句子难度差异污染**——doc A 的 90 分与 doc B 的 90 分质量不可比,池化混入跨句尺度。
- 本仓库**先 per-doc(分组)再平均**,**天然控制源句难度**(只在同一源句内比 8 条)。这对应近年讨论的 **"group-by-item" vs "no-grouping" Kendall**(Deutsch et al. 2023 指出全局池化会虚高)。即:这是个**有意识的精细化**,但**与老论文数字不可直接对比**。

### 4.4 小样本噪声

- 全局 segment-level:n 很大,单个相关数很稳。
- 本仓库:每个相关只来自 **8 个点**,单 doc 极噪;靠 ~200 个 doc 平均才稳。这是"分组"的代价。

### 4.5 度量范式已经变了

现代 WMT metrics meta-eval(Kocmi et al. 2021;Freitag et al.)**主推 pairwise ranking accuracy + tie calibration**(Deutsch et al. 2023),而非 Spearman/Pearson——相关系数对 tie、对尺度敏感且不够任务对齐。
- 本仓库的 **`dir_both` / `agreement` 更接近现代 pairwise accuracy**;
- **Spearman 反而是相对"老派"**的展示指标。

### 4.6 设定细节

- 本仓库 judge 是 **QE 式**(给 source + 候选,无参考);传统 BLEU/COMET 多为 reference-based(COMET 也有 QE 版)。人工金标为 **MQM 衍生分**,与现代 WMT 一致。
- 本仓库**暂未做显著性检验**(传统会用 bootstrap / 置换 / Williams test 比较两个 metric 的相关是否显著不同)。

### 小结

- **区别本质**:层级(per-source 排序)、对象(pairwise 而非标量)、聚合(分组平均而非全局池化)、度量(相关系数 vs pairwise accuracy)。
- 若要**对齐现代 metric meta-eval**:
  1. 以 **pairwise accuracy(≈ `dir_both`)+ tie calibration** 为主指标,Spearman 仅作参考;
  2. 增加 **system-level** 视角(每个系统跨多句聚合后再排序)——WMT 最看重;当前矩阵已丢系统名,需从 `wmt25` 原始数据重建;
  3. 增加 **bootstrap 置信区间 / 显著性检验**。
