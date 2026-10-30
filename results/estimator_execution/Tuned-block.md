# Tuned-block: Sharp/Efficient execution audit

[Definitions and coverage](README.md) · [Every fit receipt](fits.csv.gz) · [Complete candidate/stage schedules](plans.jsonl.gz)

87 recorded or explicitly reconstructed contexts; 87 have zero pilot depth, an admission exclusion, a fallback, an unavailable result, or a variant without hierarchical depth. They form 87 rows below. Identical parameter/reason rows are grouped across repetitions and, for G1, across anonymous group keys; no parameters are averaged. Fit-level group/repetition/source locators remain in the CSV. Positive-depth successful contexts remain in the CSV as coverage controls.

**Read the two tables together by row ID.** `w1, M1` refer to the initial candidate at `m0=n`; they are formula diagnostics, **not** evidence that a stage ran. For a stopped or excluded fit they are counterfactual. `eta selected` can differ after rejected candidate schedules; its first-stage values and every failed candidate are in the CSV/plan archive. `M1` is reports required for that round, while `N` is the actual fitting sample, not total dataset size. Resource numbers are saved estimates/limits, not measured RAM usage. `NA` means not applicable or not recorded, never zero.

## Why the fit stopped or did not run

| ID | Dataset / setting | Fit phase | Estimator / configuration | Contexts | Executed depth | Depth evidence | Saved status | Explanation |
|---|---|---|---|---|---|---|---|---|
| Tuned-block-1 | dots2024_A_r2 / E0-dots2024_A_r2-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-2 | dots2024_A_r2 / E0-dots2024_A_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-3 | dots2024_A_r2 / E0-dots2024_A_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-4 | dots2024_A_r2 / E0-dots2024_A_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-5 | dots2024_A_r3 / E0-dots2024_A_r3-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-6 | dots2024_A_r3 / E0-dots2024_A_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-7 | dots2024_A_r3 / E0-dots2024_A_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-8 | dots2024_A_r3 / E0-dots2024_A_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-9 | dots2024_A_r5 / E0-dots2024_A_r5-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-10 | dots2024_A_r5 / E0-dots2024_A_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-11 | dots2024_A_r5 / E0-dots2024_A_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-12 | dots2024_A_r5 / E0-dots2024_A_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-13 | dots2024_A_r6 / E0-dots2024_A_r6-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-14 | dots2024_A_r6 / E0-dots2024_A_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-15 | dots2024_A_r6 / E0-dots2024_A_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-16 | dots2024_A_r6 / E0-dots2024_A_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-17 | dots2024_B_r2 / E0-dots2024_B_r2-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-18 | dots2024_B_r2 / E0-dots2024_B_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-19 | dots2024_B_r2 / E0-dots2024_B_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-20 | dots2024_B_r2 / E0-dots2024_B_r2-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-21 | dots2024_B_r3 / E0-dots2024_B_r3-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-22 | dots2024_B_r3 / E0-dots2024_B_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-23 | dots2024_B_r3 / E0-dots2024_B_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-24 | dots2024_B_r3 / E0-dots2024_B_r3-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-25 | dots2024_B_r5 / E0-dots2024_B_r5-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-26 | dots2024_B_r5 / E0-dots2024_B_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-27 | dots2024_B_r5 / E0-dots2024_B_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-28 | dots2024_B_r5 / E0-dots2024_B_r5-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-29 | dots2024_B_r6 / E0-dots2024_B_r6-n30-N240 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-30 | dots2024_B_r6 / E0-dots2024_B_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-31 | dots2024_B_r6 / E0-dots2024_B_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-32 | dots2024_B_r6 / E0-dots2024_B_r6-n30-N240 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-33 | patras_cost / E0-patras_cost-n36-N313 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-34 | patras_cost / E0-patras_cost-n36-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-35 | patras_cost / E0-patras_cost-n36-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-36 | patras_cost / E0-patras_cost-n36-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-37 | patras_cost / E0-patras_cost-n36-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-38 | patras_population / E0-patras_population-n48-N313 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-39 | patras_population / E0-patras_population-n48-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-40 | patras_population / E0-patras_population-n48-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-41 | patras_population / E0-patras_population-n48-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-42 | patras_population / E0-patras_population-n48-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-43 | patras_population / E0-patras_population-n48-N313 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-44 | sushi_b / E0-sushi_b-n100-N4000 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-45 | sushi_b / E0-sushi_b-n100-N4000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-46 | sushi_b / E0-sushi_b-n100-N4000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-47 | sushi_b / E0-sushi_b-n100-N4000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-48 | sushi_b / E0-sushi_b-n100-N4000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-49 | sushi_b / E0-sushi_b-n100-N4000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-50 | sushi_b / L0-sushi_b-n100-N1000 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-51 | sushi_b / L0-sushi_b-n100-N1000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-52 | sushi_b / L0-sushi_b-n100-N1000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-53 | sushi_b / L0-sushi_b-n100-N1000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-54 | sushi_b / L0-sushi_b-n100-N1000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-55 | sushi_b / L0-sushi_b-n100-N1000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-56 | sushi_b / L0-sushi_b-n100-N300 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-57 | sushi_b / L0-sushi_b-n100-N300 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-58 | sushi_b / L0-sushi_b-n100-N300 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-59 | sushi_b / L0-sushi_b-n100-N300 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-60 | sushi_b / L0-sushi_b-n100-N300 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-61 | sushi_b / L0-sushi_b-n100-N300 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-62 | sushi_b / L0-sushi_b-n100-N3000 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-63 | sushi_b / L0-sushi_b-n100-N3000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-64 | sushi_b / L0-sushi_b-n100-N3000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-65 | sushi_b / L0-sushi_b-n100-N3000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-66 | sushi_b / L0-sushi_b-n100-N3000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-67 | sushi_b / L0-sushi_b-n100-N3000 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-68 | synthetic_pl / S0-synthetic_pl-n16-N100 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-69 | synthetic_pl / S0-synthetic_pl-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-70 | synthetic_pl / S0-synthetic_pl-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-71 | synthetic_pl / S0-synthetic_pl-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-72 | synthetic_pl / S0-synthetic_pl-n32-N100 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-73 | synthetic_pl / S0-synthetic_pl-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-74 | synthetic_pl / S0-synthetic_pl-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-75 | synthetic_pl / S0-synthetic_pl-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-76 | synthetic_sm / S0-synthetic_sm-n16-N100 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-77 | synthetic_sm / S0-synthetic_sm-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-78 | synthetic_sm / S0-synthetic_sm-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-79 | synthetic_sm / S0-synthetic_sm-n16-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-80 | synthetic_sm / S0-synthetic_sm-n32-N100 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-81 | synthetic_sm / S0-synthetic_sm-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-82 | synthetic_sm / S0-synthetic_sm-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-83 | synthetic_sm / S0-synthetic_sm-n32-N100 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | sieve_resource_budget | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Exact block sieve stopped: working_array_memory_budget. |
| Tuned-block-84 | wheat / E0-wheat-n16-N394 | development refit | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-85 | wheat / E0-wheat-n16-N394 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-86 | wheat / E0-wheat-n16-N394 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |
| Tuned-block-87 | wheat / E0-wheat-n16-N394 | validation candidate | borda_block_sieve | 1 | NA | not defined for this variant | ok | This tuned variant uses one global Borda pilot and disjoint blocks; no A/eta/W hierarchy or stopping depth is defined. Candidate/refit completed. |

