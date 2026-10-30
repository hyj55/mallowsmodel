# E0: supplementary center-estimator comparison

[Design and formulas](../../docs/estimator_comparison.md) · [All-method summary](summary.csv) · [Per-partition scores](repeat_scores.csv.gz) · [Borda paired contrasts](borda_comparisons.csv) · [Fitted parameters](predictors.jsonl.gz) · [P0 main results](../main/README.md) · [B0 global sieve](../global_sieve/README.md)

E0 compares Sharp, Fotakis, independently admitted Efficient and global clipped Borda on the same 23 tasks and five development/test allocations. PL and likelihood-center SM are the saved P0 references, included in the same tables. This is one supplementary estimator comparison; no test-selected E0 estimator replaces P0's likelihood center.

## Complete comparison

The table gives whole-ranking test NLL, averaged equally across five allocations; lower is better. All SM centers use the same development-data dispersion fit on [0,10]. A full mean requires all five planned fits. NA is an unavailable full comparison, not zero loss or a mean over the successful subset. The availability table below gives every denominator; conditional subset means remain explicitly labeled in the CSV.

| Task | PL NLL | Likelihood SM NLL | Sharp NLL | Fotakis NLL | Efficient NLL | Global Borda NLL |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 3.13793 | 3.11623 | 3.11623 | 3.11623 | NA | 3.11623 |
| Dots 2013, gap 5 | 3.09017 | 3.08019 | 3.08019 | 3.08019 | NA | 3.08019 |
| Dots 2013, gap 7 | 2.90931 | 2.90742 | 2.90742 | 2.90742 | NA | 2.90742 |
| Dots 2013, gap 9 | 2.85413 | 2.80998 | 2.80998 | 2.80998 | NA | 2.80998 |
| Puzzle, minimum 11 steps | 3.11026 | 3.09985 | 3.09985 | 3.09985 | NA | 3.09985 |
| Puzzle, minimum 5 steps | 2.84437 | 2.77503 | 2.77503 | 2.77503 | NA | 2.77503 |
| Puzzle, minimum 7 steps | 2.87793 | 2.85703 | 2.85703 | 2.85703 | NA | 2.85703 |
| Puzzle, minimum 9 steps | 3.01953 | 3.00423 | 3.03499 | 3.00423 | NA | 3.00423 |
| Beans | 1.78969 | 1.80301 | 1.79947 | 1.79352 | NA | 1.79178 |
| Dots 2024 A r2 | 0.58080 | 0.62505 | NA | NA | 0.61100 | 0.61100 |
| Dots 2024 A r3 | 1.35561 | 1.48428 | NA | NA | NA | 1.43432 |
| Dots 2024 A r5 | 4.11050 | 4.15226 | NA | NA | NA | 4.14245 |
| Dots 2024 A r6 | 5.63734 | 5.72212 | NA | 5.70054 | NA | 5.73429 |
| Dots 2024 B r2 | 0.67852 | 0.81687 | NA | NA | 0.70855 | 0.70855 |
| Dots 2024 B r3 | 1.56516 | 1.68061 | NA | NA | NA | 1.57454 |
| Dots 2024 B r5 | 4.33936 | 4.39048 | NA | NA | NA | 4.41195 |
| Dots 2024 B r6 | 6.06293 | 6.04469 | NA | NA | NA | 6.03088 |
| PatrasIQ cost | 4.98551 | 5.32014 | NA | NA | NA | 5.30278 |
| PatrasIQ population | 5.52365 | 5.62551 | NA | NA | NA | 5.57209 |
| Sounds | 0.67411 | 0.68172 | 0.68359 | 0.67987 | NA | 0.67716 |
| Sushi A | 14.23722 | 14.26433 | 14.30875 | 14.26433 | NA | 14.27070 |
| Sushi B | 14.23999 | 14.23601 | NA | NA | NA | 14.23391 |
| Wheat | 1.43954 | 1.58081 | NA | 1.56505 | NA | 1.59975 |

## Paired SM–PL differences on both scales

