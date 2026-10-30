# S4-calibration: Sharp/Efficient execution audit

[Definitions and coverage](README.md) · [Every fit receipt](fits.csv.gz) · [Complete candidate/stage schedules](plans.jsonl.gz)

4800 recorded or explicitly reconstructed contexts; 2820 have zero pilot depth, an admission exclusion, a fallback, an unavailable result, or a variant without hierarchical depth. They form 141 rows below. Identical parameter/reason rows are grouped across repetitions and, for G1, across anonymous group keys; no parameters are averaged. Fit-level group/repetition/source locators remain in the CSV. Positive-depth successful contexts remain in the CSV as coverage controls.

**Read the tables together by row ID.** `w1, M1` refer to the initial candidate at `m0=n`; they are formula diagnostics, **not** evidence that a stage ran. For a stopped or excluded fit they are counterfactual. `eta selected` can differ after rejected candidate schedules; its first-stage values and every failed candidate are in the CSV/plan archive. `M1` is reports required for that round, while `N` is the actual fitting sample, not total dataset size. Resource numbers are saved estimates/limits, not measured RAM usage. `NA` means not applicable or not recorded, never zero.

## Why the fit stopped or did not run

| ID | Dataset / setting | Fit phase | Estimator / configuration | Contexts | Executed depth | Depth evidence | Saved status | Explanation |
|---|---|---|---|---|---|---|---|---|
| S4-calibration-1 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-2 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-3 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_A256 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-4 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-5 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_K0.3 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-6 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-7 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-8 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-9 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-10 | n128-r32-N8-b0.8-lo0.8 | final | efficient__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-11 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-12 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-13 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof_A16 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-14 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting. Terminal global Borda is still computed. |
| S4-calibration-15 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-16 | n128-r32-N8-b0.8-lo0.8 | final | efficient__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-17 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-18 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-19 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_A256 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-20 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-21 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_K0.3 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-22 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-23 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-24 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-25 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-26 | n128-r32-N8-b0.8-lo0.8 | final | sharp__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-27 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-28 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-29 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof_A16 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-30 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-31 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-32 | n128-r32-N8-b0.8-lo0.8 | final | sharp__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-33 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-34 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-35 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_A256 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-36 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-37 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-38 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-39 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-40 | n128-r8-N290-b0.8-lo0.8 | final | efficient__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-41 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-42 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-43 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof_A16 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting, sample_budget. Terminal global Borda is still computed. |
| S4-calibration-44 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting, sample_budget. Terminal global Borda is still computed. |
| S4-calibration-45 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-calibration-46 | n128-r8-N290-b0.8-lo0.8 | final | efficient__proof_A8 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting, sample_budget. Terminal global Borda is still computed. |
| S4-calibration-47 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-48 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A128 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-49 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A16 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-50 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A256 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-51 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A64 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-52 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_A8 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-53 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-54 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-55 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_terminal0.015625 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-56 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_terminal0.125 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-57 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_terminal1 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-58 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_terminal8 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-59 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-60 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-61 | n128-r8-N290-b0.8-lo0.8 | final | sharp__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-62 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-63 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof_A128 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-64 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof_A16 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-65 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof_A32 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-66 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof_A64 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-67 | n128-r8-N290-b0.8-lo0.8 | final | sharp__proof_A8 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-68 | n128-r8-N290-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.000244141 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-69 | n128-r8-N290-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.00195312 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-70 | n128-r8-N290-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.015625 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-71 | n128-r8-N290-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.125 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-72 | n128-r8-N290-b0.8-lo0.8 | final | sharp__wide_anchor_terminal8 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-73 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-74 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-75 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-76 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-77 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-78 | n512-r32-N263-b0.8-lo0.8 | final | efficient__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting, sample_budget. |
| S4-calibration-79 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-calibration-80 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-calibration-81 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof_A16 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting, sample_budget. |
| S4-calibration-82 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting, sample_budget. Terminal global Borda is still computed. |
| S4-calibration-83 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: sample_budget. Terminal global Borda is still computed. |
| S4-calibration-84 | n512-r32-N263-b0.8-lo0.8 | final | efficient__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting, sample_budget. |
| S4-calibration-85 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-86 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_A128 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-87 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_A256 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-88 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_A64 | 20 | 0 | saved | resource_limit | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-89 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-90 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-91 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_terminal0.015625 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-92 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_terminal0.125 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-93 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-94 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-95 | n512-r32-N263-b0.8-lo0.8 | final | sharp__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-96 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-97 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-98 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof_A16 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-99 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-100 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-101 | n512-r32-N263-b0.8-lo0.8 | final | sharp__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-102 | n512-r32-N263-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.015625 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-103 | n512-r32-N263-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.125 | 20 | 1 | saved | resource_limit | Hierarchy executed 1 stages. Terminal result unavailable: resource_limit. Resource receipt: working_array_memory_budget. |
| S4-calibration-104 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-105 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-106 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_A256 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-107 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-108 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_K0.3 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-109 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-110 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-111 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-112 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-113 | n64-r16-N8-b0.8-lo0.8 | final | efficient__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-114 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-115 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-116 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof_A16 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Higher resolutions rejected: noncontracting. Terminal global Borda is still computed. |
| S4-calibration-117 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-118 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal global Borda is still computed. |
| S4-calibration-119 | n64-r16-N8-b0.8-lo0.8 | final | efficient__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-120 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_A1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-121 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-122 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_A16 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-123 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_A256 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-124 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-125 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_K0.3 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-126 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_K1.0 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-127 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_KNone | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: sample_budget. |
| S4-calibration-128 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_width0.25 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-129 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_width0.5 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-130 | n64-r16-N8-b0.8-lo0.8 | final | sharp__anchor_width1 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-131 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-132 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof_A128 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-133 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof_A16 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-134 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof_A32 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-135 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof_A64 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-136 | n64-r16-N8-b0.8-lo0.8 | final | sharp__proof_A8 | 20 | 0 | saved | ok | Global Borda fallback: no feasible schedule; candidate failures: noncontracting. |
| S4-calibration-137 | n64-r16-N8-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.000244141 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-138 | n64-r16-N8-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.00195312 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-139 | n64-r16-N8-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.015625 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-140 | n64-r16-N8-b0.8-lo0.8 | final | sharp__wide_anchor_terminal0.125 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |
| S4-calibration-141 | n64-r16-N8-b0.8-lo0.8 | final | sharp__wide_anchor_terminal8 | 20 | 0 | saved | ok | Zero pilot stages: selected eta*m0 <= A; the root is terminal. Terminal pair-sieve is still required. |