## Initial geometry and sample requirement

| ID | n = m0 | r | N | lambda | A | eta initial | eta selected | w1 | 8w1 | M1 | floor(N/2) | W* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tuned-block-1 | 30 | 2 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-2 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-3 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-4 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-5 | 30 | 3 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-6 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-7 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-8 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-9 | 30 | 5 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-10 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-11 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-12 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-13 | 30 | 6 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-14 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-15 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-16 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-17 | 30 | 2 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-18 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-19 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-20 | 30 | 2 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-21 | 30 | 3 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-22 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-23 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-24 | 30 | 3 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-25 | 30 | 5 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-26 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-27 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-28 | 30 | 5 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-29 | 30 | 6 | 240 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-30 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-31 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-32 | 30 | 6 | 180 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-33 | 36 | 6 | 313 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-34 | 36 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-35 | 36 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-36 | 36 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-37 | 36 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-38 | 48 | 6 | 313 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-39 | 48 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-40 | 48 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-41 | 48 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-42 | 48 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-43 | 48 | 6 | 235 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-44 | 100 | 10 | 4000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-45 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-46 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-47 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-48 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-49 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-50 | 100 | 10 | 1000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-51 | 100 | 10 | 750 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-52 | 100 | 10 | 750 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-53 | 100 | 10 | 750 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-54 | 100 | 10 | 750 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-55 | 100 | 10 | 750 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-56 | 100 | 10 | 300 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-57 | 100 | 10 | 225 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-58 | 100 | 10 | 225 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-59 | 100 | 10 | 225 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-60 | 100 | 10 | 225 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-61 | 100 | 10 | 225 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-62 | 100 | 10 | 3000 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-63 | 100 | 10 | 2250 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-64 | 100 | 10 | 2250 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-65 | 100 | 10 | 2250 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-66 | 100 | 10 | 2250 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-67 | 100 | 10 | 2250 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-68 | 16 | 3 | 100 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-69 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-70 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-71 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-72 | 32 | 3 | 100 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-73 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-74 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-75 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-76 | 16 | 3 | 100 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-77 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-78 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-79 | 16 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-80 | 32 | 3 | 100 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-81 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-82 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-83 | 32 | 3 | 75 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-84 | 16 | 3 | 394 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-85 | 16 | 3 | 295 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-86 | 16 | 3 | 295 | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-87 | 16 | 3 | 295 | NA | NA | NA | NA | NA | NA | NA | NA | NA |

