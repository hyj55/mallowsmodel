# Full-data shell and display-context characteristics

[All data characteristics](../README.md) · [Every dataset beside its NLL gap](comparison.md) · [Complete comparison CSV](nll_comparison.csv)

Characteristics 2 and 3 use **every eligible report in each entire task**, before any experimental allocation. They reuse characteristic 1's full-data reference centers: certified Kendall-objective minima for the 23 P1 tasks, explicitly approximate centers for the ten ATP annual tasks. All 18 available objective-reference versions are retained too, giving 51 descriptions of 33 tasks. No model is refitted, no new train/test split is created, and no prediction experiment or model-selection rule is introduced.

Item coding, eligibility, source versions and NLL targets are unchanged. “Same displayed set” means the same unordered set of the task's item IDs. In pooled Dots/Puzzle tasks these are difficulty-category IDs; this does not establish identity of the physical boards/images or eliminate trial mixtures. The calculations do not condition on assessor, season or other metadata. Frequencies and reference orders are derived from the same whole dataset and are descriptive.

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

## Relation to existing prediction gaps

The [complete comparison](comparison.md) includes every task, unavailable-feature reason, existing Δ and incomplete-fit denominator. Δ=NLL(SM)−NLL(PL), positive in favor of PL. P1 uses its original 30 confirmation partitions and exact/certified SM versus unpenalized PL. ATP retains its separate T1 procedure and prediction target. No conditional finite-only mean replaces a missing complete comparison. Different ranking lengths and sampling support prevent a pooled feature correlation from becoming a general prediction law.

Observed examples make these limits concrete:

- Beans has T=0.2347 and nominal uniform reference 0.2458. Its one-item replacement effect is +2.66 percentage points across 420 changed-h contrasts, all with repeated displays. The existing P1 gap is +0.01251, favoring PL despite the positive gap association.
- Puzzle minimum 5 steps has T=0.0968 and reference 0.0645, while its P1 gap is −0.05756, favoring SM. A nonzero empirical departure from shell uniformity does not imply PL must predict better.
- Sushi A has T≈0.99351, but its nominal reference is already ≈0.99335 because ten-item shells contain many possible permutations. Raw TV near one cannot be interpreted without this occupancy information. Its gap is +0.02555; it has no display-context contrast.
- Wheat has a +7.56-point replacement effect across 2,022 changed-h contrasts, but only 70 have both displays repeated. Its P1 gap is +0.14741. Both counts and the population/display mixture qualify interpretation.
- dots2024 B at r=6 has R=−33.33 points over only 30 matched contrasts, none with both displays repeated, yet its all-context slope is +3.01 points per h. Its P1 point gap is −0.01556. The two context summaries target different contrasts, and the matched subset is sparse.
- Sushi B has no repeated nontrivial display/shell cell. Its raw shell distance is completely determined by single-observation occupancy. Broader context variation is computable, but almost all exact displays are singletons, and the P1 NLL comparison is incomplete.

## Tables, detailed frequencies and reproduction

| Artifact | Contents |
|---|---|
| [comparison.md](comparison.md) | Per-task shell and context characteristics beside saved NLLs, availability and figures |
| [nll_comparison.csv](nll_comparison.csv) | All primary metrics, support fields and unchanged prediction comparisons |
| [summary.csv](summary.csv) | All 33 tasks and all 51 full-data/objective-reference descriptions |
| [shells/](shells/) | Per occupied display-ID/shell: report count, possible/observed/zero-count order counts, TV and nominal reference |
| [pairs/](pairs/) | Per pair: context counts, all-context variation, gap slope and endpoint rates/counts |
| [associations.csv](associations.csv) | Descriptive correlations among complete available P1 comparisons; no significance test |
| [manifest.json](manifest.json) | Input, code, output and local-detail hashes; reuse of the existing reference centers |

Exact ranking-frequency tables and pair × exact-display outcome tables can reconstruct source reports, especially for singleton displays. Consistent with [source redistribution terms](../../../THIRD_PARTY_NOTICES.md), those complete counted tables remain local in `results/private/structure_features/<dataset>/`. They include `full_data_rankings.csv.gz`, `full_data_context_cells.csv.gz`, `full_data_displays.csv.gz` and `full_data_swaps.csv.gz`, plus corresponding objective-reference files when available. Missing permutations have zero counts within each occupied shell, encoded by its known shell size; no unobserved order is discarded from TV. The public scripts regenerate all these detailed counts from the pinned sources without fitting a prediction model.

```bash
python download_repeated_data.py
python describe_structure_features.py
python make_structure_feature_summary.py
python validate_structure_features.py --sources
```

The saved full-data centers must be present; they are included with characteristic 1. ATP acquisition and source verification reuse its pinned manifest. Public verification without source acquisition or private details is `python validate_structure_features.py`. Source replay independently reconstructs the ranking and pair/display frequencies and checks every matched replacement. `python validate_pair_features.py` continues to verify characteristic 1 unchanged.