## Initial geometry and sample requirement

| ID | n = m0 | r | N | lambda | A | eta initial | eta selected | w1 | 8w1 | M1 | floor(N/2) | W* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S4-calibration-1 | 128 | 32 | 8 | 0.488189 | 1 | 0.488189 | NA | 2 | 16 | 1 | 4 | NA |
| S4-calibration-2 | 128 | 32 | 8 | 0.488189 | 128 | 0.488189 | 0.488189 | 2 | 16 | 1 | 4 | NA |
| S4-calibration-3 | 128 | 32 | 8 | 0.488189 | 256 | 0.488189 | 0.488189 | 2 | 16 | 1 | 4 | NA |
| S4-calibration-4 | 128 | 32 | 8 | 0.488189 | 64 | 0.488189 | 0.488189 | 2 | 16 | 1 | 4 | NA |
| S4-calibration-5 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 2 | 16 | 24 | 4 | NA |
| S4-calibration-6 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 2 | 16 | 78 | 4 | NA |
| S4-calibration-7 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 2 | 16 | 54981570 | 4 | NA |
| S4-calibration-8 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 5 | 40 | 1 | 4 | NA |
| S4-calibration-9 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 10 | 80 | 1 | 4 | NA |
| S4-calibration-10 | 128 | 32 | 8 | 0.488189 | 4 | 0.488189 | NA | 19 | 152 | 1 | 4 | NA |
| S4-calibration-11 | 128 | 32 | 8 | 0.488189 | 256 | 0.488189 | 0.488189 | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-12 | 128 | 32 | 8 | 0.488189 | 128 | 0.488189 | 0.488189 | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-13 | 128 | 32 | 8 | 0.488189 | 16 | 0.488189 | NA | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-14 | 128 | 32 | 8 | 0.488189 | 32 | 0.488189 | 0.2440945 | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-15 | 128 | 32 | 8 | 0.488189 | 64 | 0.488189 | 0.488189 | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-16 | 128 | 32 | 8 | 0.488189 | 8 | 0.488189 | NA | 19 | 152 | 54981570 | 4 | NA |
| S4-calibration-17 | 128 | 32 | 8 | 0.488189 | 1 | 0.2440945 | NA | 2 | 16 | 1 | 4 | 1 |
| S4-calibration-18 | 128 | 32 | 8 | 0.488189 | 128 | 0.2440945 | 0.2440945 | 2 | 16 | 1 | 4 | 2 |
| S4-calibration-19 | 128 | 32 | 8 | 0.488189 | 256 | 0.2440945 | 0.2440945 | 2 | 16 | 1 | 4 | 3 |
| S4-calibration-20 | 128 | 32 | 8 | 0.488189 | 64 | 0.2440945 | 0.2440945 | 2 | 16 | 1 | 4 | 1 |
| S4-calibration-21 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 2 | 16 | 12 | 4 | 1 |
| S4-calibration-22 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 2 | 16 | 39 | 4 | 1 |
| S4-calibration-23 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 2 | 16 | 27490785 | 4 | 1 |
| S4-calibration-24 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 7 | 56 | 1 | 4 | 1 |
| S4-calibration-25 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 14 | 112 | 1 | 4 | 1 |
| S4-calibration-26 | 128 | 32 | 8 | 0.488189 | 4 | 0.2440945 | NA | 27 | 216 | 1 | 4 | 1 |
| S4-calibration-27 | 128 | 32 | 8 | 0.488189 | 256 | 0.2440945 | 0.2440945 | 27 | 216 | 27490785 | 4 | 8391 |
| S4-calibration-28 | 128 | 32 | 8 | 0.488189 | 128 | 0.2440945 | 0.2440945 | 27 | 216 | 27490785 | 4 | 4196 |
| S4-calibration-29 | 128 | 32 | 8 | 0.488189 | 16 | 0.2440945 | NA | 27 | 216 | 27490785 | 4 | 525 |
| S4-calibration-30 | 128 | 32 | 8 | 0.488189 | 32 | 0.2440945 | 0.2440945 | 27 | 216 | 27490785 | 4 | 1049 |
| S4-calibration-31 | 128 | 32 | 8 | 0.488189 | 64 | 0.2440945 | 0.2440945 | 27 | 216 | 27490785 | 4 | 2098 |
| S4-calibration-32 | 128 | 32 | 8 | 0.488189 | 8 | 0.2440945 | NA | 27 | 216 | 27490785 | 4 | 263 |
| S4-calibration-33 | 128 | 8 | 290 | 0.9990157 | 1 | 0.9990157 | NA | 1 | 8 | 31 | 145 | NA |
| S4-calibration-34 | 128 | 8 | 290 | 0.9990157 | 128 | 0.9990157 | 0.9990157 | 1 | 8 | 31 | 145 | NA |
| S4-calibration-35 | 128 | 8 | 290 | 0.9990157 | 256 | 0.9990157 | 0.9990157 | 1 | 8 | 31 | 145 | NA |
| S4-calibration-36 | 128 | 8 | 290 | 0.9990157 | 4 | 0.9990157 | NA | 1 | 8 | 3014 | 145 | NA |
| S4-calibration-37 | 128 | 8 | 290 | 0.9990157 | 4 | 0.9990157 | NA | 1 | 8 | 2138809088 | 145 | NA |
| S4-calibration-38 | 128 | 8 | 290 | 0.9990157 | 4 | 0.9990157 | NA | 4 | 32 | 31 | 145 | NA |
| S4-calibration-39 | 128 | 8 | 290 | 0.9990157 | 4 | 0.9990157 | NA | 7 | 56 | 31 | 145 | NA |
| S4-calibration-40 | 128 | 8 | 290 | 0.9990157 | 4 | 0.9990157 | NA | 13 | 104 | 31 | 145 | NA |
| S4-calibration-41 | 128 | 8 | 290 | 0.9990157 | 256 | 0.9990157 | 0.9990157 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-42 | 128 | 8 | 290 | 0.9990157 | 128 | 0.9990157 | 0.9990157 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-43 | 128 | 8 | 290 | 0.9990157 | 16 | 0.9990157 | 0.124877 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-44 | 128 | 8 | 290 | 0.9990157 | 32 | 0.9990157 | 0.2497539 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-45 | 128 | 8 | 290 | 0.9990157 | 64 | 0.9990157 | 0.4995079 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-46 | 128 | 8 | 290 | 0.9990157 | 8 | 0.9990157 | 0.06243848 | 13 | 104 | 2138809088 | 145 | NA |
| S4-calibration-47 | 128 | 8 | 290 | 0.9990157 | 1 | 0.05511811 | NA | 5 | 40 | 2 | 145 | 1 |
| S4-calibration-48 | 128 | 8 | 290 | 0.9990157 | 128 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 5 |
| S4-calibration-49 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 1 |
| S4-calibration-50 | 128 | 8 | 290 | 0.9990157 | 256 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 10 |
| S4-calibration-51 | 128 | 8 | 290 | 0.9990157 | 64 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 3 |
| S4-calibration-52 | 128 | 8 | 290 | 0.9990157 | 8 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 1 |
| S4-calibration-53 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | NA | 5 | 40 | 167 | 145 | 1 |
| S4-calibration-54 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | NA | 5 | 40 | 118003261 | 145 | 1 |
| S4-calibration-55 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 2 |
| S4-calibration-56 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 10 |
| S4-calibration-57 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 73 |
| S4-calibration-58 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | 0.05511811 | 5 | 40 | 2 | 145 | 581 |
| S4-calibration-59 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | NA | 17 | 136 | 2 | 145 | 1 |
| S4-calibration-60 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | NA | 34 | 272 | 2 | 145 | 1 |
| S4-calibration-61 | 128 | 8 | 290 | 0.9990157 | 4 | 0.05511811 | NA | 67 | 536 | 2 | 145 | 1 |
| S4-calibration-62 | 128 | 8 | 290 | 0.9990157 | 256 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 37157 |
| S4-calibration-63 | 128 | 8 | 290 | 0.9990157 | 128 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 18579 |
| S4-calibration-64 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 2323 |
| S4-calibration-65 | 128 | 8 | 290 | 0.9990157 | 32 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 4645 |
| S4-calibration-66 | 128 | 8 | 290 | 0.9990157 | 64 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 9290 |
| S4-calibration-67 | 128 | 8 | 290 | 0.9990157 | 8 | 0.05511811 | 0.05511811 | 67 | 536 | 118003261 | 145 | 1162 |
| S4-calibration-68 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 9 | 72 | 5 | 145 | 1 |
| S4-calibration-69 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 9 | 72 | 5 | 145 | 1 |
| S4-calibration-70 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 9 | 72 | 5 | 145 | 5 |
| S4-calibration-71 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 9 | 72 | 5 | 145 | 37 |
| S4-calibration-72 | 128 | 8 | 290 | 0.9990157 | 16 | 0.05511811 | 0.05511811 | 9 | 72 | 5 | 145 | 2323 |
| S4-calibration-73 | 512 | 32 | 263 | 0.9971869 | 1 | 0.9971869 | NA | 2 | 16 | 31 | 131 | NA |
| S4-calibration-74 | 512 | 32 | 263 | 0.9971869 | 4 | 0.9971869 | NA | 2 | 16 | 3096 | 131 | NA |
| S4-calibration-75 | 512 | 32 | 263 | 0.9971869 | 4 | 0.9971869 | NA | 2 | 16 | 2197028442 | 131 | NA |
| S4-calibration-76 | 512 | 32 | 263 | 0.9971869 | 4 | 0.9971869 | NA | 6 | 48 | 31 | 131 | NA |
| S4-calibration-77 | 512 | 32 | 263 | 0.9971869 | 4 | 0.9971869 | NA | 12 | 96 | 31 | 131 | NA |
| S4-calibration-78 | 512 | 32 | 263 | 0.9971869 | 4 | 0.9971869 | NA | 24 | 192 | 31 | 131 | NA |
| S4-calibration-79 | 512 | 32 | 263 | 0.9971869 | 256 | 0.9971869 | 0.4985934 | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-80 | 512 | 32 | 263 | 0.9971869 | 128 | 0.9971869 | 0.2492967 | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-81 | 512 | 32 | 263 | 0.9971869 | 16 | 0.9971869 | NA | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-82 | 512 | 32 | 263 | 0.9971869 | 32 | 0.9971869 | 0.06232418 | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-83 | 512 | 32 | 263 | 0.9971869 | 64 | 0.9971869 | 0.1246484 | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-84 | 512 | 32 | 263 | 0.9971869 | 8 | 0.9971869 | NA | 24 | 192 | 2197028442 | 131 | NA |
| S4-calibration-85 | 512 | 32 | 263 | 0.9971869 | 1 | 0.06066536 | NA | 7 | 56 | 2 | 131 | 1 |
| S4-calibration-86 | 512 | 32 | 263 | 0.9971869 | 128 | 0.06066536 | 0.06066536 | 7 | 56 | 2 | 131 | 5 |
| S4-calibration-87 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 7 | 56 | 2 | 131 | 9 |
| S4-calibration-88 | 512 | 32 | 263 | 0.9971869 | 64 | 0.06066536 | 0.06066536 | 7 | 56 | 2 | 131 | 3 |
| S4-calibration-89 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | NA | 7 | 56 | 189 | 131 | 1 |
| S4-calibration-90 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | NA | 7 | 56 | 133659525 | 131 | 1 |
| S4-calibration-91 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | 0.06066536 | 7 | 56 | 2 | 131 | 2 |
| S4-calibration-92 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | 0.06066536 | 7 | 56 | 2 | 131 | 9 |
| S4-calibration-93 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | NA | 28 | 224 | 2 | 131 | 1 |
| S4-calibration-94 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | NA | 55 | 440 | 2 | 131 | 1 |
| S4-calibration-95 | 512 | 32 | 263 | 0.9971869 | 4 | 0.06066536 | NA | 109 | 872 | 2 | 131 | 1 |
| S4-calibration-96 | 512 | 32 | 263 | 0.9971869 | 256 | 0.06066536 | 0.06066536 | 109 | 872 | 133659525 | 131 | 33759 |
| S4-calibration-97 | 512 | 32 | 263 | 0.9971869 | 128 | 0.06066536 | 0.06066536 | 109 | 872 | 133659525 | 131 | 16880 |
| S4-calibration-98 | 512 | 32 | 263 | 0.9971869 | 16 | 0.06066536 | NA | 109 | 872 | 133659525 | 131 | 2110 |
| S4-calibration-99 | 512 | 32 | 263 | 0.9971869 | 32 | 0.06066536 | 0.06066536 | 109 | 872 | 133659525 | 131 | 4220 |
| S4-calibration-100 | 512 | 32 | 263 | 0.9971869 | 64 | 0.06066536 | 0.06066536 | 109 | 872 | 133659525 | 131 | 8440 |
| S4-calibration-101 | 512 | 32 | 263 | 0.9971869 | 8 | 0.06066536 | NA | 109 | 872 | 133659525 | 131 | 1055 |
| S4-calibration-102 | 512 | 32 | 263 | 0.9971869 | 16 | 0.06066536 | 0.06066536 | 14 | 112 | 6 | 131 | 5 |
| S4-calibration-103 | 512 | 32 | 263 | 0.9971869 | 16 | 0.06066536 | 0.06066536 | 14 | 112 | 6 | 131 | 33 |
| S4-calibration-104 | 64 | 16 | 8 | 0.4761905 | 1 | 0.4761905 | NA | 1 | 8 | 1 | 4 | NA |
| S4-calibration-105 | 64 | 16 | 8 | 0.4761905 | 128 | 0.4761905 | 0.4761905 | 1 | 8 | 1 | 4 | NA |
| S4-calibration-106 | 64 | 16 | 8 | 0.4761905 | 256 | 0.4761905 | 0.4761905 | 1 | 8 | 1 | 4 | NA |
| S4-calibration-107 | 64 | 16 | 8 | 0.4761905 | 64 | 0.4761905 | 0.4761905 | 1 | 8 | 1 | 4 | NA |
| S4-calibration-108 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 1 | 8 | 22 | 4 | NA |
| S4-calibration-109 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 1 | 8 | 72 | 4 | NA |
| S4-calibration-110 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 1 | 8 | 50997616 | 4 | NA |
| S4-calibration-111 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 4 | 32 | 1 | 4 | NA |
| S4-calibration-112 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 7 | 56 | 1 | 4 | NA |
| S4-calibration-113 | 64 | 16 | 8 | 0.4761905 | 4 | 0.4761905 | NA | 14 | 112 | 1 | 4 | NA |
| S4-calibration-114 | 64 | 16 | 8 | 0.4761905 | 256 | 0.4761905 | 0.4761905 | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-115 | 64 | 16 | 8 | 0.4761905 | 128 | 0.4761905 | 0.4761905 | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-116 | 64 | 16 | 8 | 0.4761905 | 16 | 0.4761905 | 0.2380952 | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-117 | 64 | 16 | 8 | 0.4761905 | 32 | 0.4761905 | 0.4761905 | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-118 | 64 | 16 | 8 | 0.4761905 | 64 | 0.4761905 | 0.4761905 | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-119 | 64 | 16 | 8 | 0.4761905 | 8 | 0.4761905 | NA | 14 | 112 | 50997616 | 4 | NA |
| S4-calibration-120 | 64 | 16 | 8 | 0.4761905 | 1 | 0.2380952 | NA | 2 | 16 | 1 | 4 | 1 |
| S4-calibration-121 | 64 | 16 | 8 | 0.4761905 | 128 | 0.2380952 | 0.2380952 | 2 | 16 | 1 | 4 | 2 |
| S4-calibration-122 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 2 | 16 | 1 | 4 | 1 |
| S4-calibration-123 | 64 | 16 | 8 | 0.4761905 | 256 | 0.2380952 | 0.2380952 | 2 | 16 | 1 | 4 | 3 |
| S4-calibration-124 | 64 | 16 | 8 | 0.4761905 | 64 | 0.2380952 | 0.2380952 | 2 | 16 | 1 | 4 | 1 |
| S4-calibration-125 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 2 | 16 | 11 | 4 | 1 |
| S4-calibration-126 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 2 | 16 | 36 | 4 | 1 |
| S4-calibration-127 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 2 | 16 | 25498808 | 4 | 1 |
| S4-calibration-128 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 6 | 48 | 1 | 4 | 1 |
| S4-calibration-129 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 11 | 88 | 1 | 4 | 1 |
| S4-calibration-130 | 64 | 16 | 8 | 0.4761905 | 4 | 0.2380952 | NA | 21 | 168 | 1 | 4 | 1 |
| S4-calibration-131 | 64 | 16 | 8 | 0.4761905 | 256 | 0.2380952 | 0.2380952 | 21 | 168 | 25498808 | 4 | 8602 |
| S4-calibration-132 | 64 | 16 | 8 | 0.4761905 | 128 | 0.2380952 | 0.2380952 | 21 | 168 | 25498808 | 4 | 4301 |
| S4-calibration-133 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 21 | 168 | 25498808 | 4 | 538 |
| S4-calibration-134 | 64 | 16 | 8 | 0.4761905 | 32 | 0.2380952 | 0.2380952 | 21 | 168 | 25498808 | 4 | 1076 |
| S4-calibration-135 | 64 | 16 | 8 | 0.4761905 | 64 | 0.2380952 | 0.2380952 | 21 | 168 | 25498808 | 4 | 2151 |
| S4-calibration-136 | 64 | 16 | 8 | 0.4761905 | 8 | 0.2380952 | NA | 21 | 168 | 25498808 | 4 | 269 |
| S4-calibration-137 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 3 | 24 | 2 | 4 | 1 |
| S4-calibration-138 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 3 | 24 | 2 | 4 | 1 |
| S4-calibration-139 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 3 | 24 | 2 | 4 | 2 |
| S4-calibration-140 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 3 | 24 | 2 | 4 | 9 |
| S4-calibration-141 | 64 | 16 | 8 | 0.4761905 | 16 | 0.2380952 | 0.2380952 | 3 | 24 | 2 | 4 | 538 |

