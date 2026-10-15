# Three full-data characteristics beside predictive performance

[Feature definitions and support](README.md) · [Combined CSV](predictive_comparison.csv) · [Primary fitting design](../../docs/predictive_comparison.md) · [Unpenalized and detailed feature tables](comparison.md)

All three characteristics use every eligible report and the same saved full-data reference center. They are unchanged data descriptions. P0 NLL uses separately trained predictors and outer-test reports; none of these full-data characteristics selects its center, penalty or training split. Negative delta favors SM. The comparison is descriptive, not a causal explanation or an independent model test.

H is equal-gap pair-rate dispersion; T−b is within-display/shell TV minus a nominal iid-uniform sampling reference; C is within-pair variation across displays; gamma is its gap slope; R is the one-item replacement effect (distinct from the report-size upper bound also denoted R). H, C and R are in percentage points. Undefined contrasts remain NA. The nominal shell reference is not a calibrated significance test. Sparse single-report cells can produce large apparent dispersion.

| Task | NLL target | H (pp) | T−b | C (pp) | gamma | R (pp) | SM−PL NLL |
|---|---|---|---|---|---|---|---|
| beans | P0 | 6.61497 | -0.01107 | 17.13674 | 0.02737 | 2.66309 | 0.01333 |
| sushi_a | P0 | 7.35720 | 0.00016 | NA | NA | NA | 0.02711 |
| sushi_b | P0 | 14.19628 | 0.00000 | 45.57641 | 0.00765 | NA | -0.00398 |
| 00024-00000001 | P0 | 1.95893 | 0.02691 | NA | NA | NA | -0.02170 |
| 00024-00000002 | P0 | 0.99807 | 0.01197 | NA | NA | NA | -0.00998 |
| 00024-00000003 | P0 | 1.45129 | 0.02347 | NA | NA | NA | -0.00189 |
| 00024-00000004 | P0 | 1.02395 | 0.01306 | NA | NA | NA | -0.04415 |
| 00025-00000001 | P0 | 2.97026 | 0.01010 | NA | NA | NA | -0.01042 |
| 00025-00000002 | P0 | 2.62770 | 0.03227 | NA | NA | NA | -0.06934 |
| 00025-00000003 | P0 | 1.92018 | 0.02162 | NA | NA | NA | -0.02090 |
| 00025-00000004 | P0 | 3.33792 | 0.02969 | NA | NA | NA | -0.01530 |
| dots2024_A_r2 | P0 | 27.33537 | NA | NA | NA | NA | 0.04426 |
| dots2024_A_r3 | P0 | 27.17263 | 0.00000 | 30.88856 | 0.01977 | 3.15152 | 0.12868 |
| dots2024_A_r5 | P0 | 23.56071 | 0.00000 | 39.10368 | 0.01912 | 5.63380 | 0.04176 |
| dots2024_A_r6 | P0 | 21.74475 | 0.00007 | 39.93137 | 0.02267 | 5.26316 | 0.08479 |
| dots2024_B_r2 | P0 | 33.45810 | NA | NA | NA | NA | 0.13836 |
| dots2024_B_r3 | P0 | 32.88251 | -0.00725 | 32.63710 | 0.06278 | 4.64807 | 0.11545 |
| dots2024_B_r5 | P0 | 25.34492 | 0.00000 | 41.94244 | 0.03906 | -0.97087 | 0.05113 |
| dots2024_B_r6 | P0 | 23.36043 | -0.00000 | 43.53016 | 0.03015 | -33.33333 | -0.01824 |
| wheat | P0 | 19.14677 | 0.01400 | 35.83864 | 0.07657 | 7.55789 | 0.14126 |
| sounds | P0 | 9.37103 | NA | NA | NA | NA | 0.00761 |
| patras_cost | P0 | 16.45112 | 0.00645 | 14.16265 | 0.01893 | NA | 0.33462 |
| patras_population | P0 | 18.34738 | 0.00224 | 14.34192 | 0.03944 | NA | 0.10186 |
| atp_2010 | T1_chronological | 36.21983 | NA | NA | NA | NA | 0.00347 |
| atp_2011 | T1_chronological | 35.41252 | NA | NA | NA | NA | 0.02657 |
| atp_2012 | T1_chronological | 34.56174 | NA | NA | NA | NA | 0.03568 |
| atp_2013 | T1_chronological | 35.67651 | NA | NA | NA | NA | 0.04438 |
| atp_2014 | T1_chronological | 36.05044 | NA | NA | NA | NA | 0.01526 |
| atp_2015 | T1_chronological | 35.34010 | NA | NA | NA | NA | 0.04083 |
| atp_2016 | T1_chronological | 35.83199 | NA | NA | NA | NA | 0.02976 |
| atp_2017 | T1_chronological | 37.18436 | NA | NA | NA | NA | 0.01181 |
| atp_2018 | T1_chronological | 37.34418 | NA | NA | NA | NA | 0.01439 |
| atp_2019 | T1_chronological | 37.70101 | NA | NA | NA | NA | 0.02331 |

The CSV preserves all support counts, feature statuses and supplementary NLL fields, alongside clearly prefixed `primary_*` columns. P0 averages five 80/20 fits; ATP retains T1’s chronological target and is not added to P0. Raw NLL gaps have different scales across r. Shared respondents, task mixtures and unmeasured season/assessor composition prevent an interpretation as independent causal evidence.
