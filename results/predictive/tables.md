# Predictive result directory

The main experiment is **P0: manuscript Algorithm 4.1**, comparing likelihood-center SM with tuned ridge PL. Its result table and analysis are separate from all estimator supplements.

| Named analysis | Results |
|---|---|
| P0 — main Algorithm 4.1 comparison | [Independent main report and 23-task table](../main/README.md) |
| E0 — supplementary center-estimator comparison | [Sharp, Fotakis and Efficient tables](../estimator_comparison/README.md) |
| B0 — supplementary global pair-sieve | [Construction identity and results](../global_sieve/README.md) |
| L0 — supplementary Sushi learning curves | [Design and interpretation](../../docs/predictive_learning.md#l0-sushi-ab-with-thirty-outer-partitions), [numeric results](learning.csv) |
| S0 — supplementary independent simulation curves | [Design and interpretation](../../docs/predictive_learning.md#s0-independent-data-with-fixed-r3-and-r10), [numeric results](synthetic.csv) |

The raw `primary.csv` is a reproducibility export containing several methods under one allocation-family key. Use the named reports above for scientific interpretation. [Raw field dictionary and exact method mapping](README.md#keys-and-method-identity) explain that storage convention. No saved fit, split or NLL has changed.