## Constants and selected-resolution checks

The first table uses the initial resolution. This table exposes the resolution ultimately selected and the constants used to calculate each budget. A selected-resolution first round remains hypothetical when the root stops.

| ID | beta0 | cW | c terminal | K | CT | Initial eta*m0 | Selected eta*m0 | Selected w1 | Selected M1 | Initial 8w1 < m0 |
|---|---|---|---|---|---|---|---|---|---|---|
| S4-calibration-1 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-2 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | 62.48819 | 2 | 1 | yes |
| S4-calibration-3 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | 62.48819 | 2 | 1 | yes |
| S4-calibration-4 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | 62.48819 | 2 | 1 | yes |
| S4-calibration-5 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-6 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-7 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-8 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-9 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | NA | NA | NA | yes |
| S4-calibration-10 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 62.48819 | NA | NA | NA | no |
| S4-calibration-11 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | 62.48819 | 19 | 54981570 | no |
| S4-calibration-12 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | 62.48819 | 19 | 54981570 | no |
| S4-calibration-13 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | NA | NA | NA | no |
| S4-calibration-14 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | 31.24409 | 27 | 27490785 | no |
| S4-calibration-15 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | 62.48819 | 19 | 54981570 | no |
| S4-calibration-16 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 62.48819 | NA | NA | NA | no |
| S4-calibration-17 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-18 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | 31.24409 | 2 | 1 | yes |
| S4-calibration-19 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | 31.24409 | 2 | 1 | yes |
| S4-calibration-20 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | 31.24409 | 2 | 1 | yes |
| S4-calibration-21 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-22 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-23 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-24 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-25 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | NA | NA | NA | yes |
| S4-calibration-26 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 31.24409 | NA | NA | NA | no |
| S4-calibration-27 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 27490785 | no |
| S4-calibration-28 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 27490785 | no |
| S4-calibration-29 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | NA | NA | NA | no |
| S4-calibration-30 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 27490785 | no |
| S4-calibration-31 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | 31.24409 | 27 | 27490785 | no |
| S4-calibration-32 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.24409 | NA | NA | NA | no |
| S4-calibration-33 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-34 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 127.874 | 127.874 | 1 | 31 | yes |
| S4-calibration-35 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 127.874 | 127.874 | 1 | 31 | yes |
| S4-calibration-36 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-37 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-38 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-39 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-40 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 127.874 | NA | NA | NA | yes |
| S4-calibration-41 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 127.874 | 13 | 2138809088 | yes |
| S4-calibration-42 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 127.874 | 13 | 2138809088 | yes |
| S4-calibration-43 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 15.98425 | 41 | 267351136 | yes |
| S4-calibration-44 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 31.9685 | 27 | 534702272 | yes |
| S4-calibration-45 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 63.93701 | 19 | 1069404544 | yes |
| S4-calibration-46 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 127.874 | 7.992126 | 62 | 133675568 | yes |
| S4-calibration-47 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | NA | NA | NA | yes |
| S4-calibration-48 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-49 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-50 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-51 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-52 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-53 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 7.055118 | NA | NA | NA | yes |
| S4-calibration-54 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 7.055118 | NA | NA | NA | yes |
| S4-calibration-55 | 0.8 | 0.0625 | 0.015625 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-56 | 0.8 | 0.0625 | 0.125 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-57 | 0.8 | 0.0625 | 1 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-58 | 0.8 | 0.0625 | 8 | 0.01 | 31.58319 | 7.055118 | 7.055118 | 5 | 2 | yes |
| S4-calibration-59 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | NA | NA | NA | no |
| S4-calibration-60 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | NA | NA | NA | no |
| S4-calibration-61 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 7.055118 | NA | NA | NA | no |
| S4-calibration-62 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-63 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-64 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-65 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-66 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-67 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 7.055118 | 7.055118 | 67 | 118003261 | no |
| S4-calibration-68 | 0.8 | 0.125 | 0.0002441406 | 0.03 | 31.58319 | 7.055118 | 7.055118 | 9 | 5 | yes |
| S4-calibration-69 | 0.8 | 0.125 | 0.001953125 | 0.03 | 31.58319 | 7.055118 | 7.055118 | 9 | 5 | yes |
| S4-calibration-70 | 0.8 | 0.125 | 0.015625 | 0.03 | 31.58319 | 7.055118 | 7.055118 | 9 | 5 | yes |
| S4-calibration-71 | 0.8 | 0.125 | 0.125 | 0.03 | 31.58319 | 7.055118 | 7.055118 | 9 | 5 | yes |
| S4-calibration-72 | 0.8 | 0.125 | 8 | 0.03 | 31.58319 | 7.055118 | 7.055118 | 9 | 5 | yes |
| S4-calibration-73 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-74 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-75 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-76 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-77 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-78 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-79 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | 255.2798 | 35 | 1098514221 | yes |
| S4-calibration-80 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | 127.6399 | 50 | 549257111 | yes |
| S4-calibration-81 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-82 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | 31.90998 | 107 | 137314278 | yes |
| S4-calibration-83 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | 63.81996 | 73 | 274628556 | yes |
| S4-calibration-84 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 510.5597 | NA | NA | NA | yes |
| S4-calibration-85 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-calibration-86 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | 31.06067 | 7 | 2 | yes |
| S4-calibration-87 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | 31.06067 | 7 | 2 | yes |
| S4-calibration-88 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | 31.06067 | 7 | 2 | yes |
| S4-calibration-89 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-calibration-90 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-calibration-91 | 0.8 | 0.0625 | 0.015625 | 0.01 | 31.58319 | 31.06067 | 31.06067 | 7 | 2 | yes |
| S4-calibration-92 | 0.8 | 0.0625 | 0.125 | 0.01 | 31.58319 | 31.06067 | 31.06067 | 7 | 2 | yes |
| S4-calibration-93 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-calibration-94 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | NA | NA | NA | yes |
| S4-calibration-95 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 31.06067 | NA | NA | NA | no |
| S4-calibration-96 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 133659525 | no |
| S4-calibration-97 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 133659525 | no |
| S4-calibration-98 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | NA | NA | NA | no |
| S4-calibration-99 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 133659525 | no |
| S4-calibration-100 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | 31.06067 | 109 | 133659525 | no |
| S4-calibration-101 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 31.06067 | NA | NA | NA | no |
| S4-calibration-102 | 0.8 | 0.125 | 0.015625 | 0.03 | 31.58319 | 31.06067 | 31.06067 | 14 | 6 | yes |
| S4-calibration-103 | 0.8 | 0.125 | 0.125 | 0.03 | 31.58319 | 31.06067 | 31.06067 | 14 | 6 | yes |
| S4-calibration-104 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-105 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | 30.47619 | 1 | 1 | yes |
| S4-calibration-106 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | 30.47619 | 1 | 1 | yes |
| S4-calibration-107 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | 30.47619 | 1 | 1 | yes |
| S4-calibration-108 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-109 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-110 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-111 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-112 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | NA | NA | NA | yes |
| S4-calibration-113 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 30.47619 | NA | NA | NA | no |
| S4-calibration-114 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | 30.47619 | 14 | 50997616 | no |
| S4-calibration-115 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | 30.47619 | 14 | 50997616 | no |
| S4-calibration-116 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-117 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | 30.47619 | 14 | 50997616 | no |
| S4-calibration-118 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | 30.47619 | 14 | 50997616 | no |
| S4-calibration-119 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 30.47619 | NA | NA | NA | no |
| S4-calibration-120 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | NA | NA | NA | yes |
| S4-calibration-121 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | 15.2381 | 2 | 1 | yes |
| S4-calibration-122 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | 15.2381 | 2 | 1 | yes |
| S4-calibration-123 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | 15.2381 | 2 | 1 | yes |
| S4-calibration-124 | 0.8 | 0.0625 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | 15.2381 | 2 | 1 | yes |
| S4-calibration-125 | 0.8 | 0.0625 | 0.001953125 | 0.3 | 31.58319 | 15.2381 | NA | NA | NA | yes |
| S4-calibration-126 | 0.8 | 0.0625 | 0.001953125 | 1 | 31.58319 | 15.2381 | NA | NA | NA | yes |
| S4-calibration-127 | 0.8 | 0.0625 | 0.001953125 | 709775.1 | 31.58319 | 15.2381 | NA | NA | NA | yes |
| S4-calibration-128 | 0.8 | 0.25 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | NA | NA | NA | yes |
| S4-calibration-129 | 0.8 | 0.5 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | NA | NA | NA | no |
| S4-calibration-130 | 0.8 | 1 | 0.001953125 | 0.01 | 31.58319 | 15.2381 | NA | NA | NA | no |
| S4-calibration-131 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-132 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-133 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-134 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-135 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | 15.2381 | 21 | 25498808 | no |
| S4-calibration-136 | 0.8 | 1 | 8 | 709775.1 | 31.58319 | 15.2381 | NA | NA | NA | no |
| S4-calibration-137 | 0.8 | 0.125 | 0.0002441406 | 0.03 | 31.58319 | 15.2381 | 15.2381 | 3 | 2 | yes |
| S4-calibration-138 | 0.8 | 0.125 | 0.001953125 | 0.03 | 31.58319 | 15.2381 | 15.2381 | 3 | 2 | yes |
| S4-calibration-139 | 0.8 | 0.125 | 0.015625 | 0.03 | 31.58319 | 15.2381 | 15.2381 | 3 | 2 | yes |
| S4-calibration-140 | 0.8 | 0.125 | 0.125 | 0.03 | 31.58319 | 15.2381 | 15.2381 | 3 | 2 | yes |
| S4-calibration-141 | 0.8 | 0.125 | 8 | 0.03 | 31.58319 | 15.2381 | 15.2381 | 3 | 2 | yes |

