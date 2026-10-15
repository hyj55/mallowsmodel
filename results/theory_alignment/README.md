# Evidence for the estimator-theory comparison

[Theory and interpretation](../../docs/theory_alignment.md) · [All numerical tables](tables.md)

This directory relates existing estimator results to the supplied manuscript's conditions and risk targets. It contains arithmetic summaries and copies of saved public summary tables. It contains no new fitted model, simulated dataset, observation split or estimator implementation.

These are the supplementary P1/G1/S1–S3/C1 arithmetic tables. The [P0 Algorithm 4.1 main experiment](../main/README.md), [E0 supplementary estimator comparison](../estimator_comparison/README.md), and [B0 global sieve](../global_sieve/README.md) have separate reports. L0/S0 supplementary curves and all raw allocation records are indexed in [predictive](../predictive/README.md). The shared [theory chapter](../../docs/theory_alignment.md) explains both sets of evidence without treating repeated use of a source table as a new experiment.

| File | Contents |
|---|---|
| [tables.md](tables.md) | P1 training regimes and estimator contrasts; correctly specified SM risk slices; G1 Fotakis contrasts |
| [p1_regimes.csv](p1_regimes.csv) | All 23 P1 tasks: training N, n,r, λ,μ,ν,Q,Vcov,Bcov and actual coverage |
| [p1_methods.csv](p1_methods.csv) | All 115 task/method combinations, statuses, actual branches, depth, NLL and external-objective distance |
| [p1_estimator_contrasts.csv](p1_estimator_contrasts.csv) | Paired same-partition SM-estimator NLL differences, complete versus finite-conditional means and denominators |
| [pure_sm_results.csv](pure_sm_results.csv) | Pure-SM endpoints and S3 SM rows, saved risk means/intervals and dimensional coordinates |
| [g1_fotakis_vs_exact.csv](g1_fotakis_vs_exact.csv) | Every G1 task/design/allocation/scheme; paired all-report NLL, availability and equality counts |
| [c1_sm_centers.csv](c1_sm_centers.csv) | n=10,r=3 pure-SM center benchmarks: mean Kendall error and training-objective gaps for four algorithms |
| [inputs/](inputs/) | Byte-verified copies of public S3/C1 summaries from their recorded implementation snapshot |
| [sources.json](sources.json) | Source commits, Git blobs, SHA256 hashes and manuscript version; the private PDF is not redistributed |
| [manifest.json](manifest.json) | Generated-output and analysis-code hashes |

N always means training reports. Regime flags are numerical conditions, not certifications of an empirical SM law. The positive-signal constant C0 is not inferred from observed exposure. Pure-SM means retain separate design streams; no post hoc pooling across bridge, shell, gap-shape or budget settings is used. Risk intervals are copied from the original tables, with their original finite-simulation interpretation. P1 and G1 differences are descriptive summaries of repeated allocations of fixed data, not independent new samples.

From a complete repository checkout:

```bash
python analyze_theory_alignment.py
python validate_theory_alignment.py
```

The first command reads saved tables and rejects changed source hashes. The second checks saved-output hashes, independently reconstructs the derived summaries, verifies regime identities and the stated complete-ranking/tie distinctions. Neither command downloads observations or runs an estimator on experimental data.
