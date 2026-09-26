# Source audit amendment before new fits

26 September 2026, after the extension protocol commit ddad79788574374d3c31699c74a145ff75d9008f and before any extension model fit.

The original beach paper, Vitelli et al. (2018), Section 6.2, explicitly states that nontransitive patterns from nine assessors were dropped in its analysis. The current package release contains 1,442 comparisons from 60 assessors and no cyclic assessor. The upstream data-raw/Beaches_data.Rdata object contains the same 1,442-record data and derived objects; it has not supplied an independently verifiable unfiltered response table.

Therefore the released beach task is retained in the source screen but **not fitted** in this extension. Do not reconstruct deleted responses from completed rankings or posterior draws. No model performance has been inspected in making this eligibility correction.

Sounds contains all 1,380 released comparisons from 46 assessors, including cycles for 37 assessors. Its prefs4BM object in the source RData agrees with the packaged response table. Cycles across distinct pair reports are allowed; they are not ties or invalid within-report rankings and are not removed.

The two PatrasIQ files each contain all 392 documented six-item reports, across 80 distinct assigned bundles. Each bundle occurs 4–6 times. This observed restricted set of bundles is not certified as independent uniform sampling from all catalog subsets. lambda/mu are descriptive; no uniform-design theorem is claimed.

The fitting scope is now three new tasks (Sounds, cost of living, population) and one explicitly excluded source (Beaches). The fixed source index is 1 for Sounds, 2 for cost of living, 3 for population, so the exclusion does not change another task's split seed. All other settings and the 1,400 synthetic training datasets are unchanged.

Sources: https://jmlr.org/papers/volume18/15-481/15-481.pdf (Section 6.2); the pinned BayesMallows source files and original PrefLib 00034 metadata listed in data/validation_extension_sources.json.
