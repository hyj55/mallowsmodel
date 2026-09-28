# Replacement of historical Beans and Sushi comparisons

**28 September 2026 update:** the real-data point comparisons below retain their original single partition. Use the [30-repeat correction](repeated_holdout.md) ([中文](repeated_holdout_zh.md)) for average predictive performance after repeated full refitting. Original bootstrap intervals stay conditional on the original fits; synthetic results and source-only audits are unchanged.

**Completed 26 September 2026 UTC.** These exploratory fits replace earlier capped, regularized and heuristic versions in the current scientific comparison. They use a newly frozen common 60/20/20 split, not the old repeated learning-curve design. Do not pool the new and old estimates or attribute differences solely to removing regularization.

[Protocol committed before fitting](https://github.com/hyj55/mallowsmodel/commit/517990bb8cc7111513eeca9dac5dd3d97e25831b). All original reports are retained; no ties broken, items deleted, reports repaired or test data used for tuning. Source bytes match the historical manifest. The MLE uses manuscript DP at n=10 and the certified integer-formulation benchmark at n=100. PL uses Hunter's original MM update; both fits are unpenalized. [Canonical method contract](algorithms.md).

| Dataset | Source reports | n,r | Training N | lambda | mu |
|---|---:|---|---:|---:|---:|
| Beans | 842 | 10,3 | 505 | 33.667 | 151.5 |
| Sushi A | 5,000 | 10,10 | 3,000 | 3,000 | 3,000 |
| Sushi B | 5,000 | 100,10 | 3,000 | 27.273 | 300 |

All are outside the sparse-pair regime; no risk-bound claim. Sushi A/B use the same respondent split and are not independent studies. Beans has no assessor identifier. Sushi B's observed display design is strongly nonuniform; an observed lambda value does not certify the uniform-design assumption.

## Confirmation results

Negative delta favors SM. NLLs at different report sizes should not be compared.

| Task | PL NLL | SM exact MLE NLL | Delta | Conditional 95% interval |
|---|---:|---:|---:|---|
| Beans | 1.7973 | 1.7961 | -0.0012 | unavailable: assessor IDs |
| Sushi A | 14.2800 | 14.2946 | +0.0147 | [-0.0271, +0.0619] |
| Sushi B | 14.1856 | 14.1684 | -0.0173 | [-0.0641, +0.0246] |

**No clear MLE predictive winner emerges on this split.** The Beans point difference is small and descriptive. Both Sushi intervals include zero. Intervals are paired whole-respondent bootstrap intervals with 2,000 draws, conditional on these training fits, excluding training and data-selection uncertainty. These findings do not reverse or confirm every historical learning-curve result: the protocol changed.

The Sushi B integer optimization **certified lower=upper=45,149 training disagreements** within its prespecified 120-second budget. The reported center is therefore one global MLE; it is not the earlier insertion heuristic. Using HiGHS reproduces the cited integral formulation, not the original CPLEX implementation or its timing. Other tied optima could produce different test predictions.

Clipped Borda deltas are +0.0107 for Beans, +0.0108 for Sushi A and -0.0138 for Sushi B. It is separately named, not called MLE. Sharp is unavailable for all three exact sieve sizes. Section 3 is outside its schedule domain in all three tasks. Every status is retained in [scores.csv](../results/baseline_replacement/scores.csv).

The replacement confirms that once computational approximation is removed, these data do not automatically deliver a decisive model preference. It does not establish that the models have identical population performance.

## Reproduce

`python run_baseline_replacement.py` under requirements-lock.txt. The default attempts the exact n=100 solve once; failure to certify on another machine remains unavailable. No additional data cleaning or fallback is allowed. [Outputs](../results/baseline_replacement/README.md), [data descriptions](../data/README.md), [references](references.md).
