# S4-confirmation: Sharp/Efficient execution audit

[Definitions and coverage](README.md) · [Every fit receipt](fits.csv.gz) · [Complete candidate/stage schedules](plans.jsonl.gz)

36000 recorded or explicitly reconstructed contexts; 30928 have zero pilot depth, an admission exclusion, a fallback, an unavailable result, or a variant without hierarchical depth. They form 312 rows below. Identical parameter/reason rows are grouped across repetitions and, for G1, across anonymous group keys; no parameters are averaged. Fit-level group/repetition/source locators remain in the CSV. Positive-depth successful contexts remain in the CSV as coverage controls.

**Read the tables together by row ID.** `w1, M1` refer to the initial candidate at `m0=n`; they are formula diagnostics, **not** evidence that a stage ran. For a stopped or excluded fit they are counterfactual. `eta selected` can differ after rejected candidate schedules; its first-stage values and every failed candidate are in the CSV/plan archive. `M1` is reports required for that round, while `N` is the actual fitting sample, not total dataset size. Resource numbers are saved estimates/limits, not measured RAM usage. `NA` means not applicable or not recorded, never zero.

## Why the fit stopped or did not run

| ID | Dataset / setting | Fit phase | Estimator / configuration | Contexts | Executed depth | Depth evidence | Saved status | Explanation |
|---|---|---|---|---|---|---|---|---|
| S4-confirmation-1 | n12-r2-N13-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-2 | n12-r2-N13-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-3 | n12-r2-N13-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-4 | n12-r2-N13-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-5 | n12-r2-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-6 | n12-r2-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-7 | n12-r2-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-8 | n12-r2-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-9 | n12-r2-N66-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-10 | n12-r2-N66-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-11 | n12-r2-N66-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-12 | n12-r2-N66-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-13 | n12-r3-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-14 | n12-r3-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-15 | n12-r3-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-16 | n12-r3-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-17 | n12-r3-N22-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-18 | n12-r3-N22-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-19 | n12-r3-N22-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-20 | n12-r3-N22-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-21 | n12-r3-N4-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-22 | n12-r3-N4-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-23 | n12-r3-N4-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-24 | n12-r3-N4-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-25 | n12-r4-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-26 | n12-r4-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-27 | n12-r4-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-28 | n12-r4-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-29 | n12-r4-N11-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-30 | n12-r4-N11-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-31 | n12-r4-N11-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-32 | n12-r4-N11-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-33 | n12-r4-N2-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-34 | n12-r4-N2-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-35 | n12-r4-N2-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-36 | n12-r4-N2-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-37 | n128-r16-N13-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-38 | n128-r16-N13-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-39 | n128-r16-N13-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-40 | n128-r16-N13-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-41 | n128-r16-N22-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-42 | n128-r16-N22-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-43 | n128-r16-N22-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-44 | n128-r16-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-45 | n128-r16-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-46 | n128-r16-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-47 | n128-r16-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-48 | n128-r16-N45-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-49 | n128-r16-N45-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-50 | n128-r16-N45-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-51 | n128-r16-N67-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-52 | n128-r16-N67-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-53 | n128-r16-N7-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-54 | n128-r16-N7-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-55 | n128-r16-N7-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-56 | n128-r16-N7-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-57 | n128-r2-N190-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-58 | n128-r2-N190-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-59 | n128-r2-N190-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-60 | n128-r2-N190-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-61 | n128-r2-N381-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-62 | n128-r2-N381-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-63 | n128-r2-N381-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-64 | n128-r2-N381-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-65 | n128-r2-N63-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-66 | n128-r2-N63-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-67 | n128-r2-N63-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-68 | n128-r2-N63-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-69 | n128-r3-N135-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-70 | n128-r3-N135-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-71 | n128-r3-N135-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-72 | n128-r3-N135-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-73 | n128-r3-N2709-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-74 | n128-r3-N2709-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-75 | n128-r3-N2709-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-76 | n128-r3-N541-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-77 | n128-r3-N541-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-78 | n128-r3-N541-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-79 | n128-r3-N541-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-80 | n128-r32-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-81 | n128-r32-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-82 | n128-r32-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-83 | n128-r32-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-84 | n128-r32-N16-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-85 | n128-r32-N16-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-86 | n128-r32-N16-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-87 | n128-r32-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-88 | n128-r32-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-89 | n128-r32-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-90 | n128-r32-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-91 | n128-r4-N1354-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-92 | n128-r4-N1354-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-93 | n128-r4-N1354-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-94 | n128-r4-N270-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-95 | n128-r4-N270-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-96 | n128-r4-N270-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-97 | n128-r4-N270-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-98 | n128-r4-N67-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-99 | n128-r4-N67-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-100 | n128-r4-N67-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-101 | n128-r4-N67-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-102 | n128-r8-N14-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-103 | n128-r8-N14-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-104 | n128-r8-N14-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-105 | n128-r8-N14-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-106 | n128-r8-N15-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-107 | n128-r8-N15-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-108 | n128-r8-N15-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-109 | n128-r8-N15-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-110 | n128-r8-N290-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-111 | n128-r8-N290-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-112 | n128-r8-N46-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-113 | n128-r8-N46-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-114 | n128-r8-N46-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-115 | n128-r8-N58-b0.4-lo0.4 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-116 | n128-r8-N58-b0.4-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-117 | n128-r8-N58-b0.4-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-118 | n128-r8-N58-b0.8-lo0.4 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-119 | n128-r8-N58-b0.8-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-120 | n128-r8-N58-b0.8-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-121 | n128-r8-N58-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-122 | n128-r8-N58-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-123 | n128-r8-N58-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-124 | n128-r8-N58-b1.6-lo0.4 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-125 | n128-r8-N58-b1.6-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-126 | n128-r8-N58-b1.6-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-127 | n128-r8-N58-b1.6-lo1.6 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-128 | n128-r8-N58-b1.6-lo1.6 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-129 | n128-r8-N58-b1.6-lo1.6 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-130 | n128-r8-N93-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-131 | n128-r8-N93-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-132 | n16-r2-N120-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-133 | n16-r2-N120-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-134 | n16-r2-N120-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-135 | n16-r2-N120-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-136 | n16-r2-N24-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-137 | n16-r2-N24-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-138 | n16-r2-N24-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-139 | n16-r2-N24-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-140 | n16-r2-N6-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-141 | n16-r2-N6-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-142 | n16-r2-N6-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-143 | n16-r2-N6-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-144 | n16-r3-N2-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-145 | n16-r3-N2-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-146 | n16-r3-N2-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-147 | n16-r3-N2-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-148 | n16-r3-N40-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-149 | n16-r3-N40-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-150 | n16-r3-N40-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-151 | n16-r3-N40-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-152 | n16-r3-N8-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-153 | n16-r3-N8-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-154 | n16-r3-N8-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-155 | n16-r3-N8-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-156 | n16-r4-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-157 | n16-r4-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-158 | n16-r4-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-159 | n16-r4-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-160 | n16-r4-N20-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-161 | n16-r4-N20-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-162 | n16-r4-N20-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-163 | n16-r4-N20-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-164 | n16-r4-N4-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-165 | n16-r4-N4-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-166 | n16-r4-N4-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-167 | n16-r4-N4-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-168 | n2048-r32-N211-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-169 | n2048-r32-N211-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-170 | n2048-r32-N211-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-171 | n2048-r32-N4226-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-172 | n2048-r32-N4226-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-173 | n2048-r32-N845-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-174 | n2048-r32-N845-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-175 | n2048-r512-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-176 | n2048-r512-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-177 | n2048-r512-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-178 | n2048-r512-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-179 | n2048-r512-N16-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-180 | n2048-r512-N16-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-181 | n2048-r512-N16-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-182 | n2048-r512-N16-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-183 | n2048-r512-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-184 | n2048-r512-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-185 | n2048-r512-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-186 | n2048-r512-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-187 | n2048-r8-N14972-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-188 | n2048-r8-N14972-b0.8-lo0.8 | final | sharp_calibrated | 100 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-189 | n2048-r8-N14972-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-190 | n2048-r8-N3743-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-191 | n2048-r8-N3743-b0.8-lo0.8 | final | sharp_calibrated | 28 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-192 | n2048-r8-N3743-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-193 | n2048-r8-N74861-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-194 | n2048-r8-N74861-b0.8-lo0.8 | final | sharp_calibrated | 100 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-195 | n2048-r8-N74861-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-196 | n32-r3-N165-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-197 | n32-r3-N165-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-198 | n32-r3-N165-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-199 | n32-r3-N165-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-200 | n32-r3-N33-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-201 | n32-r3-N33-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-202 | n32-r3-N33-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-203 | n32-r3-N33-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-204 | n32-r3-N8-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-205 | n32-r3-N8-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-206 | n32-r3-N8-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-207 | n32-r3-N8-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-208 | n32-r8-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-209 | n32-r8-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-210 | n32-r8-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-211 | n32-r8-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-212 | n32-r8-N17-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-213 | n32-r8-N17-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-214 | n32-r8-N17-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-215 | n32-r8-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-216 | n32-r8-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-217 | n32-r8-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-218 | n32-r8-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-219 | n512-r128-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-220 | n512-r128-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-221 | n512-r128-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-222 | n512-r128-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-223 | n512-r128-N16-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-224 | n512-r128-N16-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-225 | n512-r128-N16-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-226 | n512-r128-N16-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-227 | n512-r128-N3-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-228 | n512-r128-N3-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-229 | n512-r128-N3-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-230 | n512-r128-N3-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-231 | n512-r16-N1090-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-232 | n512-r16-N1090-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-233 | n512-r16-N218-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-234 | n512-r16-N218-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-235 | n512-r16-N54-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-236 | n512-r16-N54-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-237 | n512-r16-N54-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-238 | n512-r16-N54-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-239 | n512-r3-N2180-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-240 | n512-r3-N2180-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-241 | n512-r3-N2180-b0.8-lo0.8 | final | sharp_calibrated | 4 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-242 | n512-r3-N2180-b0.8-lo0.8 | final | sharp_calibrated | 96 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-243 | n512-r3-N2180-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-244 | n512-r3-N43605-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-245 | n512-r3-N43605-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-246 | n512-r3-N43605-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-247 | n512-r3-N8721-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-248 | n512-r3-N8721-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-249 | n512-r3-N8721-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-250 | n512-r32-N13-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-251 | n512-r32-N13-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-252 | n512-r32-N13-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-253 | n512-r32-N13-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-254 | n512-r32-N263-b0.4-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-255 | n512-r32-N263-b0.4-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-256 | n512-r32-N263-b0.8-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-257 | n512-r32-N263-b0.8-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-258 | n512-r32-N263-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-259 | n512-r32-N263-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-260 | n512-r32-N263-b1.6-lo0.4 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-261 | n512-r32-N263-b1.6-lo0.4 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-262 | n512-r32-N263-b1.6-lo1.6 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-263 | n512-r32-N263-b1.6-lo1.6 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-264 | n512-r32-N52-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-265 | n512-r32-N52-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-266 | n512-r32-N52-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-267 | n512-r4-N1090-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-268 | n512-r4-N1090-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-269 | n512-r4-N1090-b0.8-lo0.8 | final | sharp_calibrated | 2 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-270 | n512-r4-N1090-b0.8-lo0.8 | final | sharp_calibrated | 98 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-271 | n512-r4-N1090-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-272 | n512-r4-N21802-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-273 | n512-r4-N21802-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-274 | n512-r4-N21802-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-275 | n512-r4-N4360-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-276 | n512-r4-N4360-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-277 | n512-r4-N4360-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-278 | n512-r8-N233-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-confirmation-279 | n512-r8-N233-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-280 | n512-r8-N233-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-281 | n512-r8-N4672-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-confirmation-282 | n512-r8-N4672-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-283 | n512-r8-N934-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-284 | n512-r8-N934-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-confirmation-285 | n8-r2-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-286 | n8-r2-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-287 | n8-r2-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-288 | n8-r2-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-289 | n8-r2-N28-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting. Terminal global Borda is still computed. |
| S4-confirmation-290 | n8-r2-N28-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-291 | n8-r2-N28-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-292 | n8-r2-N28-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-293 | n8-r2-N5-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-294 | n8-r2-N5-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-295 | n8-r2-N5-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-296 | n8-r2-N5-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-297 | n8-r3-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-298 | n8-r3-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-299 | n8-r3-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-300 | n8-r3-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-301 | n8-r3-N9-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting. Terminal global Borda is still computed. |
| S4-confirmation-302 | n8-r3-N9-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-303 | n8-r3-N9-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-304 | n8-r3-N9-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-305 | n8-r4-N1-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-306 | n8-r4-N1-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Global Borda fallback: lambda < alpha (mu < 1); no candidate resolution. |
| S4-confirmation-307 | n8-r4-N1-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-308 | n8-r4-N1-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-309 | n8-r4-N4-b0.8-lo0.8 | final | efficient_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting. Terminal global Borda is still computed. |
| S4-confirmation-310 | n8-r4-N4-b0.8-lo0.8 | final | efficient_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-confirmation-311 | n8-r4-N4-b0.8-lo0.8 | final | sharp_calibrated | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-confirmation-312 | n8-r4-N4-b0.8-lo0.8 | final | sharp_proof | 100 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |

