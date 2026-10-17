# E0: supplementary center-estimator comparison

[E0 results](../results/estimator_comparison/README.md) · [P0 main experiment](predictive_comparison.md) · [Global sieve B0](sieve_computation.md) · [Experiment map](experiments.md)

E0 asks how replacing the SM center-estimation procedure changes prediction on the same 23 empirical tasks. It compares Sharp, Fotakis, independently admitted Efficient and global clipped Borda, with the saved likelihood-center SM and PL fits in the same result tables. **P0 alone is the main Algorithm 4.1 experiment.** No E0 estimator is selected by outer-test performance to replace P0's center.

## Shared observations and separate estimators

Every candidate uses P0's five grouped 80/20 outer allocations and the same development/test reports. PL's penalty is selected inside development and its saved final fit is reused. Each SM center fits dispersion by whole-ranking likelihood on the same complete development sample, bounded to [0,10]. Neither Efficient nor Borda adds validation tuning, removes unseen items, rerolls a split or conditions admission on Sharp's success.

| Method in the unified E0 table | Construction and reference | Admission and role |
|---|---|---|
| PL | Training-only tuned positive ridge; **M**, Proposition 4.3 | Saved P0 reference, all 115 allocations |
| Likelihood-center SM | Whole-ranking Kendall objective, DP/integer optimization; **M**, Proposition 4.1 | Saved P0 reference; retains exact/approximate status |
| Sharp | **M**, Algorithm 2.1 and Lemma 2.11 | A=256 and W_star unchanged; no eight-item guard; only a complete exact construction is accepted |
| Fotakis / PosEst | Fotakis et al. (2021), Algorithm 1 | Every unordered pair must appear in development data, checked in each allocation |
| Efficient | **M**, Algorithms 3.1/3.2, pp. 19 and 24–25; equation (3.23) | Independently assessed on every allocation; schedule requires lambda<=1. Depth and reason for exclusion are explicit |
| Global clipped Borda | **M**, Proposition 2.14, p. 15, and equation (3.4), pp. 19–20 | Fitted on all 115 allocations, including outside Efficient's schedule domain; same tie rule as Efficient |

