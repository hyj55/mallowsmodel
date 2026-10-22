# B0: supplementary global pair-sieve comparison

[Construction and theorem scope](../../docs/sieve_computation.md) · [Summary CSV](summary.csv) · [E0](../estimator_comparison/README.md) · [P0 main experiment](../main/README.md)

B0 uses fixed report-size bound R=10. It is supplementary to Algorithm 4.1. In every recorded empirical configuration, Sharp has zero pilot depth and one catalogue-wide terminal block. With identical pair draws and tie rules, global sieve and Sharp coincide. The 55 available and 60 unavailable empirical B0 contexts therefore alias E0 Sharp, rather than adding fits. L0/S0 aliases follow the same rule.

The table pairs raw delta (sieve minus PL, nats/report) with delta / log(r!), a dimensionless uniform-reference ratio. NA retains unavailable full five-fit comparisons. Scaling does not resolve missing fits or create independent evidence from an alias.

| Task | r | Available / 5 | Mean delta | Delta / log(r!) | MCSE | Scaled MCSE |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 4 | 5 | -0.02170 | -0.00683 | 0.00576 | 0.00181 |
| Dots 2013, gap 5 | 4 | 5 | -0.00998 | -0.00314 | 0.00413 | 0.00130 |
| Dots 2013, gap 7 | 4 | 5 | -0.00189 | -0.00059 | 0.00541 | 0.00170 |
| Dots 2013, gap 9 | 4 | 5 | -0.04415 | -0.01389 | 0.00337 | 0.00106 |
| Puzzle, minimum 11 steps | 4 | 5 | -0.01042 | -0.00328 | 0.00294 | 0.00092 |
| Puzzle, minimum 5 steps | 4 | 5 | -0.06934 | -0.02182 | 0.00523 | 0.00165 |
| Puzzle, minimum 7 steps | 4 | 5 | -0.02090 | -0.00658 | 0.01363 | 0.00429 |
| Puzzle, minimum 9 steps | 4 | 5 | 0.01546 | 0.00486 | 0.02124 | 0.00668 |
| Beans | 3 | 5 | 0.00978 | 0.00546 | 0.00438 | 0.00244 |
| Dots 2024 A r2 | 2 | 0 | NA | NA | NA | NA |
| Dots 2024 A r3 | 3 | 0 | NA | NA | NA | NA |
| Dots 2024 A r5 | 5 | 0 | NA | NA | NA | NA |
| Dots 2024 A r6 | 6 | 0 | NA | NA | NA | NA |
| Dots 2024 B r2 | 2 | 0 | NA | NA | NA | NA |
| Dots 2024 B r3 | 3 | 0 | NA | NA | NA | NA |
| Dots 2024 B r5 | 5 | 0 | NA | NA | NA | NA |
| Dots 2024 B r6 | 6 | 0 | NA | NA | NA | NA |
| PatrasIQ cost | 6 | 0 | NA | NA | NA | NA |
| PatrasIQ population | 6 | 0 | NA | NA | NA | NA |
| Sounds | 2 | 5 | 0.00948 | 0.01367 | 0.00699 | 0.01008 |
| Sushi A | 10 | 5 | 0.07153 | 0.00474 | 0.01087 | 0.00072 |
| Sushi B | 10 | 0 | NA | NA | NA | NA |
| Wheat | 3 | 0 | NA | NA | NA | NA |

The report-size bound alone does not establish uniform displays, independent reports, a true SM law or the corollary's lambda condition. Empirical predictive NLL differs from minimax Kendall center risk. The summary has `study=B0` and preserves `raw_study=P0` solely as the original allocation-family key.