## Initial geometry and sample requirement

| ID | n = m0 | r | N | lambda | A | eta initial | eta selected | w1 | 8w1 | M1 | floor(N/2) | W* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S4-confirmation-1 | 12 | 2 | 13 | 0.1969697 | 4 | 0.1969697 | 0.1969697 | 1 | 8 | 27 | 6 | NA |
| S4-confirmation-2 | 12 | 2 | 13 | 0.1969697 | 256 | 0.1969697 | 0.1969697 | 13 | 104 | 62237456 | 6 | NA |
| S4-confirmation-3 | 12 | 2 | 13 | 0.1969697 | 4 | 0.09090909 | 0.09090909 | 2 | 16 | 5 | 6 | 1 |
| S4-confirmation-4 | 12 | 2 | 13 | 0.1969697 | 256 | 0.09090909 | 0.09090909 | 23 | 184 | 28724980 | 6 | 22528 |
| S4-confirmation-5 | 12 | 2 | 3 | 0.04545455 | 4 | 0.04545455 | NA | 3 | 24 | 6 | 1 | NA |
| S4-confirmation-6 | 12 | 2 | 3 | 0.04545455 | 256 | 0.04545455 | NA | 39 | 312 | 12706504 | 1 | NA |
| S4-confirmation-7 | 12 | 2 | 3 | 0.04545455 | 4 | 0.09090909 | 0.09090909 | 2 | 16 | 4 | 1 | 1 |
| S4-confirmation-8 | 12 | 2 | 3 | 0.04545455 | 256 | 0.09090909 | 0.09090909 | 23 | 184 | 25413008 | 1 | 22528 |
| S4-confirmation-9 | 12 | 2 | 66 | 1 | 4 | 1 | 0.25 | 1 | 8 | 161 | 33 | NA |
| S4-confirmation-10 | 12 | 2 | 66 | 1 | 256 | 1 | 1 | 5 | 40 | 379305996 | 33 | NA |
| S4-confirmation-11 | 12 | 2 | 66 | 1 | 4 | 0.09090909 | 0.09090909 | 2 | 16 | 5 | 33 | 1 |
| S4-confirmation-12 | 12 | 2 | 66 | 1 | 256 | 0.09090909 | 0.09090909 | 23 | 184 | 34482364 | 33 | 22528 |
| S4-confirmation-13 | 12 | 3 | 1 | 0.04545455 | 4 | 0.04545455 | NA | 3 | 24 | 2 | 0 | NA |
| S4-confirmation-14 | 12 | 3 | 1 | 0.04545455 | 256 | 0.04545455 | NA | 39 | 312 | 4235502 | 0 | NA |
| S4-confirmation-15 | 12 | 3 | 1 | 0.04545455 | 4 | 0.1818182 | 0.1818182 | 1 | 8 | 3 | 0 | 1 |
| S4-confirmation-16 | 12 | 3 | 1 | 0.04545455 | 256 | 0.1818182 | 0.1818182 | 14 | 112 | 16942005 | 0 | 11264 |
| S4-confirmation-17 | 12 | 3 | 22 | 1 | 4 | 1 | 0.25 | 1 | 8 | 54 | 11 | NA |
| S4-confirmation-18 | 12 | 3 | 22 | 1 | 256 | 1 | 1 | 5 | 40 | 126435332 | 11 | NA |
| S4-confirmation-19 | 12 | 3 | 22 | 1 | 4 | 0.1818182 | 0.1818182 | 1 | 8 | 4 | 11 | 1 |
| S4-confirmation-20 | 12 | 3 | 22 | 1 | 256 | 0.1818182 | 0.1818182 | 14 | 112 | 22988243 | 11 | 11264 |
| S4-confirmation-21 | 12 | 3 | 4 | 0.1818182 | 4 | 0.1818182 | 0.1818182 | 1 | 8 | 9 | 2 | NA |
| S4-confirmation-22 | 12 | 3 | 4 | 0.1818182 | 256 | 0.1818182 | 0.1818182 | 14 | 112 | 18992218 | 2 | NA |
| S4-confirmation-23 | 12 | 3 | 4 | 0.1818182 | 4 | 0.1818182 | 0.1818182 | 1 | 8 | 3 | 2 | 1 |
| S4-confirmation-24 | 12 | 3 | 4 | 0.1818182 | 256 | 0.1818182 | 0.1818182 | 14 | 112 | 18992218 | 2 | 11264 |
| S4-confirmation-25 | 12 | 4 | 1 | 0.09090909 | 4 | 0.09090909 | NA | 2 | 16 | 2 | 0 | NA |
| S4-confirmation-26 | 12 | 4 | 1 | 0.09090909 | 256 | 0.09090909 | NA | 23 | 184 | 4450053 | 0 | NA |
| S4-confirmation-27 | 12 | 4 | 1 | 0.09090909 | 4 | 0.2727273 | 0.2727273 | 1 | 8 | 2 | 0 | 1 |
| S4-confirmation-28 | 12 | 4 | 1 | 0.09090909 | 256 | 0.2727273 | 0.2727273 | 11 | 88 | 13350158 | 0 | 7510 |
| S4-confirmation-29 | 12 | 4 | 11 | 1 | 4 | 1 | 0.2727273 | 1 | 8 | 27 | 5 | NA |
| S4-confirmation-30 | 12 | 4 | 11 | 1 | 256 | 1 | 1 | 5 | 40 | 63217666 | 5 | NA |
| S4-confirmation-31 | 12 | 4 | 11 | 1 | 4 | 0.2727273 | 0.2727273 | 1 | 8 | 3 | 5 | 1 |
| S4-confirmation-32 | 12 | 4 | 11 | 1 | 256 | 0.2727273 | 0.2727273 | 11 | 88 | 17241182 | 5 | 7510 |
| S4-confirmation-33 | 12 | 4 | 2 | 0.1818182 | 4 | 0.1818182 | NA | 1 | 8 | 5 | 1 | NA |
| S4-confirmation-34 | 12 | 4 | 2 | 0.1818182 | 256 | 0.1818182 | NA | 14 | 112 | 9496109 | 1 | NA |
| S4-confirmation-35 | 12 | 4 | 2 | 0.1818182 | 4 | 0.2727273 | 0.2727273 | 1 | 8 | 3 | 1 | 1 |
| S4-confirmation-36 | 12 | 4 | 2 | 0.1818182 | 256 | 0.2727273 | 0.2727273 | 11 | 88 | 14244164 | 1 | 7510 |
| S4-confirmation-37 | 128 | 16 | 13 | 0.1919291 | 4 | 0.1919291 | NA | 2 | 16 | 35 | 6 | NA |
| S4-confirmation-38 | 128 | 16 | 13 | 0.1919291 | 256 | 0.1919291 | 0.1919291 | 32 | 256 | 80952524 | 6 | NA |
| S4-confirmation-39 | 128 | 16 | 13 | 0.1919291 | 4 | 0.1181102 | NA | 3 | 24 | 8 | 6 | 1 |
| S4-confirmation-40 | 128 | 16 | 13 | 0.1919291 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 49816938 | 6 | 17340 |
| S4-confirmation-41 | 128 | 16 | 22 | 0.3248031 | 4 | 0.3248031 | NA | 2 | 16 | 62 | 11 | NA |
| S4-confirmation-42 | 128 | 16 | 22 | 0.3248031 | 256 | 0.3248031 | 0.3248031 | 23 | 184 | 144959677 | 11 | NA |
| S4-confirmation-43 | 128 | 16 | 22 | 0.3248031 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 52712610 | 11 | 17340 |
| S4-confirmation-44 | 128 | 16 | 3 | 0.04429134 | 4 | 0.04429134 | NA | 5 | 40 | 7 | 1 | NA |
| S4-confirmation-45 | 128 | 16 | 3 | 0.04429134 | 256 | 0.04429134 | NA | 77 | 616 | 15819994 | 1 | NA |
| S4-confirmation-46 | 128 | 16 | 3 | 0.04429134 | 4 | 0.1181102 | NA | 3 | 24 | 6 | 1 | 1 |
| S4-confirmation-47 | 128 | 16 | 3 | 0.04429134 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 42186650 | 1 | 17340 |
| S4-confirmation-48 | 128 | 16 | 45 | 0.6643701 | 4 | 0.6643701 | NA | 1 | 8 | 135 | 22 | NA |
| S4-confirmation-49 | 128 | 16 | 45 | 0.6643701 | 256 | 0.6643701 | 0.6643701 | 16 | 128 | 318979489 | 22 | NA |
| S4-confirmation-50 | 128 | 16 | 45 | 0.6643701 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 56707465 | 22 | 17340 |
| S4-confirmation-51 | 128 | 16 | 67 | 0.9891732 | 256 | 0.9891732 | 0.9891732 | 13 | 104 | 493671479 | 33 | NA |
| S4-confirmation-52 | 128 | 16 | 67 | 0.9891732 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 58945849 | 33 | 17340 |
| S4-confirmation-53 | 128 | 16 | 7 | 0.1033465 | 4 | 0.1033465 | NA | 3 | 24 | 18 | 3 | NA |
| S4-confirmation-54 | 128 | 16 | 7 | 0.1033465 | 256 | 0.1033465 | NA | 45 | 360 | 40678008 | 3 | NA |
| S4-confirmation-55 | 128 | 16 | 7 | 0.1033465 | 4 | 0.1181102 | NA | 3 | 24 | 7 | 3 | 1 |
| S4-confirmation-56 | 128 | 16 | 7 | 0.1033465 | 256 | 0.1181102 | 0.1181102 | 42 | 336 | 46489152 | 3 | 17340 |
| S4-confirmation-57 | 128 | 2 | 190 | 0.02337598 | 4 | 0.02337598 | 0.02337598 | 8 | 64 | 395 | 95 | NA |
| S4-confirmation-58 | 128 | 2 | 190 | 0.02337598 | 256 | 0.02337598 | 0.02337598 | 117 | 936 | 932725574 | 95 | NA |
| S4-confirmation-59 | 128 | 2 | 190 | 0.02337598 | 4 | 0.007874016 | 0.007874016 | 16 | 128 | 45 | 95 | 1 |
| S4-confirmation-60 | 128 | 2 | 190 | 0.02337598 | 256 | 0.007874016 | 0.007874016 | 255 | 2040 | 314181246 | 95 | 260096 |
| S4-confirmation-61 | 128 | 2 | 381 | 0.046875 | 4 | 0.046875 | 0.0234375 | 5 | 40 | 855 | 190 | NA |
| S4-confirmation-62 | 128 | 2 | 381 | 0.046875 | 256 | 0.046875 | 0.046875 | 74 | 592 | 2022226807 | 190 | NA |
| S4-confirmation-63 | 128 | 2 | 381 | 0.046875 | 4 | 0.007874016 | 0.007874016 | 16 | 128 | 48 | 190 | 1 |
| S4-confirmation-64 | 128 | 2 | 381 | 0.046875 | 256 | 0.007874016 | 0.007874016 | 255 | 2040 | 339691643 | 190 | 260096 |
| S4-confirmation-65 | 128 | 2 | 63 | 0.007750984 | 4 | 0.007750984 | NA | 17 | 136 | 118 | 31 | NA |
| S4-confirmation-66 | 128 | 2 | 63 | 0.007750984 | 256 | 0.007750984 | NA | 258 | 2064 | 278189226 | 31 | NA |
| S4-confirmation-67 | 128 | 2 | 63 | 0.007750984 | 4 | 0.007874016 | 0.007874016 | 16 | 128 | 40 | 31 | 1 |
| S4-confirmation-68 | 128 | 2 | 63 | 0.007750984 | 256 | 0.007874016 | 0.007874016 | 255 | 2040 | 282604928 | 31 | 260096 |
| S4-confirmation-69 | 128 | 3 | 135 | 0.04982776 | 4 | 0.04982776 | 0.02491388 | 5 | 40 | 305 | 67 | NA |
| S4-confirmation-70 | 128 | 3 | 135 | 0.04982776 | 256 | 0.04982776 | 0.04982776 | 71 | 568 | 721575834 | 67 | NA |
| S4-confirmation-71 | 128 | 3 | 135 | 0.04982776 | 4 | 0.01574803 | 0.01574803 | 10 | 80 | 33 | 67 | 1 |
| S4-confirmation-72 | 128 | 3 | 135 | 0.04982776 | 256 | 0.01574803 | 0.01574803 | 154 | 1232 | 228053597 | 67 | 130048 |
| S4-confirmation-73 | 128 | 3 | 2709 | 0.999877 | 256 | 0.999877 | 0.999877 | 13 | 104 | 19981070965 | 1354 | NA |
| S4-confirmation-74 | 128 | 3 | 2709 | 0.999877 | 4 | 0.01574803 | 0.01574803 | 10 | 80 | 45 | 1354 | 1 |
| S4-confirmation-75 | 128 | 3 | 2709 | 0.999877 | 256 | 0.01574803 | 0.01574803 | 154 | 1232 | 314701254 | 1354 | 130048 |
| S4-confirmation-76 | 128 | 3 | 541 | 0.1996801 | 4 | 0.1996801 | 0.02496001 | 2 | 16 | 1431 | 270 | NA |
| S4-confirmation-77 | 128 | 3 | 541 | 0.1996801 | 256 | 0.1996801 | 0.1996801 | 31 | 248 | 3383489244 | 270 | NA |
| S4-confirmation-78 | 128 | 3 | 541 | 0.1996801 | 4 | 0.01574803 | 0.01574803 | 10 | 80 | 38 | 270 | 1 |
| S4-confirmation-79 | 128 | 3 | 541 | 0.1996801 | 256 | 0.01574803 | 0.01574803 | 154 | 1232 | 266843268 | 270 | 130048 |
| S4-confirmation-80 | 128 | 32 | 1 | 0.06102362 | 4 | 0.06102362 | NA | 4 | 32 | 3 | 0 | NA |
| S4-confirmation-81 | 128 | 32 | 1 | 0.06102362 | 256 | 0.06102362 | NA | 63 | 504 | 5470997 | 0 | NA |
| S4-confirmation-82 | 128 | 32 | 1 | 0.06102362 | 4 | 0.2440945 | NA | 2 | 16 | 4 | 0 | 1 |
| S4-confirmation-83 | 128 | 32 | 1 | 0.06102362 | 256 | 0.2440945 | 0.2440945 | 27 | 216 | 21883987 | 0 | 8391 |
| S4-confirmation-84 | 128 | 32 | 16 | 0.976378 | 4 | 0.976378 | NA | 1 | 8 | 50 | 8 | NA |
| S4-confirmation-85 | 128 | 32 | 16 | 0.976378 | 256 | 0.976378 | 0.976378 | 13 | 104 | 117745006 | 8 | NA |
| S4-confirmation-86 | 128 | 32 | 16 | 0.976378 | 256 | 0.2440945 | 0.2440945 | 27 | 216 | 29436252 | 8 | 8391 |
| S4-confirmation-87 | 128 | 32 | 3 | 0.1830709 | 4 | 0.1830709 | NA | 2 | 16 | 8 | 1 | NA |
| S4-confirmation-88 | 128 | 32 | 3 | 0.1830709 | 256 | 0.1830709 | NA | 32 | 256 | 18584761 | 1 | NA |
| S4-confirmation-89 | 128 | 32 | 3 | 0.1830709 | 4 | 0.2440945 | NA | 2 | 16 | 4 | 1 | 1 |
| S4-confirmation-90 | 128 | 32 | 3 | 0.1830709 | 256 | 0.2440945 | 0.2440945 | 27 | 216 | 24779682 | 1 | 8391 |
| S4-confirmation-91 | 128 | 4 | 1354 | 0.9995079 | 256 | 0.9995079 | 0.9995079 | 13 | 104 | 9986495507 | 677 | NA |
| S4-confirmation-92 | 128 | 4 | 1354 | 0.9995079 | 4 | 0.02362205 | 0.02362205 | 8 | 64 | 34 | 677 | 1 |
| S4-confirmation-93 | 128 | 4 | 1354 | 0.9995079 | 256 | 0.02362205 | 0.02362205 | 116 | 928 | 236017620 | 677 | 86699 |
| S4-confirmation-94 | 128 | 4 | 270 | 0.199311 | 4 | 0.199311 | 0.02491388 | 2 | 16 | 714 | 135 | NA |
| S4-confirmation-95 | 128 | 4 | 270 | 0.199311 | 256 | 0.199311 | 0.199311 | 31 | 248 | 1688276355 | 135 | NA |
| S4-confirmation-96 | 128 | 4 | 270 | 0.199311 | 4 | 0.02362205 | 0.02362205 | 8 | 64 | 29 | 135 | 1 |
| S4-confirmation-97 | 128 | 4 | 270 | 0.199311 | 256 | 0.02362205 | 0.02362205 | 116 | 928 | 200092013 | 135 | 86699 |
| S4-confirmation-98 | 128 | 4 | 67 | 0.04945866 | 4 | 0.04945866 | 0.02472933 | 5 | 40 | 152 | 33 | NA |
| S4-confirmation-99 | 128 | 4 | 67 | 0.04945866 | 256 | 0.04945866 | 0.04945866 | 72 | 576 | 357809921 | 33 | NA |
| S4-confirmation-100 | 128 | 4 | 67 | 0.04945866 | 4 | 0.02362205 | 0.02362205 | 8 | 64 | 25 | 33 | 1 |
| S4-confirmation-101 | 128 | 4 | 67 | 0.04945866 | 256 | 0.02362205 | 0.02362205 | 116 | 928 | 170894291 | 33 | 86699 |
| S4-confirmation-102 | 128 | 8 | 14 | 0.04822835 | 4 | 0.04822835 | NA | 5 | 40 | 32 | 7 | NA |
| S4-confirmation-103 | 128 | 8 | 14 | 0.04822835 | 256 | 0.04822835 | NA | 73 | 584 | 74550460 | 7 | NA |
| S4-confirmation-104 | 128 | 8 | 14 | 0.04822835 | 4 | 0.05511811 | NA | 5 | 40 | 13 | 7 | 1 |
| S4-confirmation-105 | 128 | 8 | 14 | 0.04822835 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 85200526 | 7 | 37157 |
| S4-confirmation-106 | 128 | 8 | 15 | 0.05167323 | 4 | 0.05167323 | NA | 5 | 40 | 35 | 7 | NA |
| S4-confirmation-107 | 128 | 8 | 15 | 0.05167323 | 256 | 0.05167323 | NA | 70 | 560 | 80510624 | 7 | NA |
| S4-confirmation-108 | 128 | 8 | 15 | 0.05167323 | 4 | 0.05511811 | NA | 5 | 40 | 13 | 7 | 1 |
| S4-confirmation-109 | 128 | 8 | 15 | 0.05167323 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 85877999 | 7 | 37157 |
| S4-confirmation-110 | 128 | 8 | 290 | 0.9990157 | 256 | 0.9990157 | 0.9990157 | 13 | 104 | 2138809088 | 145 | NA |
| S4-confirmation-111 | 128 | 8 | 290 | 0.9990157 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 37157 |
| S4-confirmation-112 | 128 | 8 | 46 | 0.1584646 | 4 | 0.1584646 | NA | 3 | 24 | 119 | 23 | NA |
| S4-confirmation-113 | 128 | 8 | 46 | 0.1584646 | 256 | 0.1584646 | 0.1584646 | 35 | 280 | 280460449 | 23 | NA |
| S4-confirmation-114 | 128 | 8 | 46 | 0.1584646 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 97551461 | 23 | 37157 |
| S4-confirmation-115 | 128 | 8 | 58 | 0.1998031 | 4 | 0.1998031 | NA | 2 | 16 | 165 | 29 | NA |
| S4-confirmation-116 | 128 | 8 | 58 | 0.1998031 | 256 | 0.1998031 | 0.1998031 | 31 | 248 | 5774051282 | 29 | NA |
| S4-confirmation-117 | 128 | 8 | 58 | 0.1998031 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 1592841733 | 29 | 37157 |
| S4-confirmation-118 | 128 | 8 | 58 | 0.1998031 | 4 | 0.1998031 | NA | 2 | 16 | 165 | 29 | NA |
| S4-confirmation-119 | 128 | 8 | 58 | 0.1998031 | 256 | 0.1998031 | 0.1998031 | 31 | 248 | 5774051282 | 29 | NA |
| S4-confirmation-120 | 128 | 8 | 58 | 0.1998031 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 1592841733 | 29 | 37157 |
| S4-confirmation-121 | 128 | 8 | 58 | 0.1998031 | 4 | 0.1998031 | NA | 2 | 16 | 154 | 29 | NA |
| S4-confirmation-122 | 128 | 8 | 58 | 0.1998031 | 256 | 0.1998031 | 0.1998031 | 31 | 248 | 362764470 | 29 | NA |
| S4-confirmation-123 | 128 | 8 | 58 | 0.1998031 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 100072958 | 29 | 37157 |
| S4-confirmation-124 | 128 | 8 | 58 | 0.1998031 | 4 | 0.1998031 | NA | 2 | 16 | 165 | 29 | NA |
| S4-confirmation-125 | 128 | 8 | 58 | 0.1998031 | 256 | 0.1998031 | 0.1998031 | 31 | 248 | 5774051282 | 29 | NA |
| S4-confirmation-126 | 128 | 8 | 58 | 0.1998031 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 1592841733 | 29 | 37157 |
| S4-confirmation-127 | 128 | 8 | 58 | 0.1998031 | 4 | 0.1998031 | NA | 2 | 16 | 144 | 29 | NA |
| S4-confirmation-128 | 128 | 8 | 58 | 0.1998031 | 256 | 0.1998031 | 0.1998031 | 31 | 248 | 27862387 | 29 | NA |
| S4-confirmation-129 | 128 | 8 | 58 | 0.1998031 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 7686176 | 29 | 37157 |
| S4-confirmation-130 | 128 | 8 | 93 | 0.320374 | 256 | 0.320374 | 0.320374 | 24 | 192 | 611899199 | 46 | NA |
| S4-confirmation-131 | 128 | 8 | 93 | 0.320374 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 105272981 | 46 | 37157 |
| S4-confirmation-132 | 16 | 2 | 120 | 1 | 4 | 1 | 0.25 | 1 | 8 | 302 | 60 | NA |
| S4-confirmation-133 | 16 | 2 | 120 | 1 | 256 | 1 | 1 | 5 | 40 | 712496119 | 60 | NA |
| S4-confirmation-134 | 16 | 2 | 120 | 1 | 4 | 0.06666667 | 0.06666667 | 2 | 16 | 7 | 60 | 1 |
| S4-confirmation-135 | 16 | 2 | 120 | 1 | 256 | 0.06666667 | 0.06666667 | 31 | 248 | 47499742 | 60 | 30720 |
| S4-confirmation-136 | 16 | 2 | 24 | 0.2 | 4 | 0.2 | 0.2 | 1 | 8 | 51 | 12 | NA |
| S4-confirmation-137 | 16 | 2 | 24 | 0.2 | 256 | 0.2 | 0.2 | 14 | 112 | 118682654 | 12 | NA |
| S4-confirmation-138 | 16 | 2 | 24 | 0.2 | 4 | 0.06666667 | 0.06666667 | 2 | 16 | 6 | 12 | 1 |
| S4-confirmation-139 | 16 | 2 | 24 | 0.2 | 256 | 0.06666667 | 0.06666667 | 31 | 248 | 39560885 | 12 | 30720 |
| S4-confirmation-140 | 16 | 2 | 6 | 0.05 | 4 | 0.05 | NA | 3 | 24 | 12 | 3 | NA |
| S4-confirmation-141 | 16 | 2 | 6 | 0.05 | 256 | 0.05 | NA | 38 | 304 | 26062318 | 3 | NA |
| S4-confirmation-142 | 16 | 2 | 6 | 0.05 | 4 | 0.06666667 | 0.06666667 | 2 | 16 | 5 | 3 | 1 |
| S4-confirmation-143 | 16 | 2 | 6 | 0.05 | 256 | 0.06666667 | 0.06666667 | 31 | 248 | 34749758 | 3 | 30720 |
| S4-confirmation-144 | 16 | 3 | 2 | 0.05 | 4 | 0.05 | NA | 3 | 24 | 4 | 1 | NA |
| S4-confirmation-145 | 16 | 3 | 2 | 0.05 | 256 | 0.05 | NA | 38 | 304 | 8687440 | 1 | NA |
| S4-confirmation-146 | 16 | 3 | 2 | 0.05 | 4 | 0.1333333 | 0.1333333 | 2 | 16 | 4 | 1 | 1 |
| S4-confirmation-147 | 16 | 3 | 2 | 0.05 | 256 | 0.1333333 | 0.1333333 | 19 | 152 | 23166505 | 1 | 15360 |
| S4-confirmation-148 | 16 | 3 | 40 | 1 | 4 | 1 | 0.25 | 1 | 8 | 101 | 20 | NA |
| S4-confirmation-149 | 16 | 3 | 40 | 1 | 256 | 1 | 1 | 5 | 40 | 237498707 | 20 | NA |
| S4-confirmation-150 | 16 | 3 | 40 | 1 | 4 | 0.1333333 | 0.1333333 | 2 | 16 | 5 | 20 | 1 |
| S4-confirmation-151 | 16 | 3 | 40 | 1 | 256 | 0.1333333 | 0.1333333 | 19 | 152 | 31666495 | 20 | 15360 |
| S4-confirmation-152 | 16 | 3 | 8 | 0.2 | 4 | 0.2 | 0.2 | 1 | 8 | 17 | 4 | NA |
| S4-confirmation-153 | 16 | 3 | 8 | 0.2 | 256 | 0.2 | 0.2 | 14 | 112 | 39560885 | 4 | NA |
| S4-confirmation-154 | 16 | 3 | 8 | 0.2 | 4 | 0.1333333 | 0.1333333 | 2 | 16 | 4 | 4 | 1 |
| S4-confirmation-155 | 16 | 3 | 8 | 0.2 | 256 | 0.1333333 | 0.1333333 | 19 | 152 | 26373924 | 4 | 15360 |
| S4-confirmation-156 | 16 | 4 | 1 | 0.05 | 4 | 0.05 | NA | 3 | 24 | 2 | 0 | NA |
| S4-confirmation-157 | 16 | 4 | 1 | 0.05 | 256 | 0.05 | NA | 38 | 304 | 4343720 | 0 | NA |
| S4-confirmation-158 | 16 | 4 | 1 | 0.05 | 4 | 0.2 | 0.2 | 1 | 8 | 3 | 0 | 1 |
| S4-confirmation-159 | 16 | 4 | 1 | 0.05 | 256 | 0.2 | 0.2 | 14 | 112 | 17374879 | 0 | 10240 |
| S4-confirmation-160 | 16 | 4 | 20 | 1 | 4 | 1 | 0.25 | 1 | 8 | 51 | 10 | NA |
| S4-confirmation-161 | 16 | 4 | 20 | 1 | 256 | 1 | 1 | 5 | 40 | 118749354 | 10 | NA |
| S4-confirmation-162 | 16 | 4 | 20 | 1 | 4 | 0.2 | 0.2 | 1 | 8 | 4 | 10 | 1 |
| S4-confirmation-163 | 16 | 4 | 20 | 1 | 256 | 0.2 | 0.2 | 14 | 112 | 23749871 | 10 | 10240 |
| S4-confirmation-164 | 16 | 4 | 4 | 0.2 | 4 | 0.2 | 0.2 | 1 | 8 | 9 | 2 | NA |
| S4-confirmation-165 | 16 | 4 | 4 | 0.2 | 256 | 0.2 | 0.2 | 14 | 112 | 19780443 | 2 | NA |
| S4-confirmation-166 | 16 | 4 | 4 | 0.2 | 4 | 0.2 | 0.2 | 1 | 8 | 3 | 2 | 1 |
| S4-confirmation-167 | 16 | 4 | 4 | 0.2 | 256 | 0.2 | 0.2 | 14 | 112 | 19780443 | 2 | 10240 |
| S4-confirmation-168 | 2048 | 32 | 211 | 0.04992825 | 4 | 0.04992825 | NA | 14 | 112 | 644 | 105 | NA |
| S4-confirmation-169 | 2048 | 32 | 211 | 0.04992825 | 256 | 0.04992825 | 0.04992825 | 223 | 1784 | 1522972747 | 105 | NA |
| S4-confirmation-170 | 2048 | 32 | 211 | 0.04992825 | 256 | 0.01514411 | 0.01514411 | 434 | 3472 | 461944341 | 105 | 135235 |
| S4-confirmation-171 | 2048 | 32 | 4226 | 0.9999847 | 256 | 0.9999847 | 0.1249981 | 47 | 376 | 39465024556 | 2113 | NA |
| S4-confirmation-172 | 2048 | 32 | 4226 | 0.9999847 | 256 | 0.01514411 | 0.01514411 | 434 | 3472 | 597671929 | 2113 | 135235 |
| S4-confirmation-173 | 2048 | 32 | 845 | 0.1999496 | 256 | 0.1999496 | 0.09997481 | 107 | 856 | 6926888841 | 422 | NA |
| S4-confirmation-174 | 2048 | 32 | 845 | 0.1999496 | 256 | 0.01514411 | 0.01514411 | 434 | 3472 | 524640102 | 422 | 135235 |
| S4-confirmation-175 | 2048 | 512 | 1 | 0.0624084 | 4 | 0.0624084 | NA | 13 | 104 | 4 | 0 | NA |
| S4-confirmation-176 | 2048 | 512 | 1 | 0.0624084 | 256 | 0.0624084 | NA | 198 | 1584 | 7374865 | 0 | NA |
| S4-confirmation-177 | 2048 | 512 | 1 | 0.0624084 | 4 | 0.2496336 | NA | 6 | 48 | 5 | 0 | 1 |
| S4-confirmation-178 | 2048 | 512 | 1 | 0.0624084 | 256 | 0.2496336 | NA | 95 | 760 | 29499458 | 0 | 8205 |
| S4-confirmation-179 | 2048 | 512 | 16 | 0.9985344 | 4 | 0.9985344 | NA | 3 | 24 | 64 | 8 | NA |
| S4-confirmation-180 | 2048 | 512 | 16 | 0.9985344 | 256 | 0.9985344 | NA | 47 | 376 | 149401508 | 8 | NA |
| S4-confirmation-181 | 2048 | 512 | 16 | 0.9985344 | 4 | 0.2496336 | NA | 6 | 48 | 6 | 8 | 1 |
| S4-confirmation-182 | 2048 | 512 | 16 | 0.9985344 | 256 | 0.2496336 | NA | 95 | 760 | 37350377 | 8 | 8205 |
| S4-confirmation-183 | 2048 | 512 | 3 | 0.1872252 | 4 | 0.1872252 | NA | 7 | 56 | 11 | 1 | NA |
| S4-confirmation-184 | 2048 | 512 | 3 | 0.1872252 | 256 | 0.1872252 | NA | 110 | 880 | 24452848 | 1 | NA |
| S4-confirmation-185 | 2048 | 512 | 3 | 0.1872252 | 4 | 0.2496336 | NA | 6 | 48 | 5 | 1 | 1 |
| S4-confirmation-186 | 2048 | 512 | 3 | 0.1872252 | 256 | 0.2496336 | NA | 95 | 760 | 32603797 | 1 | 8205 |
| S4-confirmation-187 | 2048 | 8 | 14972 | 0.1999954 | 256 | 0.1999954 | 0.09999771 | 107 | 856 | 122735421624 | 7486 | NA |
| S4-confirmation-188 | 2048 | 8 | 14972 | 0.1999954 | 4 | 0.003419638 | 0.003419638 | 67 | 536 | 296 | 7486 | 3 |
| S4-confirmation-189 | 2048 | 8 | 14972 | 0.1999954 | 256 | 0.003419638 | 0.003419638 | 1067 | 8536 | 2098601920 | 7486 | 598894 |
| S4-confirmation-190 | 2048 | 8 | 3743 | 0.04999886 | 256 | 0.04999886 | 0.04999886 | 223 | 1784 | 27020244008 | 1871 | NA |
| S4-confirmation-191 | 2048 | 8 | 3743 | 0.04999886 | 4 | 0.003419638 | 0.003419638 | 67 | 536 | 261 | 1871 | 3 |
| S4-confirmation-192 | 2048 | 8 | 3743 | 0.04999886 | 256 | 0.003419638 | 0.003419638 | 1067 | 8536 | 1848031650 | 1871 | 598894 |
| S4-confirmation-193 | 2048 | 8 | 74861 | 0.9999905 | 256 | 0.9999905 | 0.1249988 | 47 | 376 | 699099027001 | 37430 | NA |
| S4-confirmation-194 | 2048 | 8 | 74861 | 0.9999905 | 4 | 0.003419638 | 0.003419638 | 67 | 536 | 337 | 37430 | 3 |
| S4-confirmation-195 | 2048 | 8 | 74861 | 0.9999905 | 256 | 0.003419638 | 0.003419638 | 1067 | 8536 | 2390688756 | 37430 | 598894 |
| S4-confirmation-196 | 32 | 3 | 165 | 0.9979839 | 4 | 0.9979839 | 0.124748 | 1 | 8 | 447 | 82 | NA |
| S4-confirmation-197 | 32 | 3 | 165 | 0.9979839 | 256 | 0.9979839 | 0.9979839 | 7 | 56 | 1057133287 | 82 | NA |
| S4-confirmation-198 | 32 | 3 | 165 | 0.9979839 | 4 | 0.06451613 | 0.06451613 | 3 | 24 | 10 | 82 | 1 |
| S4-confirmation-199 | 32 | 3 | 165 | 0.9979839 | 256 | 0.06451613 | 0.06451613 | 38 | 304 | 68339930 | 82 | 31744 |
| S4-confirmation-200 | 32 | 3 | 33 | 0.1995968 | 4 | 0.1995968 | 0.09979839 | 2 | 16 | 75 | 16 | NA |
| S4-confirmation-201 | 32 | 3 | 33 | 0.1995968 | 256 | 0.1995968 | 0.1995968 | 18 | 144 | 176414216 | 16 | NA |
| S4-confirmation-202 | 32 | 3 | 33 | 0.1995968 | 4 | 0.06451613 | 0.06451613 | 3 | 24 | 9 | 16 | 1 |
| S4-confirmation-203 | 32 | 3 | 33 | 0.1995968 | 256 | 0.06451613 | 0.06451613 | 38 | 304 | 57022777 | 16 | 31744 |
| S4-confirmation-204 | 32 | 3 | 8 | 0.0483871 | 4 | 0.0483871 | NA | 3 | 24 | 16 | 4 | NA |
| S4-confirmation-205 | 32 | 3 | 8 | 0.0483871 | 256 | 0.0483871 | NA | 47 | 376 | 36723920 | 4 | NA |
| S4-confirmation-206 | 32 | 3 | 8 | 0.0483871 | 4 | 0.06451613 | 0.06451613 | 3 | 24 | 7 | 4 | 1 |
| S4-confirmation-207 | 32 | 3 | 8 | 0.0483871 | 256 | 0.06451613 | 0.06451613 | 38 | 304 | 48965227 | 4 | 31744 |
| S4-confirmation-208 | 32 | 8 | 1 | 0.05645161 | 4 | 0.05645161 | NA | 3 | 24 | 2 | 0 | NA |
| S4-confirmation-209 | 32 | 8 | 1 | 0.05645161 | 256 | 0.05645161 | NA | 42 | 336 | 4658956 | 0 | NA |
| S4-confirmation-210 | 32 | 8 | 1 | 0.05645161 | 4 | 0.2258065 | NA | 2 | 16 | 3 | 0 | 1 |
| S4-confirmation-211 | 32 | 8 | 1 | 0.05645161 | 256 | 0.2258065 | 0.2258065 | 17 | 136 | 18635821 | 0 | 9070 |
| S4-confirmation-212 | 32 | 8 | 17 | 0.9596774 | 4 | 0.9596774 | NA | 1 | 8 | 46 | 8 | NA |
| S4-confirmation-213 | 32 | 8 | 17 | 0.9596774 | 256 | 0.9596774 | 0.9596774 | 7 | 56 | 108459109 | 8 | NA |
| S4-confirmation-214 | 32 | 8 | 17 | 0.9596774 | 256 | 0.2258065 | 0.2258065 | 17 | 136 | 25519791 | 8 | 9070 |
| S4-confirmation-215 | 32 | 8 | 3 | 0.1693548 | 4 | 0.1693548 | NA | 2 | 16 | 7 | 1 | NA |
| S4-confirmation-216 | 32 | 8 | 3 | 0.1693548 | 256 | 0.1693548 | NA | 20 | 160 | 15738663 | 1 | NA |
| S4-confirmation-217 | 32 | 8 | 3 | 0.1693548 | 4 | 0.2258065 | NA | 2 | 16 | 3 | 1 | 1 |
| S4-confirmation-218 | 32 | 8 | 3 | 0.1693548 | 256 | 0.2258065 | 0.2258065 | 17 | 136 | 20984883 | 1 | 9070 |
| S4-confirmation-219 | 512 | 128 | 1 | 0.06213307 | 4 | 0.06213307 | NA | 7 | 56 | 3 | 0 | NA |
| S4-confirmation-220 | 512 | 128 | 1 | 0.06213307 | 256 | 0.06213307 | NA | 107 | 856 | 6404206 | 0 | NA |
| S4-confirmation-221 | 512 | 128 | 1 | 0.06213307 | 4 | 0.2485323 | NA | 4 | 32 | 4 | 0 | 1 |
| S4-confirmation-222 | 512 | 128 | 1 | 0.06213307 | 256 | 0.2485323 | 0.2485323 | 50 | 400 | 25616821 | 0 | 8241 |
| S4-confirmation-223 | 512 | 128 | 16 | 0.9941292 | 4 | 0.9941292 | NA | 2 | 16 | 57 | 8 | NA |
| S4-confirmation-224 | 512 | 128 | 16 | 0.9941292 | 256 | 0.9941292 | 0.4970646 | 24 | 192 | 133624717 | 8 | NA |
| S4-confirmation-225 | 512 | 128 | 16 | 0.9941292 | 4 | 0.2485323 | NA | 4 | 32 | 5 | 8 | 1 |
| S4-confirmation-226 | 512 | 128 | 16 | 0.9941292 | 256 | 0.2485323 | 0.2485323 | 50 | 400 | 33406180 | 8 | 8241 |
| S4-confirmation-227 | 512 | 128 | 3 | 0.1863992 | 4 | 0.1863992 | NA | 4 | 32 | 10 | 1 | NA |
| S4-confirmation-228 | 512 | 128 | 3 | 0.1863992 | 256 | 0.1863992 | NA | 58 | 464 | 21508210 | 1 | NA |
| S4-confirmation-229 | 512 | 128 | 3 | 0.1863992 | 4 | 0.2485323 | NA | 4 | 32 | 5 | 1 | 1 |
| S4-confirmation-230 | 512 | 128 | 3 | 0.1863992 | 256 | 0.2485323 | 0.2485323 | 50 | 400 | 28677614 | 1 | 8241 |
| S4-confirmation-231 | 512 | 16 | 1090 | 0.9998777 | 256 | 0.9998777 | 0.4999388 | 24 | 192 | 9107635880 | 545 | NA |
| S4-confirmation-232 | 512 | 16 | 1090 | 0.9998777 | 256 | 0.02935421 | 0.02935421 | 167 | 1336 | 267380136 | 545 | 69769 |
| S4-confirmation-233 | 512 | 16 | 218 | 0.1999755 | 256 | 0.1999755 | 0.1999755 | 56 | 448 | 1573699218 | 109 | NA |
| S4-confirmation-234 | 512 | 16 | 218 | 0.1999755 | 256 | 0.02935421 | 0.02935421 | 167 | 1336 | 231001721 | 109 | 69769 |
| S4-confirmation-235 | 512 | 16 | 54 | 0.04953523 | 4 | 0.04953523 | NA | 8 | 64 | 143 | 27 | NA |
| S4-confirmation-236 | 512 | 16 | 54 | 0.04953523 | 256 | 0.04953523 | 0.04953523 | 122 | 976 | 337438128 | 27 | NA |
| S4-confirmation-237 | 512 | 16 | 54 | 0.04953523 | 4 | 0.02935421 | NA | 11 | 88 | 29 | 27 | 1 |
| S4-confirmation-238 | 512 | 16 | 54 | 0.04953523 | 256 | 0.02935421 | 0.02935421 | 167 | 1336 | 199963335 | 27 | 69769 |
| S4-confirmation-239 | 512 | 3 | 2180 | 0.04999388 | 4 | 0.04999388 | 0.006249236 | 8 | 64 | 5764 | 1090 | NA |
| S4-confirmation-240 | 512 | 3 | 2180 | 0.04999388 | 256 | 0.04999388 | 0.04999388 | 122 | 976 | 13636224634 | 1090 | NA |
| S4-confirmation-241 | 512 | 3 | 2180 | 0.04999388 | 4 | 0.003913894 | 0.003913894 | 39 | 312 | 151 | 1090 | 2 |
| S4-confirmation-242 | 512 | 3 | 2180 | 0.04999388 | 4 | 0.003913894 | 0.003913894 | 39 | 312 | 151 | 1090 | 2 |
| S4-confirmation-243 | 512 | 3 | 2180 | 0.04999388 | 256 | 0.003913894 | 0.003913894 | 618 | 4944 | 1067545415 | 1090 | 523264 |
| S4-confirmation-244 | 512 | 3 | 43605 | 0.9999924 | 256 | 0.9999924 | 0.4999962 | 24 | 192 | 364350755485 | 21802 | NA |
| S4-confirmation-245 | 512 | 3 | 43605 | 0.9999924 | 4 | 0.003913894 | 0.003913894 | 39 | 312 | 201 | 21802 | 2 |
| S4-confirmation-246 | 512 | 3 | 43605 | 0.9999924 | 256 | 0.003913894 | 0.003913894 | 618 | 4944 | 1426041256 | 21802 | 523264 |
| S4-confirmation-247 | 512 | 3 | 8721 | 0.1999985 | 256 | 0.1999985 | 0.1999985 | 56 | 448 | 62955890468 | 4360 | NA |
| S4-confirmation-248 | 512 | 3 | 8721 | 0.1999985 | 4 | 0.003913894 | 0.003913894 | 39 | 312 | 174 | 4360 | 2 |
| S4-confirmation-249 | 512 | 3 | 8721 | 0.1999985 | 256 | 0.003913894 | 0.003913894 | 618 | 4944 | 1232022931 | 4360 | 523264 |
| S4-confirmation-250 | 512 | 32 | 13 | 0.04929061 | 4 | 0.04929061 | NA | 8 | 64 | 35 | 6 | NA |
| S4-confirmation-251 | 512 | 32 | 13 | 0.04929061 | 256 | 0.04929061 | NA | 123 | 984 | 81191163 | 6 | NA |
| S4-confirmation-252 | 512 | 32 | 13 | 0.04929061 | 4 | 0.06066536 | NA | 7 | 56 | 15 | 6 | 1 |
| S4-confirmation-253 | 512 | 32 | 13 | 0.04929061 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 99927586 | 6 | 33759 |
| S4-confirmation-254 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 34361759920 | 131 | NA |
| S4-confirmation-255 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 2090449273 | 131 | 33759 |
| S4-confirmation-256 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 34361759920 | 131 | NA |
| S4-confirmation-257 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 2090449273 | 131 | 33759 |
| S4-confirmation-258 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 2197028442 | 131 | NA |
| S4-confirmation-259 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 133659525 | 131 | 33759 |
| S4-confirmation-260 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 34361759920 | 131 | NA |
| S4-confirmation-261 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 2090449273 | 131 | 33759 |
| S4-confirmation-262 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 171612576 | 131 | NA |
| S4-confirmation-263 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 10440309 | 131 | 33759 |
| S4-confirmation-264 | 512 | 32 | 52 | 0.1971624 | 4 | 0.1971624 | NA | 4 | 32 | 159 | 26 | NA |
| S4-confirmation-265 | 512 | 32 | 52 | 0.1971624 | 256 | 0.1971624 | 0.1971624 | 57 | 456 | 374860003 | 26 | NA |
| S4-confirmation-266 | 512 | 32 | 52 | 0.1971624 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 115341540 | 26 | 33759 |
| S4-confirmation-267 | 512 | 4 | 1090 | 0.04999388 | 4 | 0.04999388 | 0.006249236 | 8 | 64 | 2882 | 545 | NA |
| S4-confirmation-268 | 512 | 4 | 1090 | 0.04999388 | 256 | 0.04999388 | 0.04999388 | 122 | 976 | 6818112317 | 545 | NA |
| S4-confirmation-269 | 512 | 4 | 1090 | 0.04999388 | 4 | 0.005870841 | 0.005870841 | 30 | 240 | 113 | 545 | 2 |
| S4-confirmation-270 | 512 | 4 | 1090 | 0.04999388 | 4 | 0.005870841 | 0.005870841 | 30 | 240 | 113 | 545 | 2 |
| S4-confirmation-271 | 512 | 4 | 1090 | 0.04999388 | 256 | 0.005870841 | 0.005870841 | 466 | 3728 | 800659062 | 545 | 348843 |
| S4-confirmation-272 | 512 | 4 | 21802 | 0.9999694 | 256 | 0.9999694 | 0.4999847 | 24 | 192 | 182170845696 | 10901 | NA |
| S4-confirmation-273 | 512 | 4 | 21802 | 0.9999694 | 4 | 0.005870841 | 0.005870841 | 30 | 240 | 151 | 10901 | 2 |
| S4-confirmation-274 | 512 | 4 | 21802 | 0.9999694 | 256 | 0.005870841 | 0.005870841 | 466 | 3728 | 1069528862 | 10901 | 348843 |
| S4-confirmation-275 | 512 | 4 | 4360 | 0.1999755 | 256 | 0.1999755 | 0.1999755 | 56 | 448 | 31473984357 | 2180 | NA |
| S4-confirmation-276 | 512 | 4 | 4360 | 0.1999755 | 4 | 0.005870841 | 0.005870841 | 30 | 240 | 131 | 2180 | 2 |
| S4-confirmation-277 | 512 | 4 | 4360 | 0.1999755 | 256 | 0.005870841 | 0.005870841 | 466 | 3728 | 924006881 | 2180 | 348843 |
| S4-confirmation-278 | 512 | 8 | 233 | 0.04987158 | 4 | 0.04987158 | NA | 8 | 64 | 616 | 116 | NA |
| S4-confirmation-279 | 512 | 8 | 233 | 0.04987158 | 256 | 0.04987158 | 0.04987158 | 122 | 976 | 1457059857 | 116 | NA |
| S4-confirmation-280 | 512 | 8 | 233 | 0.04987158 | 256 | 0.01369863 | 0.01369863 | 267 | 2136 | 400222450 | 116 | 149504 |
| S4-confirmation-281 | 512 | 8 | 4672 | 1 | 256 | 1 | 0.5 | 24 | 192 | 39037904663 | 2336 | NA |
| S4-confirmation-282 | 512 | 8 | 4672 | 1 | 256 | 0.01369863 | 0.01369863 | 267 | 2136 | 534765818 | 2336 | 149504 |
| S4-confirmation-283 | 512 | 8 | 934 | 0.1999144 | 256 | 0.1999144 | 0.1999144 | 56 | 448 | 6742161904 | 467 | NA |
| S4-confirmation-284 | 512 | 8 | 934 | 0.1999144 | 256 | 0.01369863 | 0.01369863 | 267 | 2136 | 461989681 | 467 | 149504 |
| S4-confirmation-285 | 8 | 2 | 1 | 0.03571429 | 4 | 0.03571429 | NA | 3 | 24 | 2 | 0 | NA |
| S4-confirmation-286 | 8 | 2 | 1 | 0.03571429 | 256 | 0.03571429 | NA | 43 | 344 | 4104901 | 0 | NA |
| S4-confirmation-287 | 8 | 2 | 1 | 0.03571429 | 4 | 0.1428571 | 0.1428571 | 1 | 8 | 3 | 0 | 1 |
| S4-confirmation-288 | 8 | 2 | 1 | 0.03571429 | 256 | 0.1428571 | 0.1428571 | 15 | 120 | 16419601 | 0 | 14336 |
| S4-confirmation-289 | 8 | 2 | 28 | 1 | 4 | 1 | 0.5 | 1 | 8 | 65 | 14 | NA |
| S4-confirmation-290 | 8 | 2 | 28 | 1 | 256 | 1 | 1 | 4 | 32 | 153609642 | 14 | NA |
| S4-confirmation-291 | 8 | 2 | 28 | 1 | 4 | 0.1428571 | 0.1428571 | 1 | 8 | 4 | 14 | 1 |
| S4-confirmation-292 | 8 | 2 | 28 | 1 | 256 | 0.1428571 | 0.1428571 | 15 | 120 | 21944235 | 14 | 14336 |
| S4-confirmation-293 | 8 | 2 | 5 | 0.1785714 | 4 | 0.1785714 | 0.1785714 | 1 | 8 | 10 | 2 | NA |
| S4-confirmation-294 | 8 | 2 | 5 | 0.1785714 | 256 | 0.1785714 | 0.1785714 | 13 | 104 | 22781546 | 2 | NA |
| S4-confirmation-295 | 8 | 2 | 5 | 0.1785714 | 4 | 0.1428571 | 0.1428571 | 1 | 8 | 3 | 2 | 1 |
| S4-confirmation-296 | 8 | 2 | 5 | 0.1785714 | 256 | 0.1428571 | 0.1428571 | 15 | 120 | 18225237 | 2 | 14336 |
| S4-confirmation-297 | 8 | 3 | 1 | 0.1071429 | 4 | 0.1071429 | NA | 2 | 16 | 2 | 0 | NA |
| S4-confirmation-298 | 8 | 3 | 1 | 0.1071429 | 256 | 0.1071429 | NA | 18 | 144 | 4365902 | 0 | NA |
| S4-confirmation-299 | 8 | 3 | 1 | 0.1071429 | 4 | 0.2857143 | 0.2857143 | 1 | 8 | 2 | 0 | 1 |
| S4-confirmation-300 | 8 | 3 | 1 | 0.1071429 | 256 | 0.2857143 | 0.2857143 | 9 | 72 | 11642406 | 0 | 7168 |
| S4-confirmation-301 | 8 | 3 | 9 | 0.9642857 | 4 | 0.9642857 | 0.4821429 | 1 | 8 | 21 | 4 | NA |
| S4-confirmation-302 | 8 | 3 | 9 | 0.9642857 | 256 | 0.9642857 | 0.9642857 | 4 | 32 | 49168447 | 4 | NA |
| S4-confirmation-303 | 8 | 3 | 9 | 0.9642857 | 4 | 0.2857143 | 0.2857143 | 1 | 8 | 3 | 4 | 1 |
| S4-confirmation-304 | 8 | 3 | 9 | 0.9642857 | 256 | 0.2857143 | 0.2857143 | 9 | 72 | 14568429 | 4 | 7168 |
| S4-confirmation-305 | 8 | 4 | 1 | 0.2142857 | 4 | 0.2142857 | NA | 1 | 8 | 2 | 0 | NA |
| S4-confirmation-306 | 8 | 4 | 1 | 0.2142857 | 256 | 0.2142857 | NA | 11 | 88 | 4635255 | 0 | NA |
| S4-confirmation-307 | 8 | 4 | 1 | 0.2142857 | 4 | 0.4285714 | 0.4285714 | 1 | 8 | 2 | 0 | 1 |
| S4-confirmation-308 | 8 | 4 | 1 | 0.2142857 | 256 | 0.4285714 | 0.4285714 | 7 | 56 | 9270509 | 0 | 4779 |
| S4-confirmation-309 | 8 | 4 | 4 | 0.8571429 | 4 | 0.8571429 | 0.4285714 | 1 | 8 | 10 | 2 | NA |
| S4-confirmation-310 | 8 | 4 | 4 | 0.8571429 | 256 | 0.8571429 | 0.8571429 | 5 | 40 | 21558681 | 2 | NA |
| S4-confirmation-311 | 8 | 4 | 4 | 0.8571429 | 4 | 0.4285714 | 0.4285714 | 1 | 8 | 2 | 2 | 1 |
| S4-confirmation-312 | 8 | 4 | 4 | 0.8571429 | 256 | 0.4285714 | 0.4285714 | 7 | 56 | 10779341 | 2 | 4779 |

