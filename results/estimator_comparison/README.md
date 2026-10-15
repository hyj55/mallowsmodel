# E0: supplementary center-estimator comparison

[Design](../../docs/estimator_comparison.md) · [Summary CSV](summary.csv) · [P0 main results](../main/README.md) · [B0 global sieve](../global_sieve/README.md)

E0 compares Sharp, Fotakis and eligible Efficient with the same tuned PL reference on five allocations per task. It is supplementary to Algorithm 4.1. The test scores never select a replacement for P0's likelihood center. Shared allocations and PL fits make E0 paired with P0, not an independent replication.

A full mean/MCSE requires all five planned fits. Missing fits are neither zero loss nor replaced by another estimator; conditional means have explicit finite denominators. Delta is named SM estimator minus PL whole-ranking NLL.

## Sharp

| Task | Mean delta | MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | -0.02170 | 0.00576 | 5/5 | {"ok": 5} |
| Dots 2013, gap 5 | -0.00998 | 0.00413 | 5/5 | {"ok": 5} |
| Dots 2013, gap 7 | -0.00189 | 0.00541 | 5/5 | {"ok": 5} |
| Dots 2013, gap 9 | -0.04415 | 0.00337 | 5/5 | {"ok": 5} |
| Puzzle, minimum 11 steps | -0.01042 | 0.00294 | 5/5 | {"ok": 5} |
| Puzzle, minimum 5 steps | -0.06934 | 0.00523 | 5/5 | {"ok": 5} |
| Puzzle, minimum 7 steps | -0.02090 | 0.01363 | 5/5 | {"ok": 5} |
| Puzzle, minimum 9 steps | 0.01546 | 0.02124 | 5/5 | {"ok": 5} |
| Beans | 0.00978 | 0.00438 | 5/5 | {"ok": 5} |
| Dots 2024 A r2 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 A r3 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 A r5 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 A r6 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 B r2 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 B r3 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 B r5 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Dots 2024 B r6 | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| PatrasIQ cost | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| PatrasIQ population | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Sounds | 0.00948 | 0.00699 | 5/5 | {"ok": 5} |
| Sushi A | 0.07153 | 0.01087 | 5/5 | {"ok": 5} |
| Sushi B | NA | NA | 0/5 | {"sieve_resource_budget": 5} |
| Wheat | NA | NA | 0/5 | {"sieve_resource_budget": 5} |

## Fotakis / PosEst

| Task | Mean delta | MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | -0.02170 | 0.00576 | 5/5 | {"ok": 5} |
| Dots 2013, gap 5 | -0.00998 | 0.00413 | 5/5 | {"ok": 5} |
| Dots 2013, gap 7 | -0.00189 | 0.00541 | 5/5 | {"ok": 5} |
| Dots 2013, gap 9 | -0.04415 | 0.00337 | 5/5 | {"ok": 5} |
| Puzzle, minimum 11 steps | -0.01042 | 0.00294 | 5/5 | {"ok": 5} |
| Puzzle, minimum 5 steps | -0.06934 | 0.00523 | 5/5 | {"ok": 5} |
| Puzzle, minimum 7 steps | -0.02090 | 0.01363 | 5/5 | {"ok": 5} |
| Puzzle, minimum 9 steps | -0.01530 | 0.00906 | 5/5 | {"ok": 5} |
| Beans | 0.00383 | 0.00371 | 5/5 | {"ok": 5} |
| Dots 2024 A r2 | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Dots 2024 A r3 | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Dots 2024 A r5 | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Dots 2024 A r6 | 0.06320 | 0.05475 | 5/5 | {"ok": 5} |
| Dots 2024 B r2 | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Dots 2024 B r3 | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Dots 2024 B r5 | NA | NA | 2/5 | {"not_p_frequent": 3, "ok": 2} |
| Dots 2024 B r6 | NA | NA | 4/5 | {"not_p_frequent": 1, "ok": 4} |
| PatrasIQ cost | NA | NA | 0/5 | {"not_p_frequent": 5} |
| PatrasIQ population | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Sounds | 0.00576 | 0.00522 | 5/5 | {"ok": 5} |
| Sushi A | 0.02711 | 0.00870 | 5/5 | {"ok": 5} |
| Sushi B | NA | NA | 0/5 | {"not_p_frequent": 5} |
| Wheat | 0.12550 | 0.03590 | 5/5 | {"ok": 5} |

## Efficient fallback

| Task | Mean delta | MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | NA | NA | 0/5 | {"sharp_available": 5} |
| Dots 2013, gap 5 | NA | NA | 0/5 | {"sharp_available": 5} |
| Dots 2013, gap 7 | NA | NA | 0/5 | {"sharp_available": 5} |
| Dots 2013, gap 9 | NA | NA | 0/5 | {"sharp_available": 5} |
| Puzzle, minimum 11 steps | NA | NA | 0/5 | {"sharp_available": 5} |
| Puzzle, minimum 5 steps | NA | NA | 0/5 | {"sharp_available": 5} |
| Puzzle, minimum 7 steps | NA | NA | 0/5 | {"sharp_available": 5} |
| Puzzle, minimum 9 steps | NA | NA | 0/5 | {"sharp_available": 5} |
| Beans | NA | NA | 0/5 | {"sharp_available": 5} |
| Dots 2024 A r2 | 0.03020 | 0.01624 | 5/5 | {"ok": 5} |
| Dots 2024 A r3 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Dots 2024 A r5 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Dots 2024 A r6 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Dots 2024 B r2 | 0.03004 | 0.02091 | 5/5 | {"ok": 5} |
| Dots 2024 B r3 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Dots 2024 B r5 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Dots 2024 B r6 | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| PatrasIQ cost | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| PatrasIQ population | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Sounds | NA | NA | 0/5 | {"sharp_available": 5} |
| Sushi A | NA | NA | 0/5 | {"sharp_available": 5} |
| Sushi B | NA | NA | 0/5 | {"outside_schedule_domain": 5} |
| Wheat | NA | NA | 0/5 | {"outside_schedule_domain": 5} |

## Scope

Sharp completes all five allocations for eleven empirical tasks and remains unavailable for twelve. There are 60 unavailable E0 fits, 15 L0 fits and 80 S0 fits: 155 distinct supplementary contexts. All current E0/L0/S0 Sharp contexts with n<=10 are available; no tuned-width variant is needed to complete that size range. Fotakis requires complete observed pair coverage. Efficient has its declared domain and fallback gate. Neither numerical exposure nor a completed fit certifies the manuscript's sampling assumptions.

B0 aliases Sharp when the constructions coincide. Raw `study=P0` is an allocation-family key; these named views distinguish E0 from the main experiment. [Exact sieve construction and resources](../../docs/sieve_computation.md) explain computational limits and the role of W_star.
