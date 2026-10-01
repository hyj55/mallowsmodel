# Beans: three-variety field evaluations

[Data catalogue](README.md) · [Prediction design](../docs/repeated_holdout.md) · [Learning curves](../docs/learning_curves.md) · [Year transfer](../docs/temporal_prediction.md)

## Source and observation

The PlackettLuce package's [Beans documentation](https://hturner.github.io/PlackettLuce/reference/beans.html) describes a Nicaragua sample from farmer trials. The experiment uses the [R object at commit ea031f7](https://github.com/hturner/PlackettLuce/blob/ea031f7b129910c518daabf7c3e769aa499ea639/data/beans.rda), verified by [sources.json](sources.json). The originating study is van Etten et al. (2019), [PNAS](https://doi.org/10.1073/pnas.1813720116). The package sample is not claimed to be the full original field study.

There are 842 reports. Each evaluates three assigned varieties from ten. The 14 released columns are:

| Variables | Meaning | Experimental use |
|---|---|---|
| `variety_a`, `variety_b`, `variety_c` | Assigned variety names in positions A/B/C | Identify the displayed triple |
| `best`, `worst` | Preferred and least preferred assigned position | Decode the ordering |
| `var_a`, `var_b`, `var_c` | Better/worse judgments against a local variety | Not part of the fitted ranking task |
| `season`, `year` | Growing season and planting year | Descriptive metadata; year-transfer allocation; season-specific diagnostic cells |
| `maxTN` | Maximum night temperature during the vegetative cycle, °C | Not a model feature or P1/P2 stratum |
| `lon`, `lat` | Plot coordinates | Not a model feature or geographic holdout variable |
| `planting_date` | Trial start | Metadata only |

There is no farmer identifier. Distinct rows are not thereby proven to come from independent people.

## Decoding and preservation

Map variety names to ten categorical labels. If best=C and worst=A, the report is C > B > A on the assigned triple. The middle item is logically determined; no preference is imputed. Every assigned triple must have three distinct varieties, valid nonmissing A/B/C responses, and different best/worst choices. All 842 pass. The local-variety comparisons are not appended as extra pair observations.

All 120 possible unordered triples occur in the full source, and all 45 pairs occur. Full-source item frequencies range 234–270 and pair frequencies 44–65. This near balance does not prove independent uniform assignment or a single homogeneous preference population.

## Season composition and allocation

| Source season | Reports |
|---|---:|
| Apante 2015 (`Ap - 15`) | 481 |
| Postrera 2015 (`Po - 15`) | 177 |
| Apante 2016 (`Ap - 16`) | 87 |
| Primera 2016 (`Pr - 16`) | 64 |
| Postrera 2016 (`Po - 16`) | 33 |

P1/P2 split reports 505/168/169. P1 repeats this randomization 30 times. **These splits do not stratify by year, season, temperature or location.** Season is loaded as metadata, but is not used by the P1 split function. Randomization balances composition in expectation, not exactly in every partition; repeated refitting averages partition randomness without proving invariance across seasons.

L1 uses one 673/169 development/test allocation and nested budgets; L2 includes budgets as small as two reports. T1 deliberately trains on the 658 reports labeled 2015 and tests on the 184 labeled 2016. The five T1 repetitions reshuffle/tune within the same training years; they do not create five independent temporal test sets. Season-stratified context diagnostics adjust the diagnostic cells only, not SM or PL fitting.

For P1/P2 N=505, λ=33.6667 and μ=151.5. With unidentified farmers, point comparisons are descriptive; saved report-bootstrap intervals in the regularized analyses require an independence assumption that cannot be verified here and are not used as population-level evidence.