## Constants and selected-resolution checks

The first table uses the initial resolution. This table exposes the resolution ultimately selected and the constants used to calculate each budget. A selected-resolution first round remains hypothetical when the root stops.

| ID | beta0 | cW | c terminal | K | CT | Initial eta*m0 | Selected eta*m0 | Selected w1 | Selected M1 | Initial 8w1 < m0 |
|---|---|---|---|---|---|---|---|---|---|---|
| Tuned-block-1 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-2 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-3 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-4 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-5 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-6 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-7 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-8 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-9 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-10 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-11 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-12 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-13 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-14 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-15 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-16 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-17 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-18 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-19 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-20 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-21 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-22 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-23 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-24 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-25 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-26 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-27 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-28 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-29 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-30 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-31 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-32 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-33 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-34 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-35 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-36 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-37 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-38 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-39 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-40 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-41 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-42 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-43 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-44 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-45 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-46 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-47 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-48 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-49 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-50 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-51 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-52 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-53 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-54 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-55 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-56 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-57 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-58 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-59 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-60 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-61 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-62 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-63 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-64 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-65 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-66 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-67 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-68 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-69 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-70 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-71 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-72 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-73 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-74 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-75 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-76 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-77 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-78 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-79 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-80 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-81 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-82 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-83 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-84 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-85 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-86 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| Tuned-block-87 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |

## Terminal blocks and resource receipts

Ranges show different saved repetitions in the same row; exact integers and individual receipts are in the CSV. Formula W* can exceed n; the actual terminal block is clipped by the available items. A large W* is not itself a memory-allocation count.