Each cell is **raw mean delta / scaled mean delta**: the first value is SM NLL minus PL NLL in nats/report; the second is that same difference divided by log(r!). For example, a scaled value 0.05 means 5% of the uniform-ranking loss, not a five-percentage-point accuracy gap. Negative favors the named SM estimator. This uses the same five paired allocations and requires all five fits. Scaling changes neither signs nor availability. r is the display/report size, not catalogue n; [limitations](../../docs/criteria.md#uniform-reference-scaled-loss-difference) still apply.

| Task | Likelihood SM − PL: raw / scaled | Sharp − PL: raw / scaled | Fotakis − PL: raw / scaled | Efficient − PL: raw / scaled | Global Borda − PL: raw / scaled |
|---|---|---|---|---|---|
| Dots 2013, gap 3 | -0.02170 / -0.00683 | -0.02170 / -0.00683 | -0.02170 / -0.00683 | NA (0/5) | -0.02170 / -0.00683 |
| Dots 2013, gap 5 | -0.00998 / -0.00314 | -0.00998 / -0.00314 | -0.00998 / -0.00314 | NA (0/5) | -0.00998 / -0.00314 |
| Dots 2013, gap 7 | -0.00189 / -0.00059 | -0.00189 / -0.00059 | -0.00189 / -0.00059 | NA (0/5) | -0.00189 / -0.00059 |
| Dots 2013, gap 9 | -0.04415 / -0.01389 | -0.04415 / -0.01389 | -0.04415 / -0.01389 | NA (0/5) | -0.04415 / -0.01389 |
| Puzzle, minimum 11 steps | -0.01042 / -0.00328 | -0.01042 / -0.00328 | -0.01042 / -0.00328 | NA (0/5) | -0.01042 / -0.00328 |
| Puzzle, minimum 5 steps | -0.06934 / -0.02182 | -0.06934 / -0.02182 | -0.06934 / -0.02182 | NA (0/5) | -0.06934 / -0.02182 |
| Puzzle, minimum 7 steps | -0.02090 / -0.00658 | -0.02090 / -0.00658 | -0.02090 / -0.00658 | NA (0/5) | -0.02090 / -0.00658 |
| Puzzle, minimum 9 steps | -0.01530 / -0.00481 | +0.01546 / +0.00486 | -0.01530 / -0.00481 | NA (0/5) | -0.01530 / -0.00481 |
| Beans | +0.01333 / +0.00744 | +0.00978 / +0.00546 | +0.00383 / +0.00214 | NA (0/5) | +0.00209 / +0.00117 |
| Dots 2024 A r2 | +0.04426 / +0.06385 | NA (0/5) | NA (0/5) | +0.03020 / +0.04358 | +0.03020 / +0.04358 |
| Dots 2024 A r3 | +0.12868 / +0.07182 | NA (0/5) | NA (0/5) | NA (0/5) | +0.07872 / +0.04393 |
| Dots 2024 A r5 | +0.04176 / +0.00872 | NA (0/5) | NA (0/5) | NA (0/5) | +0.03196 / +0.00667 |
| Dots 2024 A r6 | +0.08479 / +0.01289 | NA (0/5) | +0.06320 / +0.00961 | NA (0/5) | +0.09695 / +0.01474 |
| Dots 2024 B r2 | +0.13836 / +0.19961 | NA (0/5) | NA (0/5) | +0.03004 / +0.04333 | +0.03004 / +0.04333 |
| Dots 2024 B r3 | +0.11545 / +0.06443 | NA (0/5) | NA (0/5) | NA (0/5) | +0.00938 / +0.00524 |
| Dots 2024 B r5 | +0.05113 / +0.01068 | NA (0/5) | NA (2/5) | NA (0/5) | +0.07260 / +0.01516 |
| Dots 2024 B r6 | -0.01824 / -0.00277 | NA (0/5) | NA (4/5) | NA (0/5) | -0.03205 / -0.00487 |
| PatrasIQ cost | +0.33462 / +0.05086 | NA (0/5) | NA (0/5) | NA (0/5) | +0.31726 / +0.04822 |
| PatrasIQ population | +0.10186 / +0.01548 | NA (0/5) | NA (0/5) | NA (0/5) | +0.04844 / +0.00736 |
| Sounds | +0.00761 / +0.01098 | +0.00948 / +0.01367 | +0.00576 / +0.00831 | NA (0/5) | +0.00305 / +0.00440 |
| Sushi A | +0.02711 / +0.00179 | +0.07153 / +0.00474 | +0.02711 / +0.00179 | NA (0/5) | +0.03348 / +0.00222 |
| Sushi B | -0.00398 / -0.00026 | NA (0/5) | NA (0/5) | NA (0/5) | -0.00608 / -0.00040 |
| Wheat | +0.14126 / +0.07884 | NA (0/5) | +0.12550 / +0.07005 | NA (0/5) | +0.16020 / +0.08941 |

The [summary CSV](summary.csv) includes raw/scaled MCSEs and all other delta statistics. The [scaled per-partition view](scaled_repeat_scores.csv.gz) additionally gives raw/scaled conditional bootstrap endpoints. Divide each original difference, MCSE or endpoint by the same positive log(r!); unavailable intervals remain unavailable. These are derived views of saved scores, not refitted models or another experiment.

## Global Borda against every other method

Each cell is **mean(Borda NLL − comparator NLL), with paired partition MCSE in parentheses**. Negative favors Borda. Compute each difference within the same allocation first, then average those five differences; the MCSE is their sample standard deviation divided by sqrt(5). It is not obtained by treating the two methods as independent. It is not a population confidence interval. Full differences and MCSEs require 5/5 paired fits.

| Task | Borda − PL | Borda − Likelihood SM | Borda − Sharp | Borda − Fotakis | Borda − Efficient |
|---|---|---|---|---|---|
| Dots 2013, gap 3 | -0.02170 (0.00576) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Dots 2013, gap 5 | -0.00998 (0.00413) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Dots 2013, gap 7 | -0.00189 (0.00541) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Dots 2013, gap 9 | -0.04415 (0.00337) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Puzzle, minimum 11 steps | -0.01042 (0.00294) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Puzzle, minimum 5 steps | -0.06934 (0.00523) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Puzzle, minimum 7 steps | -0.02090 (0.01363) | +0.00000 (0.00000) | +0.00000 (0.00000) | +0.00000 (0.00000) | NA (0/5) |
| Puzzle, minimum 9 steps | -0.01530 (0.00906) | +0.00000 (0.00000) | -0.03076 (0.01934) | +0.00000 (0.00000) | NA (0/5) |
| Beans | +0.00209 (0.00231) | -0.01123 (0.00882) | -0.00768 (0.00213) | -0.00174 (0.00271) | NA (0/5) |
| Dots 2024 A r2 | +0.03020 (0.01624) | -0.01405 (0.02161) | NA (0/5) | NA (0/5) | +0.00000 (0.00000) |
| Dots 2024 A r3 | +0.07872 (0.03121) | -0.04996 (0.03207) | NA (0/5) | NA (0/5) | NA (0/5) |
| Dots 2024 A r5 | +0.03196 (0.02902) | -0.00981 (0.01936) | NA (0/5) | NA (0/5) | NA (0/5) |
| Dots 2024 A r6 | +0.09695 (0.03100) | +0.01216 (0.04241) | NA (0/5) | +0.03375 (0.04572) | NA (0/5) |
| Dots 2024 B r2 | +0.03004 (0.02091) | -0.10832 (0.01687) | NA (0/5) | NA (0/5) | +0.00000 (0.00000) |
| Dots 2024 B r3 | +0.00938 (0.02120) | -0.10607 (0.01779) | NA (0/5) | NA (0/5) | NA (0/5) |
| Dots 2024 B r5 | +0.07260 (0.04521) | +0.02147 (0.03634) | NA (0/5) | NA (2/5) | NA (0/5) |
| Dots 2024 B r6 | -0.03205 (0.03345) | -0.01380 (0.01165) | NA (0/5) | NA (4/5) | NA (0/5) |
| PatrasIQ cost | +0.31726 (0.05625) | -0.01736 (0.05108) | NA (0/5) | NA (0/5) | NA (0/5) |
| PatrasIQ population | +0.04844 (0.07153) | -0.05342 (0.02154) | NA (0/5) | NA (0/5) | NA (0/5) |
| Sounds | +0.00305 (0.00789) | -0.00456 (0.00378) | -0.00643 (0.00332) | -0.00271 (0.00422) | NA (0/5) |
| Sushi A | +0.03348 (0.00851) | +0.00637 (0.00214) | -0.03805 (0.01342) | +0.00637 (0.00214) | NA (0/5) |
| Sushi B | -0.00608 (0.00869) | -0.00210 (0.00351) | NA (0/5) | NA (0/5) | NA (0/5) |
| Wheat | +0.16020 (0.02696) | +0.01894 (0.00765) | NA (0/5) | +0.03470 (0.02691) | NA (0/5) |

Descriptive task counts use a 1e-12 nats/report equality tolerance. Tasks share sources and people; these are not independent votes or significance tests.

| Comparator | Complete task comparisons | Borda lower | Equal | Borda higher |
|---|---|---|---|---|
| PL | 23 | 10 | 0 | 13 |
| Likelihood SM | 23 | 11 | 8 | 4 |
| Sharp | 11 | 4 | 7 | 0 |
| Fotakis | 13 | 2 | 8 | 3 |
| Efficient | 2 | 0 | 2 | 0 |

## Interpretation

- Against PL, Borda's five-allocation mean is lower in 10/23 tasks. This does not identify a universally preferred model family or establish significant winners.
- Against likelihood-center SM, Borda is lower in 11 tasks, equal in eight and higher in four. Likelihood optimization minimizes training disagreement; it need not minimize held-out loss. For example, Dots 2024 B r2 has Borda-minus-likelihood -0.10832 (MCSE 0.01687), whereas Wheat has +0.01894 (MCSE 0.00765). P0's three uncertified Sushi B centers retain their original status.
- Among the eleven tasks with complete Sharp fits, Borda is lower in four and equal in seven. This comparison says nothing about Borda versus the twelve unavailable full-catalogue Sharp fits. B0 aliases those Sharp results where their constructions coincide.
- Fotakis has complete five-allocation comparisons on thirteen tasks: Borda is lower in two, equal in eight and higher in three. Partial Fotakis availability on two further tasks is retained without converting it into a five-fit mean.
- Efficient and Borda coincide exactly in both admitted tasks. There is no observed positive-depth hierarchy in E0, so these data do not measure an active hierarchy's advantage over Borda.
- The source objective order is never used to fit these centers. For preference data, no true preference center is observed; the comparison is predictive NLL, not true-center recovery risk.

## Efficient admission, depth and estimator availability

Efficient is assessed independently of Sharp on every allocation. Equation (3.23)'s schedule requires lambda = N r(r−1)/(n(n−1)) <= 1. Only Dots 2024 A/B r2 meet that requirement (10 fits); the other 105 allocations are explicitly outside its domain. Their missing depth is **not** depth zero. Global Borda is fitted on all 115 allocations, including those outside Efficient's schedule domain.

For admitted tasks, eta<=lambda<=1 and n<=100 imply eta*n<=100<256=A. Thus the schedule has zero hierarchy stages and the root is the terminal block. All development reports still score-sort that full catalogue. With the same tie seed 93847, Efficient and Borda have identical order, training distance, fitted beta, every test-report loss and bootstrap endpoints. Both names remain visible for comparison, with alias_of=sm_global_borda on Efficient; they are not independent estimator evidence. If a future admitted configuration has positive depth, its separate Borda fit remains in this same E0 table.

| Task | Development lambda | Sharp | Fotakis | Efficient | Efficient depth | Global Borda |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | 636.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Dots 2013, gap 5 | 635.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Dots 2013, gap 7 | 640.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Dots 2013, gap 9 | 635.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Puzzle, minimum 11 steps | 634.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Puzzle, minimum 5 steps | 636.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Puzzle, minimum 7 steps | 636.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Puzzle, minimum 9 steps | 637.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Beans | 44.86667 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 A r2 | 0.55172 | 0/5 | 0/5 | 5/5 | 0 in 5/5 | 5/5 |
| Dots 2024 A r3 | 1.65517 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 A r5 | 5.51724 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 A r6 | 8.27586 | 0/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 B r2 | 0.55172 | 0/5 | 0/5 | 5/5 | 0 in 5/5 | 5/5 |
| Dots 2024 B r3 | 1.65517 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 B r5 | 5.51724 | 0/5 | 2/5 | 0/5 | not applicable | 5/5 |
| Dots 2024 B r6 | 8.27586 | 0/5 | 4/5 | 0/5 | not applicable | 5/5 |
| PatrasIQ cost | 7.45238 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| PatrasIQ population | 4.16223 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| Sounds | 16.36364 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Sushi A | 4000.00000 | 5/5 | 5/5 | 0/5 | not applicable | 5/5 |
| Sushi B | 36.36364 | 0/5 | 0/5 | 0/5 | not applicable | 5/5 |
| Wheat | 9.85000 | 0/5 | 5/5 | 0/5 | not applicable | 5/5 |

## Uncertainty, data reuse and scope

The summary saves each estimator's paired delta against PL and its MCSE, plus all five split scores. Within each eligible split, 2,000 paired bootstrap draws resample identified test units while every predictor stays fixed. The same bootstrap draws are used across methods. The 2.5th and 97.5th percentiles are conditional test-sampling intervals; they omit training/tuning uncertainty and are not averaged into a CI for the five-split mean. Beans, Wheat and the anonymous PrefLib tasks have no supported sampling interval. The Borda-versus-method table above uses paired partition MCSE, not a bootstrap CI.

Random allocations, data preprocessing and existing PL/likelihood/Sharp/Fotakis parameters are reused exactly. Global Borda and Efficient use complete development reports and a common fixed tie rule, with no extra validation selection. The global Borda baseline is exposure-normalized clipped scoring, not an unnormalized sum of wins. The [design](../../docs/estimator_comparison.md) gives its formula and references.

Sharp has 60 unavailable E0 fits; the further 15 L0 and 80 S0 contexts give 155 unavailable supplementary fits. These are not missing P0 main results. Numerical admission and completion do not establish uniform displays, independent reports or a true SM law. The [sieve report](../../docs/sieve_computation.md) records those limits.

## Files and reproduction

| File | Contents |
|---|---|
| summary.csv | All six methods on 23 tasks; 138 rows, availability, mean NLL, raw/scaled delta, MCSE and explicitly conditional means |
| repeat_scores.csv.gz | 690 rows: six methods × 23 tasks × five unchanged allocations; depth, status, alias and conditional intervals |
| scaled_repeat_scores.csv.gz | Same 690 saved score rows, with log(r!), scaled differences and scaled conditional interval endpoints appended |
| borda_comparisons.csv | Raw/scaled Borda-minus-comparator paired differences, complete/conditional denominators, MCSE and split ranges |
| predictors.jsonl.gz | All six method records per allocation, source hashes, tie rules and Efficient depth/domain metadata |
| manifest.json | Fitting/scoring code, input and output hashes; the report manifest separately verifies generated summaries |

Run `python run_estimator_comparison.py` after acquiring the shared sources to fit the score candidates and replay saved references. Run `python build_study_reports.py` to rebuild E0's tables without fitting. Public verification is `python validate_estimator_comparison.py`; `--sources` additionally reconstructs all 115 partitions, the score estimators, test predictions and conditional bootstrap endpoints. `python build_study_reports.py --check` verifies the generated report. No separate experiment or new split is introduced.

## E0: Sharp/Efficient execution and stopping

[Per-setting reasons and first-round parameters](../estimator_execution/E0.md) distinguish actual depth from a missing or unattempted fit. Counts below are fit contexts, not independent datasets. No predictor is refitted for this audit.

| Execution category | Contexts |
|---|---|
| outside_schedule_domain | 105 |
| root_A_stop | 65 |
| root_A_stop;sieve_resource_budget | 60 |
