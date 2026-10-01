# Mechanism, coverage and empirical diagnostic files

[S1/S2/D1 design](../../docs/strict_feature_analysis.md) · [P2 fixed prediction](../../docs/baseline_replacement.md) · [Criteria](../../docs/criteria.md) · [Uncertainty](../../docs/uncertainty.md)

The directory contains 4,760 independently generated training datasets, fixed-partition results for 16 empirical tasks, discovery-budget controls and a tricot source screen. P1's 30-partition means for the same empirical tasks are in [repeated_holdout](../repeated_holdout/README.md). They have a different uncertainty target from the conditional P2 diagnostics.

## Reproduce

Use the [shared reproduction guide](../../docs/reproducibility.md) for installation, full experiment commands, fixed seeds and solver limitations. Source files remain in ignored data/raw directories. The agricultural downloader runs the eligibility audit only. Replaying a fixed random stream adds no independent evidence.

## Files

| Files | Contents |
|---|---|
| bridge_*, shell_*, coverage_* | Every simulation fit, losses, law features, selector results, summaries and counts |
| real_datasets.csv | Reports, training coverage, distinct displays and grouping limitations |
| real_splits.csv | Specified source record indices and reconstructed group IDs |
| real_parameters.json | Centers, dispersions, PL worths, status and solver certificates |
| real_results.csv, real_predictions.csv | All method statuses and confirmation losses |
| real_shells.csv | Exact shell-mass and within-shell decomposition |
| real_gap_profiles.csv | Equal-displayed-gap reliability; worth-gap bin cutoffs fixed by training |
| real_context.csv | Within-pair context diagnostics around the training center |
| real_objective_* | Separate objective-reference diagnostics; not replacement estimators |
| real_selection.csv | Discovery choices and disjoint confirmation performance |
| followup_budget_* | Same 200 training fits, nested 20/60/200/1000 discovery budgets |
| tricot_eligibility.csv | All nine agricultural candidates and outcome-independent exclusions |
| validation.json | Source checks, independent algorithm tests, all 80 real-row replays, design counts and pre-disconnect checks |
| recovery_status.json | Actual workflow outcome, run URL and source commit |

N means **training reports**. Value means mixture weight a, or shell tilt h. Delta is SM NLL minus PL NLL. Risk is unnormalized Kendall distance to a generating reference, which is a true SM center only for the pure-SM law. Objective Kendall distance in real tasks is not loss against a known latent SM center.

## Exactness and uncertainty

- MLE: exact subset DP for n<=18, otherwise the certified Conitzer integral formulation. Sharp: exact published sieve, unavailable above block size 8. Efficient: Algorithm 3.1 only for lambda<=1; every successful fit has depth zero. Borda: separately named equation (3.4). PL: Hunter's simultaneous unaccelerated equation (30).
- SM dispersion is unbounded; infinite beta and predictive loss are retained. Non-strongly-connected PL comparisons are unavailable, not stabilized by deleted items or added comparisons. Undefined estimates are NaN; divergent loss is infinity.
- Plain summary metrics are NaN if a required run is undefined, and can be infinite. Suffixes finite_conditional, defined, infinite, finite, and status counts disclose conditioning. Plain lo/hi intervals are provided only when every repetition is finite.
- Simulation intervals are paired-replicate t intervals: $`\mathrm{mean}\pm t_{0.975,R-1}\,\mathrm{SD}/\sqrt R`$. Pairs within a ranking are not independent repetitions. With unbounded SM estimates, finite-N boundary events can make unconditional expected log loss infinite even when an observed simulation cell has all finite fits.
- Real intervals are paired whole-report percentile bootstraps with 2,000 draws, conditional on fixed fits. One participant contributes one report per 2024 arm/size task, and folds align across sizes. The anonymous PrefLib export lacks assessor/trial IDs; G1 recovers trial membership but not cross-trial assessors; independent-record intervals are unsupported. Outputs keep point values with uncertainty_status=unavailable_assessor_ids. Intervals are pointwise, unadjusted, and exclude training and source-selection uncertainty.
- Where respondent units are identified, context is a descriptive slope of correctly oriented outcomes on displayed-center gap with pair fixed effects. Only pairs with at least two gap levels, each observed at least twice, are eligible. Whole reports are bootstrapped; undefined resamples are counted through valid_bootstraps. Insufficient variation is unavailable, not a zero effect.
- For shell d, define Q(Y|S)=P_PL(D=d|S)/|shell_d(S)| about the fixed training center. Then log(P_PL/P_SM)=log(Q/P_SM)+log(P_PL/Q). Q is an exact diagnostic, never a fitted replacement model.
- Recovery uses the same seeds and sources after a workspace disconnect; it supplies no additional independent replication. Validation records agreement with rounded pre-disconnect summaries. Numerical differences would be disclosed rather than used to select a favorable run.
