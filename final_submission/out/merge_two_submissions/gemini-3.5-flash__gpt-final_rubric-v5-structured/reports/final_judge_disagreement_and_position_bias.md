# Final Judge Disagreement And Position Bias

- Final preliminary input: `/home/stroshi/UvA-MT-at-WMT26/final_submission/out/merge_two_submissions/gemini-3.5-flash__gpt-final_rubric-v5-structured/preliminary_final.jsonl`
- Selected-language cross dir: `/home/stroshi/UvA-MT-at-WMT26/results/gemini-3.5-flash/experiments/two-best/gemini-3.5-flash__gpt-final_rubric-v5-structured/cross-matrix`
- Older-language cross dir: `/home/stroshi/UvA-MT-at-WMT26/results/gemini-2.5-flash/artifacts/two-best/gemini-3.5-flash__gpt-final/cross-matrix`
- Model A: `gemini-3.5-flash`
- Model B: `gpt-final`
- `A/B disagreement` means the judge gave inconsistent results for the same unordered pair when the prompt order was swapped.
- `position A` / `position B` count wins for the first vs second hypothesis position in the judged prompt, not the underlying model identity.

| lang | docs | unique pairs | A/B disagreements | disagreement % | pos A wins | pos B wins | ties | pos A % | pos B % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ALL | 18317 | 274755 | 87271 | 31.76% | 315450 | 216695 | 53999 | 53.82% | 36.97% |
| arz | 150 | 2250 | 887 | 39.42% | 2723 | 1884 | 193 | 56.73% | 39.25% |
| arz_Arab | 198 | 2970 | 737 | 24.81% | 3117 | 3189 | 30 | 49.20% | 50.33% |
| bel_Cyrl | 198 | 2970 | 775 | 26.09% | 2928 | 3357 | 51 | 46.21% | 52.98% |
| ces_Latn | 198 | 2970 | 810 | 27.27% | 3102 | 3166 | 68 | 48.96% | 49.97% |
| cs | 1050 | 15750 | 4556 | 28.93% | 21475 | 12018 | 107 | 63.91% | 35.77% |
| cs_CZ | 917 | 13755 | 3191 | 23.20% | 12262 | 9365 | 7717 | 41.79% | 31.91% |
| de_AT | 319 | 4785 | 2369 | 49.51% | 5739 | 2745 | 1724 | 56.22% | 26.89% |
| de_CH | 322 | 4830 | 2245 | 46.48% | 6304 | 2822 | 1178 | 61.18% | 27.39% |
| de_DE | 2149 | 32235 | 10264 | 31.84% | 34113 | 22216 | 12439 | 49.61% | 32.31% |
| de_IT | 2707 | 40605 | 21378 | 52.65% | 57115 | 21499 | 8010 | 65.93% | 24.82% |
| deu_Latn | 513 | 7695 | 1970 | 25.60% | 7749 | 8480 | 187 | 47.20% | 51.66% |
| ekk_Latn | 198 | 2970 | 660 | 22.22% | 3078 | 3231 | 27 | 48.58% | 50.99% |
| et_EE | 917 | 13755 | 2897 | 21.06% | 12882 | 9330 | 7132 | 43.90% | 31.80% |
| hye_Armn | 198 | 2970 | 743 | 25.02% | 2745 | 3442 | 149 | 43.32% | 54.32% |
| ind_Latn | 198 | 2970 | 699 | 23.54% | 2949 | 3349 | 38 | 46.54% | 52.86% |
| is | 345 | 5175 | 964 | 18.63% | 5426 | 4566 | 1048 | 49.15% | 41.36% |
| isl_Latn | 198 | 2970 | 674 | 22.69% | 2992 | 3275 | 69 | 47.22% | 51.69% |
| jpn_Jpan | 388 | 5820 | 1589 | 27.30% | 5645 | 6684 | 87 | 45.47% | 53.83% |
| kaz_Cyrl | 198 | 2970 | 641 | 21.58% | 2995 | 3314 | 27 | 47.27% | 52.30% |
| ko_KR | 1880 | 28200 | 8499 | 30.14% | 32052 | 21376 | 6732 | 53.28% | 35.53% |
| kor_Hang | 198 | 2970 | 729 | 24.55% | 2939 | 3397 | 0 | 46.39% | 53.61% |
| lij_Latn | 198 | 2970 | 705 | 23.74% | 3543 | 2761 | 32 | 55.92% | 43.58% |
| lld_Latn | 198 | 2970 | 523 | 17.61% | 3115 | 3221 | 0 | 49.16% | 50.84% |
| ru | 1000 | 15000 | 5471 | 36.47% | 21615 | 10140 | 245 | 67.55% | 31.69% |
| ru_RU | 917 | 13755 | 4200 | 30.53% | 14799 | 8962 | 5583 | 50.43% | 30.54% |
| rus_Cyrl | 198 | 2970 | 720 | 24.24% | 3033 | 3236 | 67 | 47.87% | 51.07% |
| sme_Latn | 198 | 2970 | 672 | 22.63% | 3011 | 3266 | 59 | 47.52% | 51.55% |
| tha_Thai | 198 | 2970 | 474 | 15.96% | 3083 | 3233 | 20 | 48.66% | 51.03% |
| ukr_Cyrl | 513 | 7695 | 1938 | 25.19% | 7550 | 8741 | 125 | 45.99% | 53.25% |
| vie_Latn | 315 | 4725 | 874 | 18.50% | 5928 | 4111 | 41 | 58.81% | 40.78% |
| zh_CN | 747 | 11205 | 3021 | 26.96% | 13624 | 9599 | 681 | 56.99% | 40.16% |
| zho_Hans | 198 | 2970 | 675 | 22.73% | 2871 | 3387 | 78 | 45.31% | 53.46% |
| zho_Hant_TW | 198 | 2970 | 721 | 24.28% | 2948 | 3333 | 55 | 46.53% | 52.60% |
