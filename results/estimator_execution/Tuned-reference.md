# Tuned-reference: Sharp/Efficient execution audit

[Definitions and coverage](README.md) · [Every fit receipt](fits.csv.gz) · [Complete candidate/stage schedules](plans.jsonl.gz)

19 recorded or explicitly reconstructed contexts; 19 have zero pilot depth, an admission exclusion, a fallback, an unavailable result, or a variant without hierarchical depth. They form 19 rows below. Identical parameter/reason rows are grouped across repetitions and, for G1, across anonymous group keys; no parameters are averaged. Fit-level group/repetition/source locators remain in the CSV. Positive-depth successful contexts remain in the CSV as coverage controls.

**Read the two tables together by row ID.** `w1, M1` refer to the initial candidate at `m0=n`; they are formula diagnostics, **not** evidence that a stage ran. For a stopped or excluded fit they are counterfactual. `eta selected` can differ after rejected candidate schedules; its first-stage values and every failed candidate are in the CSV/plan archive. `M1` is reports required for that round, while `N` is the actual fitting sample, not total dataset size. Resource numbers are saved estimates/limits, not measured RAM usage. `NA` means not applicable or not recorded, never zero.

## Why the fit stopped or did not run

| ID | Dataset / setting | Fit phase | Estimator / configuration | Contexts | Executed depth | Depth evidence | Saved status | Explanation |
|---|---|---|---|---|---|---|---|---|
| Tuned-reference-1 | dots2024_A_r2 / E0-dots2024_A_r2-n30-N240 | saved reference | sm_efficient_fallback | 1 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| Tuned-reference-2 | dots2024_A_r3 / E0-dots2024_A_r3-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-3 | dots2024_A_r5 / E0-dots2024_A_r5-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-4 | dots2024_A_r6 / E0-dots2024_A_r6-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-5 | dots2024_B_r2 / E0-dots2024_B_r2-n30-N240 | saved reference | sm_efficient_fallback | 1 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| Tuned-reference-6 | dots2024_B_r3 / E0-dots2024_B_r3-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-7 | dots2024_B_r5 / E0-dots2024_B_r5-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-8 | dots2024_B_r6 / E0-dots2024_B_r6-n30-N240 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-9 | patras_cost / E0-patras_cost-n36-N313 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-10 | patras_population / E0-patras_population-n48-N313 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-11 | sushi_b / E0-sushi_b-n100-N4000 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-12 | sushi_b / L0-sushi_b-n100-N1000 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-13 | sushi_b / L0-sushi_b-n100-N300 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-14 | sushi_b / L0-sushi_b-n100-N3000 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-15 | synthetic_pl / S0-synthetic_pl-n16-N100 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-16 | synthetic_pl / S0-synthetic_pl-n32-N100 | saved reference | sm_efficient_fallback | 1 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| Tuned-reference-17 | synthetic_sm / S0-synthetic_sm-n16-N100 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |
| Tuned-reference-18 | synthetic_sm / S0-synthetic_sm-n32-N100 | saved reference | sm_efficient_fallback | 1 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| Tuned-reference-19 | wheat / E0-wheat-n16-N394 | saved reference | sm_efficient_fallback | 1 | NA | not attempted | outside_schedule_domain | Not run: Efficient requires lambda <= 1. |

## Initial geometry and sample requirement

