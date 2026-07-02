#!/usr/bin/env bash
set -euo pipefail

SOURCE_MODEL=gemini-3.5-flash JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh ru_RU
SOURCE_MODEL=gemini-3.5-flash JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh ar_AR
SOURCE_MODEL=gemini-3.5-flash JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh zh_CN

SOURCE_MODEL=gpt-5.5 JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh ru_RU
SOURCE_MODEL=gpt-5.5 JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh ar_AR
SOURCE_MODEL=gpt-5.5 JUDGE_MODEL=gemini-2.5-flash JUDGE_REASONING_EFFORT=none .local_scripts/generation/judge/run_judge_lang.sh zh_CN
