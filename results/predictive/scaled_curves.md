# L0/S0: raw and uniform-reference-scaled differences

[Design and uncertainty](../../docs/predictive_learning.md) · [Metric definition](../../docs/criteria.md#uniform-reference-scaled-loss-difference) · [Per-repetition scores and conditional intervals](scaled_curve_scores.csv.gz)

Delta is each SM estimator's NLL minus paired PL NLL; negative favors SM. The adjacent ratio divides by log(r!), the loss of uniform ranking on the actual display. Ratios are dimensionless, not percentages or accuracies. Raw scores, fitted parameters, test reports, repetitions and availability are unchanged. All delta statistics and existing interval endpoints in the linked numeric views have matching `delta_uniform*` columns. NA stays NA.

## L0: Sushi learning

The table shows likelihood-center SM versus PL; the [all-estimator CSV](learning_comparison.csv) additionally preserves Sharp, Fotakis, admitted Efficient fallback and the global-sieve alias. These curve estimators retain their stated identities; this is not the independently admitted six-method E0 table. N=4000 is the linked P0/E0 endpoint, not another fit. Each point uses five allocations and r=10. MCSE describes fixed-data partition precision, not population sampling uncertainty. All points share the divisor log(10!), so scaling changes neither within-curve trends nor the ordering of Sushi A/B gaps. Conditional test-unit bootstrap endpoints are in the per-repetition view; no bootstrap endpoints are averaged into a curve-mean CI.

| Task | Development N | Available / 5 | Mean delta | Delta / log(r!) | MCSE | Scaled MCSE |
|---|---|---|---|---|---|---|
| Sushi A | 20 | 5 | -0.11349 | -0.00751 | 0.09465 | 0.00627 |
| Sushi A | 50 | 5 | -0.03070 | -0.00203 | 0.09429 | 0.00624 |
| Sushi A | 100 | 5 | 0.02638 | 0.00175 | 0.01392 | 0.00092 |
| Sushi A | 300 | 5 | 0.03691 | 0.00244 | 0.00645 | 0.00043 |
| Sushi A | 1000 | 5 | 0.03412 | 0.00226 | 0.00800 | 0.00053 |
| Sushi A | 3000 | 5 | 0.02962 | 0.00196 | 0.00711 | 0.00047 |
| Sushi B | 20 | 5 | 3.24335 | 0.21473 | 0.36589 | 0.02422 |
| Sushi B | 50 | 5 | 0.91086 | 0.06030 | 0.11107 | 0.00735 |
| Sushi B | 100 | 5 | 0.36112 | 0.02391 | 0.03252 | 0.00215 |
| Sushi B | 300 | 5 | 0.07580 | 0.00502 | 0.02017 | 0.00134 |
| Sushi B | 1000 | 5 | 0.03123 | 0.00207 | 0.00771 | 0.00051 |
| Sushi B | 3000 | 5 | -0.00221 | -0.00015 | 0.00941 | 0.00062 |
| Sushi A | 4000 | 5 | 0.02711 | 0.00179 | 0.00870 | 0.00058 |
| Sushi B | 4000 | 5 | -0.00398 | -0.00026 | 0.00657 | 0.00044 |

## S0: independent simulations

The table shows likelihood-center SM versus PL; the [all-estimator CSV](synthetic_comparison.csv) retains every estimator and unavailable cell. Each cell has twenty independent training/test draws. All use r=3, including the growing-catalogue n curve, so the divisor is always log(3!), not log(n!). The intervals are the existing pointwise Student-t 95% intervals for the independent-repetition mean. Divide each endpoint by log(3!) to obtain the scaled interval. This is a change of units, not an additional inference; it does not make these simulated populations interchangeable with empirical tasks.

| Generating law | n | Development N | Available / 20 | Mean delta | Delta / log(r!) | Raw 95% interval | Scaled 95% interval |
|---|---|---|---|---|---|---|---|
| synthetic_pl | 6 | 100 | 20 | 0.03693 | 0.02061 | [+0.01634, +0.05751] | [+0.00912, +0.03210] |
| synthetic_pl | 10 | 20 | 20 | 0.22947 | 0.12807 | [+0.10232, +0.35662] | [+0.05711, +0.19903] |
| synthetic_pl | 10 | 100 | 20 | 0.06633 | 0.03702 | [+0.04937, +0.08330] | [+0.02755, +0.04649] |
| synthetic_pl | 10 | 500 | 20 | 0.05137 | 0.02867 | [+0.04513, +0.05761] | [+0.02519, +0.03215] |
| synthetic_pl | 16 | 100 | 20 | 0.11073 | 0.06180 | [+0.09765, +0.12380] | [+0.05450, +0.06910] |
| synthetic_pl | 32 | 100 | 20 | 0.25069 | 0.13991 | [+0.21686, +0.28452] | [+0.12103, +0.15879] |
| synthetic_sm | 6 | 100 | 20 | -0.06870 | -0.03834 | [-0.08233, -0.05507] | [-0.04595, -0.03074] |
| synthetic_sm | 10 | 20 | 20 | 0.24261 | 0.13540 | [+0.12065, +0.36457] | [+0.06734, +0.20347] |
| synthetic_sm | 10 | 100 | 20 | -0.04265 | -0.02381 | [-0.06706, -0.01825] | [-0.03743, -0.01019] |
| synthetic_sm | 10 | 500 | 20 | -0.06156 | -0.03436 | [-0.06550, -0.05762] | [-0.03656, -0.03216] |
| synthetic_sm | 16 | 100 | 20 | 0.00030 | 0.00017 | [-0.02132, +0.02191] | [-0.01190, +0.01223] |
| synthetic_sm | 32 | 100 | 20 | 0.20505 | 0.11444 | [+0.13709, +0.27302] | [+0.07651, +0.15238] |