[References](references.md#supplied-manuscript-m) identify the manuscript version and [the estimator inventory](algorithms.md#estimator-inventory-and-references) gives source/implementation locators. Numerical admission, computational completion and theoretical guarantees are separate: observed lambda does not verify independent reports, uniform displays, a true SM population or all sufficient constants.

## What global Borda computes

Let K_i count development reports displaying item i. For a strict report of size r, let rank_t(i) be its one-based position, with the preferred item first. Its full-catalogue score is

```math
K_i=\sum_{t=1}^{N}\mathbf{1}\{i\in S_t\},\qquad
s_i=\operatorname{clip}_{[-n,n]}\!\left[
\frac{n-1}{(r-1)K_i}
\sum_{t:i\in S_t}\bigl(r+1-2\operatorname{rank}_t(i)\bigr)
\right].
```

For K_i=0 use s_i=0. Sort descending; exact score ties use one fixed seeded label-priority array (seed 93847), shared with Efficient. No source objective order is used. This is appearance-normalized scoring: frequently displayed items do not gain merely from appearing in more reports. It is not an unnormalized sum of pair wins. Fit the common bounded dispersion on all development rankings after obtaining the center.

## Efficient admission and depth-zero identity

Equation (3.23) defines the schedule for

```math
\frac{r-1}{n-1}\le\eta\le\lambda
=\frac{Nr(r-1)}{n(n-1)}\le1.
```

The fixed schedule inputs are beta_0=0.1 and A=256. Efficient has no Sharp-failure gate in E0. The current full-budget allocations satisfy lambda<=1 only for dots2024 A r2 and B r2 (lambda=480/870, five fits each). The remaining 21 tasks have 105 `outside_schedule_domain` records. Their depth is unavailable, not zero; Borda is still fitted and compared normally. The procedure does not cap lambda at one, thin reports, or silently extend the hierarchy beyond the stated schedule domain.

All E0 catalogues have n<=100. For an admitted resolution, eta*n<=100<256=A, so the root already satisfies the stopping condition and T=0. Algorithm 3.2 still score-sorts its terminal block using all remaining reports; with no pilot stage consumed, that is the full catalogue and all development reports. It therefore equals global clipped Borda under the common tie rule. This identity is checked for order, training distance, dispersion, every test loss and conditional bootstrap endpoints. Efficient is labeled as an alias of Borda in these ten records; retaining both columns does not create independent evidence.

The same E0 implementation also keeps a separately fitted global Borda comparator if an admitted Efficient run has T>0. No current E0 result has positive depth. A difference in an unrelated experiment's tie seed can change tied Borda orders; equal algorithm names alone do not prove byte-identical fits across experiments.

## Evaluation and uncertainty

For each available estimator a and allocation b, compute whole-ranking test NLL L_ab on the unchanged displayed sets. The ordinary summary records Delta_ab=L_ab−L_PL,b. The Borda contrast table instead records d_ab=L_Borda,b−L_ab. Negative d favors Borda. For five complete paired allocations:

```math
\overline d_a=\frac15\sum_{b=1}^{5}d_{ab},\qquad
\widehat{\mathrm{MCSE}}(\overline d_a)
=\frac{\operatorname{sd}(d_{a1},\ldots,d_{a5})}{\sqrt5}.
```

Pairing is retained before calculating the variance; the two estimators' separate standard errors are not combined as independent quantities. This MCSE measures integration over randomly selected allocations of fixed observations. It is not a population CI. Complete means/MCSEs require all five planned fits. Available-subset means and their denominators are separately labeled; no partial fit is imputed. Split minima/maxima are descriptive.

Supported per-split CIs use the same 2,000 paired test-unit bootstrap draws as P0. Resampling whole identified units retains their within-unit reports and cross-model pairing. Percentiles 2.5/97.5 condition on the fitted predictors and independent-unit sampling; they omit training and tuning uncertainty. Beans, Wheat and anonymous PrefLib tasks have no supported sampling CI. Bootstrap endpoints are not averaged across allocations. The Borda contrast table uses partition MCSE, not bootstrap CI. See [uncertainty](uncertainty.md).

Test NLL does not estimate true-center minimax risk on real data. [S0](predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10) supplies separately named known-generator curves.

## Global-sieve identity and missing fits

All recorded E0 Sharp schedules have zero pilot depth and a single terminal block covering the catalogue. Their terminal operation is a pair-sieve, unlike Efficient's score sorting. With identical selected-pair seeds, these Sharp results equal **B0 global pair-sieve**. B0 aliases them; global pair-sieve and global Borda are different estimators.

Sharp is available for 55 E0 contexts: eleven tasks, each 5/5. The other 60 cover Wheat, Sushi B, both PatrasIQ tasks and the eight dots2024 arm/size tasks. Together with 15 L0 and 80 S0 failures, these are 155 outstanding Sharp computations. P0's 115 paired predictions remain available. [Resource details](sieve_computation.md#completion-results-and-remaining-limits).

## Result files and implementation mapping

The complete E0 output lives in [results/estimator_comparison](../results/estimator_comparison/README.md), including one six-method NLL table, paired Borda contrasts, statuses/depths, fitted parameters and uncertainty. These are parts of E0, not a separate added experiment.

| Artifact or method key | Role |
|---|---|
| `results/estimator_comparison/summary.csv` | Named E0 summary: six methods × 23 tasks; PL/likelihood SM remain references |
| `results/estimator_comparison/repeat_scores.csv.gz` | All 690 allocation/method rows, including explicit unavailable Efficient fits |
| `sm_efficient` / `sm_global_borda` | E0 score candidates, fitted by `run_estimator_comparison.py`; core construction in `src/estimator_comparison.py` |
| `results/predictive/` raw `study=P0` | Shared allocation source for P0/E0/B0; not itself a main-only selection |
| Raw `pl`, `sm_likelihood`, `sm_sharp`, `sm_fotakis` | Saved parameters and scores reused unchanged in E0 |
| Raw `sm_efficient_fallback` | Conditional execution key in the shared P0/L0/S0 source export; not E0's complete admission table. Its ten successful empirical fits replay exactly as `sm_efficient` |
| Raw `sm_global_sieve` | B0 alias, not Borda |

Source-array hashes verify the same development and test reports. Fitting and report manifests record their respective input/output hashes. [Reproduction](reproducibility.md#reproduce-the-e0-estimator-comparison) distinguishes fitting the score candidates from rebuilding the saved tables.