## Constants and selected-resolution checks

The first table uses the initial resolution. This table exposes the resolution ultimately selected and the constants used to calculate each budget. A selected-resolution first round remains hypothetical when the root stops.

| ID | beta0 | cW | c terminal | K | CT | Initial eta*m0 | Selected eta*m0 | Selected w1 | Selected M1 | Initial 8w1 < m0 |
|---|---|---|---|---|---|---|---|---|---|---|
| S4-confirmation-1 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 2.363636 | 2.363636 | 1 | 27 | yes |
| S4-confirmation-2 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.363636 | 2.363636 | 13 | 62237456 | no |
| S4-confirmation-3 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.090909 | 1.090909 | 2 | 5 | no |
| S4-confirmation-4 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.090909 | 1.090909 | 23 | 28724980 | no |
| S4-confirmation-5 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.5454545 | NA | NA | NA | no |
| S4-confirmation-6 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.5454545 | NA | NA | NA | no |
| S4-confirmation-7 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.090909 | 1.090909 | 2 | 4 | no |
| S4-confirmation-8 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.090909 | 1.090909 | 23 | 25413008 | no |
| S4-confirmation-9 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 12 | 3 | 1 | 41 | yes |
| S4-confirmation-10 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 12 | 12 | 5 | 379305996 | no |
| S4-confirmation-11 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.090909 | 1.090909 | 2 | 5 | no |
| S4-confirmation-12 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.090909 | 1.090909 | 23 | 34482364 | no |
| S4-confirmation-13 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.5454545 | NA | NA | NA | no |
| S4-confirmation-14 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.5454545 | NA | NA | NA | no |
| S4-confirmation-15 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.181818 | 2.181818 | 1 | 3 | yes |
| S4-confirmation-16 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.181818 | 2.181818 | 14 | 16942005 | no |
| S4-confirmation-17 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 12 | 3 | 1 | 14 | yes |
| S4-confirmation-18 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 12 | 12 | 5 | 126435332 | no |
| S4-confirmation-19 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.181818 | 2.181818 | 1 | 4 | yes |
| S4-confirmation-20 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.181818 | 2.181818 | 14 | 22988243 | no |
| S4-confirmation-21 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 2.181818 | 2.181818 | 1 | 9 | yes |
| S4-confirmation-22 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.181818 | 2.181818 | 14 | 18992218 | no |
| S4-confirmation-23 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.181818 | 2.181818 | 1 | 3 | yes |
| S4-confirmation-24 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.181818 | 2.181818 | 14 | 18992218 | no |
| S4-confirmation-25 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 1.090909 | NA | NA | NA | no |
| S4-confirmation-26 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.090909 | NA | NA | NA | no |
| S4-confirmation-27 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.272727 | 3.272727 | 1 | 2 | yes |
| S4-confirmation-28 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.272727 | 3.272727 | 11 | 13350158 | no |
| S4-confirmation-29 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 12 | 3.272727 | 1 | 8 | yes |
| S4-confirmation-30 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 12 | 12 | 5 | 63217666 | no |
| S4-confirmation-31 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.272727 | 3.272727 | 1 | 3 | yes |
| S4-confirmation-32 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.272727 | 3.272727 | 11 | 17241182 | no |
| S4-confirmation-33 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 2.181818 | NA | NA | NA | yes |
| S4-confirmation-34 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.181818 | NA | NA | NA | no |
| S4-confirmation-35 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.272727 | 3.272727 | 1 | 3 | yes |
| S4-confirmation-36 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.272727 | 3.272727 | 11 | 14244164 | no |
| S4-confirmation-37 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 24.56693 | NA | NA | NA | yes |
| S4-confirmation-38 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 24.56693 | 24.56693 | 32 | 80952524 | no |
| S4-confirmation-39 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 15.11811 | NA | NA | NA | yes |
| S4-confirmation-40 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 49816938 | no |
| S4-confirmation-41 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 41.5748 | NA | NA | NA | yes |
| S4-confirmation-42 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 41.5748 | 41.5748 | 23 | 144959677 | no |
| S4-confirmation-43 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 52712610 | no |
| S4-confirmation-44 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 5.669291 | NA | NA | NA | yes |
| S4-confirmation-45 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 5.669291 | NA | NA | NA | no |
| S4-confirmation-46 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 15.11811 | NA | NA | NA | yes |
| S4-confirmation-47 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 42186650 | no |
| S4-confirmation-48 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 85.03937 | NA | NA | NA | yes |
| S4-confirmation-49 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 85.03937 | 85.03937 | 16 | 318979489 | no |
| S4-confirmation-50 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 56707465 | no |
| S4-confirmation-51 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 126.6142 | 126.6142 | 13 | 493671479 | yes |
| S4-confirmation-52 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 58945849 | no |
| S4-confirmation-53 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 13.22835 | NA | NA | NA | yes |
| S4-confirmation-54 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 13.22835 | NA | NA | NA | no |
| S4-confirmation-55 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 15.11811 | NA | NA | NA | yes |
| S4-confirmation-56 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.11811 | 15.11811 | 42 | 46489152 | no |
| S4-confirmation-57 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 2.992126 | 2.992126 | 8 | 395 | yes |
| S4-confirmation-58 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.992126 | 2.992126 | 117 | 932725574 | no |
| S4-confirmation-59 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.007874 | 1.007874 | 16 | 45 | no |
| S4-confirmation-60 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.007874 | 1.007874 | 255 | 314181246 | no |
| S4-confirmation-61 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6 | 3 | 8 | 428 | yes |
| S4-confirmation-62 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6 | 6 | 74 | 2022226807 | no |
| S4-confirmation-63 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.007874 | 1.007874 | 16 | 48 | no |
| S4-confirmation-64 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.007874 | 1.007874 | 255 | 339691643 | no |
| S4-confirmation-65 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.992126 | NA | NA | NA | no |
| S4-confirmation-66 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.992126 | NA | NA | NA | no |
| S4-confirmation-67 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.007874 | 1.007874 | 16 | 40 | no |
| S4-confirmation-68 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.007874 | 1.007874 | 255 | 282604928 | no |
| S4-confirmation-69 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.377953 | 3.188976 | 7 | 153 | yes |
| S4-confirmation-70 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.377953 | 6.377953 | 71 | 721575834 | no |
| S4-confirmation-71 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.015748 | 2.015748 | 10 | 33 | yes |
| S4-confirmation-72 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.015748 | 2.015748 | 154 | 228053597 | no |
| S4-confirmation-73 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.9843 | 127.9843 | 13 | 19981070965 | yes |
| S4-confirmation-74 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.015748 | 2.015748 | 10 | 45 | yes |
| S4-confirmation-75 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.015748 | 2.015748 | 154 | 314701254 | no |
| S4-confirmation-76 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.55906 | 3.194882 | 7 | 179 | yes |
| S4-confirmation-77 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.55906 | 25.55906 | 31 | 3383489244 | no |
| S4-confirmation-78 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.015748 | 2.015748 | 10 | 38 | yes |
| S4-confirmation-79 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.015748 | 2.015748 | 154 | 266843268 | no |
| S4-confirmation-80 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 7.811024 | NA | NA | NA | yes |
| S4-confirmation-81 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.811024 | NA | NA | NA | no |
| S4-confirmation-82 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-confirmation-83 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 21883987 | no |
| S4-confirmation-84 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 124.9764 | NA | NA | NA | yes |
| S4-confirmation-85 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 124.9764 | 124.9764 | 13 | 117745006 | yes |
| S4-confirmation-86 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 29436252 | no |
| S4-confirmation-87 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 23.43307 | NA | NA | NA | yes |
| S4-confirmation-88 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 23.43307 | NA | NA | NA | no |
| S4-confirmation-89 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-confirmation-90 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 24779682 | no |
| S4-confirmation-91 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.937 | 127.937 | 13 | 9986495507 | yes |
| S4-confirmation-92 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.023622 | 3.023622 | 8 | 34 | yes |
| S4-confirmation-93 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.023622 | 3.023622 | 116 | 236017620 | no |
| S4-confirmation-94 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.51181 | 3.188976 | 7 | 90 | yes |
| S4-confirmation-95 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.51181 | 25.51181 | 31 | 1688276355 | no |
| S4-confirmation-96 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.023622 | 3.023622 | 8 | 29 | yes |
| S4-confirmation-97 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.023622 | 3.023622 | 116 | 200092013 | no |
| S4-confirmation-98 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.330709 | 3.165354 | 8 | 76 | yes |
| S4-confirmation-99 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.330709 | 6.330709 | 72 | 357809921 | no |
| S4-confirmation-100 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.023622 | 3.023622 | 8 | 25 | yes |
| S4-confirmation-101 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.023622 | 3.023622 | 116 | 170894291 | no |
| S4-confirmation-102 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.173228 | NA | NA | NA | yes |
| S4-confirmation-103 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.173228 | NA | NA | NA | no |
| S4-confirmation-104 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.055118 | NA | NA | NA | yes |
| S4-confirmation-105 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 85200526 | no |
| S4-confirmation-106 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.614173 | NA | NA | NA | yes |
| S4-confirmation-107 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.614173 | NA | NA | NA | no |
| S4-confirmation-108 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.055118 | NA | NA | NA | yes |
| S4-confirmation-109 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 85877999 | no |
| S4-confirmation-110 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 127.874 | 13 | 2138809088 | yes |
| S4-confirmation-111 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-confirmation-112 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 20.28346 | NA | NA | NA | yes |
| S4-confirmation-113 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 20.28346 | 20.28346 | 35 | 280460449 | no |
| S4-confirmation-114 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 97551461 | no |
| S4-confirmation-115 | 0.4 | 0.0625 | 0.001953125 | 0.3 | 60.79787 | 25.5748 | NA | NA | NA | yes |
| S4-confirmation-116 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 25.5748 | 25.5748 | 31 | 5774051282 | no |
| S4-confirmation-117 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 7.055118 | 7.055118 | 67 | 1592841733 | no |
| S4-confirmation-118 | 0.4 | 0.0625 | 0.001953125 | 0.3 | 60.79787 | 25.5748 | NA | NA | NA | yes |
| S4-confirmation-119 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 25.5748 | 25.5748 | 31 | 5774051282 | no |
| S4-confirmation-120 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 7.055118 | 7.055118 | 67 | 1592841733 | no |
| S4-confirmation-121 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.5748 | NA | NA | NA | yes |
| S4-confirmation-122 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.5748 | 25.5748 | 31 | 362764470 | no |
| S4-confirmation-123 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 100072958 | no |
| S4-confirmation-124 | 0.4 | 0.0625 | 0.001953125 | 0.3 | 60.79787 | 25.5748 | NA | NA | NA | yes |
| S4-confirmation-125 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 25.5748 | 25.5748 | 31 | 5774051282 | no |
| S4-confirmation-126 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 7.055118 | 7.055118 | 67 | 1592841733 | no |
| S4-confirmation-127 | 1.6 | 0.0625 | 0.001953125 | 0.3 | 18.07129 | 25.5748 | NA | NA | NA | yes |
| S4-confirmation-128 | 1.6 | 1 | 8 | 58202.29 | 18.07129 | 25.5748 | 25.5748 | 31 | 27862387 | no |
| S4-confirmation-129 | 1.6 | 1 | 8 | 58202.29 | 18.07129 | 7.055118 | 7.055118 | 67 | 7686176 | no |
| S4-confirmation-130 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 41.00787 | 41.00787 | 24 | 611899199 | no |
| S4-confirmation-131 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 105272981 | no |
| S4-confirmation-132 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 16 | 4 | 1 | 76 | yes |
| S4-confirmation-133 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 16 | 16 | 5 | 712496119 | no |
| S4-confirmation-134 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.066667 | 1.066667 | 2 | 7 | no |
| S4-confirmation-135 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.066667 | 1.066667 | 31 | 47499742 | no |
| S4-confirmation-136 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 3.2 | 3.2 | 1 | 51 | yes |
| S4-confirmation-137 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 118682654 | no |
| S4-confirmation-138 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.066667 | 1.066667 | 2 | 6 | no |
| S4-confirmation-139 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.066667 | 1.066667 | 31 | 39560885 | no |
| S4-confirmation-140 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-141 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-142 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.066667 | 1.066667 | 2 | 5 | no |
| S4-confirmation-143 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.066667 | 1.066667 | 31 | 34749758 | no |
| S4-confirmation-144 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-145 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-146 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.133333 | 2.133333 | 2 | 4 | no |
| S4-confirmation-147 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.133333 | 2.133333 | 19 | 23166505 | no |
| S4-confirmation-148 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 16 | 4 | 1 | 26 | yes |
| S4-confirmation-149 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 16 | 16 | 5 | 237498707 | no |
| S4-confirmation-150 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.133333 | 2.133333 | 2 | 5 | no |
| S4-confirmation-151 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.133333 | 2.133333 | 19 | 31666495 | no |
| S4-confirmation-152 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 3.2 | 3.2 | 1 | 17 | yes |
| S4-confirmation-153 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 39560885 | no |
| S4-confirmation-154 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.133333 | 2.133333 | 2 | 4 | no |
| S4-confirmation-155 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.133333 | 2.133333 | 19 | 26373924 | no |
| S4-confirmation-156 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-157 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.8 | NA | NA | NA | no |
| S4-confirmation-158 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.2 | 3.2 | 1 | 3 | yes |
| S4-confirmation-159 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 17374879 | no |
| S4-confirmation-160 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 16 | 4 | 1 | 13 | yes |
| S4-confirmation-161 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 16 | 16 | 5 | 118749354 | no |
| S4-confirmation-162 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.2 | 3.2 | 1 | 4 | yes |
| S4-confirmation-163 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 23749871 | no |
| S4-confirmation-164 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 3.2 | 3.2 | 1 | 9 | yes |
| S4-confirmation-165 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 19780443 | no |
| S4-confirmation-166 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.2 | 3.2 | 1 | 3 | yes |
| S4-confirmation-167 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.2 | 3.2 | 14 | 19780443 | no |
| S4-confirmation-168 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 102.2531 | NA | NA | NA | yes |
| S4-confirmation-169 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.2531 | 102.2531 | 223 | 1522972747 | yes |
| S4-confirmation-170 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.01514 | 31.01514 | 434 | 461944341 | no |
| S4-confirmation-171 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2047.969 | 255.9961 | 137 | 4933128070 | yes |
| S4-confirmation-172 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.01514 | 31.01514 | 434 | 597671929 | no |
| S4-confirmation-173 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 409.4968 | 204.7484 | 154 | 3463444421 | yes |
| S4-confirmation-174 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.01514 | 31.01514 | 434 | 524640102 | no |
| S4-confirmation-175 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 127.8124 | NA | NA | NA | yes |
| S4-confirmation-176 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.8124 | NA | NA | NA | yes |
| S4-confirmation-177 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-178 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-179 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 2044.999 | NA | NA | NA | yes |
| S4-confirmation-180 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2044.999 | NA | NA | NA | yes |
| S4-confirmation-181 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-182 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-183 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 383.4372 | NA | NA | NA | yes |
| S4-confirmation-184 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 383.4372 | NA | NA | NA | yes |
| S4-confirmation-185 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-186 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.2496 | NA | NA | NA | yes |
| S4-confirmation-187 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 409.5906 | 204.7953 | 154 | 61367710812 | yes |
| S4-confirmation-188 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.00342 | 7.00342 | 67 | 296 | yes |
| S4-confirmation-189 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.00342 | 7.00342 | 1067 | 2098601920 | no |
| S4-confirmation-190 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.3977 | 102.3977 | 223 | 27020244008 | yes |
| S4-confirmation-191 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.00342 | 7.00342 | 67 | 261 | yes |
| S4-confirmation-192 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.00342 | 7.00342 | 1067 | 1848031650 | no |
| S4-confirmation-193 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2047.98 | 255.9976 | 137 | 87387378376 | yes |
| S4-confirmation-194 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.00342 | 7.00342 | 67 | 337 | yes |
| S4-confirmation-195 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.00342 | 7.00342 | 1067 | 2390688756 | no |
| S4-confirmation-196 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 31.93548 | 3.991935 | 2 | 56 | yes |
| S4-confirmation-197 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.93548 | 31.93548 | 7 | 1057133287 | no |
| S4-confirmation-198 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.064516 | 2.064516 | 3 | 10 | yes |
| S4-confirmation-199 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.064516 | 2.064516 | 38 | 68339930 | no |
| S4-confirmation-200 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.387097 | 3.193548 | 2 | 38 | yes |
| S4-confirmation-201 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.387097 | 6.387097 | 18 | 176414216 | no |
| S4-confirmation-202 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.064516 | 2.064516 | 3 | 9 | yes |
| S4-confirmation-203 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.064516 | 2.064516 | 38 | 57022777 | no |
| S4-confirmation-204 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 1.548387 | NA | NA | NA | yes |
| S4-confirmation-205 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.548387 | NA | NA | NA | no |
| S4-confirmation-206 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.064516 | 2.064516 | 3 | 7 | yes |
| S4-confirmation-207 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.064516 | 2.064516 | 38 | 48965227 | no |
| S4-confirmation-208 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 1.806452 | NA | NA | NA | yes |
| S4-confirmation-209 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.806452 | NA | NA | NA | no |
| S4-confirmation-210 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.225806 | NA | NA | NA | yes |
| S4-confirmation-211 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.225806 | 7.225806 | 17 | 18635821 | no |
| S4-confirmation-212 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 30.70968 | NA | NA | NA | yes |
| S4-confirmation-213 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.70968 | 30.70968 | 7 | 108459109 | no |
| S4-confirmation-214 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.225806 | 7.225806 | 17 | 25519791 | no |
| S4-confirmation-215 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 5.419355 | NA | NA | NA | yes |
| S4-confirmation-216 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 5.419355 | NA | NA | NA | no |
| S4-confirmation-217 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 7.225806 | NA | NA | NA | yes |
| S4-confirmation-218 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.225806 | 7.225806 | 17 | 20984883 | no |
| S4-confirmation-219 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 31.81213 | NA | NA | NA | yes |
| S4-confirmation-220 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.81213 | NA | NA | NA | no |
| S4-confirmation-221 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 127.2485 | NA | NA | NA | yes |
| S4-confirmation-222 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.2485 | 127.2485 | 50 | 25616821 | yes |
| S4-confirmation-223 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 508.9941 | NA | NA | NA | yes |
| S4-confirmation-224 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 508.9941 | 254.4971 | 35 | 66812359 | yes |
| S4-confirmation-225 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 127.2485 | NA | NA | NA | yes |
| S4-confirmation-226 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.2485 | 127.2485 | 50 | 33406180 | yes |
| S4-confirmation-227 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 95.4364 | NA | NA | NA | yes |
| S4-confirmation-228 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 95.4364 | NA | NA | NA | yes |
| S4-confirmation-229 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 127.2485 | NA | NA | NA | yes |
| S4-confirmation-230 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.2485 | 127.2485 | 50 | 28677614 | yes |
| S4-confirmation-231 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.9374 | 255.9687 | 35 | 4553817940 | yes |
| S4-confirmation-232 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.02935 | 15.02935 | 167 | 267380136 | no |
| S4-confirmation-233 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.3875 | 102.3875 | 56 | 1573699218 | yes |
| S4-confirmation-234 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.02935 | 15.02935 | 167 | 231001721 | no |
| S4-confirmation-235 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.36204 | NA | NA | NA | yes |
| S4-confirmation-236 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.36204 | 25.36204 | 122 | 337438128 | no |
| S4-confirmation-237 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 15.02935 | NA | NA | NA | yes |
| S4-confirmation-238 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.02935 | 15.02935 | 167 | 199963335 | no |
| S4-confirmation-239 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.59687 | 3.199609 | 28 | 721 | yes |
| S4-confirmation-240 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.59687 | 25.59687 | 122 | 13636224634 | no |
| S4-confirmation-241 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.003914 | 2.003914 | 39 | 151 | yes |
| S4-confirmation-242 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.003914 | 2.003914 | 39 | 151 | yes |
| S4-confirmation-243 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.003914 | 2.003914 | 618 | 1067545415 | no |
| S4-confirmation-244 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.9961 | 255.998 | 35 | 182175377743 | yes |
| S4-confirmation-245 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.003914 | 2.003914 | 39 | 201 | yes |
| S4-confirmation-246 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.003914 | 2.003914 | 618 | 1426041256 | no |
| S4-confirmation-247 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.3992 | 102.3992 | 56 | 62955890468 | yes |
| S4-confirmation-248 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.003914 | 2.003914 | 39 | 174 | yes |
| S4-confirmation-249 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.003914 | 2.003914 | 618 | 1232022931 | no |
| S4-confirmation-250 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.23679 | NA | NA | NA | yes |
| S4-confirmation-251 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.23679 | NA | NA | NA | no |
| S4-confirmation-252 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-confirmation-253 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 99927586 | no |
| S4-confirmation-254 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 510.5597 | 255.2798 | 35 | 17180879960 | yes |
| S4-confirmation-255 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 31.06067 | 31.06067 | 109 | 2090449273 | no |
| S4-confirmation-256 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 510.5597 | 255.2798 | 35 | 17180879960 | yes |
| S4-confirmation-257 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 31.06067 | 31.06067 | 109 | 2090449273 | no |
| S4-confirmation-258 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | 255.2798 | 35 | 1098514221 | yes |
| S4-confirmation-259 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 133659525 | no |
| S4-confirmation-260 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 510.5597 | 255.2798 | 35 | 17180879960 | yes |
| S4-confirmation-261 | 0.4 | 1 | 8 | 1.051579e+07 | 60.79787 | 31.06067 | 31.06067 | 109 | 2090449273 | no |
| S4-confirmation-262 | 1.6 | 1 | 8 | 58202.29 | 18.07129 | 510.5597 | 255.2798 | 35 | 85806288 | yes |
| S4-confirmation-263 | 1.6 | 1 | 8 | 58202.29 | 18.07129 | 31.06067 | 31.06067 | 109 | 10440309 | no |
| S4-confirmation-264 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 100.9472 | NA | NA | NA | yes |
| S4-confirmation-265 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 100.9472 | 100.9472 | 57 | 374860003 | yes |
| S4-confirmation-266 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 115341540 | no |
| S4-confirmation-267 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.59687 | 3.199609 | 28 | 361 | yes |
| S4-confirmation-268 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.59687 | 25.59687 | 122 | 6818112317 | no |
| S4-confirmation-269 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.005871 | 3.005871 | 30 | 113 | yes |
| S4-confirmation-270 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.005871 | 3.005871 | 30 | 113 | yes |
| S4-confirmation-271 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.005871 | 3.005871 | 466 | 800659062 | no |
| S4-confirmation-272 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 511.9843 | 255.9922 | 35 | 91085422848 | yes |
| S4-confirmation-273 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.005871 | 3.005871 | 30 | 151 | yes |
| S4-confirmation-274 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.005871 | 3.005871 | 466 | 1069528862 | no |
| S4-confirmation-275 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.3875 | 102.3875 | 56 | 31473984357 | yes |
| S4-confirmation-276 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.005871 | 3.005871 | 30 | 131 | yes |
| S4-confirmation-277 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.005871 | 3.005871 | 466 | 924006881 | no |
| S4-confirmation-278 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 25.53425 | NA | NA | NA | yes |
| S4-confirmation-279 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 25.53425 | 25.53425 | 122 | 1457059857 | no |
| S4-confirmation-280 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.013699 | 7.013699 | 267 | 400222450 | no |
| S4-confirmation-281 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 512 | 256 | 34 | 19518952332 | yes |
| S4-confirmation-282 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.013699 | 7.013699 | 267 | 534765818 | no |
| S4-confirmation-283 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 102.3562 | 102.3562 | 56 | 6742161904 | yes |
| S4-confirmation-284 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.013699 | 7.013699 | 267 | 461989681 | no |
| S4-confirmation-285 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.2857143 | NA | NA | NA | no |
| S4-confirmation-286 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.2857143 | NA | NA | NA | no |
| S4-confirmation-287 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.142857 | 1.142857 | 1 | 3 | no |
| S4-confirmation-288 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.142857 | 1.142857 | 15 | 16419601 | no |
| S4-confirmation-289 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 8 | 4 | 1 | 33 | no |
| S4-confirmation-290 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 8 | 8 | 4 | 153609642 | no |
| S4-confirmation-291 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.142857 | 1.142857 | 1 | 4 | no |
| S4-confirmation-292 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.142857 | 1.142857 | 15 | 21944235 | no |
| S4-confirmation-293 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 1.428571 | 1.428571 | 1 | 10 | no |
| S4-confirmation-294 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.428571 | 1.428571 | 13 | 22781546 | no |
| S4-confirmation-295 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 1.142857 | 1.142857 | 1 | 3 | no |
| S4-confirmation-296 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.142857 | 1.142857 | 15 | 18225237 | no |
| S4-confirmation-297 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 0.8571429 | NA | NA | NA | no |
| S4-confirmation-298 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 0.8571429 | NA | NA | NA | no |
| S4-confirmation-299 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.285714 | 2.285714 | 1 | 2 | no |
| S4-confirmation-300 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.285714 | 2.285714 | 9 | 11642406 | no |
| S4-confirmation-301 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 7.714286 | 3.857143 | 1 | 11 | no |
| S4-confirmation-302 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.714286 | 7.714286 | 4 | 49168447 | no |
| S4-confirmation-303 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 2.285714 | 2.285714 | 1 | 3 | no |
| S4-confirmation-304 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 2.285714 | 2.285714 | 9 | 14568429 | no |
| S4-confirmation-305 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 1.714286 | NA | NA | NA | no |
| S4-confirmation-306 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 1.714286 | NA | NA | NA | no |
| S4-confirmation-307 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.428571 | 3.428571 | 1 | 2 | no |
| S4-confirmation-308 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.428571 | 3.428571 | 7 | 9270509 | no |
| S4-confirmation-309 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 6.857143 | 3.428571 | 1 | 5 | no |
| S4-confirmation-310 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 6.857143 | 6.857143 | 5 | 21558681 | no |
| S4-confirmation-311 | 0.8 | 0.0625 | 0.001953125 | 0.1 | 31.58319 | 3.428571 | 3.428571 | 1 | 2 | no |
| S4-confirmation-312 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 3.428571 | 3.428571 | 7 | 10779341 | no |

