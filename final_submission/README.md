# Final Submission Workflow

This folder contains the final WMT2026 submission pipeline.

## Scripts

- `build_alignment_mask.py`
  Reads matrix judge outputs, compares every hypothesis to the source-side
  structure, and writes a per-hypothesis alignment mask JSONL plus a small
  report.
- `select_final_hypotheses.py`
  Builds the audit-friendly final file in exact source order. It keeps the
  judged best hypothesis when structurally valid, otherwise it falls back to
  the best-scoring structurally valid hypothesis and logs the fix.
- `align_to_source.py`
  Legacy direct aligner that selects `hypos[best]` in source order without the
  structural fallback stage.
- `make_submission_jsonl.py`
  Projects the audit-friendly final file into a thin WMT submission JSONL with
  at least `doc_id`, `tgt_lang`, and `hypothesis`.
- `run_wmt_alignment_check.sh`
  Runs the vendored WMT checker on a submission file and writes small logs.
- `vendor/genmt_check_alignment.py`
  Vendored from:
  `https://github.com/wmt-conference/wmt-collect-translations/blob/main/genmt_check_alignment.py`
- `run_final_submission_pipeline.sh`
  Runs the full pipeline and writes small reports.

## Pipeline Stages

1. Build `alignment_mask.jsonl` from the judge matrices and source JSONL.
2. Build `preliminary_final.jsonl` in source order, fixing only those samples
   whose judged winner fails the structural check but some alternative judged
   hypothesis passes it.
   Rows with no structurally valid candidate are kept as-is and flagged as
   unfixable in the audit-friendly output and reports.
3. Assert that the number of fixed samples does not exceed `--max-fixes`
   (default: `20`).
4. Project the preliminary file to a thin WMT submission JSONL.
5. Run the vendored WMT alignment checker and collect logs.

## Typical Usage

```bash
bash final_submission/run_final_submission_pipeline.sh \
  --matrix-dir results/gemini-2.5-flash/artifacts/gpt-final/matrix \
  --max-fixes 20
```

Outputs are written under `final_submission/out/<matrix-dir-name>/`.
