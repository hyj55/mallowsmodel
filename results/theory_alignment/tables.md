# Saved results used in the theory comparison

[Interpretation and theorem conditions](../../docs/theory_alignment.md) · [Files and reproduction](README.md)

These are arithmetic summaries of existing runs. N always counts training reports. Risk is unnormalized Kendall loss only in the pure-SM simulation tables; empirical NLL is not that risk. NA remains unavailable. No new fit or sample was generated.

## P1 training regimes

Only dots2024 A/B r=2 pass the numerical λ≤1 screen. All rows still lack a verified homogeneous-SM, independent-uniform-display sampling law. The coverage ratio μ/log(er) is not certification of the unknown sufficient constant C0.

| dataset | n | r | N | lambda_ | mu | coverage_ratio | pair_min_across_partitions | full_ranking |
|---|---|---|---|---|---|---|---|---|
| 00024-00000001 | 4 | 4 | 477 | 477 | 477 | 199.89 | 477 | True |
| 00024-00000002 | 4 | 4 | 476 | 476 | 476 | 199.47 | 476 | True |
| 00024-00000003 | 4 | 4 | 480 | 480 | 480 | 201.15 | 480 | True |
| 00024-00000004 | 4 | 4 | 476 | 476 | 476 | 199.47 | 476 | True |
| 00025-00000001 | 4 | 4 | 475 | 475 | 475 | 199.05 | 475 | True |
| 00025-00000002 | 4 | 4 | 477 | 477 | 477 | 199.89 | 477 | True |
| 00025-00000003 | 4 | 4 | 477 | 477 | 477 | 199.89 | 477 | True |
| 00025-00000004 | 4 | 4 | 478 | 478 | 478 | 200.31 | 478 | True |
| beans | 10 | 3 | 505 | 33.667 | 151.5 | 72.191 | 17 | False |
| dots2024_A_r2 | 30 | 2 | 180 | 0.41379 | 12 | 7.0874 | 0 | False |
| dots2024_A_r3 | 30 | 3 | 180 | 1.2414 | 18 | 8.5771 | 0 | False |
| dots2024_A_r5 | 30 | 5 | 180 | 4.1379 | 30 | 11.497 | 0 | False |
| dots2024_A_r6 | 30 | 6 | 180 | 6.2069 | 36 | 12.895 | 0 | False |
| dots2024_B_r2 | 30 | 2 | 180 | 0.41379 | 12 | 7.0874 | 0 | False |
| dots2024_B_r3 | 30 | 3 | 180 | 1.2414 | 18 | 8.5771 | 0 | False |
| dots2024_B_r5 | 30 | 5 | 180 | 4.1379 | 30 | 11.497 | 0 | False |
| dots2024_B_r6 | 30 | 6 | 180 | 6.2069 | 36 | 12.895 | 0 | False |
| patras_cost | 36 | 6 | 235 | 5.5952 | 39.167 | 14.029 | 0 | False |
| patras_population | 48 | 6 | 235 | 3.125 | 29.375 | 10.522 | 0 | False |
| sounds | 12 | 2 | 810 | 12.273 | 135 | 79.733 | 4 | False |
| sushi_a | 10 | 10 | 3000 | 3000 | 3000 | 908.38 | 3000 | True |
| sushi_b | 100 | 10 | 3000 | 27.273 | 300 | 90.838 | 0 | False |
| wheat | 16 | 3 | 295 | 7.375 | 55.312 | 26.357 | 1 | False |

## P1 estimator predictions

All differences are paired on the same confirmation reports and averaged over the same 30 partitions. The table displays only complete means; the CSV preserves finite-conditional differences and their denominators. Signs here compare SM center estimators, not SM versus PL.

