# Exploratory mechanism diagnostics, locked 2026-09-25

This extension follows examination of the original predictive results and a user
request. It is exploratory, not a new independent confirmatory experiment.
The following diagnostics were specified before their outcomes were computed.
Only conditional whole-ranking likelihood is included; joint likelihood is omitted.

## Algorithm policy

Use exact subset DP at n=10. At n=100 retain the existing eight-start insertion
fit plus MILP bounds; no new claim of exactness. Greedy, Borda, and PosEst remain
initializers / appendix baselines, not separate models in the primary comparison.
No choice of optimizer depends on held-out losses.

## Frozen comparisons

Reuse the original 20% test split, saved fitted parameters, largest prespecified
budgets (Beans 673, Sushi A/B 3000), and all 5/5/3 training repetitions. Models,
centers, worths and dispersion are never refitted using diagnostic test outcomes.
An additional Beans N=20 decomposition explains the prespecified beta-shrinkage
comparison. No selected favorable pairs or subsets are the headline result.

## A. Pair probabilities with the correct report size

There is no direct r=2 real dataset. Do not treat pair orientations extracted
from r=3 or r=10 reports as common-upset observations. For a pair with displayed
center gap h, SM predicts P_h(beta) from manuscript Lemma 2.3. PL predicts
logistic(theta_i-theta_j). Average binary log loss and Brier loss over the pairs
within each report, then over reports; uncertainty resamples whole reports.
For illustration pool h=1 pairs in three PL worth-gap bins whose cutoffs are
chosen using training displayed pairs only. Confidence intervals resample reports.

## B. Exact shell decomposition of the original predictive loss

Fix the training-estimated SM center. D is the report's Kendall distance from
that center and a_r(d) is the Mahonian shell count. Compute Q_PL(D=d|S) exactly
by a subset/polynomial dynamic program. SM conditional on D is uniform, 1/a_r(d).
Define Q_sym(Y|S)=Q_PL(D(Y)|S)/a_r(D(Y)). This is a normalized diagnostic
distribution, not a newly trained competitor. Then, report by report,

    NLL_SM - NLL_PL
      = (NLL_SM - NLL_sym) + (NLL_sym - NLL_PL).

The first component compares shell masses (inversion-count distributions).
The second measures the predictive benefit of PL's nonuniform probabilities
within the same shell. Average loss components over the original fits before
2,000 report-bootstrap resamples. This avoids sparse frequency tables (test:
Beans 169 reports / 91 sets; Sushi A 1000 / 1; Sushi B 1000 / 1000).
It is a predictive decomposition relative to an estimated center, not an
omnibus goodness-of-fit test or a causal explanation.

## C. Context effect holding item pair fixed

Orient each pair by the training SM center and compute displayed gap h and
observed success Z. Estimate a within-cell linear probability slope of Z on h.
Primary cells are item pairs; Beans additionally uses pair x growing-season
cells, and Sushi B uses pair x current east/west-region cells as sensitivity.
Eligible cells have at least two observations at each of at least two distinct
gaps, selected from display information only. Keep this cell set fixed during
bootstrap; recompute weighted cell centering within each bootstrap draw.
Compute identical slopes with Z replaced by the SM and PL predicted probabilities.
PL predicts zero slope. SM's prediction uses its fitted beta and the same exposure
pattern. Use 2,000 whole-report resamples; save effective report/cell counts.
Sushi A has no within-pair context variation and is explicitly not applicable.
Assessor ID is unavailable in Beans and each Sushi respondent gives one report
per task: unmeasured heterogeneity is not removed. Do not infer causal context effects.

## Verification and interpretation

Verify pair marginals and shell DP against exhaustive small-permutation sums,
the exact report-level decomposition, and analytic three-item examples. Run
two fixed-context simulations with known parameters to illustrate that the
context diagnostic can detect the two distinct model mechanisms.
Intervals are conditional on the saved fits, pointwise and exploratory. They
do not incorporate training variability, multiplicity, unknown farmer clusters,
or uncertainty in which fitted center defines the shells and pair orientations.
Retain results even if mechanisms oppose one another or no effect is resolved.
