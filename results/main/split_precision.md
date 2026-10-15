# P0: what thirty random allocations contribute

[Main results](README.md) · [Computed prefix summaries](split_precision.csv) · [Uncertainty definitions](../../docs/uncertainty.md#partition-monte-carlo-standard-error)

This is an arithmetic audit of saved P0 results, not another experiment, new simulation, or selection of a better split. The models, splits and scientific comparisons are unchanged. Prefixes use the prespecified repetition order (IDs 0–4, 0–9, 0–19 and 0–29); none is chosen for a favorable result.

## Uses across the study

| Component | Use of the 30 allocations | Interval interpretation |
|---|---|---|
| P0 main experiment | Average whole-ranking NLL and paired delta; MCSE, split quantiles, fit/certificate counts | MCSE is conditional partition precision; no population CI for the 30-split mean |
| E0 estimator comparison / B0 sieve aliases | Corresponding summaries for separately named estimators; unavailable fits keep their denominators | Same distinction; aliases are not extra repetitions |
| L0 Sushi learning curves | At each N average 30 test losses; compare nested budgets on the same test within a repetition | Bars are MCSEs; budget points and Sushi A/B share allocations |
| P1 unpenalized control | Average 30 confirmation scores and descriptive diagnostics; report coverage and split spread | No within-split bootstrap in P1; its bars are MCSEs |
| Full-data feature comparison | Join each unchanged full-data feature to P0's 30-split mean NLL difference | Features themselves are not recomputed on 30 splits; no causal or sampling CI is created |

P0/E0/L0 additionally save a separate 2,000-draw test-unit bootstrap inside each eligible split. That bootstrap conditions on the fitted model and does not use the 30 split outcomes as its resampling units. B0 reuses the corresponding Sharp quantities. S0 instead uses **20 independently generated training/test datasets**, whose Student-t mean intervals have a different target. The number 30 is not a universal repetition rule for G1, T1 or the other simulations.

## How many allocations are useful?

Conditional on the observed dataset and fixed fitting rules, independently randomized partitions give

```math
\widehat{\mathrm{MCSE}}_B=\frac{s_\Delta}{\sqrt B},\qquad
\operatorname{Var}(\overline\Delta_B\mid\mathcal D)
=\frac{\operatorname{Var}(\Delta_b\mid\mathcal D)}{B}.
```

Thirty has no special theoretical status. At a fixed partition variance, increasing B from 10 to 30 reduces MCSE by about **42%**, and increasing it from 20 to 30 by about **18%**. Doubling 30 to 60 reduces it by about 29%; halving the MCSE requires approximately four times as many fits. The estimated SD can change as repetitions are added, so observed MCSE need not decrease monotonically.

Thirty is a defensible precision/computation tradeoff here, not a requirement or a guarantee of adequate precision. The 23 task MCSEs range from 0.00223 to 0.02108 nats/report. A useful budget depends on the reporting precision and effect sizes that matter for the particular task and r, rather than obtaining a desired sign or significance decision. For future studies, a separate pilot can estimate partition SD and support a prespecified repetition budget approximately proportional to (SD / desired MCSE)^2. This does not create a population CI or justify stopping when a preferred model wins.

The completed 30 fits should be retained. Reducing their number now saves no fitting work and discards information. For a new expensive exploratory run, 10–20 partitions can be a starting budget, followed by a documented precision assessment; the current results do not prove that ten will suffice in a new dataset. The Sharp bottleneck is construction of ten distinct shared packings, not 530 independent reconstructions. Fewer partitions would therefore not remove the catalogue-scale exact-sieve obstacle.

## Observed prefix arithmetic

| Task | First 10 mean | First 20 mean | All 30 mean | All 30 MCSE | Absolute 10-to-30 difference | Absolute 20-to-30 difference |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | -0.01702 | -0.01164 | -0.01241 | 0.00226 | 0.00460 | 0.00077 |
| Dots 2013, gap 5 | -0.01191 | -0.01548 | -0.01452 | 0.00223 | 0.00260 | 0.00096 |
| Dots 2013, gap 7 | -0.00182 | -0.00916 | -0.01255 | 0.00311 | 0.01073 | 0.00339 |
| Dots 2013, gap 9 | -0.03657 | -0.03857 | -0.03515 | 0.00413 | 0.00142 | 0.00343 |
| Puzzle, minimum 11 steps | -0.00460 | -0.01136 | -0.01161 | 0.00273 | 0.00701 | 0.00024 |
| Puzzle, minimum 5 steps | -0.05863 | -0.05834 | -0.05855 | 0.00365 | 0.00008 | 0.00021 |
| Puzzle, minimum 7 steps | -0.03125 | -0.02071 | -0.02293 | 0.00368 | 0.00831 | 0.00222 |
| Puzzle, minimum 9 steps | -0.00955 | -0.01061 | -0.00881 | 0.00265 | 0.00074 | 0.00179 |
| Beans | 0.01508 | 0.01328 | 0.01275 | 0.00240 | 0.00233 | 0.00053 |
| Dots 2024 A r2 | 0.04419 | 0.09393 | 0.09381 | 0.01382 | 0.04963 | 0.00012 |
| Dots 2024 A r3 | 0.10102 | 0.12722 | 0.10598 | 0.01671 | 0.00496 | 0.02125 |
| Dots 2024 A r5 | 0.02293 | 0.05075 | 0.04912 | 0.01987 | 0.02618 | 0.00163 |
| Dots 2024 A r6 | 0.10240 | 0.06886 | 0.07953 | 0.02108 | 0.02288 | 0.01067 |
| Dots 2024 B r2 | 0.12939 | 0.10144 | 0.11691 | 0.01358 | 0.01248 | 0.01547 |
| Dots 2024 B r3 | 0.11894 | 0.12841 | 0.11766 | 0.01532 | 0.00128 | 0.01075 |
| Dots 2024 B r5 | 0.05153 | 0.02626 | 0.01198 | 0.01465 | 0.03955 | 0.01428 |
| Dots 2024 B r6 | -0.02779 | -0.03464 | -0.04621 | 0.01352 | 0.01842 | 0.01157 |
| PatrasIQ cost | 0.31719 | 0.29487 | 0.28339 | 0.01974 | 0.03380 | 0.01148 |
| PatrasIQ population | 0.07202 | 0.05895 | 0.07579 | 0.02056 | 0.00377 | 0.01683 |
| Sounds | 0.00894 | 0.01099 | 0.01304 | 0.00267 | 0.00410 | 0.00205 |
| Sushi A | 0.02923 | 0.02790 | 0.02543 | 0.00330 | 0.00381 | 0.00248 |
| Sushi B | 0.00104 | 0.00957 | 0.00975 | 0.00509 | 0.00871 | 0.00018 |
| Wheat | 0.15305 | 0.16417 | 0.15917 | 0.01337 | 0.00612 | 0.00500 |

The first 10 and first 20 means have the same direction as all 30 for all 23 tasks. Nevertheless, their largest absolute differences from the 30-split means are **0.04963** and **0.02125** nats/report, respectively; their median absolute differences are **0.00612** and **0.00248**. Sushi B changes mean sign between the first five and all thirty splits. Matching signs therefore do not show that numerical precision is already adequate.

These are overlapping prefixes of one prespecified sequence, not independent experiments or a formal convergence test. The 30-split mean is a reference for this audit, not a known population truth or the exact expectation over all possible partitions. No repetition was removed and no model or hyperparameter was selected using this audit.