| dataset | Borda − exact | Sharp − exact | Efficient − Borda |
|---|---|---|---|
| 00024-00000001 | 0 | 0.0027375 | NA |
| 00024-00000002 | 0 | 0.0015599 | NA |
| 00024-00000003 | 0 | 0 | NA |
| 00024-00000004 | 0 | 0 | NA |
| 00025-00000001 | 0 | 0.00091573 | NA |
| 00025-00000002 | 0 | 0 | NA |
| 00025-00000003 | 0 | 0.017926 | NA |
| 00025-00000004 | 0 | 0.0024297 | NA |
| beans | -0.01303 | NA | NA |
| dots2024_A_r2 | -0.1761 | NA | 0 |
| dots2024_A_r3 | -0.092552 | NA | NA |
| dots2024_A_r5 | -0.072583 | NA | NA |
| dots2024_A_r6 | 0.014321 | NA | NA |
| dots2024_B_r2 | -0.15175 | NA | 0 |
| dots2024_B_r3 | -0.12902 | NA | NA |
| dots2024_B_r5 | -0.035894 | NA | NA |
| dots2024_B_r6 | 0.013853 | NA | NA |
| patras_cost | -0.0072252 | NA | NA |
| patras_population | -0.068909 | NA | NA |
| sounds | -0.005867 | NA | NA |
| sushi_a | 0.00363 | NA | NA |
| sushi_b | NA | NA | NA |
| wheat | -0.013654 | NA | NA |

The [method inventory](p1_methods.csv) records all five methods for every task, including status counts, branches, depth, complete/conditional NLL and external-objective distance. That external distance is not true-center risk.

## Pure-SM center-risk comparisons

SM β=.8 and uniformly sampled displays. Intervals below are the saved working t intervals over independent training draws, not new CIs and not minimax envelopes. A randomized generating center removes favorable fixed-label choices; an average across sampled centers does not numerically evaluate a supremum over centers.

### S1 bridge endpoint: n=8, equal-gap stream

