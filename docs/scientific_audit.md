# Scientific validity and verification

[Study design](experiments.md) · [Estimator definitions](algorithms.md) · [Uncertainty](uncertainty.md) · [Evidence registry](implementation_registry.md)

The study separates three questions: whether a calculation matches its stated procedure, whether its inference assumptions fit the observation design, and whether a result supports a general scientific claim. Passing implementation checks does not establish the other two.

## Interpretation safeguards

| Issue | Treatment and remaining limitation |
|---|---|
| Different predictive procedures | Unbounded SM/unpenalized PL and bounded/shrunk SM/ridge PL are named separately. Both belong to the study, but their results are not pooled as one estimator |
| Manuscript scope | SM laws and specified estimators follow the supplied manuscript; an unpenalized comparison is a declared variant of its regularized Section 4 prediction procedure |
| Exact center | DP is exact within its guard; larger instances need a checked optimum certificate. A timed-out incumbent is unavailable in exact comparisons |
| Approximate center | Insertion and bounded optimization in L1/L2/T1/C1 are explicitly labeled; their training bounds do not certify test performance |
| Estimator theorem domain | Uniform display sampling, independent reports, signal lower bounds and sufficient sample-size constants are not verified merely by numeric λ/μ. Recorded efficient fits have hierarchy depth zero |
| Anonymous records | Beans, PrefLib and wheat do not support verified independent-person intervals. Their P2 interval fields are unavailable; fixed point values and descriptive split summaries remain usable |
| Missing village identities | Wheat's missing labels are not treated as one cluster. Village-adjusted inference is unavailable |
| Repeated participants | Sounds splits and resamples people. Other shared-participant tasks are analyzed separately; their conclusions are not independent study replications |
| Nonfinite outcomes | Undefined estimates, infinite losses and finite-conditional summaries have separate counts and targets |
| Diagnostic calibration | D2 documents confounding and sparse-overlap bootstrap failure. Nominal context intervals are exploratory |
| Many comparisons | No multiplicity or source-search adjustment is claimed |

## Corrections preserved in the evidence record

The frozen [audit amendment](protocols/AUDIT_AMENDMENT.md) withdraws independent-record or artificial-village inference where sampling units cannot be justified. It does not repair a source ranking, delete an inconvenient response or change a fitted point value. Some immutable result snapshots therefore contain interval columns whose inferential interpretation is superseded by [the uncertainty guide](uncertainty.md).

The implementation rejects noninteger item labels rather than silently truncating them. The unpenalized efficient entry point rejects $`\lambda>1`$; exposure simulations that deliberately cap that schedule are documented as a separate empirical extension. Neither change establishes that a real population satisfies the manuscript assumptions.

## Checks on numerical results

Source hashes and parser checks preserve original strict reports, complete catalogues and multiplicities. Original voting-trial frequencies exactly reconcile with all eight PrefLib tasks. Split checks verify disjoint memberships, documented person/group boundaries and shared task alignments. Mathematical tests cover small-state normalization, pair marginals, shell recursion, exact center optimization and PL likelihood optimization.

The [refit comparison](../results/audit/refit_comparison.json) checks 16 PrefLib/dots2024 tasks plus wheat against saved fitted parameters and predictions; all centers, dispersion/worth values and point losses agree to the recorded tolerance. Its 90 rows include both wheat held-out partitions and are not 90 independent studies. The group and repeated-partition validators replay saved memberships and parameters and recompute published aggregates. Such replay is verification, not another training repetition.

The D2 archive contains 1,400 generated datasets and their parameters. A completeness check recovered ten omitted parameter-log records from the original fixed seeds; their already stored fit/diagnostic values agreed before append. No extra datasets or favorable reruns were added. Archive-part checks restore the exact recorded bytes. [Storage and replay details](../results/validation_extension/README.md).

## What repository verification does

The read-only workflow runs tests, restores lossless generated-data archives and checks public output hashes, counts and aggregations. It does not refit the full experiment or publish new outputs on a documentation change. Full source/prediction replay is a separate local check, and some detailed empirical caches must be regenerated from permitted source downloads. [Reproduction commands](reproducibility.md) distinguish these levels.

Remaining limits are substantive: unknown cross-trial identities, nonuniform displays, dependence between tasks and years, data-dependent source selection, computational certificate limits, and conditional rather than full-learning-procedure intervals. The [findings](findings.md) are stated at that level of evidence.
