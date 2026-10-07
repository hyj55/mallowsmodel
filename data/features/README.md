# Equal-gap pair frequencies in the full datasets

[Data catalogue](../README.md) · [Every dataset beside its NLL gap](comparison.md) · [Machine-readable comparison](nll_comparison.csv) · [Every gap](by_gap.csv)

This is a **descriptive data characteristic**, calculated on every eligible report in each entire empirical task. It asks whether different pairs have similar observed win rates when their items have the same separation in the displayed-set reference order. It is not a new experiment, train/test split, significance test, or model-selection rule. Existing predictive fits and NLL results are unchanged.

## Population and reference order

The calculation covers all 23 P1 tasks and the ten ATP annual tasks. PrefLib frequencies are expanded exactly as recorded. No report is selected because of its outcome or pair count. Excluded source tasks without SM–PL predictions and synthetic populations are outside this empirical catalogue. For ATP, “entire task” means all completed matches in that year satisfying T1's existing prior-season-catalogue rule, before its January–June / July–December division; it includes the cold-player test matches. The separate T1 main NLL target is narrower and is identified below.

A direction and an h value require a common reference order. For the primary description, use all reports to minimize the total Kendall objective. The saved centers for **all 23 P1 tasks are certified optima**: subset DP for n≤18 and integer optimization for larger catalogues. ATP's 418–469-item catalogues use a deterministic two-start insertion approximation, explicitly marked uncertified. The two initial orders sort aggregate win rate and aggregate win-minus-loss counts; every subsequent insertion strictly reduces the Kendall objective. Catalogue items remain present, including zero-exposure ATP items. Deterministic tie handling does not imply a unique optimum.

This computes a reference center for description, not a new predictive fit: it does not estimate full-data PL worths, tune a dispersion, or score a held-out ranking. Reference orders, objective values, solver certificates and report hashes are saved in [centers.json](centers.json). They are data-dependent, so this is not an independent model check.

Dots/Puzzle, dots2024 and PatrasIQ additionally retain their source objective order as `reference=objective`. Both references use the entire task. The primary comparison uses `reference=full_data` consistently across datasets; the objective version is available in the pair tables, [by_gap.csv](by_gap.csv) and [summary.csv](summary.csv). An objective difficulty order is not assumed to be a known population preference center.

## Exact pair frequencies at equal h

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

## Scalar summary, with the h-specific results preserved

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

## Sampling support and interpretation

H describes the observed frequencies; it is **not a noise-corrected estimate of population heterogeneity**. A pair seen once has frequency zero or one, even if every underlying pair probability were identical. The tables therefore also retain minimum/median/maximum cell counts, singleton counts and the share of occurrences in cells with at least five reports. The five-report field is only a coverage description: no such threshold filters the feature calculation.

No binomial independence assumption, confidence interval, bootstrap or p-value is added. Pairs from one ranking share an outcome, and some sources have repeated or unidentified assessors. Full-data center estimation adds another dependence on the observations. Seasons, respondent mixtures and physical-stimulus coding can also contribute to the observed pattern. These are whole-task summaries, not metadata-adjusted features.

The principal contrast is informative but qualified:

- Dots 2013 has H≈1.00–1.96 percentage points and Puzzle H≈1.92–3.34. Each pair has about 800 observations at its relevant h. All eight P1 mean gaps favor SM.
- Sushi A has H≈7.36 with 5,000 observations per pair, and P1 favors PL by +0.02555 nats/report. Its adjacent-pair H1 is 8.07 points. This is a well-supported descriptive departure from equal observed pair frequencies at equal h; it does not by itself identify a generating family.
- PatrasIQ cost has H≈16.45 and the largest complete P1 PL advantage, +0.27794. Median pair × h support is only five observations, so H combines frequency heterogeneity with appreciable sampling variation.
- dots2024 has large raw H values but median cell counts of only one to three. dots2024 B at r=6 has H≈23.36 yet a slightly SM-favorable P1 point gap, −0.01556. A large raw H is not a universal predictor of the winner.
- ATP has median pair counts of one, approximate centers, a different prediction procedure and a temporal target. Its large raw dispersions cannot be ranked against densely repeated preference pairs as if they measured population heterogeneity on equal footing.

