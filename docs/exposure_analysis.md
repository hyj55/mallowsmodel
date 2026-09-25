# Exposure regimes and ATP tennis: experiment update

## Status and scope

The local extension completed 1,740 independent simulated datasets, 60 small-budget real-data training fits, and ten ATP seasons. Twelve checks passed; 58 representative simulation replicates and all saved real fits were reconstructed, with maximum NLL discrepancy 1.42e-14. The workspace disconnected during upload. **This report preserves the verified findings; the full extension files are being recovered separately.** The original benchmark remains intact.

## Sports data identified

Manuscript Section 4 cites Cantwell and Moore (2022), *Belief propagation for permutations, rankings, and partial orders*, Physical Review E 105, L052303. Page 5 and reference 27 identify **Jeff Sackmann's ATP matches, 2010–2019**. Their reported average degree of about 11 corresponds to our **mu**, not our pair exposure lambda. Their approximate marginal-likelihood criterion differs from our held-out predictive criterion.

- [Paper](https://arxiv.org/abs/2110.00513)
- [Authors' code](https://github.com/gcant/pairwise-comparison-BP)
- [Original data repository](https://github.com/JeffSackmann/tennis_atp)
- [Pinned archival mirror](https://github.com/Aneeshers/tennis-sackmann-archive/tree/83733587353df8a41f2fd4f516147d5aa83f5a8d/atp)

The original endpoint returned 404. The mirror preserves Sackmann's attribution and CC BY-NC-SA 4.0 terms. We use the same source and historical period, without claiming to recover the exact 2022 snapshot or preprocessing.

## Assumptions and available sparse data

mu = N*r/n; lambda = N*r*(r-1)/(n*(n-1)).
Consequently lambda = mu*(r-1)/(n-1): these are not independent coordinates.

| Task | n | r | Training N | lambda | mu |
|---|---:|---:|---:|---:|---:|
| Beans, original reports subsampled | 10 | 3 | 14 | .9333 | 4.20 |
| Sushi B, original reports subsampled | 100 | 10 | 100 | .9091 | 10.00 |
| ATP 2019, chronological training | 418 | 2 | 1,444 | .01657 | 6.91 |
| Uniform SM simulation | 64 | 8 | 22 | .3056 | 2.75 |

New data are not necessary just to obtain lambda<1. Sushi B already meets that numeric condition at N=100; Beans requires N<15. For Sushi A, r=n and lambda=N, so no positive integer N gives lambda<1.

Numeric sparsity does **not** establish independent uniform subsets, beta>=beta0, or sufficient coverage mu>=C0*log(e*r). C0 is unspecified; mu/log(e*r)>1 is not a certificate. Real matchups and display sets need not be uniform. Only the SM synthetic generator is known to satisfy the model and uniform-sampling assumptions; the coverage threshold remains explicitly qualified.

## Estimators implemented in the local run

| Method | Computation | Interpretation |
|---|---|---|
| Section 2, Algorithm 2.1 | Proof-constant pilot, one orientation-independent uniform pair per report/block, exact greedy permutation sieve, disagreement minimization over the sieve | Sharp risk rate under stated conditions; not an MLE |
| Section 3, Algorithm 3.1 | Proof constants, fresh batches, full accumulated offsets, terminal scores and documented fallback | Near-minimax up to one logarithm |
| Center MLE | Exact subset DP at n=8 and for Beans n=10 | Global training optimum; no inherited sharp risk guarantee |
| Insertion | One insertion search from the Section 3 order for large real catalogs | Approximate likelihood fitting |
| PL | Whole-ranking likelihood with positive ridge and training-only tuning | Predictive comparator |

Exact sieve enumeration was limited to blocks of at most eight items. Larger exact sieves were explicitly unavailable, not replaced by MLE.

**Every executed Section 3 fit had depth zero and equaled exposure-normalized Borda.** With the proof threshold A=256 this necessarily happens at n<=256 in the sparse regime; tennis also had small lambda*n. The hierarchy was implemented and its offset logic checked, but these results do not establish a benefit from active refinement. For lambda>1, starting resolution was capped at 1 as a labeled empirical extension.

## Center recovery: retain MLE

Synthetic subsets are sampled first; their SM rankings are generated directly by insertion. The true center is randomized independently of estimator tie-breaking. Thirty independent replicates are used per target design. PL controls match SM's expected inversions.

Selected SM-generated results, n=8, beta=.8; entries are mean Kendall distances, maximum 28:

| r | N | lambda | mu | Section 2 sieve | Section 3/Borda | Exact center MLE | PL order |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2 | 16 | .571 | 4 | 10.90 | 8.70 | 9.17 | 8.10 |
| 2 | 28 | 1 | 7 | 9.07 | 8.10 | 8.30 | 7.97 |
| 4 | 4 | .857 | 2 | 14.63 | 7.97 | 8.87 | 8.43 |
| 4 | 64 | 13.714 | 32 | 5.13 | 1.13 | .57 | 1.27 |

The literal sieve radius is phi=m*choose(m,2)/k. If phi reaches the permutation-space diameter, its packing contains one predetermined order; at n=8 this occurs for k<=8. Pair extraction also discards information from long reports. These finite-sample effects explain poor sieve performance without contradicting the theorem.

MLE should remain as a useful comparator. Neither these average-over-random-center experiments nor exact optimization establishes worst-case minimax optimality.

## Different exposure regimes

For n=64,r=8 under the SM DGP:

| N | lambda | mu | Fraction of pairs incorrectly ordered by Section 3 |
|---|---:|---:|---:|
| 2 | .0278 | .25 | .424 |
| 22 | .3056 | 2.75 | .188 |
| 72 | 1 | 9 | .102 |
| 216 | 3 | 27 | .056 |

At N=2 about 49 of 64 labels are unseen. Tiny-sample profile beta often hits its cap and gives very poor prediction. Greater coverage improves recovery in these cells. The lambda>1 row is empirical evidence outside the sparse theorem.

Conditional NLL difference, Section 3 SM with validation beta shrinkage minus regularized PL:

| N | lambda | mu | SM-generated difference [95% CI] | PL-generated difference [95% CI] |
|---|---:|---:|---:|---:|
| 22 | .306 | 2.75 | -.094 [-.293, .105] | .339 [.206, .471] |
| 72 | 1 | 9 | -.079 [-.142, -.015] | .506 [.463, .549] |
| 216 | 3 | 27 | -.244 [-.278, -.210] | .603 [.585, .621] |

Intervals use paired independent simulation replicates. Raw profiled and shrunk beta were both retained. Beta shrinkage changes prediction, not the center, and is not MLE. For N<5 the protocol fixes multiplier .5 and PL penalty 1 without validation. Beta is capped at 10; a separable sample can have an unrestricted supremum at infinity.

The coverage grid also uses r=2 and 32. Changing r changes both coverage and within-report signal, so it does not isolate a causal effect of mu. At n=64,r=32 one report already gives lambda=.246; smaller target lambda values are unattainable. Two rounded targets coincide at N=1 and contribute 60 independent replicates per DGP.

## Chronological tennis results

Each year's catalog is fixed from the previous season. January–June trains; July–December tests. January–March / April–June is the inner tuning split. Whole tournaments remain together because the date field is a tournament start date. Invalid matches, walkovers, retirements, defaults and abandoned matches are excluded. No chronological shuffle is used.

Catalogs contain 418–469 players; training has 1,444–1,636 matches. Lambda ranges .0144–.0177 and mu 6.64–7.46. Nonuniformity is substantial: in 2010, 195 of 461 catalog players are unseen, versus about .60 expected unseen under uniform sampling at the same average exposure.

The primary test contains 9,495 matches with both players seen in training. A separate all-catalog analysis has 10,082 matches, including 587 cold-start matches. Out-of-catalog matches are separately excluded and counted. No dataset supplies a true center.

Equal-weight mean over ten seasons:

| Fit | Test log loss | Brier | Difference vs PL [95% year-level CI] |
|---|---:|---:|---:|
| Regularized PL/Bradley–Terry | .63444 | .22218 | — |
| Section 3 center, raw beta | .69231 | .24623 | .05787 [.04847, .06728] |
| Section 3 center, shrunk beta | .65898 | .23311 | .02455 [.01497, .03412] |
| Insertion center, shrunk beta | .66392 | .23552 | .02948 [.01790, .04107] |
| Same PL order, SM with shrunk beta | .65612 | — | .02169 [.01340, .02997] |

The same-order check is exploratory. It removes a difference in fitted ordering, yet PL still predicts better. In bins defined by training PL strength gaps, favored players win about 56% of the closest matches and 83% of the widest-gap matches. PL predicts about 55% and 88%; common-upset SM about 61–64%. Within a season SM's correct-order probability is constant; pooled-bin differences reflect season composition. PL is overconfident at large gaps but captures meaningful heterogeneity.

Per-season intervals resample held-out tournaments. Aggregate intervals are t intervals across annual differences. They condition on fits; repeated players and serial dependence remain limitations. This prediction result does not refute the cited article's different marginal-likelihood comparison.

## A sensitivity that changes the interpretation

At Sushi B N=100, shrunk Section 3 SM initially outperformed validation-tuned PL by -.16987 nats. Fixed PL penalty 10 instead yields NLL 14.60024, compared with SM's 14.60707: difference .00683 [-.03409,.04754]. The apparent SM advantage disappears. At N=5, shrinkage often reduces SM to the uniform model, while fixed-penalty PL beats that baseline.

Therefore tiny-validation-set tuning can dominate model rankings. Fixed PL penalties 1 and 10 and the uniform-ranking baseline were added as exploratory sensitivities, not selected retrospectively as the main winner.

## Recommendation

Retain the exact sieve as a small-n statistical-construction check, Section 3/Borda as the scalable score baseline, exact center MLE where feasible, and labeled approximations at larger n. Keep center risk separate from whole-report conditional prediction. Do not include joint probabilities.

The next meaningful extension is an active hierarchy with separately specified empirical constants; its advantage is not demonstrated by these depth-zero runs. Claims about minimax rates need broader n/beta investigations and cannot follow from this finite grid.

## References

The supplied unpublished manuscript specifies Algorithms 2.1/3.1/3.2, Lemma 2.11 and Sections 4.1, 4.3–4.4; it is not redistributed. The sports sources are linked above. Beans, Sushi, original likelihood fitting and noisy-sorting references remain in [the repository bibliography](references.md).
