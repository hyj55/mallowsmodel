# Full-data ranking characteristics

[Data catalogue](../README.md) · [All three features beside every NLL gap](comparison.md) · [Combined CSV](all_features.csv)

The three characteristics below describe **every eligible report in each entire empirical task**. They share the same reference center, source population and observation coding. All are data descriptions; none adds a prediction experiment, a train/test split or a model-selection rule. Existing fits and prediction losses are unchanged.

| Characteristic | What stays fixed | What is compared | Main summaries |
|---|---|---|---|
| [1. Equal-gap pair frequencies](#characteristic-1-equal-gap-pair-frequencies) | Displayed-center gap h | Different pairs' observed win rates | H, and H1 for adjacent pairs |
| [2. Frequencies within a display and shell](#characteristic-2-uniform-frequencies-within-the-same-display-and-shell) | Exact displayed set S and Kendall distance d | Frequencies of all possible orders, including unobserved orders | TV, nominal uniform-sampling reference and occupancy |
| [3. Same pair across displays](#characteristic-3-a-fixed-pair-across-exact-displayed-sets) | Focal pair; additionally all but one other item for matched replacements | Win rates across exact displayed sets and their association with h | Display variation C, slope γ and one-item replacement effect R |

The [comparison page](comparison.md#all-three-characteristics-by-dataset) starts with all three characteristics and NLL side by side for each dataset, followed by detailed support tables. Larger raw dispersion need not mean stronger population heterogeneity: repeated observations, possible-order counts and undefined contrasts are part of the description.

## Population and reference order

The calculation covers all 23 P1 tasks and the ten ATP annual tasks. PrefLib frequencies are expanded exactly as recorded. No report is selected because of its outcome or pair count. Excluded source tasks without SM–PL predictions and synthetic populations are outside this empirical catalogue. For ATP, “entire task” means all completed matches in that year satisfying T1's existing prior-season-catalogue rule, before its January–June / July–December division; it includes the cold-player test matches. The separate T1 main NLL target is narrower and is identified below.

A direction and an h value require a common reference order. For the primary description, use all reports to minimize the total Kendall objective. The saved centers for **all 23 P1 tasks are certified optima**: subset DP for n≤18 and integer optimization for larger catalogues. ATP's 418–469-item catalogues use a deterministic two-start insertion approximation, explicitly marked uncertified. The two initial orders sort aggregate win rate and aggregate win-minus-loss counts; every subsequent insertion strictly reduces the Kendall objective. Catalogue items remain present, including zero-exposure ATP items. Deterministic tie handling does not imply a unique optimum.

This computes a reference center for description, not a new predictive fit: it does not estimate full-data PL worths, tune a dispersion, or score a held-out ranking. Reference orders, objective values, solver certificates and report hashes are saved in [centers.json](centers.json). They are data-dependent, so this is not an independent model check.

Dots/Puzzle, dots2024 and PatrasIQ additionally retain their source objective order as `reference=objective`. Both references use the entire task. The primary comparison uses `reference=full_data` consistently across datasets; the objective version is available in the pair tables, [by_gap.csv](by_gap.csv) and [summary.csv](summary.csv). An objective difficulty order is not assumed to be a known population preference center.

Across the three characteristics, all 18 available objective-reference versions are retained, giving 51 descriptions of 33 tasks. “Same displayed set” means the same unordered set of the task's item IDs. In pooled Dots/Puzzle tasks these are difficulty-category IDs; this does not establish identity of the physical boards/images or eliminate trial mixtures. The calculations do not condition on assessor, season or other metadata. Frequencies and reference orders come from the same whole dataset.

## Characteristic 1: equal-gap pair frequencies

### Exact frequencies and displayed-center gap

Let the declared reference order be π. In report t, restrict π to the displayed set S_t. Orient each pair (i,j) so that i precedes j in π, and define

```math
h_t(i,j)=\operatorname{pos}_{\pi|_{S_t}}(j)-\operatorname{pos}_{\pi|_{S_t}}(i).
```

Adjacent items have h=1; h−1 is the number of displayed items between them. This is neither their distance in the full catalogue nor their distance in the noisy reported order. If a pair occurs at different h values in different displays, it contributes to separate cells.

For every observed pair × h cell, save

```math
m_{ijh}=\sum_t\mathbf{1}\{i,j\in S_t,\ h_t(i,j)=h\},\qquad
w_{ijh}=\sum_t\mathbf{1}\{i,j\in S_t,\ h_t(i,j)=h,\ i\prec_{Y_t}j\},\qquad
\widehat p_{ijh}=w_{ijh}/m_{ijh}.
```

Every full report contributes all its unordered pairs. The pair direction is never flipped to make its observed win rate exceed 50%. Cells with zero occurrences are absent, not assigned zero wins or probability one half. Item IDs are zero-based catalogue codes from the original task loaders; ATP's index-to-player-ID mapping is in [manifest.json](manifest.json). Counts aggregate reports without publishing respondent records.

The [selective-Mallows definition](https://proceedings.mlr.press/v130/fotakis21a/fotakis21a.pdf) implies a common pair probability at a given displayed-center gap for a single center and dispersion. For h=1 this probability is logistic(β); larger h values have their own probabilities. Accordingly, **different h values are never treated as having the same expected win rate**. Agreement of these empirical frequencies is a necessary structural pattern, not sufficient evidence for an SM generating law. Unequal frequencies alone do not verify PL's additive-log-odds constraints either.

### Scalar summary, with the h-specific results preserved

Let K_h be the number of observed pairs at gap h and M_h the sum of their counts. The occurrence-weighted mean rate and cross-pair standard deviation are

```math
\overline p_h=\frac{\sum_{ij}w_{ijh}}{M_h},\qquad
\sigma_h=\sqrt{\frac{\sum_{ij}m_{ijh}(\widehat p_{ijh}-\overline p_h)^2}{M_h}}.
```

The main whole-dataset feature is

```math
H=\sqrt{\frac{\sum_{h:K_h\ge2}M_h\sigma_h^2}{\sum_{h:K_h\ge2}M_h}}.
```

Differences are computed **within each exact h first**, then their variances are averaged. A larger H means more dispersed *observed* pair frequencies at equal h. H1 is σ_1. The comparison table reports 100H and 100H1 in percentage points. For example, H=0.07 is a seven-percentage-point RMS deviation from the relevant h-specific mean; it is not a seven-percent ranking error rate.

Each pair × h frequency is weighted by its occurrence count. The supplementary `equal_pair_sd` gives every observed pair equal weight within an h. A stratum with only one pair cannot compare different pairs: its dispersion is `NA`, and its occurrences are not used in H. Its count and rate remain published. For a full four-item display, h=3 has one pair and therefore cannot establish common pair reliability. `comparable_occurrence_share` reports how much of the data supports a cross-pair comparison.

### Sampling support and interpretation

H describes the observed frequencies; it is **not a noise-corrected estimate of population heterogeneity**. A pair seen once has frequency zero or one, even if every underlying pair probability were identical. The tables therefore also retain minimum/median/maximum cell counts, singleton counts and the share of occurrences in cells with at least five reports. The five-report field is only a coverage description: no such threshold filters the feature calculation.

No binomial independence assumption, confidence interval, bootstrap or p-value is added. Pairs from one ranking share an outcome, and some sources have repeated or unidentified assessors. Full-data center estimation adds another dependence on the observations. Seasons, respondent mixtures and physical-stimulus coding can also contribute to the observed pattern. These are whole-task summaries, not metadata-adjusted features.

## Characteristic 2: uniform frequencies within the same display and shell

Fix a displayed set S and the reference center restricted to it. Let d be Kendall distance to that restricted center. The [SM probability law](https://proceedings.mlr.press/v130/fotakis21a/fotakis21a.pdf) assigns equal probability to every ordering of S at the same d. The relevant empirical comparison therefore fixes **both S and d**, not merely d across different displays.

For each observed ordering y, calculate its original frequency $`c_{S,y}`$. Let $`m_{S,d}`$ be the total reports in that exact display/shell, and $`a_r(d)`$ the number of *possible* orderings in it. The conditional empirical frequencies are

```math
\widehat f_{S,d}(y)=\frac{c_{S,y}}{m_{S,d}},\qquad
a_r(d)=[z^d]\prod_{k=1}^{r}(1+z+\cdots+z^{k-1}).
```

The full observed ranking table retains c, c divided by all reports on S, and c divided by m. A possible but unobserved ordering has c=0. These zeros are counted exactly through the shell size and observed-order count, rather than materializing millions of permutations for every ten-item display. An entirely unobserved shell has m=0 and no empirical conditional frequency. A shell with a=1 imposes no equality between different orders and is marked noncomparable.

The descriptive total-variation distance from equal frequencies is

```math
T_{S,d}=\frac12\sum_{y:d_K(y,\pi|_S)=d}
\left|\widehat f_{S,d}(y)-\frac1{a_r(d)}\right|.
```

It is computed from actual observed ranking counts, including the contribution of all zero-count orders. T=0 means exact empirical equality; a larger value means greater empirical departure. For example, BAC and ACB counts 1 and 9 in the same three-item d=1 shell give T=0.4. The task summary is the observation-weighted average of T over occupied shells with a>1. All reports are counted, including reports in noncomparable shells; the latter's share is recorded and is not treated as evidence of uniformity.

This is **not** the saved-fit NLL shell decomposition: no PL likelihood, symmetrized PL distribution or fitted shell probability enters these frequency calculations.

### Sampling support and nominal uniform reference

A single observation in an a-order shell necessarily gives T=1−1/a. This can be near one even under perfectly uniform probabilities. To show that sampling scale, retain the following exact reference for m independent uniform draws in a **fixed** shell:

```math
b(m,a)=\frac{a}{2}\mathbb E\left|\frac Xm-\frac1a\right|,
\quad X\sim\operatorname{Binomial}(m,1/a).
```

For a>1, the code evaluates the equivalent finite expression

```math
b(m,a)=\left(1-\frac1a\right)
\Pr\!\left\{\operatorname{Binomial}(m-1,1/a)=\left\lfloor m/a\right\rfloor\right\}.
```

The comparison shows observed T, b, and T−b, with the same observation weights. It also shows the shell observation count, m/a, and the share of observations in shells repeated at least twice. In particular, many observations per shell need not mean enough observations per possible ranking when r is large.

**T−b is not a calibrated test or an unbiased estimate of population distance.** The reference assumes a fixed order and independent uniform draws; estimated centers, repeated assessors and mixtures violate or complicate those conditions. Negative differences are retained. No simulated experiment, confidence interval, bootstrap or p-value is attached. A difference from this reference alone is not a claim that the empirical departure exceeds sampling uncertainty.

## Characteristic 3: a fixed pair across exact displayed sets

Orient pair (i,j) by the same declared reference center. For every exact display S containing it, retain count $`m_{ijS}`$, agreement count $`w_{ijS}`$, rate $`\widehat p_{ijS}=w_{ijS}/m_{ijS}`$, and gap $`h_{ijS}`$ in the reference restricted to S. The gap is the difference between their positions in that restricted order: adjacent items have h=1, and one intervening displayed item gives h=2. Distinct displays are not initially collapsed into h bins. Different pairs' baseline probabilities are never pooled before computing variation.

For a pair appearing in at least two distinct displays, let its count-weighted mean rate be $`\overline p_{ij}`$. The full-task unsigned display-variation feature is

```math
C=\sqrt{\frac{\sum_{ij:K_{ij}\ge2}\sum_S
m_{ijS}(\widehat p_{ijS}-\overline p_{ij})^2}
{\sum_{ij:K_{ij}\ge2}\sum_Sm_{ijS}}}.
```

Here $`K_{ij}`$ counts exact displayed sets, not repeat reports. Report 100C in percentage points. C includes all eligible pair occurrences, even contexts observed just once; their sampling support is explicitly recorded. The supplementary variance decomposition separates the between-h component from the residual variation between displays sharing the **same pair and same h**. Their squared components add exactly to C² on the same set of eligible pairs. A zero between-h component caused by no changing h is not a successful test of context invariance.

### Direction of the gap effect

To retain the direction in the proposed SM example, compute a within-pair slope using all available pair/display cells:

```math
\gamma=\frac{\sum_{ij,S}m_{ijS}(h_{ijS}-\overline h_{ij})
(\widehat p_{ijS}-\overline p_{ij})}
{\sum_{ij,S}m_{ijS}(h_{ijS}-\overline h_{ij})^2}.
```

Pair means use that pair's occurrence counts. The slope is defined only if the denominator is positive. A positive value means higher displayed-center gaps are associated with greater observed agreement; a negative value means the reverse. Per-pair tables also retain minimum/maximum h, both endpoint counts and rates, and their difference. There is no outcome-dependent eligibility filter or minimum-count cutoff in the primary calculation.

### Exactly one other item replaced

The closest match to the A,C example compares two displays with the same r, the same focal pair, and the same other r−3 items. They differ by one removed and one added **nonfocal** item. Every such contrast is enumerated from the complete observed display catalogue.

If this replacement changes h, its magnitude is exactly one. Orient that contrast from lower h to higher h and calculate

```math
\delta_e=\widehat p_{ijS_{\rm high}}-\widehat p_{ijS_{\rm low}},\qquad
w_e=\frac{m_{ijS_{\rm high}}m_{ijS_{\rm low}}}
{m_{ijS_{\rm high}}+m_{ijS_{\rm low}}},\qquad
R=\frac{\sum_e w_e\delta_e}{\sum_e w_e}.
```

The weight balances the two context counts and is fixed by observation counts, not outcome or NLL. It does not assert independence of contrasts. With r=3 this directly compares replacing the third item; with r>3 it holds all remaining items fixed. Replacements that leave h unchanged are retained separately through their weighted absolute rate change.

The table reports 100R in percentage points, how many changed-h contrasts exist, and how many have both displays repeated at least twice. A supplementary R restricted to that repeated-display subset is recorded in the CSV with its distinct denominator. It is a support description derived from the same full dataset, not a new train/test analysis. Contrasts reuse reports and pairs; their count is not an independent sample size.

The exact supplied SM example has R=16/21−2/3=2/21, about 9.52 percentage points. A PL population with one worth vector has zero same-pair contrast across displays. These identities are checked by exhaustive unit-test frequency tables, not added as empirical experiments.

### What these context characteristics can establish

Positive γ or R is consistent with the direction of an SM gap effect, but does not establish a selective-Mallows generating mechanism. Center error and assessor/display, season/display or other mixture associations can produce apparent effects. Stable observed rates are compatible with PL and with SM in cases where changing the display does not materially change its pair probabilities. C, γ and R are different descriptions: C measures any exact-display variation, γ summarizes its association with h across all contexts, and R uses only matched one-item replacements. They can therefore have different signs or availability.

Fixed full displays, including Sushi A and each pooled PrefLib condition, provide no same-pair display contrast. For r=2, a pair itself fixes the entire display. Those entries are NA, not measured zeros. PatrasIQ and Sushi B can have broader pair/display contrasts without any observed one-item replacement that changes h; their R is then NA while C and γ remain available.

## Matching to existing NLL results

For each of the 23 P1 tasks, join its feature to `split=confirmation, method=mle` in [the existing scores](../../results/repeated_holdout/scores.csv). Δ is the original 30-partition mean of NLL(SM)−NLL(PL), with exact/certified-center SM and unpenalized PL. Positive favors PL. The feature is calculated once from the whole task, not averaged over the training/test partitions.

Sushi B, dots2024 A/B at r=2, and PatrasIQ population have incomplete paired predictions. Their full Δ remains missing. Separate columns retain the finite-repetition count and its conditional mean; those conditional means are not substituted into the scatterplot or correlations. Existing partition MCSE is copied to the CSV with its original meaning and is not a population CI for this feature–loss relationship.

ATP rows use the corresponding year's saved `target=seen, method=efficient_shrunk` gap against ridge PL. These are July–December matches whose players appeared in January–June. The full-year feature also includes the training half and the cold-player test reports, so its population is broader. [The copied input table](tennis_nll_source.csv) is byte-identical to the [recorded T1 table](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure/tennis_by_year.csv). T1 points are displayed separately from P1.

The main comparison keeps whole-ranking NLL in nats/report. Since ranking lengths differ, absolute Δ magnitudes are not directly comparable measures of model advantage across all datasets. `delta_per_pair_scale` additionally divides that whole-ranking difference by r(r−1)/2; it is merely a rescaling, not a newly calculated pairwise loss.

[Equal-gap descriptive correlations](associations.csv) use only complete NLL comparisons, retain separate within-r and ATP summaries, and have no inferential p-values. The pooled association across 19 complete P1 tasks is positive (Pearson 0.693), but the eight r=4 tasks have Pearson 0.028, and the three complete r=6 tasks have −0.983. These small, related task collections do not establish a general feature-to-performance law.

## Reading all three characteristics with NLL

The three characteristics describe different structural constraints; they are not interchangeable measures or votes for a model family. Use the [joint dataset table](comparison.md) and its support counts together.

- Dots 2013 has H≈1.00–1.96 percentage points and Puzzle H≈1.92–3.34, with about 800 observations per pair. All eight complete P1 gaps favor SM. Their coded display is fixed, so characteristic 3 is unavailable. Puzzle minimum 5 steps has shell TV .09677 versus nominal reference .06450 and Δ=−.05756: an empirical shell departure does not require PL to win.
- Sushi A has H=7.36 points with 5,000 observations per pair and Δ=+.02555. Its shell TV .99351 is close to the nominal sampling reference .99335 because the possible-order space is large; raw TV near one alone is uninformative about model violation. Its display is fixed, so characteristic 3 is unavailable.
- Beans has shell TV .23473 versus nominal reference .24580 and a +2.66-point matched replacement effect over 420 contrasts, all with at least two observations in both displays. The positive association with h coexists with Δ=+.01251 favoring PL.
- Wheat has R=+7.56 points and Δ=+.14741. Only 70 of its 2,022 contrasts have both displays observed at least twice. Its support and population/display mixture limit interpretation.
- PatrasIQ cost has H=16.45 points and the largest complete P1 PL advantage, Δ=+.27794, but median pair × h count is only five. It has broader pair/display comparisons, yet no single-item replacement contrast that changes h.
- dots2024 has median pair × h counts of only one to three. B at r=6 has H=23.36 points and Δ=−.01556 favoring SM. Its R=−33.33 points comes from 30 contrasts with no repeated observations in both displays, while its broader slope is +3.01 points per h. These summaries use different contrasts and cannot be reduced to one universal winner rule.
- Sushi B has no repeated nontrivial display/shell cell: its raw TV is determined by single-observation occupancy. Most exact displays are singletons, and its complete NLL comparison is unavailable.
- ATP has median pair counts of one, approximate centers and a different temporal prediction target. Its r=2 reports provide no nontrivial shell or same-pair display contrast. Large H cannot be compared with densely repeated preference pairs as if the sampling support were equal.

## Files and reproduction

All three characteristics have one methods page (this page) and one [comparison page](comparison.md). The `structure/` subdirectory stores the shell and context tables; it is a data-storage grouping, not a separate report to read.

| File | Contents |
|---|---|
| [comparison.md](comparison.md) | All three features and NLL together for every task; detailed support tables and figures |
| [all_features.csv](all_features.csv) | Joined columns for all three characteristics, support, NLL targets and availability; one primary row per task |
| [nll_comparison.csv](nll_comparison.csv), [structure/nll_comparison.csv](structure/nll_comparison.csv) | Saved source summaries used to build the combined table |
| [summary.csv](summary.csv), [structure/summary.csv](structure/summary.csv) | Full-data and objective-reference descriptions |
| [by_gap.csv](by_gap.csv) | Every h: mean pair rate, occurrence-weighted/equal-pair SD, support and comparability |
| [pairs/](pairs/), [pair_rates.csv.gz](pair_rates.csv.gz) | Characteristic 1's oriented pair × h wins, losses, counts and rates; plain per-task CSVs and combined compressed file |
| [structure/shells/](structure/shells/) | Occupied display-ID/shell counts, possible/observed/zero-count orders, TV and nominal reference |
| [structure/pairs/](structure/pairs/) | Per-pair context counts, variation, gap slope and endpoint rates/counts |
| [centers.json](centers.json) | Complete reference orders, objective values, certificates and report hashes |
| [associations.csv](associations.csv), [structure/associations.csv](structure/associations.csv) | Descriptive feature–NLL correlations; no significance tests |
| [manifest.json](manifest.json), [structure/manifest.json](structure/manifest.json) | Source/code/output hashes, catalogue mappings, scope and local-detail hashes |
| [tennis_sources.json](tennis_sources.json) | Pinned ATP annual-source checksums and attribution |

Exact ranking-frequency tables and pair × exact-display outcome tables can reconstruct source reports, especially for singleton displays. Consistent with [source redistribution terms](../../THIRD_PARTY_NOTICES.md), these complete counted tables remain local in `results/private/structure_features/<dataset>/`: `full_data_rankings.csv.gz`, `full_data_context_cells.csv.gz`, `full_data_displays.csv.gz` and `full_data_swaps.csv.gz`, plus corresponding objective-reference files. Missing permutations have zero counts within each occupied shell, encoded by its shell size; none is discarded from TV. Public scripts regenerate these tables from the pinned sources.

To rebuild the combined comparison from the saved feature tables, without reprocessing observations or fitting models:

```bash
python make_feature_summary.py
python validate_pair_features.py
python validate_structure_features.py
```

To reconstruct all three characteristics from the original reports:

```bash
python download_repeated_data.py
python describe_pair_features.py
python describe_structure_features.py
python make_feature_summary.py
python validate_pair_features.py --sources
python validate_structure_features.py --sources
```

The descriptors verify source hashes and replay saved reference centers. Missing ATP annual files are downloaded from their pinned source and verified. `describe_pair_features.py --refresh-centers` explicitly recomputes centers; integer certification can depend on the 120-second budget. The default preserves the published references. Source validation independently reconstructs every pair × h cell, exact ranking and pair/display count and checks matched replacements. Neither procedure reruns P1 or T1 prediction. The previous summary command names remain compatibility entry points to the same combined report.