| ID | n = m0 | r | N | lambda | A | eta initial | eta selected | w1 | 8w1 | M1 | floor(N/2) | W* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tuned-reference-1 | 30 | 2 | 240 | 0.5517241 | 256 | 0.5517241 | 0.5517241 | 10 | 80 | 6570512652741 | 120 | NA |
| Tuned-reference-2 | 30 | 3 | 240 | 1.655172 | 256 | 1.655172 | NA | 5 | 40 | 7238455428890 | 120 | NA |
| Tuned-reference-3 | 30 | 5 | 240 | 5.517241 | 256 | 5.517241 | NA | 3 | 24 | 7988430376353 | 120 | NA |
| Tuned-reference-4 | 30 | 6 | 240 | 8.275862 | 256 | 8.275862 | NA | 3 | 24 | 8242691931067 | 120 | NA |
| Tuned-reference-5 | 30 | 2 | 240 | 0.5517241 | 256 | 0.5517241 | 0.5517241 | 10 | 80 | 6570512652741 | 120 | NA |
| Tuned-reference-6 | 30 | 3 | 240 | 1.655172 | 256 | 1.655172 | NA | 5 | 40 | 7238455428890 | 120 | NA |
| Tuned-reference-7 | 30 | 5 | 240 | 5.517241 | 256 | 5.517241 | NA | 3 | 24 | 7988430376353 | 120 | NA |
| Tuned-reference-8 | 30 | 6 | 240 | 8.275862 | 256 | 8.275862 | NA | 3 | 24 | 8242691931067 | 120 | NA |
| Tuned-reference-9 | 36 | 6 | 313 | 7.452381 | 256 | 7.452381 | NA | 3 | 24 | 10813304216198 | 156 | NA |
| Tuned-reference-10 | 48 | 6 | 313 | 4.162234 | 256 | 4.162234 | NA | 4 | 32 | 10572058190978 | 156 | NA |
| Tuned-reference-11 | 100 | 10 | 4000 | 36.36364 | 256 | 36.36364 | NA | 2 | 16 | 165531929882941 | 2000 | NA |
| Tuned-reference-12 | 100 | 10 | 1000 | 9.090909 | 256 | 9.090909 | NA | 4 | 32 | 37744965932677 | 500 | NA |
| Tuned-reference-13 | 100 | 10 | 300 | 2.727273 | 256 | 2.727273 | NA | 7 | 56 | 10377076399111 | 150 | NA |
| Tuned-reference-14 | 100 | 10 | 3000 | 27.27273 | 256 | 27.27273 | NA | 2 | 16 | 121883451629848 | 1500 | NA |
| Tuned-reference-15 | 16 | 3 | 100 | 2.5 | 256 | 2.5 | NA | 3 | 24 | 2960494734880 | 50 | NA |
| Tuned-reference-16 | 32 | 3 | 100 | 0.6048387 | 256 | 0.6048387 | 0.6048387 | 9 | 72 | 2776619687847 | 50 | NA |
| Tuned-reference-17 | 16 | 3 | 100 | 2.5 | 256 | 2.5 | NA | 3 | 24 | 2960494734880 | 50 | NA |
| Tuned-reference-18 | 32 | 3 | 100 | 0.6048387 | 256 | 0.6048387 | 0.6048387 | 9 | 72 | 2776619687847 | 50 | NA |
| Tuned-reference-19 | 16 | 3 | 394 | 9.85 | 256 | 9.85 | NA | 2 | 16 | 13063941840539 | 197 | NA |

## Constants and selected-resolution checks

The first table uses the initial resolution. This table exposes the resolution ultimately selected and the constants used to calculate each budget. A selected-resolution first round remains hypothetical when the root stops.

| ID | beta0 | cW | c terminal | K | CT | Initial eta*m0 | Selected eta*m0 | Selected w1 | Selected M1 | Initial 8w1 < m0 |
|---|---|---|---|---|---|---|---|---|---|---|
| Tuned-reference-1 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 16.55172 | 16.55172 | 10 | 6570512652741 | no |
| Tuned-reference-2 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 49.65517 | NA | NA | NA | no |
| Tuned-reference-3 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 165.5172 | NA | NA | NA | yes |
| Tuned-reference-4 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 248.2759 | NA | NA | NA | yes |
| Tuned-reference-5 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 16.55172 | 16.55172 | 10 | 6570512652741 | no |
| Tuned-reference-6 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 49.65517 | NA | NA | NA | no |
| Tuned-reference-7 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 165.5172 | NA | NA | NA | yes |
| Tuned-reference-8 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 248.2759 | NA | NA | NA | yes |
| Tuned-reference-9 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 268.2857 | NA | NA | NA | yes |
| Tuned-reference-10 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 199.7872 | NA | NA | NA | yes |
| Tuned-reference-11 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 3636.364 | NA | NA | NA | yes |
| Tuned-reference-12 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 909.0909 | NA | NA | NA | yes |
| Tuned-reference-13 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 272.7273 | NA | NA | NA | yes |
| Tuned-reference-14 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 2727.273 | NA | NA | NA | yes |
| Tuned-reference-15 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 40 | NA | NA | NA | no |
| Tuned-reference-16 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 19.35484 | 19.35484 | 9 | 2776619687847 | no |
| Tuned-reference-17 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 40 | NA | NA | NA | no |
| Tuned-reference-18 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 19.35484 | 19.35484 | 9 | 2776619687847 | no |
| Tuned-reference-19 | 0.1 | 1 | 8 | 2.625836e+09 | 240.2 | 157.6 | NA | NA | NA | no |

## Terminal blocks and resource receipts

Ranges show different saved repetitions in the same row; exact integers and individual receipts are in the CSV. Formula W* can exceed n; the actual terminal block is clipped by the available items. A large W* is not itself a memory-allocation count.

| ID | Consumed pilot reports | Requested blocks (variant) | Actual terminal / failed block items | Resource reason | Pairs in failed block | Estimated bytes | Memory limit bytes | Time limit seconds |
|---|---|---|---|---|---|---|---|---|
| Tuned-reference-1 | 0 | NA | 30 | NA | NA | NA | NA | NA |
| Tuned-reference-5 | 0 | NA | 30 | NA | NA | NA | NA | NA |
| Tuned-reference-16 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| Tuned-reference-18 | 0 | NA | 32 | NA | NA | NA | NA | NA |
