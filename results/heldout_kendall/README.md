# Held-out report Kendall distance alongside NLL

[Experiment map](../../docs/experiments.md) · [All summaries](summary.csv) · [Every allocation](allocation_scores.csv.gz) · [Beta audit](beta_summary.csv) · [Dispersion assumptions](../../docs/dispersion_assumptions.md)

For each fitted catalogue order, restrict it to the items shown in each test report, count discordant pairs, sum across reports, and **divide by the number of test reports**. Do not divide an already averaged loss again. Report size r is retained because the range is 0 to r(r-1)/2. No further pair-count normalization is applied.

```math
L_{K,\mathrm{test}}(\widehat\pi)
=\frac{1}{N_{\mathrm{test}}}\sum_{t\in\mathrm{test}}
d_K(Y_t,\widehat\pi|_{S_t}).
```

This measures agreement with noisy held-out reports. It is not d_K(pi_hat, pi_true), nor a distance to an order fitted on the test set. It needs no beta and does not change if a predictor's dispersion changes while its center stays fixed. SM uses its saved center; PL uses its saved descending-worth order and original tie rule. Common-order controls retain their imposed common order. A uniform reference law alone has no identified fitted center, so its NLL reference is not assigned an arbitrary center error.

The exact-population NLLs in S1 and D2 have no finite test sample. Their companion distance is the corresponding probability-weighted expectation for one new report. S2 retains its sampled test reports. Test losses with an infinite NLL can still have a finite Kendall distance; those distances remain included. A failed estimator with no admitted center remains unavailable.

G1 local/matched predictors first pool discordance sums and report counts across their disjoint evaluation groups within a split. An unavailable group leaves the complete split score unavailable; the separately labeled subset mean is not substituted. Across splits, means give each original allocation equal weight. Selector results inherit the **already selected** model's distance; no selector is rerun on Kendall outcomes and aliases are not additional fits.

## Results

- [P0](P0.md)
- [E0](E0.md)
- [B0](B0.md)
- [L0_S0](L0_S0.md)
- [P1](P1.md)
- [P2](P2.md)
- [G1](G1.md)
- [L1](L1.md)
- [L2](L2.md)
- [S1_S2_D1](S1_S2_D1.md)
- [S3](S3.md)
- [D2](D2.md)
- [T1_C1](T1_C1.md)
- [tuned_blocks](tuned_blocks.md)
- [S4-T](S4-T.md)

| Study | Score records, including unavailable and validation | Defined distances |
|---|---|---|
| B0 | 115 | 55 |
| C1_ATP | 20 | 20 |
| C1_cutting_plane | 2 | 2 |
| C1_outer | 40 | 40 |
| C1_same_order | 40 | 40 |
| D1 | 9520 | 6287 |
| D1_budget | 1600 | 1536 |
| D2 | 2800 | 2779 |
| E0 | 690 | 481 |
| G1 | 55800 | 31353 |
| L0 | 360 | 240 |
| L1 | 320 | 320 |
| L2 | 300 | 300 |
| L2_penalty | 120 | 120 |
| P0 | 230 | 230 |
| P1 | 1150 | 772 |
| P1_selection | 160 | 94 |
| P2 | 230 | 156 |
| P2_selection | 32 | 20 |
| S0 | 1440 | 958 |
| S1 | 22000 | 17803 |
| S2 | 1080 | 837 |
| S3 | 11100 | 11100 |
| S4-T | 172800 | 154971 |
| T1_ATP | 100 | 100 |
| T1_Beans | 20 | 20 |
| Tuned_blocks | 201 | 141 |

S4 itself reports true-center risk and has no predictive NLL/test-set evaluation to supplement. S4-T includes both selection-validation and independent confirmation scores in the machine tables; its readable page shows confirmation. Full-data feature/NLL joins, shell decompositions, and diagnostic subgroups reuse the originating predictors rather than creating additional center fits.

## Calculation and provenance

The original fits, allocations, NLLs, and selected constants are preserved. Saved orders are replayed against the original evaluation reports. S4-T already saves integer held-out distance sums, which are divided by its saved holdout count. Where a positive finite beta and an SM NLL were saved but the order was not, the identity `(NLL - log Z_r(beta)) / beta` recovers the same mean distance; integer totals are checked for sampled tests. This algebra is not used at beta=0 or infinity. Those boundaries and missing PL orders use deterministic source-version replays, checked against the original NLL (and original true-center error where saved). Recovered orders are retained in witness archives.

`inputs/legacy/` pins the source and selected outputs at commit 89b21645; Git blob hashes are verified by `inputs/legacy_tree.json`. These files are provenance, not alternate active experiments. P1/G1 parameter archives omit raw reports and participant membership lists; source-based allocation reconstruction supplies the evaluation sets. Raw licensed datasets remain outside the repository.

Rebuild with `build_heldout_kendall.py` (predictive, repeated, fixed_real, groups, learning, tuned_blocks, validation_simulations, s4t); `replay_strict_kendall.py` (bridge, shell, coverage); `replay_legacy_kendall.py` (small, coverage, synthetic, real, tennis, controls); then `build_kendall_selectors.py` and `summarize_heldout_kendall.py --integrate`. The read-only `verify_heldout_kendall.py` checks saved-score coverage, identities and source hashes. Existing estimation producers are unchanged.