| ID | Consumed pilot reports | Requested blocks (variant) | Actual terminal / failed block items | Resource reason | Pairs in failed block | Estimated bytes | Memory limit bytes | Time limit seconds |
|---|---|---|---|---|---|---|---|---|
| Tuned-block-1 | 120 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-2 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-3 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-4 | 90 | 2 | 15 | working_array_memory_budget | 19 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-5 | 120 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-6 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-7 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-8 | 90 | 2 | 15 | working_array_memory_budget | 38 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-9 | 120 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-10 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-11 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-12 | 90 | 2 | 15 | working_array_memory_budget | 75 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-13 | 120 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-14 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-15 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-16 | 90 | 2 | 15 | working_array_memory_budget | 79 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-17 | 120 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-18 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-19 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-20 | 90 | 2 | 15 | working_array_memory_budget | 25 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-21 | 120 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-22 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-23 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-24 | 90 | 2 | 15 | working_array_memory_budget | 51 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-25 | 120 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-26 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-27 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-28 | 90 | 2 | 15 | working_array_memory_budget | 76 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-29 | 120 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-30 | 90 | 3 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-31 | 90 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-32 | 90 | 2 | 15 | working_array_memory_budget | 82 | 40537905408000 | 4294967296 | 120 |
| Tuned-block-33 | 156 | 5 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-34 | 117 | 4 | 9 | NA | NA | NA | NA | NA |
| Tuned-block-35 | 117 | 5 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-36 | 117 | 2 | 18 | working_array_memory_budget | 109 | 2.3688e17 | 4294967296 | 120 |
| Tuned-block-37 | 117 | 3 | 12 | working_array_memory_budget | 77 | 11975040000 | 4294967296 | 120 |
| Tuned-block-38 | 156 | 6 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-39 | 117 | 5 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-40 | 117 | 6 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-41 | 117 | 2 | 24 | working_array_memory_budget | 114 | 3.0401e25 | 4294967296 | 120 |
| Tuned-block-42 | 117 | 3 | 16 | working_array_memory_budget | 83 | 690452066304000 | 4294967296 | 120 |
| Tuned-block-43 | 117 | 4 | 12 | working_array_memory_budget | 59 | 11975040000 | 4294967296 | 120 |
| Tuned-block-44 | 2000 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-45 | 1500 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-46 | 1500 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-47 | 1500 | 2 | 50 | working_array_memory_budget | 1500 | 3.0718e66 | 4294967296 | 120 |
| Tuned-block-48 | 1500 | 3 | 34 | working_array_memory_budget | 1499 | 2.0371e40 | 4294967296 | 120 |
| Tuned-block-49 | 1500 | 4 | 25 | working_array_memory_budget | 1487 | 7.9107e26 | 4294967296 | 120 |
| Tuned-block-50 | 500 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-51 | 375 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-52 | 375 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-53 | 375 | 2 | 50 | working_array_memory_budget | 375 | 3.0718e66 | 4294967296 | 120 |
| Tuned-block-54 | 375 | 3 | 34 | working_array_memory_budget | 374 | 2.0371e40 | 4294967296 | 120 |
| Tuned-block-55 | 375 | 4 | 25 | working_array_memory_budget | 366 | 7.9107e26 | 4294967296 | 120 |
| Tuned-block-56 | 150 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-57 | 112 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-58 | 112 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-59 | 112 | 2 | 50 | working_array_memory_budget | 113 | 3.0718e66 | 4294967296 | 120 |
| Tuned-block-60 | 112 | 3 | 34 | working_array_memory_budget | 113 | 2.0371e40 | 4294967296 | 120 |
| Tuned-block-61 | 112 | 4 | 25 | working_array_memory_budget | 111 | 7.9107e26 | 4294967296 | 120 |
| Tuned-block-62 | 1500 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-63 | 1125 | 10 | 10 | NA | NA | NA | NA | NA |
| Tuned-block-64 | 1125 | 13 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-65 | 1125 | 2 | 50 | working_array_memory_budget | 1125 | 3.0718e66 | 4294967296 | 120 |
| Tuned-block-66 | 1125 | 3 | 34 | working_array_memory_budget | 1122 | 2.0371e40 | 4294967296 | 120 |
| Tuned-block-67 | 1125 | 4 | 25 | working_array_memory_budget | 1107 | 7.9107e26 | 4294967296 | 120 |
| Tuned-block-68 | 50 | 4 | 4 | NA | NA | NA | NA | NA |
| Tuned-block-69 | 37 | 2 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-70 | 37 | 3 | 6 | NA | NA | NA | NA | NA |
| Tuned-block-71 | 37 | 4 | 4 | NA | NA | NA | NA | NA |
| Tuned-block-72 | 50 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-73 | 37 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-74 | 37 | 2 | 16 | working_array_memory_budget | 19 | 690452066304000 | 4294967296 | 120 |
| Tuned-block-75 | 37 | 3 | 11 | working_array_memory_budget | 15 | 19689849120 | 4294967296 | 120 |
| Tuned-block-76 | 50 | 4 | 4 | NA | NA | NA | NA | NA |
| Tuned-block-77 | 37 | 2 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-78 | 37 | 3 | 6 | NA | NA | NA | NA | NA |
| Tuned-block-79 | 37 | 4 | 4 | NA | NA | NA | NA | NA |
| Tuned-block-80 | 50 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-81 | 37 | 4 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-82 | 37 | 2 | 16 | working_array_memory_budget | 21 | 690452066304000 | 4294967296 | 120 |
| Tuned-block-83 | 37 | 3 | 11 | working_array_memory_budget | 13 | 20062906560 | 4294967296 | 120 |
| Tuned-block-84 | 197 | 4 | 4 | NA | NA | NA | NA | NA |
| Tuned-block-85 | 147 | 2 | 8 | NA | NA | NA | NA | NA |
| Tuned-block-86 | 147 | 3 | 6 | NA | NA | NA | NA | NA |
| Tuned-block-87 | 147 | 4 | 4 | NA | NA | NA | NA | NA |
