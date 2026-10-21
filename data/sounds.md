# Sounds

[Data catalogue](README.md) · [Main prediction](../docs/predictive_comparison.md) · [Group analysis](../docs/group_sensitivity.md)

In the main [P0 comparison](../docs/predictive_comparison.md), each of five allocations has 36 development assessors (1,080 reports) and ten test assessors (300 reports). A 27/9 assessor inner split selects PL ridge before refitting on all 36. Final-development lambda=16.3636 and mu=180. The paired conditional bootstrap resamples whole test assessors, retaining all thirty judgments together. The separate E0 Sharp comparison uses the full-space shortcut for this twelve-item catalogue; B0 reuses its selected pairs and sieve. P0 itself needs no sieve.

The source is the BayesMallows [Sounds object and documentation](https://github.com/ocbe-uio/BayesMallows/blob/a26cf89d3142ea3499489730e7c2b3ef9a26bfb2/man/sounds.Rd), with upstream `Sounds.RData` and conversion code pinned in [validation_extension_sources.json](validation_extension_sources.json). The study is credited to [Crispino et al. (2019)](https://doi.org/10.1214/18-AOAS1203) and Barrett and Crispino (2018). Participants compare how human the agency in sounds appears; these are preference/judgment outcomes, not a known true order.

The released 1,380×3 table has `assessor`, `top_item`, `bottom_item`. Each of 46 assessors supplies 30 pair reports from 12 sound items. `assessor` is a usable repeated-person ID; `top_item` and `bottom_item` specify the ordered displayed pair. No age, location, season or temperature is used or present in this three-column fitting table.

Map item labels 1–12 to 0–11 and preserve every pair. Cycles across one person's reports are retained; they are not repaired into one transitive complete ranking. Across the full source all 66 pairs occur, with 13 or more reports per pair; item exposure ranges 207–243. P1/P2 hold whole assessors together: 27/9/10 people, giving 810/270/300 reports. λ=12.2727 and μ=135 in training.

P1/P2 compare pooled predictive models and pair-reliability profiles. P2's source-assessor bootstrap preserves within-person dependence; P1 instead reports partition MCSE without a bootstrap. G1's within-person design instead puts different reports of the same person in train and test to predict additional judgments of a known person; its whole-person holdout tests new people. Person labels select local fits but are not covariates in SM or PL. r=2 provides a direct contrast between SM's common correct-order probability and PL's heterogeneous strengths; there is no changing displayed gap for an individual pair.
