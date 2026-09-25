# Locked initial protocol

Written before any held-out model comparison. Seed: 20260920.

Primary question: with the same number of observed reports, does a direct
subset Mallows law or a direct Plackett--Luce law better predict a new whole
ranking on its observed displayed set? Secondary question: does optimization
error explain an apparent Mallows disadvantage?

## Data and estimand

- Beans: validate assigned triples and decode best/middle/worst; exclude
  comparisons with the local variety. Ten experimental labels. Record-level
  split because no assessor ID is supplied; dependence across repeated farmers
  remains an explicit limitation.
- Sushi A: original ten-item complete reports; exact optimization control.
- Sushi B: original ten-of-100 reports; larger partial-ranking benchmark.
- Keep each report intact. Sushi A/B use the same held-out respondent indices,
  are fitted separately, and are not pooled as independent datasets.
- Real data evaluate conditional likelihood; their subset design is not
  assumed uniform or ignorable with respect to unmeasured assessor preferences.
- No generated-full-ranking-then-thinned data are used.

## Split, budget and inference

Hold out 20% once, using the fixed seed. Use five seeded nested subsamples of
the other 80%. N always counts ALL development reports, including tuning.
Within each subsample, use 80% to fit / 20% to select hyperparameters, then
refit on all N reports. Never use test rankings for tuning or solver selection.

Beans budgets: 20, 50, 100, 200, 400, and all development reports.
Sushi A budgets: 20, 50, 100, 300, 1000, 3000.
Sushi B budgets: 100, 300, 1000, 3000 (three repetitions for cost).

Primary score: natural-log whole-ranking NLL. Define Delta=NLL_SM-NLL_PL;
positive means PL predicts better. For each test report, average the paired
loss difference across training repetitions; bootstrap test reports (2,000
resamples) to give a 95% interval conditional on those fits. Repetitions are
not treated as independent datasets. Report training-repeat variability
separately, not as a population confidence interval. All intervals are
pointwise and exploratory, without multiplicity correction.

## Fits

SM center: exact subset DP for n=10. For n=100, eight-start insertion search
(Borda, FKS PosEst, equal-reliability greedy, five seeded random starts), then
a 10-second MILP attempt with certified lower bound. Use the lowest training
Kemeny cost. Report the residual gap; call a fit exact only when certified.
Unseen items remain in the catalog, ties use fixed seeded label priorities.

SM dispersion: profile conditional MLE, beta in [0,10] fixed in advance.
This finite cap prevents infinite predictive loss at a boundary fit. Main
comparison uses this MLE. Prespecified sensitivity: select a multiplicative
beta factor in {0,.25,.5,.75,1} using the inner validation set, refit the
center/dispersion on all N, and apply the chosen factor.

PL: optimize the full listwise sum log likelihood with tau*||theta||^2/2;
select tau in {.01,.1,1,10,100} by inner validation, refit on all N.
Near-unpenalized sensitivity: tau=1e-6, explicitly not an existence-guaranteed
unpenalized MLE. Both models use finite predictions and the same information
budget. Do not equate counts of continuous parameters with total complexity:
the SM center is itself estimated over n! permutations.

## Algorithm check and synthetic check

On real development samples, benchmark normalized Borda, literal FKS PosEst,
equal-reliability greedy, multistart insertion, and exact DP/certified MILP.
Compare training objective and time, with optimum gaps when available.

Simulation: n=10, r=3, uniform independent subsets, random central labels,
N in {20,50,100,300}, 30 independent replicates per DGP. DGPs: selective
Mallows beta=.8; PL with equal latent gaps; PL with unequal gaps. Scale each
PL worth vector to match the Mallows expected within-report inversion count
(not its full entropy). Test on 2,000 independently generated reports.
Measure prediction and central Kendall error. Use independent-replicate
uncertainty for simulations. This is model/estimator validation, NOT a test
of the intermediate-information minimax rate (most N here exceed that range).

## Follow-up policy

Analyze the locked primary outputs first. Any follow-up is labeled exploratory.
Useful targets are solver gaps, inversion-count calibration, sensitivity to
regularization, and beans season transfer. Do not search many subgroups for a
preferred winner. Theoretical sharp estimator is not an MLE algorithm and is
not substituted for exact Kemeny fitting.

Raw third-party data are downloaded on demand, hashed, ignored by git, and
excluded from distributable archives. Do not redistribute Sushi source data.