## Terminal blocks and resource receipts

Ranges show different saved repetitions in the same row; exact integers and individual receipts are in the CSV. Formula W* can exceed n; the actual terminal block is clipped by the available items. A large W* is not itself a memory-allocation count.

| ID | Consumed pilot reports | Requested blocks (variant) | Actual terminal / failed block items | Resource reason | Pairs in failed block | Estimated bytes | Memory limit bytes | Time limit seconds |
|---|---|---|---|---|---|---|---|---|
| S4-calibration-1 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-2 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-3 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-4 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-5 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-6 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-7 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-8 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-9 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-10 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-11 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-12 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-13 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-14 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-15 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-16 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-17 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-18 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-calibration-19 | 0 | NA | 24 | NA | NA | NA | NA | NA |
| S4-calibration-20 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-21 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-22 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-23 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-24 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-25 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-26 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-27 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-28 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-29 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-30 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-31 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-32 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-33 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-34 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-35 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-36 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-37 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-38 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-39 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-40 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-41 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-42 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-43 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-44 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-45 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-46 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-47 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-48 | 0 | NA | 25 | working_array_memory_budget | 128 to 166 | 7.9107e26 | 536870912 | 30 |
| S4-calibration-49 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-50 | 0 | NA | 50 | working_array_memory_budget | 249 to 272 | 3.0718e66 | 536870912 | 30 |
| S4-calibration-51 | 0 | NA | 15 | working_array_memory_budget | 55 to 86 | 40537905408000 | 536870912 | 30 |
| S4-calibration-52 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-53 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-54 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-55 | 2 | NA | 14 | working_array_memory_budget | 49 to 80 | 2528170444800 | 536870912 | 30 |
| S4-calibration-56 | 2 | NA | 50 | working_array_memory_budget | 246 to 267 | 3.0718e66 | 536870912 | 30 |
| S4-calibration-57 | 2 | NA | 128 | working_array_memory_budget | 288 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-58 | 2 | NA | 128 | working_array_memory_budget | 288 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-59 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-60 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-61 | 0 | NA | 128 | NA | NA | NA | NA | NA |
| S4-calibration-62 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-63 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-64 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-65 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-66 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-67 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-68 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-69 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-70 | 0 | NA | 25 | working_array_memory_budget | 128 to 166 | 7.9107e26 | 536870912 | 30 |
| S4-calibration-71 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-72 | 0 | NA | 128 | working_array_memory_budget | 290 | 9.9104e217 | 536870912 | 30 |
| S4-calibration-73 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-74 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-75 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-76 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-77 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-78 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-79 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-80 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-81 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-82 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-83 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-84 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-85 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-86 | 0 | NA | 25 | working_array_memory_budget | 108 to 139 | 7.9107e26 | 536870912 | 30 |
| S4-calibration-87 | 0 | NA | 45 | working_array_memory_budget | 200 to 219 | 1.0885e58 | 536870912 | 30 |
| S4-calibration-88 | 0 | NA | 15 | working_array_memory_budget | 56 to 71 | 40537905408000 | 536870912 | 30 |
| S4-calibration-89 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-90 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-91 | 2 | NA | 14 | working_array_memory_budget | 44 to 68 | 2528170444800 | 536870912 | 30 |
| S4-calibration-92 | 2 | NA | 45 | working_array_memory_budget | 191 to 219 | 1.0885e58 | 536870912 | 30 |
| S4-calibration-93 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-94 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-95 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-96 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-97 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-98 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-99 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-100 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-101 | 0 | NA | 512 | NA | NA | NA | NA | NA |
| S4-calibration-102 | 6 | NA | 25 | working_array_memory_budget | 108 to 134 | 7.9107e26 | 536870912 | 30 |
| S4-calibration-103 | 6 | NA | 165 | working_array_memory_budget | 256 to 257 | 1.7953e298 | 536870912 | 30 |
| S4-calibration-104 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-105 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-106 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-107 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-108 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-109 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-110 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-111 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-112 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-113 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-114 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-115 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-116 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-117 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-118 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-119 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-120 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-121 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-calibration-122 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-123 | 0 | NA | 24 | NA | NA | NA | NA | NA |
| S4-calibration-124 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-125 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-126 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-127 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-128 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-129 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-130 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-131 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-132 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-133 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-134 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-135 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-136 | 0 | NA | 64 | NA | NA | NA | NA | NA |
| S4-calibration-137 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-138 | 0 | NA | 8 | NA | NA | NA | NA | NA |
| S4-calibration-139 | 0 | NA | 16 | NA | NA | NA | NA | NA |
| S4-calibration-140 | 0 | NA | 63 | NA | NA | NA | NA | NA |
| S4-calibration-141 | 0 | NA | 64 | NA | NA | NA | NA | NA |
