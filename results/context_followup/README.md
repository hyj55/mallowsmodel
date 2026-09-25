# Context follow-up

Read [the English report](../../docs/context_followup.md) and [pre-fit protocol](../../docs/protocols/CONTEXT_FOLLOWUP.md).

One intact breadwheat task, five estimator statuses, two held-out splits. Six SP-Rank tasks are audited without fits. No original microdata are rehosted.

- `scores.csv`: all available/unavailable methods, conditional NLL and paired working intervals.
- `context.csv`: observed and model-implied fixed-effect slopes, support counts, undefined-bootstrap counts and warnings. A single contributing metadata block cannot support cluster inference, even if its numerical interval is a point.
- `coverage.json`: display diversity, lambda, mu and missing-village counts.
- `splits.csv`: original row indices and anonymous metadata-block labels; every row appears once.
- `parameters.json`: unchanged estimator outputs and convergence metadata; NaN marks unavailable values.
- `sprank_audit.csv`: all six source tasks, including zero objective-gap variation.
- `validation.json`: focused checks and pre-fit protocol commits.

Run `python run_context_followup.py` with the locked environment plus `rdata==1.0.0`. The source manifest is `data/context_followup_sources.json`. Scientific limitations and references are in the report.
