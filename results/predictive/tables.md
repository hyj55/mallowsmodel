# Primary predictive comparison

[Design](../../docs/predictive_comparison.md) · [All estimators](primary.csv) · [Learning curves](learning.csv) · [Synthetic controls](synthetic.csv)

Each row averages 30 refitted 80/20 outer partitions. PL ridge is chosen inside development data; SM dispersion is bounded by 10. Delta is SM minus PL whole-ranking NLL (nats/report). A negative value favors SM. The MCSE concerns random partitions of this fixed dataset, **not a population confidence interval**. Exact-center counts refer to the whole-ranking objective, not the pair-sieve objective.

| Task | n | r | Development reports | Mean delta | Partition MCSE | Available | Certified centers |
|---|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 4 | 4 | 636 | -0.01241 | +0.00226 | 30/30 | 30/30 |
| Dots 2013, gap 5 | 4 | 4 | 635 | -0.01452 | +0.00223 | 30/30 | 30/30 |
| Dots 2013, gap 7 | 4 | 4 | 640 | -0.01255 | +0.00311 | 30/30 | 30/30 |
| Dots 2013, gap 9 | 4 | 4 | 635 | -0.03515 | +0.00413 | 30/30 | 30/30 |
| Puzzle, minimum 11 steps | 4 | 4 | 634 | -0.01161 | +0.00273 | 30/30 | 30/30 |
| Puzzle, minimum 5 steps | 4 | 4 | 636 | -0.05855 | +0.00365 | 30/30 | 30/30 |
| Puzzle, minimum 7 steps | 4 | 4 | 636 | -0.02293 | +0.00368 | 30/30 | 30/30 |
| Puzzle, minimum 9 steps | 4 | 4 | 637 | -0.00881 | +0.00265 | 30/30 | 30/30 |
| Beans | 10 | 3 | 673 | +0.01275 | +0.00240 | 30/30 | 30/30 |
| Dots 2024 A r2 | 30 | 2 | 240 | +0.09381 | +0.01382 | 30/30 | 30/30 |
| Dots 2024 A r3 | 30 | 3 | 240 | +0.10598 | +0.01671 | 30/30 | 30/30 |
| Dots 2024 A r5 | 30 | 5 | 240 | +0.04912 | +0.01987 | 30/30 | 30/30 |
| Dots 2024 A r6 | 30 | 6 | 240 | +0.07953 | +0.02108 | 30/30 | 30/30 |
| Dots 2024 B r2 | 30 | 2 | 240 | +0.11691 | +0.01358 | 30/30 | 30/30 |
| Dots 2024 B r3 | 30 | 3 | 240 | +0.11766 | +0.01532 | 30/30 | 30/30 |
| Dots 2024 B r5 | 30 | 5 | 240 | +0.01198 | +0.01465 | 30/30 | 30/30 |
| Dots 2024 B r6 | 30 | 6 | 240 | -0.04621 | +0.01352 | 30/30 | 30/30 |
| PatrasIQ cost | 36 | 6 | 313 | +0.28339 | +0.01974 | 30/30 | 30/30 |
| PatrasIQ population | 48 | 6 | 313 | +0.07579 | +0.02056 | 30/30 | 30/30 |
| Sounds | 12 | 2 | 1080 | +0.01304 | +0.00267 | 30/30 | 30/30 |
| Sushi A | 10 | 10 | 4000 | +0.02543 | +0.00330 | 30/30 | 30/30 |
| Sushi B | 100 | 10 | 4000 | +0.00975 | +0.00509 | 30/30 | 5/30 |
| Wheat | 16 | 3 | 394 | +0.15917 | +0.01337 | 30/30 | 30/30 |

## Sharp and global pair-sieve

| Task | Sharp minus PL | Partition MCSE | Available | Status counts |
|---|---|---|---|---|
| Dots 2013, gap 3 | -0.01002 | +0.00262 | 30/30 | {"ok": 30} |
| Dots 2013, gap 5 | -0.01452 | +0.00223 | 30/30 | {"ok": 30} |
| Dots 2013, gap 7 | -0.01255 | +0.00311 | 30/30 | {"ok": 30} |
| Dots 2013, gap 9 | -0.03515 | +0.00413 | 30/30 | {"ok": 30} |
| Puzzle, minimum 11 steps | -0.00979 | +0.00279 | 30/30 | {"ok": 30} |
| Puzzle, minimum 5 steps | -0.05855 | +0.00365 | 30/30 | {"ok": 30} |
| Puzzle, minimum 7 steps | -0.02293 | +0.00368 | 30/30 | {"ok": 30} |
| Puzzle, minimum 9 steps | +0.01314 | +0.00595 | 30/30 | {"ok": 30} |
| Beans | +0.00314 | +0.00194 | 30/30 | {"ok": 30} |
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
| Sounds | +0.01306 | +0.00259 | 30/30 | {"ok": 30} |
| Sushi A | +0.06029 | +0.00555 | 30/30 | {"ok": 30} |
| Sushi B | NA | NA | 0/30 | {"sieve_resource_budget": 30} |
| Wheat | NA | NA | 0/30 | {"sieve_resource_budget": 30} |

For these empirical designs Sharp has zero pilot depth and one terminal block containing the catalogue. B0 uses the identical retained pairs and exact sieve, so its rows are explicit aliases of Sharp; it is a supplementary theoretical comparison, not additional independent evidence. Computational failures are retained. A small r does not make factorial enumeration tractable for a large n.
