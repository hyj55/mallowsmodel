# Additional sources and mechanism validation

Frozen before the new fits and simulations, 26 September 2026. This is a follow-up motivated by the previous results, not a preregistered original study. Earlier data/estimators/results remain unchanged. Seed 202609260; 200 independent synthetic training samples per cell.

## Questions

1. In new directly elicited pairwise and six-item rankings, does the fixed-method predictive comparison agree with the previously suggested structural explanation?
2. Can the existing context diagnostic detect actual selective-Mallows effects at realistic diagnostic sample sizes? How does estimation of the center affect it?
3. Can assessor heterogeneity coupled to displayed-set assignment produce an apparent Mallows-like context effect even when every assessor group follows context-independent PL?

Synthetic studies assess these finite-sample questions and diagnostic failure modes, not minimax rates or the existence of a mechanism in real observations.

## Fixed additional source scope

Include both genuine pairwise datasets from the BayesMallows release: beaches and sounds. Use commit a26cf89d3142ea3499489730e7c2b3ef9a26bfb2, original data files plus decoding scripts and documentation. Retain all stated comparisons and assessor IDs, including nontransitive responses. Do not compute a transitive closure, infer missing preferences, or treat derived/simulated package examples as empirical data.

Include both original PrefLib 00034 PatrasIQ tasks, cost of living (36 cities) and population (48 countries), commit 1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80. Each of 392 volunteers ranked one assigned six-item set per task according to source documentation. Expand multiplicities losslessly. Objective answer order is a diagnostic reference, not a known latent Mallows center. No cross-task respondent matching is recoverable, so the two tasks are analyzed separately and not counted as independent studies.

The metadata screen also records potato visual/weighing and Breakfast Items: the former has only 12 assessors and a fixed display; the latter has 21 households and fixed displays in six meal scenarios. They are not selected for this round's repeated-pair/changed-display question. Single-choice context data are not converted to complete rankings. Record all scoped decisions; do not continue screening or change eligibility after examining a model winner.

## Real experiments

Use a fixed 60/20/20 split of whole assessor units for beaches/sounds. For PatrasIQ use original report units, justified by the documented one-report-per-volunteer-per-task design. Anonymous multiplicities do not establish cross-task identities. Every original observation belongs to exactly one split; no source rows/items are dropped.

Use unchanged src/strict_models.py: manuscript exact center DP when n<=18; otherwise certified Conitzer integral LP3 with HiGHS, 120 seconds and no uncertified fallback; unbounded profile dispersion; Hunter simultaneous unpenalized MM; literal sharp/efficient availability; separately named equation (3.4) Borda. beta0=.1 is a fixed scheduling input, not an asserted population bound. Record unavailable algorithms.

Primary endpoint: confirmation whole-ranking conditional NLL and paired SM-minus-PL difference. Compute 2,000 whole-unit percentile bootstrap draws, conditional on fits, by resampling assessor blocks for repeated pairwise observations. PatrasIQ bootstrap resamples individual reports under its documented sampling-unit interpretation. These are pointwise exploratory intervals; source selection, volunteer sampling, training uncertainty and dependence between the two PatrasIQ tasks preclude population-wide model prevalence claims.

For pairs, report held-out orientation agreement in three PL log-worth-gap bins, with cuts determined from training. Do not demand common pair probabilities after breaking a longer ranking into pairs. For six-item reports, retain the exact shell decomposition and the existing context slope, separately about training MLE and external objective orders. Use the existing eligibility rule (at least two gap levels with at least two observations each), and report unavailable contrasts. Discovery does not alter an estimator or select the reported confirmation hypotheses.

## Synthetic A: power and uncertain centers

n=8, r=3, uniform independent displayed subsets; true SM beta=.8 versus true PL with equal adjacent log-worth gaps, using the existing expected-inversion-matched generator. N=28 or 448; 200 repetitions per cell (800 training datasets). Randomize item labels independently of fixed fitting tie rules.

Fit exact SM MLE and Hunter PL once on training. Draw 1,000 independent diagnostic reports and use nested prefixes M=60,200,1000. On each prefix apply the unchanged context diagnostic twice: (i) true reference order/beta=.8, explicitly an oracle diagnostic, (ii) fitted SM order/beta. The oracle is not a competing estimator. Use 499 report-bootstrap draws per diagnostic, fixed before simulation. Record intervals, eligible pairs, estimated/predicted slopes, rejection of zero, and rejection of the fitted SM slope. Count undefined diagnostics and boundary fits explicitly.

Compute exact population whole-ranking test NLL and Kendall error of each fitted center, not a selected finite test sample. Record the original context selector (closer to fitted SM predicted slope versus zero), its population-NLL selection accuracy and regret. No threshold is optimized using the results. Report Monte Carlo rates over repetitions with Wilson intervals; do not count the nested diagnostic budgets as independent training datasets.

## Synthetic B: heterogeneity confounded with assignment

n=4, r=3, two displays S_in={0,1,2} and S_out={0,2,3}, each with probability 1/2. The common reference order is 0<1<2<3; the focal pair is (0,2). Group g has a genuine PL worth vector with log worth -s_g*(0,1,2,3), where s_0=.2, s_1=.8. Thus within each group the focal pair probability does not depend on the display.

Set P(g=1|S_in)=(1+rho)/2 and P(g=1|S_out)=(1-rho)/2, rho=0,.45,.9. Marginal group shares and marginal display shares remain 1/2. This intentionally changes assignment dependence; it does not claim to hold inversion noise fixed. The exact focal context contrast is rho*[logistic(1.6)-logistic(.4)], numerically evaluated as a control.

Use N=448, 200 repetitions per rho (600 training datasets), independent diagnostic prefixes M=60,200,1000. Generate each whole report directly from its group's PL on its shown set. Fit the same single-population SM and PL estimators; compute exact population NLL under the mixture. Neither fit is asserted to be a correctly specified model of heterogeneous assessors.

With the fixed true reference order, compare the existing pooled pair-fixed-effect diagnostic against pair-by-group fixed effects, using 499 whole-report bootstrap draws. There is one independent assessor/report in this synthetic experiment. Record lack of overlap as unavailable. No adjusted group model replaces a main fitted estimator. Also record the exact population focal contrast and the unadjusted versus adjusted rejection rates. A positive pooled effect alone must not be called evidence for selective Mallows.

## Reporting and integrity

Total new synthetic training datasets: 1,400. All draws, parameters, statuses, diagnostics and source hashes are saved; no discarded unfavorable runs. Do not modify the existing estimator modules. New code defines data acquisition, declared synthetic laws, inference summaries and verification only. Cite the manuscript, Hunter/Conitzer and every new empirical source. Maintain one extension report linked from the current README; earlier result directories remain distinct.
