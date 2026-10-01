# Sounds and PatrasIQ

[Data catalogue](README.md) · [Prediction](../docs/repeated_holdout.md) · [Group analysis](../docs/group_sensitivity.md)

## Sounds

The source is the BayesMallows [Sounds object and documentation](https://github.com/ocbe-uio/BayesMallows/blob/a26cf89d3142ea3499489730e7c2b3ef9a26bfb2/man/sounds.Rd), with upstream `Sounds.RData` and conversion code pinned in [validation_extension_sources.json](validation_extension_sources.json). The study is credited to [Crispino et al. (2019)](https://doi.org/10.1214/18-AOAS1203) and Barrett and Crispino (2018). Participants compare how human the agency in sounds appears; these are preference/judgment outcomes, not a known true order.

The released 1,380×3 table has `assessor`, `top_item`, `bottom_item`. Each of 46 assessors supplies 30 pair reports from 12 sound items. `assessor` is a usable repeated-person ID; `top_item` and `bottom_item` specify the ordered displayed pair. No age, location, season or temperature is used or present in this three-column fitting table.

Map item labels 1–12 to 0–11 and preserve every pair. Cycles across one person's reports are retained; they are not repaired into one transitive complete ranking. Across the full source all 66 pairs occur, with 13 or more reports per pair; item exposure ranges 207–243. P1/P2 hold whole assessors together: 27/9/10 people, giving 810/270/300 reports. λ=12.2727 and μ=135 in training.

P1/P2 compare pooled predictive models and pair-reliability profiles. P2's source-assessor bootstrap preserves within-person dependence; P1 instead reports partition MCSE without a bootstrap. G1's within-person design instead puts different reports of the same person in train and test to predict additional judgments of a known person; its whole-person holdout tests new people. Person labels select local fits but are not covariates in SM or PL. r=2 provides a direct contrast between SM's common correct-order probability and PL's heterogeneous strengths; there is no changing displayed gap for an individual pair.

## PatrasIQ cost and population

The [PrefLib Cities Survey page](https://preflib.github.io/PrefLib-Jekyll/dataset/00034), its [pinned study description](https://github.com/PrefLib/PrefLib-Data/blob/1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80/datasets/00034%20-%20cities/info.txt), and [Caragiannis et al. (2017)](https://ojs.aaai.org/index.php/AAAI/article/view/10585) describe 392 volunteers at PatrasIQ in April 2016. Each person ordered six cities by estimated cost of living and six countries by estimated population, in decreasing order.

| Task | Source file | M | n | r | Distinct displayed bundles |
|---|---|---:|---:|---:|---:|
| `patras_cost` | `00034-00000001.soi` | 392 | 36 cities | 6 | 80 |
| `patras_population` | `00034-00000002.soi` | 392 | 48 countries | 6 | 80 |

Both files and the study description are pinned in [the manifest](validation_extension_sources.json). Each ranking record stores multiplicity and an ordered list of six IDs; headers identify alternatives and task totals. There are no respondent ID, demographic, time, location or per-response condition columns. The collection place/date describes the source, not an input feature. The source's alternative ordering encodes an external answer order derived from April 2016 cost/population references, not a known latent SM center.

Expand multiplicities exactly and shift IDs to zero-based labels, preserving all 392 reports per task. The actual pinned files give cost item counts 58–70 and population counts 46–51; these file counts take precedence over approximate ranges in the narrative source description. Bundles recur 4–6 times. Full-source pair coverage is 538/630 and 795/1,128 respectively, so complete item coverage does not mean complete pair coverage.

P1/P2 use 235/78/79 reports. Cost training λ=5.5952, μ=39.1667; population λ=3.125, μ=29.375. The source explicitly documents one report per volunteer **within each task**, supporting report-level resampling under independent-volunteer sampling. Anonymous exports prevent pairing the same volunteer across the two tasks; these are not independent studies and their splits cannot be verified as aligned across tasks. Neither task is split by demographics or bundle strata.

Both tasks contribute whole-ranking prediction, shell decomposition and fitted/objective-reference context diagnostics. No participant-local fit is attempted from a single report per task. Numerical cost/population values are not fitted covariates.
