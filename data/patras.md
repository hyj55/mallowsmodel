# PatrasIQ cost and population

[Data catalogue](README.md) · [Main prediction](../docs/predictive_comparison.md) · [Estimator comparison](../docs/estimator_comparison.md)

The main [P0 comparison](../docs/predictive_comparison.md) uses 313 development and 79 test reports per task, over five allocations, with a 235/78 inner split for PL tuning. It retains the documented one-report-per-volunteer unit within a task and does not invent cross-task matching. Both r=6 tasks enter the separate E0 estimator comparison and B0 sieve supplement with R=10; computational failures and missing-pair Fotakis admission are recorded without changing the catalogue. Conditional intervals require independently sampled volunteers, while their five-split mean has a partition MCSE rather than a population CI.

The [PrefLib Cities Survey page](https://preflib.github.io/PrefLib-Jekyll/dataset/00034), its [pinned study description](https://github.com/PrefLib/PrefLib-Data/blob/1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80/datasets/00034%20-%20cities/info.txt), and [Caragiannis et al. (2017)](https://ojs.aaai.org/index.php/AAAI/article/view/10585) describe 392 volunteers at PatrasIQ in April 2016. Each person ordered six cities by estimated cost of living and six countries by estimated population, in decreasing order.

| Task | Source file | M | n | r | Distinct displayed bundles |
|---|---|---:|---:|---:|---:|
| `patras_cost` | `00034-00000001.soi` | 392 | 36 cities | 6 | 80 |
| `patras_population` | `00034-00000002.soi` | 392 | 48 countries | 6 | 80 |

Both files and the study description are pinned in [the manifest](validation_extension_sources.json). Each ranking record stores multiplicity and an ordered list of six IDs; headers identify alternatives and task totals. There are no respondent ID, demographic, time, location or per-response condition columns. The collection place/date describes the source, not an input feature. The source's alternative ordering encodes an external answer order derived from April 2016 cost/population references, not a known latent SM center.

Expand multiplicities exactly and shift IDs to zero-based labels, preserving all 392 reports per task. The actual pinned files give cost item counts 58–70 and population counts 46–51; these file counts take precedence over approximate ranges in the narrative source description. Bundles recur 4–6 times. Full-source pair coverage is 538/630 and 795/1,128 respectively, so complete item coverage does not mean complete pair coverage.

P1/P2 use 235/78/79 reports. Cost training λ=5.5952, μ=39.1667; population λ=3.125, μ=29.375. The source explicitly documents one report per volunteer **within each task**, supporting report-level resampling under independent-volunteer sampling. Anonymous exports prevent pairing the same volunteer across the two tasks; these are not independent studies and their splits cannot be verified as aligned across tasks. Neither task is split by demographics or bundle strata.

Both tasks contribute whole-ranking prediction, shell decomposition and fitted/objective-reference context diagnostics. No participant-local fit is attempted from a single report per task. Numerical cost/population values are not fitted covariates.
