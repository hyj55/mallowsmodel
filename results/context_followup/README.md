# Context follow-up outputs

[Current report](../../docs/context_followup.md). Original rankings and fit point estimates are unchanged. Earlier cluster intervals and village-adjusted estimates are withdrawn under the [audit amendment](../../docs/protocols/AUDIT_AMENDMENT.md).

- `scores.csv`: all methods/statuses; conditional NLL; CI fields unavailable because sampling-unit identity is missing.
- `context.csv`: descriptive unadjusted slopes and support counts; village-adjusted analysis unavailable, with explicit status.
- `coverage.json`: catalog, display counts, exposure and missing village information.
- `splits.csv`: source row and split indices; village=-1 means missing metadata, never an inferential cluster.
- `parameters.json`: fitted centers, dispersions, worths and convergence metadata.
- `sprank_audit.csv`: every cohort/domain task, including zero objective-gap variation.
- `validation.json`: current audit checks; the former cluster-validation record is in Git history.

Run `python run_context_followup.py`. Raw inputs are downloaded by immutable URL and checked against data/context_followup_sources.json. No source rankings are rehosted.