| r | N | lambda_ | method | risk | risk_lo | risk_hi | successful_fits | repetitions |
|---|---|---|---|---|---|---|---|---|
| 2 | 8 | 0.28571 | borda | 11.1 | 9.906 | 12.294 | 40 | 40 |
| 2 | 8 | 0.28571 | efficient | 11.1 | 9.906 | 12.294 | 40 | 40 |
| 2 | 8 | 0.28571 | mle | 11.65 | 10.248 | 13.052 | 40 | 40 |
| 2 | 8 | 0.28571 | pl | NA | NA | NA | 0 | 40 |
| 2 | 8 | 0.28571 | sharp | 13.4 | 12.286 | 14.514 | 40 | 40 |
| 2 | 28 | 1 | borda | 8.325 | 7.4135 | 9.2365 | 40 | 40 |
| 2 | 28 | 1 | efficient | 8.325 | 7.4135 | 9.2365 | 40 | 40 |
| 2 | 28 | 1 | mle | 9.1 | 7.8951 | 10.305 | 40 | 40 |
| 2 | 28 | 1 | pl | NA | NA | NA | 23 | 40 |
| 2 | 28 | 1 | sharp | 10.575 | 9.444 | 11.706 | 40 | 40 |
| 2 | 112 | 4 | borda | 5.025 | 4.2041 | 5.8459 | 40 | 40 |
| 2 | 112 | 4 | efficient | NA | NA | NA | 0 | 40 |
| 2 | 112 | 4 | mle | 4.375 | 3.3645 | 5.3855 | 40 | 40 |
| 2 | 112 | 4 | pl | 5.15 | 4.3162 | 5.9838 | 40 | 40 |
| 2 | 112 | 4 | sharp | 4.675 | 3.7241 | 5.6259 | 40 | 40 |
| 2 | 448 | 16 | borda | 1.675 | 1.3101 | 2.0399 | 40 | 40 |
| 2 | 448 | 16 | efficient | NA | NA | NA | 0 | 40 |
| 2 | 448 | 16 | mle | 0.55 | 0.21069 | 0.88931 | 40 | 40 |
| 2 | 448 | 16 | pl | 1.45 | 1.0956 | 1.8044 | 40 | 40 |
| 2 | 448 | 16 | sharp | 0.45 | 0.15183 | 0.74817 | 40 | 40 |
| 3 | 8 | 0.85714 | borda | 9.1 | 8.061 | 10.139 | 40 | 40 |
| 3 | 8 | 0.85714 | efficient | 9.1 | 8.061 | 10.139 | 40 | 40 |
| 3 | 8 | 0.85714 | mle | 9.075 | 8.1186 | 10.031 | 40 | 40 |
| 3 | 8 | 0.85714 | pl | NA | NA | NA | 7 | 40 |
| 3 | 8 | 0.85714 | sharp | 13.825 | 12.633 | 15.017 | 40 | 40 |
| 3 | 28 | 3 | borda | 4.275 | 3.6073 | 4.9427 | 40 | 40 |
| 3 | 28 | 3 | efficient | NA | NA | NA | 0 | 40 |
| 3 | 28 | 3 | mle | 4.425 | 3.5563 | 5.2937 | 40 | 40 |
| 3 | 28 | 3 | pl | NA | NA | NA | 37 | 40 |
| 3 | 28 | 3 | sharp | 8.65 | 7.6321 | 9.6679 | 40 | 40 |
| 3 | 112 | 12 | borda | 1.85 | 1.4062 | 2.2938 | 40 | 40 |
| 3 | 112 | 12 | efficient | NA | NA | NA | 0 | 40 |
| 3 | 112 | 12 | mle | 0.95 | 0.56032 | 1.3397 | 40 | 40 |
| 3 | 112 | 12 | pl | 1.875 | 1.4515 | 2.2985 | 40 | 40 |
| 3 | 112 | 12 | sharp | 4.175 | 3.3656 | 4.9844 | 40 | 40 |
| 3 | 448 | 48 | borda | 0.6 | 0.37328 | 0.82672 | 40 | 40 |
| 3 | 448 | 48 | efficient | NA | NA | NA | 0 | 40 |
| 3 | 448 | 48 | mle | 0.075 | -0.01031 | 0.16031 | 40 | 40 |
| 3 | 448 | 48 | pl | 0.425 | 0.23493 | 0.61507 | 40 | 40 |
| 3 | 448 | 48 | sharp | 0.575 | 0.34727 | 0.80273 | 40 | 40 |

The second gap-shape stream and the shell-tilt-zero endpoint are retained separately in [all pure-SM results](pure_sm_results.csv); they are additional saved streams, not pooled as extra settings or selected by performance.

### S2: n=32, r=3

| N | lambda_ | mu | method | risk | risk_lo | risk_hi | successful_fits |
|---|---|---|---|---|---|---|---|
| 40 | 0.24194 | 3.75 | borda | 153.93 | 146.05 | 161.8 | 40 |
| 40 | 0.24194 | 3.75 | efficient | 153.93 | 146.05 | 161.8 | 40 |
| 40 | 0.24194 | 3.75 | pl | NA | NA | NA | 0 |
| 160 | 0.96774 | 15 | borda | 89.5 | 84.722 | 94.278 | 40 |
| 160 | 0.96774 | 15 | efficient | 89.5 | 84.722 | 94.278 | 40 |
| 160 | 0.96774 | 15 | pl | 89.725 | 84.659 | 94.791 | 40 |
| 640 | 3.871 | 60 | borda | 45.2 | 42.802 | 47.598 | 40 |
| 640 | 3.871 | 60 | efficient | NA | NA | NA | 0 |
| 640 | 3.871 | 60 | pl | 45.05 | 42.729 | 47.371 | 40 |

### S3 complete rankings: n=r=8

