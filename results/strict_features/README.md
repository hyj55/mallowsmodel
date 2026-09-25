# Strict feature-transition study

Read [the English analysis](../../docs/strict_feature_analysis.md). These results follow the frozen [main protocol](../../docs/protocols/STRICT_FEATURE_PROTOCOL.md), [source addendum](../../docs/protocols/STRICT_SOURCE_ADDENDUM.md), and explicitly exploratory [follow-up](../../docs/protocols/STRICT_FEATURE_FOLLOWUP.md).

## Reproduce

From the repository root with Python 3.12 and requirements-lock.txt installed:

~~~bash
python download_strict_data.py
python download_strict_tricot.py
python run_strict_simulations.py --part bridge
python run_strict_simulations.py --part shell
python run_strict_simulations.py --part coverage
python run_strict_real.py
python run_strict_followups.py --part budgets
python run_strict_followups.py --part objective
python validate_strict_features.py
python make_strict_figures.py
~~~

The master seed is **202609251**. Fitting, discovery, testing and algorithm randomization use separate streams. Use another checkout to preserve recorded outputs. Runtimes can vary; an exact solver can select a different tied optimum on another version, but must certify its objective. All eight recorded n=30 real centers are certified.

The agricultural downloader reproduces the eligibility audit, not extra fits. Raw source files stay under ignored data/raw/strict_features/ and are retrieved from immutable commits; the manifest verifies SHA256 hashes. Original response files and the private manuscript are not rehosted. Figure-only reproduction: python make_strict_figures.py.

## Files

| Files | Contents |
|---|---|
| bridge_*, shell_*, coverage_* | Every simulation fit, losses, law features, selector results, summaries and counts |
| real_datasets.csv | Reports, training coverage, distinct displays and grouping limitations |
| real_splits.csv | Original record indices and reconstructed group IDs |
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
- Simulation intervals are paired-replicate t intervals: mean ± t(0.975,R−1) × SD/sqrt(R). Pairs within a ranking are not independent repetitions. With unbounded SM estimates, finite-N boundary events can make unconditional expected log loss infinite even when an observed simulation cell has all finite fits.
- Real intervals are paired whole-report percentile bootstraps with 2,000 draws, conditional on fixed fits. One participant contributes one report per 2024 arm/size task, and folds align across sizes. PrefLib lacks assessor/trial IDs, so its intervals are anonymous-record working calculations. Intervals are pointwise, unadjusted, and exclude training and source-selection uncertainty.
- Context is a descriptive slope of correctly oriented outcomes on displayed-center gap with pair fixed effects. Only pairs with at least two gap levels, each observed at least twice, are eligible. Whole reports are bootstrapped; undefined resamples are counted through valid_bootstraps. Insufficient variation is unavailable, not a zero effect.
- For shell d, define Q(Y|S)=P_PL(D=d|S)/|shell_d(S)| about the fixed training center. Then log(P_PL/P_SM)=log(Q/P_SM)+log(P_PL/Q). Q is an exact diagnostic, never a fitted replacement model.
- Recovery uses the same seeds and sources after a workspace disconnect; it supplies no additional independent replication. Validation records agreement with rounded pre-disconnect summaries. Numerical differences would be disclosed rather than used to select a favorable run.
