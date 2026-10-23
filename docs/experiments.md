# Research questions and experimental design

[Study guide](../README.md) · [Data](../data/README.md) · [Estimators](algorithms.md) · [Criteria](criteria.md) · [Uncertainty](uncertainty.md) · [Findings](findings.md)

## What is compared?

An observation is a displayed item set S together with its reported ordering Y. Both models are fitted to the same training rankings and evaluated on the same held-out rankings. Metadata are not model covariates. The comparison concerns conditional predictive distributions P(Y | S), not the probability of selecting S.

Three sizes must remain distinct: n is the item catalogue, r is the number of items in one report, and N is the number of training reports. A person may contribute more than one report. M denotes the available source reports; it is not necessarily the number of independent people. [Data notation and coverage](../data/README.md#notation-and-coverage) define these quantities precisely.

## Experiment map

The identifiers below are reading aids; filenames preserve the executable and output locations. **P0 is the only main experiment: Algorithm 4.1, comparing likelihood-center SM with PL. E0 separately names the center-estimator comparison, and B0 separately names global sieve.** L0/S0 use the same finite fitting rules for learning and catalogue-size questions. The remaining components are organized in the [supplementary guide](supplementary.md).

| ID | Scientific question | Data and design | Estimators | Output and detailed design |
|---|---|---|---|---|
| P0 | Main experiment: Algorithm 4.1 | All 23 tasks; 5 grouped 80/20 outer allocations, 60/20 inner tuning split | Whole-ranking likelihood-center SM and positive-ridge PL only | [Main design](predictive_comparison.md), [independent main results](../results/main/README.md) |
| E0 | Supplementary center-estimator comparison | Same empirical allocations as P0; distinct estimator outcomes | Sharp, admitted Fotakis, independently admitted Efficient and global Borda; same saved PL/likelihood-SM references | [E0 design](estimator_comparison.md), [E0 results](../results/estimator_comparison/README.md) |
| L0 | Prediction as training size grows | Sushi A/B; 5 aligned outer tests, nested N=20–3000 plus reused P0 N=4000 | P0 likelihood-center/PL procedures plus explicitly labeled estimator supplements; r=R=10 | [Learning design](predictive_learning.md), `results/predictive/learning.csv` |
| S0 | Prediction and center error as N or n grows | Direct SM/PL; 240 independent draws; fixed r=3, R=10 | P0 likelihood-center/PL procedures plus estimator supplements; known-order Kendall error and test NLL | [Controlled curves](predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10), `results/predictive/synthetic.csv` |
| B0 | Global sieve under a fixed report-size bound | All empirical tasks with r<=10 and S0; R stays 10 | Exact global pair-sieve; explicit alias where identical to Sharp | [Sieve supplement](sieve_computation.md), `sm_global_sieve` rows in predictive tables |
| Tuned block sieve | Can a Borda pilot and smaller exact sieves make unresolved Sharp cells usable? | One ID-0 allocation/draw for each of 19 unresolved E0/L0/S0 cells; validation selects block count | Explicit Borda-pilot variant with disjoint unpadded blocks; paired saved PL/SM/Fotakis/Efficient and two Borda controls | [Complete standalone report](tuned_block_sieve.md), `results/tuned_block_sieve/` |
| P1 | Supplementary unpenalized prediction and fit existence | All 23 empirical tasks; 5 independent randomizations of the fixed data; 60/20/20 | Unpenalized PL; SM exact, Sharp, efficient, clipped Borda, with unavailable statuses | [Unpenalized control](repeated_holdout.md), `results/repeated_holdout/` |
| P2 | Conditional prediction and diagnostics for specified fitted models | Same 23 tasks; one specified 60/20/20 allocation per task | Same candidate family as P1 | [Fixed-partition analysis](baseline_replacement.md); baseline, strict-feature, wheat and validation result directories |
| L1 | How training budget changes prediction | Beans, Sushi A/B; nested training subsets and fixed outer tests | Exact small-catalogue or approximate large-catalogue SM; bounded/shrunk dispersion; tuned ridge PL | [Learning curves](learning_curves.md); snapshot `results/real_*` |
| L2 | What happens with very low exposure? | Beans and Sushi B; six budgets, five repetitions per budget | Efficient/Borda SM; Beans exact center or Sushi B insertion; bounded/shrunk dispersion; ridge PL and fixed-penalty controls | [Small-budget design](learning_curves.md#small-budget-prediction); snapshot `results/exposure/real_*` |
| G1 | Does fitting within a trial/person help? | Four Puzzle, four Dots 2013 tasks, Sounds; five 70/30 within-group splits, matched pooled controls, five group holdouts | SM exact and Fotakis; Sharp or efficient when admitted; unpenalized PL | [Group analysis](group_sensitivity.md), `results/group_sensitivity/` |
| S1 | Which model benefits as within-shell probabilities change? | Uniform-subset bridge and shell laws; n=8; 40 independent training draws per cell | SM exact, Sharp, efficient, clipped Borda; unpenalized PL | [Mechanism simulations](strict_feature_analysis.md), `results/strict_features/bridge_*`, `shell_*` |
| S2 | How do sparse observations affect estimation and fit existence? | Uniform-subset n=32 bridge; 40 independent draws per cell | SM efficient and clipped Borda; unpenalized PL; no exact center fitted | [Coverage simulations](strict_feature_analysis.md#coverage-design), `results/strict_features/coverage_*` |
| S4 | Can active hierarchies and smaller constants improve true-center risk and computation? | Independent Section 4.4 design; separate calibration; 100 fresh confirmation draws per setting | Proof/calibrated Efficient and Sharp, global Borda, small-n exact Kemeny; full-ranking majority endpoint | [Standalone code, protocol, results and report](../experiments/section44/README.md); no results are pooled with other experiments |
| S3 | How do regularization and exposure affect sample-size curves? | n=10 learning curves; n=8 and n=64 exposure grids; independent simulation repetitions | Specified bounded/shrunk SM and ridge PL variants; center methods depend on grid | [Regularized simulations](learning_curves.md#simulation-learning-and-exposure-grids); snapshot synthetic/exposure tables |
| D1 | Can discovery diagnostics choose a fitted model? | S1/S2 discovery samples; nested budgets on 200 S1 training fits; 16 PrefLib/dots2024 real tasks | Already fitted competitors; no diagnostic-based center refitting | [Selection design](strict_feature_analysis.md#discovery-based-selection), selection and budget tables |
| D2 | Are context effects and their intervals trustworthy? | SM/PL n=8 and heterogeneous PL n=4; 200 independent draws per setting | Exact SM and unpenalized PL; oracle/fitted and pooled/group-adjusted diagnostics | [Diagnostic validation](validation_extension.md), `results/validation_extension/synthetic_*` |
| T1 | Does prediction transfer over time? | Beans 2015 to 2016; ATP 2010–2019 chronological seasons | Bounded/shrunk SM and ridge PL; scalable/insertion centers for ATP | [Temporal design](temporal_prediction.md); snapshot transfer/tennis tables |
| C1 | Could optimization or different fitted orders explain a comparison? | Beans/Sushi objective benchmarks, common-order constraints, Sushi B objective bounds, ATP common-order fit | Explicitly constrained or benchmark methods | [Structural controls](structural_controls.md); snapshot benchmark, same-order and pilot tables |
| A1 | Which sources and claims are supported by the observation design? | Tricot catalogue, Beaches, SP-Rank, fixed-display screens; source and prediction replays | No fitted model for excluded/audit-only tasks | [Source screening](../data/screening.md), [validity checks](scientific_audit.md) |

Sushi A/B, PatrasIQ's two tasks, and the four sizes within a dots2024 arm share participants. Reusing them for different questions is valuable but does not create independent studies. A replay of saved predictions is verification, not an extra experimental repetition.

## Training, discovery and confirmation

P0 uses the first 80% of the same unit permutations as development and the final 20% as test. Its first 60% / next 20% division tunes PL inside development; final models refit on all 80%. L0 nests smaller budgets within these development units. Validation never selects between SM and PL. See [P0](predictive_comparison.md) for formulas and uncertainty targets.

In P1/P2, training fits the center, dispersion or worths. Discovery supplies explicitly recorded diagnostics or a model choice. Confirmation evaluates the chosen rule or each prespecified candidate. The methods are not retuned on confirmation. P1 averages the scores of 5 separately fitted models; it does not average their probabilities into an ensemble.

L1/L2 use a different allocation: one outer test set and an inner validation subset of the development data for penalties or dispersion multipliers. Final models use the entire specified development budget N. T1 uses calendar boundaries rather than random outer shuffles. G1 uses two-way train/test splits because it compares prespecified fitting schemes, not validation-selected penalties.

Random shuffling changes membership, never the preference order inside a report. It does not enforce equal demographic, seasonal or geographic proportions unless the design explicitly stratifies those variables. P1/P2 do not impose such balance. G1 stratifies by trial/person for within-group prediction; its whole-group holdout addresses a different target.

## Estimator allocation by empirical dataset

For **P0**, every task fits whole-ranking likelihood-center SM and ridge PL. Exact subset DP covers Beans, Sushi A, Dots/Puzzle, Wheat and Sounds; larger catalogues use integer optimization with explicit certificate/gap reporting. The [main results](../results/main/README.md) cover all 115 paired comparisons.

For **E0**, every empirical task attempts Sharp; Fotakis requires full observed pair coverage. Efficient is independently assessed on every allocation and admitted when lambda<=1, irrespective of Sharp status. Global clipped Borda is fitted on all 23 tasks; depth-zero Efficient equals it under their shared tie rule. Both appear in the same E0 results. **B0** uses fixed R=10 and aliases Sharp where the constructions coincide. [E0 availability](../results/estimator_comparison/README.md) is separate from main-result completeness. L0/S0 retain these methods as labeled supplementary curves. The raw runner stores E0/B0 under the same allocation-family key as P0; [the exact mapping](estimator_comparison.md#reading-name-versus-stored-key) is explicit.

The following table is the **supplementary P1/P2 allocation**, whose byte-locked implementation is retained for replay. Its eight-item restriction does not apply to the E0/L0/S0 Sharp comparisons.

“Attempted” includes a recorded exclusion or failure. An unavailable Sharp or exact fit is not relabeled as another algorithm.

| Dataset family | P1/P2 SM exact center | P1/P2 additional centers | Other experiments and reasons |
|---|---|---|---|
| Beans, n=10 | Subset DP | Sharp sieve unavailable; efficient outside $`\lambda\le1`$; clipped Borda fitted | L1/L2 exact DP is feasible; small-budget efficient/Borda and dispersion/penalty variants probe coverage and tuning; T1 tests year transfer |
| Sushi A, n=10 | Subset DP | Sharp sieve unavailable; efficient outside $`\lambda\le1`$; clipped Borda fitted | L1 uses exact DP; fixed full display isolates sample-size effects without changing item exposure |
| Sushi B, n=100 | Integer formulation, 120-second optimum-certificate requirement | Sharp sieve unavailable; efficient outside $`\lambda\le1`$ at N=3,000; clipped Borda fitted | L1 uses a declared approximate center; L2 uses efficient/Borda and insertion because exact large-catalogue repeated optimization is costly |
| Dots 2013 and Puzzle, n=4 | Subset DP | Sharp can be computed but is outside the sparse theorem regime; efficient excluded; clipped Borda fitted | G1 exact and Fotakis admitted; Sharp/efficient excluded by G1's conservative theorem-domain policy |
| dots2024, n=30 | Certified integer formulation | Sharp sieve unavailable; efficient admitted only for r=2 ($`\lambda\approx0.414`$); clipped Borda fitted | Tasks remain separate by arm and r; no person-local fit is attempted from a single report per task |
| Wheat, n=16 | Subset DP | Sharp sieve unavailable; efficient outside $`\lambda\le1`$; clipped Borda fitted | Unadjusted diagnostics only; missing participant/village identities prevent supported cluster inference |
| Sounds, n=12 | Subset DP | Sharp sieve unavailable; efficient outside $`\lambda\le1`$ for pooled P1/P2; clipped Borda fitted | G1 local budgets can admit efficient as the declared Sharp fallback; exact requires all items seen, Fotakis all pairs seen |
| PatrasIQ cost / population, n=36/48 | Certified integer formulation | Sharp sieve unavailable; efficient outside $`\lambda\le1`$; clipped Borda fitted | Prediction and diagnostics exploit six-item reports and documented one-report-per-person tasks |
| ATP, n varies by season | Not attempted | Efficient/Borda and insertion with bounded/shrunk β | Ridge PL ensures a predictive comparator in sparse seasonal catalogues; common-order controls separate ordering from strength heterogeneity |

Every P1/P2 task also attempts Hunter's unpenalized listwise PL MM fit, subject to finite-MLE and convergence checks. G1 deliberately uses a stricter admission policy than P1/P2. Numeric λ and observed coverage do not verify uniform displayed-set sampling, independence, or the manuscript's sufficient sample-size constants. See [estimator definitions and admission](algorithms.md).

## How to locate any reported number

Follow the experiment's result dictionary, then identify its dataset, estimator, split, training budget, and aggregation unit. Read the finite/available counts before its loss or interval. [Criteria](criteria.md) defines the quantity; [uncertainty](uncertainty.md) defines the error bar. This prevents confusing, for example, one model's test-only bootstrap CI with uncertainty around a five-partition average, or a regularized fit with an unpenalized fit.