## Terminal blocks and resource receipts

Ranges show different saved repetitions in the same row; exact integers and individual receipts are in the CSV. Formula W* can exceed n; the actual terminal block is clipped by the available items. A large W* is not itself a memory-allocation count.

| ID | Consumed pilot reports | Requested blocks (variant) | Actual terminal / failed block items | Resource reason | Pairs in failed block | Estimated bytes | Memory limit bytes | Time limit seconds |
|---|---|---|---|---|---|---|---|---|
| S4-confirmation-1 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-2 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-3 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-4 | 0 | NA | 12 | working_array_memory_budget | 13 | 11975040000 | 536870912 | 30 |
| S4-confirmation-5 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-6 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-7 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-8 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-9 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-10 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-11 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-12 | 0 | NA | 12 | working_array_memory_budget | 66 | 11975040000 | 536870912 | 30 |
| S4-confirmation-13 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-14 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-15 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-16 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-17 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-18 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-19 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-20 | 0 | NA | 12 | working_array_memory_budget | 22 | 11975040000 | 536870912 | 30 |
| S4-confirmation-21 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-22 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-23 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-24 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-25 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-26 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-27 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-28 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-29 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-30 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-31 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-32 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-33 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-34 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-35 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-36 | 0 | NA | 12 | NA | NA | NA | NA | NA |
| S4-confirmation-37 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-38 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-39 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-40 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-41 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-42 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-43 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-44 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-45 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-46 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-47 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-48 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-49 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-50 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-51 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-52 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-53 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-54 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-55 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-56 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-57 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-58 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-59 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-60 | 0 | NA | 128 | working_array_memory_budget | 190 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-61 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-62 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-63 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-64 | 0 | NA | 128 | working_array_memory_budget | 381 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-65 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-66 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-67 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-68 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-69 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-70 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-71 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-72 | 0 | NA | 128 | working_array_memory_budget | 135 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-73 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-74 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-75 | 0 | NA | 128 | working_array_memory_budget | 2709 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-76 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-77 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-78 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-79 | 0 | NA | 128 | working_array_memory_budget | 541 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-80 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-81 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-82 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-83 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-84 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-85 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-86 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-87 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-88 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-89 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-90 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-91 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-92 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-93 | 0 | NA | 128 | working_array_memory_budget | 1354 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-94 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-95 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-96 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-97 | 0 | NA | 128 | working_array_memory_budget | 270 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-98 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-99 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-100 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-101 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-102 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-103 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-104 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-105 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-106 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-107 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-108 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-109 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-110 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-111 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-confirmation-112 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-113 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-114 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-115 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-116 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-117 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-118 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-119 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-120 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-121 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-122 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-123 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-124 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-125 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-126 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-127 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-128 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-129 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-130 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-131 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-confirmation-132 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-133 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-134 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-135 | 0 | NA | 16 | working_array_memory_budget | 120 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-136 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-137 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-138 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-139 | 0 | NA | 16 | working_array_memory_budget | 24 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-140 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-141 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-142 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-143 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-144 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-145 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-146 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-147 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-148 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-149 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-150 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-151 | 0 | NA | 16 | working_array_memory_budget | 40 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-152 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-153 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-154 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-155 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-156 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-157 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-158 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-159 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-160 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-161 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-162 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-163 | 0 | NA | 16 | working_array_memory_budget | 20 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-164 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-165 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-166 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-167 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-168 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-169 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-170 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-171 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-172 | 0 | NA | 2048 | working_array_memory_budget | 4226 | 6.8530e5897 | 536870912 | 30 |
| S4-confirmation-173 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-174 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-175 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-176 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-177 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-178 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-179 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-180 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-181 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-182 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-183 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-184 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-185 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-186 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-187 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-188 | 296 | NA | 15 to 21 | working_array_memory_budget | 16 to 44 | 40537905408000 to 2.1969e21 | 536870912 | 30 |
| S4-confirmation-189 | 0 | NA | 2048 | working_array_memory_budget | 14972 | 6.8530e5897 | 536870912 | 30 |
| S4-confirmation-190 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-191 | 261 | NA | 23 to 24 | working_array_memory_budget | 24 to 29 | 1.2150e24 to 3.0401e25 | 536870912 | 30 |
| S4-confirmation-192 | 0 | NA | 2048 | working_array_memory_budget | 3743 | 6.8530e5897 | 536870912 | 30 |
| S4-confirmation-193 | 0 | NA | 2048 | NA | NA | NA | NA | NA |
| S4-confirmation-194 | 337 | NA | 15 | working_array_memory_budget | 81 to 124 | 40537905408000 | 536870912 | 30 |
| S4-confirmation-195 | 0 | NA | 2048 | working_array_memory_budget | 74861 | 6.8530e5897 | 536870912 | 30 |
| S4-confirmation-196 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-197 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-198 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-199 | 0 | NA | 32 | working_array_memory_budget | 165 | 1.7103e37 | 536870912 | 30 |
| S4-confirmation-200 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-201 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-202 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-203 | 0 | NA | 32 | working_array_memory_budget | 33 | 1.7103e37 | 536870912 | 30 |
| S4-confirmation-204 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-205 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-206 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-207 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-208 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-209 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-210 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-211 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-212 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-213 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-214 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-215 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-216 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-217 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-218 | 0 | NA | 32 | NA | NA | NA | NA | NA |
| S4-confirmation-219 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-220 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-221 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-222 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-223 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-224 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-225 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-226 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-227 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-228 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-229 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-230 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-231 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-232 | 0 | NA | 512 | working_array_memory_budget | 1090 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-233 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-234 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-235 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-236 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-237 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-238 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-239 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-240 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-241 | 0 | NA | 16 | working_array_memory_budget | 17 to 18 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-242 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-243 | 0 | NA | 512 | working_array_memory_budget | 2180 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-244 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-245 | 0 | NA | 14 | working_array_memory_budget | 67 to 113 | 2528170444800 | 536870912 | 30 |
| S4-confirmation-246 | 0 | NA | 512 | working_array_memory_budget | 43605 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-247 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-248 | 0 | NA | 10 to 16 | working_array_memory_budget | 11 to 28 | 1001391552 to 690452066304000 | 536870912 | 30 |
| S4-confirmation-249 | 0 | NA | 512 | working_array_memory_budget | 8721 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-250 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-251 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-252 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-253 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-254 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-255 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-256 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-257 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-258 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-259 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-260 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-261 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-262 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-263 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-264 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-265 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-266 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-267 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-268 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-269 | 0 | NA | 16 | working_array_memory_budget | 18 | 690452066304000 | 536870912 | 30 |
| S4-confirmation-270 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-confirmation-271 | 0 | NA | 512 | working_array_memory_budget | 1090 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-272 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-273 | 0 | NA | 14 | working_array_memory_budget | 66 to 108 | 2528170444800 | 536870912 | 30 |
| S4-confirmation-274 | 0 | NA | 512 | working_array_memory_budget | 21802 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-275 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-276 | 0 | NA | 10 to 16 | working_array_memory_budget | 11 to 27 | 1213665152 to 690452066304000 | 536870912 | 30 |
| S4-confirmation-277 | 0 | NA | 512 | working_array_memory_budget | 4360 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-278 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-279 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-280 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-281 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-282 | 0 | NA | 512 | working_array_memory_budget | 4672 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-283 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-confirmation-284 | 0 | NA | 512 | working_array_memory_budget | 934 | 3.5642e1169 | 536870912 | 30 |
| S4-confirmation-285 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-286 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-287 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-288 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-289 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-290 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-291 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-292 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-293 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-294 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-295 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-296 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-297 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-298 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-299 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-300 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-301 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-302 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-303 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-304 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-305 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-306 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-307 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-308 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-309 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-310 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-confirmation-311 | 0 | NA | 7 | NA | NA | NA | NA | NA |
| S4-confirmation-312 | 0 | NA | 8 | NA | NA | NA | NA | NA |
