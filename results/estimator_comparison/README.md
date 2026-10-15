# E0: supplementary center-estimator comparison

[Design and naming](../../docs/estimator_comparison.md) · [All E0 rows](summary.csv) · [Separate P0 main results](../main/README.md) · [B0 global sieve](../global_sieve/README.md)

E0 compares Sharp, Fotakis and the admitted Efficient fallback with the same tuned PL reference, on the 23-task allocations used by P0. It asks how a different SM center procedure changes prediction. **E0 is not Algorithm 4.1's main experiment.** Its results do not replace `sm_likelihood`, and the best test-scoring estimator is never selected as the main SM result.

The 30 allocations, data and PL reference are shared, so this is a paired supplementary comparison, not an independent replication of P0. Delta is the named SM estimator minus PL whole-ranking NLL. Full means/MCSEs remain NA unless all 30 planned fits exist. Conditional means in the CSV have explicit denominators and must not substitute for missing full comparisons.

## Sharp

| Task | Mean delta | Partition MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | -0.01002 | 0.00262 | 30/30 | {"ok": 30} |
| Dots 2013, gap 5 | -0.01452 | 0.00223 | 30/30 | {"ok": 30} |
| Dots 2013, gap 7 | -0.01255 | 0.00311 | 30/30 | {"ok": 30} |
| Dots 2013, gap 9 | -0.03515 | 0.00413 | 30/30 | {"ok": 30} |
| Puzzle, minimum 11 steps | -0.00979 | 0.00279 | 30/30 | {"ok": 30} |
| Puzzle, minimum 5 steps | -0.05855 | 0.00365 | 30/30 | {"ok": 30} |
| Puzzle, minimum 7 steps | -0.02293 | 0.00368 | 30/30 | {"ok": 30} |
| Puzzle, minimum 9 steps | 0.01314 | 0.00595 | 30/30 | {"ok": 30} |
| Beans | 0.00314 | 0.00194 | 30/30 | {"ok": 30} |
| Dots 2024 A r2 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 A r3 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 A r5 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 A r6 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 B r2 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 B r3 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 B r5 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Dots 2024 B r6 | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| PatrasIQ cost | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| PatrasIQ population | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Sounds | 0.01306 | 0.00259 | 30/30 | {"ok": 30} |
| Sushi A | 0.06029 | 0.00555 | 30/30 | {"ok": 30} |
| Sushi B | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Wheat | NA | NA | 0/30 | {"sieve_resource_budget": 30} |

## Fotakis / PosEst

| Task | Mean delta | Partition MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | -0.01241 | 0.00226 | 30/30 | {"ok": 30} |
| Dots 2013, gap 5 | -0.01452 | 0.00223 | 30/30 | {"ok": 30} |
| Dots 2013, gap 7 | -0.01255 | 0.00311 | 30/30 | {"ok": 30} |
| Dots 2013, gap 9 | -0.03515 | 0.00413 | 30/30 | {"ok": 30} |
| Puzzle, minimum 11 steps | -0.01161 | 0.00273 | 30/30 | {"ok": 30} |
| Puzzle, minimum 5 steps | -0.05855 | 0.00365 | 30/30 | {"ok": 30} |
| Puzzle, minimum 7 steps | -0.02293 | 0.00368 | 30/30 | {"ok": 30} |
| Puzzle, minimum 9 steps | -0.00881 | 0.00265 | 30/30 | {"ok": 30} |
| Beans | 0.00423 | 0.00164 | 30/30 | {"ok": 30} |
| Dots 2024 A r2 | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Dots 2024 A r3 | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Dots 2024 A r5 | NA | NA | 4/30 | {"not_p_frequent": 26, "ok": 4} |
| Dots 2024 A r6 | NA | NA | 29/30 | {"not_p_frequent": 1, "ok": 29} |
| Dots 2024 B r2 | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Dots 2024 B r3 | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Dots 2024 B r5 | NA | NA | 6/30 | {"not_p_frequent": 24, "ok": 6} |
| Dots 2024 B r6 | NA | NA | 17/30 | {"not_p_frequent": 13, "ok": 17} |
| PatrasIQ cost | NA | NA | 0/30 | {"not_p_frequent": 30} |
| PatrasIQ population | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Sounds | 0.00881 | 0.00257 | 30/30 | {"ok": 30} |
| Sushi A | 0.02543 | 0.00330 | 30/30 | {"ok": 30} |
| Sushi B | NA | NA | 0/30 | {"not_p_frequent": 30} |
| Wheat | 0.15267 | 0.01129 | 30/30 | {"ok": 30} |

## Efficient fallback

| Task | Mean delta | Partition MCSE | Available | Statuses |
|---|---|---|---|---|
| Dots 2013, gap 3 | NA | NA | 0/30 | {"sharp_available": 30} |
| Dots 2013, gap 5 | NA | NA | 0/30 | {"sharp_available": 30} |
| Dots 2013, gap 7 | NA | NA | 0/30 | {"sharp_available": 30} |
| Dots 2013, gap 9 | NA | NA | 0/30 | {"sharp_available": 30} |
| Puzzle, minimum 11 steps | NA | NA | 0/30 | {"sharp_available": 30} |
| Puzzle, minimum 5 steps | NA | NA | 0/30 | {"sharp_available": 30} |
| Puzzle, minimum 7 steps | NA | NA | 0/30 | {"sharp_available": 30} |
| Puzzle, minimum 9 steps | NA | NA | 0/30 | {"sharp_available": 30} |
| Beans | NA | NA | 0/30 | {"sharp_available": 30} |
| Dots 2024 A r2 | 0.04777 | 0.01032 | 30/30 | {"ok": 30} |
| Dots 2024 A r3 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Dots 2024 A r5 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Dots 2024 A r6 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Dots 2024 B r2 | 0.01988 | 0.00738 | 30/30 | {"ok": 30} |
| Dots 2024 B r3 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Dots 2024 B r5 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Dots 2024 B r6 | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| PatrasIQ cost | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| PatrasIQ population | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Sounds | NA | NA | 0/30 | {"sharp_available": 30} |
| Sushi A | NA | NA | 0/30 | {"sharp_available": 30} |
| Sushi B | NA | NA | 0/30 | {"outside_schedule_domain": 30} |
| Wheat | NA | NA | 0/30 | {"outside_schedule_domain": 30} |

## Interpretation and computation

Sharp has 330 completed fits across eleven tasks and 360 unavailable fits across twelve tasks. For Beans, Sharp-minus-PL is +0.00314, compared with P0's likelihood-center delta +0.01275; for Sushi A the respective values are +0.06029 and +0.02543. Both comparisons retain the same held-out reports. They show that estimator choice matters without selecting a replacement after observing test scores.

Fotakis passes its complete-pair gate in 416 of 690 contexts. Efficient is available in the 60 dots2024 r=2 contexts under its declared lambda<=1 fallback policy. Neither missing coverage nor resource failure is a zero loss. The B0 global sieve aliases Sharp in these configurations and is not an additional independent result.

The outstanding 530 Sharp fits comprise **360 E0, 90 L0 and 80 S0**. None is a missing P0 main comparison. See the [exact computation account](../../docs/sieve_computation.md#completion-results-and-remaining-limits). In the immutable raw files these E0 rows retain `study=P0` as their allocation-family key; this view records `raw_study=P0, study=E0`. A shared storage key does not define the scientific experiment name.
