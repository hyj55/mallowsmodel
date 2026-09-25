# Follow-up: diagnostic sample size and repeated contexts

Written after inspecting the initial 16 real tasks and 4,760 simulations, before the following additional computations. All additions are exploratory. No fitted estimator or primary result is replaced.

1. Diagnostic-data budget: replay the original bridge n=8,r=3,N=448,equal-gap cells (five mixture weights, 40 replicates each) with the SAME fitted samples and exact test distribution. Use nested first 20,60,200,1000 independent discovery reports to measure how diagnostic sample size changes the already specified pairwise/context selectors. The 1000-report result must reproduce the saved primary selector. This is a measurement of selection reliability, not a new regularizer or modified estimator.
2. Objective-order checks: the original protocol also requests diagnostics around the externally supplied order. Calculate the same context diagnostic around that fixed reference, with dispersion profiled on training reports only. This is an oracle/reference diagnostic, never a competing estimated-center algorithm. Preserve separate confirmation data.
3. More repeated contexts: the public AgrDataSci/tricot-data catalog is pinned at commit 169edfaba947b5afee52c1e217e0ff275fb71e34. Include EVERY catalog entry with at least 500 listed participants, without consulting rank-analysis results or ranking outcomes. Nine candidate source files meet this rule:

- amaranth-e7c470820fcb.json: 988 listed participants, amaranth, BJ
- okra-9d74b18afc10.json: 675 listed participants, okra, ML
- amaranth-d5ebb545926f.json: 675 listed participants, amaranth, ML
- okra-3aec31c2d6e6.json: 505 listed participants, okra, BJ
- amaranth-37af14eaf361.json: 543 listed participants, amaranth, BJ
- groundnut-c3c46a31b5cb.json: 1000 listed participants, groundnut, TZ
- groundnut-f9d88801f7fa.json: 599 listed participants, groundnut, TZ
- groundnut-7525d0c24f31.json: 873 listed participants, groundnut, TZ
- cowpea-46c9305acadb.json: 504 listed participants, cowpea, NG

For these candidates inspect metadata for an overall preference/performance ranking trait. Select only explicitly described overall evaluations; analyze different collection moments as separate tasks, with whole block/assessor IDs in the same 60/20/20 split across tasks from a source. No direction-dependent selection, arbitrary trait choice, response inversion, item removal, ranking truncation, outlier removal, tie breaking, or imputation is permitted. Use the source-defined catalog. If a trait/moment includes tied, incomplete, or non-triadic reported ranks, mark that whole task ineligible for the strict fixed-r comparison rather than silently repair it. A completely absent assessment is counted as missing, not fabricated. Schema decisions are recorded before any model fit. Keep all eligible tasks, including failures or results favoring either model.

Use the same exact DP (n<=18), certified integer formulation (larger n), uncapped dispersion profile, literal sharp/efficient estimators in their computational domains, Hunter MM, diagnostics, and uncertainty rules as the frozen main protocol. Prespecify global clipped Borda as the named comparison outside Algorithm 3.1's schedule domain. Ground-truth central order is unavailable for crop preference tasks; do not calculate center risk there. These agricultural follow-ups are separate from the initial 16-task confirmation study, and their collection moments are not independent replications.

A smaller Rwanda wheat source (91 reported overall assessments) was structurally inspected but is outside the >=500-participant rule. The large 2019 India/Ethiopia replication dataset was identified at doi:10.7910/DVN/4ICF6W; its public API returned HTTP 403 in this session, so its records have not been used.
