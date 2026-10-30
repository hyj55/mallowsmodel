# Execution-audit input receipts

[sources.json](sources.json) identifies each source, its original Git blob/SHA256 where applicable, its byte-verified local copy, and any explicit projection.

`group_fit_receipts.csv.gz` retains only Sharp/Efficient fit-audit rows for G1 repetitions 0–4: anonymous group keys, training counts, coverage, status and depth. It contains no report memberships or respondent IDs. Its context counts must exactly match the public G1 eligibility table.

`snapshot_*_replicates.csv.gz` and `snapshot_tennis_by_year.csv.gz` are gzip transports of the exact public source CSV bytes. Parameter JSON projections retain only Efficient metadata, removing order vectors and all train/test indices. The two `.py.txt` files are immutable source evidence, not active experiment modules. All originate in the implementation snapshot recorded in the source manifest. They are read to explain the corresponding result family, not to introduce different fitting rules into other experiments.

`snapshot_schedule_feasibility.csv.gz` preserves the producer's standalone schedule preflight for context. It is not a fit receipt and is not counted as an executed experiment. Exact inner T1 training counts were not retained in the source parameter/audit files; the audit does not fabricate them.