| N | method | risk | risk_lo | risk_hi | repetitions |
|---|---|---|---|---|---|
| 1 | efficient | 4.7667 | 3.9024 | 5.631 | 30 |
| 1 | mle | 4.7667 | 3.9024 | 5.631 | 30 |
| 1 | pl | 4.7667 | 3.9024 | 5.631 | 30 |
| 1 | sharp | 14.567 | 13.008 | 16.125 | 30 |
| 2 | efficient | 3.6333 | 2.9162 | 4.3505 | 30 |
| 2 | mle | 4.1667 | 3.3002 | 5.0332 | 30 |
| 2 | pl | 3.8 | 3.1178 | 4.4822 | 30 |
| 2 | sharp | 14.033 | 12.509 | 15.557 | 30 |
| 8 | efficient | 0.96667 | 0.64916 | 1.2842 | 30 |
| 8 | mle | 0.96667 | 0.69841 | 1.2349 | 30 |
| 8 | pl | 1.1667 | 0.8402 | 1.4931 | 30 |
| 8 | sharp | 13.433 | 12.167 | 14.699 | 30 |
| 32 | efficient | 0.26667 | 0.048862 | 0.48447 | 30 |
| 32 | mle | 0.16667 | 0.025127 | 0.30821 | 30 |
| 32 | pl | 0.26667 | 0.072185 | 0.46115 | 30 |
| 32 | sharp | 6.2667 | 5.3112 | 7.2221 | 30 |

The saved efficient label is depth-zero Borda, which equals sorting average positions here. Sharp uses a pair sieve, not Theorem 2.17’s tournament estimator. There is no saved full-ranking majority-estimator risk series.

### S3 coverage: n=64, depth-zero global scores

| r | N | lambda_ | mu | nu | Vcov | coverage_dominated | risk | risk_lo | risk_hi | repetitions |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 60 | 0.029762 | 1.875 | 1.9048 | 1.9049 | False | 818.73 | 792.74 | 844.73 | 30 |
| 2 | 605 | 0.3001 | 18.906 | 19.206 | 19.208 | False | 497.63 | 475.1 | 520.17 | 30 |
| 2 | 2016 | 1 | 63 | 64 | 64.005 | False | 301.7 | 290.32 | 313.08 | 30 |
| 2 | 6048 | 3 | 189 | 192 | 192.02 | False | 183.43 | 176.38 | 190.49 | 30 |
| 8 | 2 | 0.027778 | 0.25 | 1.7778 | 0.26706 | True | 853.87 | 826.15 | 881.58 | 30 |
| 8 | 22 | 0.30556 | 2.75 | 19.556 | 2.9377 | False | 378.83 | 365.25 | 392.42 | 30 |
| 8 | 72 | 1 | 9 | 64 | 9.6143 | False | 205.37 | 196.94 | 213.79 | 30 |
| 8 | 216 | 3 | 27 | 192 | 28.843 | False | 112.67 | 107.56 | 117.77 | 30 |
| 32 | 1 | 0.24603 | 0.5 | 15.746 | 0.69315 | True | 540.9 | 527.31 | 554.49 | 60 |
| 32 | 4 | 0.98413 | 2 | 62.984 | 2.7726 | False | 153.9 | 144.8 | 163 | 30 |
| 32 | 12 | 2.9524 | 6 | 188.95 | 8.3178 | False | 57.1 | 53.69 | 60.51 | 30 |

## C1 / S3 learning: center benchmarks under SM

n=10, r=3, β=.8; 30 independent streams, with nested budgets within each stream. These are means of saved per-stream errors; no new intervals are attached. The objective gap uses the exact DP optimum. A zero gap certifies the attained training objective, not a general risk guarantee for the algorithm.

