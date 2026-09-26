# Historical baseline replacement: frozen before fitting
2026-09-26 UTC (25 September, New York). Exploratory correction after source/code audit; not independent confirmation of old findings.

Inputs: the exact Beans and Sushi A/B bytes in data/sources.json, originally used by the historical benchmark. Keep every strict original report and the full source catalog (10,10,100). If any task contains invalid/missing/non-strict reports, exclude the entire task and record why; no row repairs or item deletion. Preserve best/middle/worst decoding for complete Beans triples. Source package Beans has 842 rows; Sushi A and B each have 5000 aligned respondent rows.

Seed 202609253. Beans: independently permute row IDs; 60% fit,20% discovery,remainder confirmation. Sushi: one shared permutation of all 5000 respondent indices; same 60/20/20 assignment in A and B. Original rows and report order intact. No seed search. No new objective truth labels.

For each task: SM exact DP for n<=18; otherwise Conitzer integral LP3 formulation, HiGHS backend, fixed120-second solve budget, only a certified optimum accepted. This is an exact-optimization benchmark, not replication of original CPLEX implementation. Literal sharp and efficient wrappers(beta0=.1) and separately named equation(3.4) Borda; Hunter simultaneous PL MM. Unbounded beta and no penalties/floors. No fallback if center unavailable or PL MLE fails. All methods receive the same training reports.

Primary: paired confirmation conditional whole-ranking NLL, SM minus PL. Sushi one report per respondent/task: 2000 paired respondent bootstrap draws conditional on training. Shared participants mean A/B are not independent studies. Beans has no assessor ID: descriptive NLL only, no inferential CI. Missing identification is not replaced by arbitrary clusters. The MLE comparison is marked unavailable if its optimum is uncertified, even if an incumbent exists.

Report training lambda/mu, label/pair exposure, complete splits, all fit statuses, fitted parameters and raw-data hashes. This replaces, not pools with, historical regularized/heuristic comparisons. No claim of minimax rates or uniform real subset sampling; no new ranking data are manufactured. Sports results with selected catalogs, omitted matches, capped beta or penalized PL are retired to Git history until a separate original-report design is specified.
