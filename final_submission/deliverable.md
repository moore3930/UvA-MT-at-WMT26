# Deliverable: Final Submission Pipeline Update

- Added a structural mask stage before final hypothesis selection.
- Added mask-aware fallback selection with explicit fix logging and a hard
  `max_fixes` assertion.
- Preserved source-order output and thin WMT submission generation.
- Kept unfixable rows in the output, flagged for audit, so the pipeline can
  still produce a complete submission and the WMT checker can report the
  residual misalignment count.

## Two-Best Final Export Checklist

- Run completed successfully for `gemini-3.5-flash__gpt-final`.
- Final submission file: `final_submission/out/two-best/gemini-3.5-flash__gpt-final/submission.jsonl`
- Audit summary: `final_submission/out/two-best/gemini-3.5-flash__gpt-final/reports/pipeline_summary.md`
- Selection report: `final_submission/out/two-best/gemini-3.5-flash__gpt-final/reports/selection_report.json`
- Fixed samples: `final_submission/out/two-best/gemini-3.5-flash__gpt-final/reports/fixed_samples.jsonl`
- Alignment check: `1914 checked, 1914 aligned, 0 misaligned, 16403 skipped (0 missing from translation file)`
- Export stats: `18317` rows written, `5` structural fixes, `2` cross-model fixes, `0` unfixable rows.