## Matching to existing NLL results

For each of the 23 P1 tasks, join its feature to `split=confirmation, method=mle` in [the existing scores](../../results/repeated_holdout/scores.csv). Δ is the original 30-partition mean of NLL(SM)−NLL(PL), with exact/certified-center SM and unpenalized PL. Positive favors PL. The feature is calculated once from the whole task, not averaged over the training/test partitions.

Sushi B, dots2024 A/B at r=2, and PatrasIQ population have incomplete paired predictions. Their full Δ remains missing. Separate columns retain the finite-repetition count and its conditional mean; those conditional means are not substituted into the scatterplot or correlations. Existing partition MCSE is copied to the CSV with its original meaning and is not a population CI for this feature–loss relationship.

ATP rows use the corresponding year's saved `target=seen, method=efficient_shrunk` gap against ridge PL. These are July–December matches whose players appeared in January–June. The full-year feature also includes the training half and the cold-player test reports, so its population is broader. [The copied input table](tennis_nll_source.csv) is byte-identical to the [recorded T1 table](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/results/exposure/tennis_by_year.csv). T1 points are displayed separately from P1.

The main comparison keeps whole-ranking NLL in nats/report. Since ranking lengths differ, absolute Δ magnitudes are not directly comparable measures of model advantage across all datasets. `delta_per_pair_scale` additionally divides that whole-ranking difference by r(r−1)/2; it is merely a rescaling, not a newly calculated pairwise loss.

[Descriptive correlations](associations.csv) use only complete NLL comparisons, retain separate within-r and ATP summaries, and have no inferential p-values. The pooled association across 19 complete P1 tasks is positive (Pearson 0.693), but the eight r=4 tasks have Pearson 0.028, and the three complete r=6 tasks have −0.983. These small, related task collections do not establish a general feature-to-performance law.

## Files and reproduction

| File | Contents |
|---|---|
| [comparison.md](comparison.md) | Readable table for all 33 tasks, links to individual pair counts, and scatterplot |
| [nll_comparison.csv](nll_comparison.csv) | One primary feature row per task, existing NLLs, availability and support |
| [summary.csv](summary.csv) | Whole-task H, H1 and support, for full-data and available objective references |
| [by_gap.csv](by_gap.csv) | Every h separately: mean rate, occurrence-weighted/equal-pair SD, support and comparability |
| [pairs/](pairs/) | Plain CSV per task: reference, h, oriented item IDs, wins, losses, counts and rates |
| [pair_rates.csv.gz](pair_rates.csv.gz) | The same pair tables combined and losslessly compressed |
| [centers.json](centers.json) | Complete reference permutations, objectives, certification and report hashes |
| [associations.csv](associations.csv) | Descriptive correlations; no significance tests |
| [manifest.json](manifest.json) | Source/code/output hashes, catalogue mappings, exclusions and scope |
| [tennis_sources.json](tennis_sources.json) | Existing pinned ATP annual-source checksums and attribution |

After acquiring the study's sources with `python download_repeated_data.py`:

```bash
python describe_pair_features.py
python make_pair_feature_summary.py
python validate_pair_features.py --sources
```

The first command verifies source hashes and replays saved full-data centers; missing ATP annual files are downloaded from their pinned source and verified. `--refresh-centers` explicitly recomputes reference centers; exact-integer certification can depend on the 120-second runtime budget. The default preserves the published reference choices. `python validate_pair_features.py` checks public artifacts without downloading sources; `--sources` additionally reconstructs every cell through an independent report-by-report counter. No command above reruns P1 or T1 prediction.