| N | lambda_ | method | risk | mean_training_objective_gap | max_training_objective_gap | zero_objective_gap_repetitions | repetitions |
|---|---|---|---|---|---|---|---|
| 20 | 1.3333 | borda | 9.6667 | 3.1333 | 6 | 0 | 30 |
| 20 | 1.3333 | greedy | 10.267 | 2.4 | 5 | 2 | 30 |
| 20 | 1.3333 | multistart | 9.7 | 0 | 0 | 30 | 30 |
| 20 | 1.3333 | posest | 10.967 | 4.9667 | 11 | 0 | 30 |
| 50 | 3.3333 | borda | 6.4667 | 4.6333 | 16 | 2 | 30 |
| 50 | 3.3333 | greedy | 7.2 | 3.8333 | 13 | 1 | 30 |
| 50 | 3.3333 | multistart | 6.5333 | 0 | 0 | 30 | 30 |
| 50 | 3.3333 | posest | 7.6333 | 6.4333 | 14 | 0 | 30 |
| 100 | 6.6667 | borda | 4.4333 | 5.9 | 16 | 0 | 30 |
| 100 | 6.6667 | greedy | 4.9333 | 4.0333 | 15 | 7 | 30 |
| 100 | 6.6667 | multistart | 3.5667 | 0 | 0 | 30 | 30 |
| 100 | 6.6667 | posest | 4.6667 | 6 | 24 | 2 | 30 |
| 300 | 20 | borda | 2 | 9.7 | 20 | 4 | 30 |
| 300 | 20 | greedy | 1.5667 | 5.0333 | 15 | 8 | 30 |
| 300 | 20 | multistart | 0.26667 | 0 | 0 | 30 | 30 |
| 300 | 20 | posest | 1.0333 | 4.8333 | 17 | 16 | 30 |

## G1: Fotakis versus exact SM

Primary 70% within-group allocations, 100 repetitions. Only complete all-report NLL comparisons enter a complete mean; local unavailable groups are not silently removed. Negative means favor Fotakis-center SM prediction. All 50%/80% and group-holdout comparisons are also in [the CSV](g1_fotakis_vs_exact.csv).

| dataset | scheme | complete_finite_pairs | repetitions | fotakis_minus_exact | identical_nll_repetitions |
|---|---|---|---|---|---|
| dots-3 | local | 100 | 100 | -0.0090088 | 0 |
| dots-3 | matched_pool | 100 | 100 | -0.020955 | 0 |
| dots-3 | pooled | 100 | 100 | 0 | 100 |
| dots-5 | local | 100 | 100 | -0.013233 | 0 |
| dots-5 | matched_pool | 100 | 100 | -0.020979 | 0 |
| dots-5 | pooled | 100 | 100 | 0 | 100 |
| dots-7 | local | 100 | 100 | -0.02157 | 0 |
| dots-7 | matched_pool | 100 | 100 | -0.026411 | 0 |
| dots-7 | pooled | 100 | 100 | 0 | 100 |
| dots-9 | local | 100 | 100 | -0.024682 | 0 |
| dots-9 | matched_pool | 100 | 100 | -0.023555 | 0 |
| dots-9 | pooled | 100 | 100 | 0 | 100 |
| puzzle-11 | local | 100 | 100 | -0.012235 | 0 |
| puzzle-11 | matched_pool | 100 | 100 | -0.01989 | 0 |
| puzzle-11 | pooled | 100 | 100 | 0 | 100 |
| puzzle-5 | local | 100 | 100 | -0.022479 | 0 |
| puzzle-5 | matched_pool | 100 | 100 | -0.020691 | 1 |
| puzzle-5 | pooled | 100 | 100 | 0 | 100 |
| puzzle-7 | local | 100 | 100 | -0.014719 | 0 |
| puzzle-7 | matched_pool | 100 | 100 | -0.031774 | 0 |
| puzzle-7 | pooled | 100 | 100 | 0 | 100 |
| puzzle-9 | local | 100 | 100 | -0.0039607 | 0 |
| puzzle-9 | matched_pool | 100 | 100 | -0.021652 | 0 |
| puzzle-9 | pooled | 100 | 100 | 0 | 100 |
| sounds | local | 0 | 100 | NA | 0 |
| sounds | matched_pool | 0 | 100 | NA | 0 |
| sounds | pooled | 100 | 100 | -0.0059743 | 0 |
