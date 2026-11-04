# S4-T: constants selected separately for each training setting

[Repository](../../README.md) · [Protocol](PROTOCOL.md) · [Original S4](../section44/README.md) · [Every selected configuration](results/selected_parameters.md) · [All candidate scores](results/calibration_candidates.json) · [Depth and stopping parameters](results/execution.md)

This additional simulation asks whether choosing constants separately for each `(n,r,N)` changes the comparison with global Borda. Original S4 is preserved. Here N is **training** report count. The same group uses the same selected constants across repetitions and signal controls.

There are **82 parameter-selection groups, 90 signal settings, 1,800 independent training/validation draws and 9,000 independent training/test draws**. Candidate selection uses validation whole-ranking NLL; confirmation reports both held-out NLL and true-center Kendall error. Lower is better for both.

## Results against global Borda

The tables count settings by the sign of their mean paired difference. They are descriptive, not independent votes. The last columns use Holm-adjusted two-sided tests within each method/outcome family. Incomplete settings are excluded from these sign counts and retained below.

| Method | Outcome | Complete settings / 90 | Lower / equal / higher mean | Holm 5% lower / higher |
|---|---|---:|---:|---:|
| Efficient, per-setting | nll | 90/90 | 20 / 67 / 3 | 17 / 0 |
| Efficient, per-setting | kendall | 90/90 | 6 / 67 / 17 | 6 / 16 |
| Sharp, per-setting | nll | 90/90 | 42 / 46 / 2 | 35 / 0 |
| Sharp, per-setting | kendall | 90/90 | 0 / 46 / 44 | 0 / 43 |

**Global Borda is no longer uniformly best in these completed comparisons.** Per-setting Efficient reduces true-center Kendall error in six large-catalogue settings (n=512 or 2048), and also improves test NLL in all six. Both improvements survive the stated Holm correction. These six choices all have A=4, c_width=1/16 and K=1, and execute positive-depth hierarchies on every draw. Efficient still has higher mean center error in 17 other settings; this is a setting-dependent improvement, not domination.

**For Sharp, the answer depends on the outcome.** The selected Sharp configurations never have lower mean true-center Kendall error than Borda, but have lower mean test NLL in 42 settings (35 after Holm correction). All 46 equal settings select an inherited Borda fallback. Efficient has 23 positive-depth settings; its 67 equal settings consist of 63 Borda fallbacks and four zero-depth hierarchies. Sharp has nine positive-depth settings; its other 35 non-fallback settings run a terminal sieve without a pilot hierarchy.

A lower test NLL and a lower center error are different claims. Validation NLL does not use the true center and does not directly optimize the Kendall error reported by original S4. The NLL score includes a train-only fitted dispersion, so two different centers can have the same predictive loss when both fitted dispersions are zero.

## Where Efficient improves center recovery

These are all six settings with lower mean Kendall error. Relative reduction divides the paired mean reduction by the Borda mean error; it is descriptive. Every setting has beta=beta0=0.8.

| n,r,N | Borda mean Kendall error | Selected Efficient mean error | Relative reduction | Paired difference [95% CI] | Test NLL difference |
|---|---:|---:|---:|---|---:|
| 512,4,21802 | 6283.8 | 5920.1 | 5.79% | -363.64 [-415.16, -312.12] | -0.0047434 |
| 512,8,4672 | 4952 | 4580.3 | 7.51% | -371.7 [-412.04, -331.36] | -0.021769 |
| 512,16,1090 | 3980 | 3565.3 | 10.42% | -414.68 [-444.71, -384.65] | -0.13814 |
| 2048,8,14972 | 90871 | 85466 | 5.95% | -5405.6 [-5720, -5091.2] | -0.02274 |
| 2048,8,74861 | 40893 | 38519 | 5.81% | -2373.9 [-2603.8, -2144] | -0.0095454 |
| 2048,32,4226 | 27017 | 21986 | 18.62% | -5030.9 [-5149.4, -4912.4] | -0.41562 |

## Why predictive and center-error conclusions differ

The scored quantity is beta_hat times the test report inversion count plus log Z_r(beta_hat), averaged over test reports. Full-center Kendall error instead counts all inverted catalogue pairs once. The estimated dispersion and the displayed-set loss both matter; the two metrics need not order estimators the same way.

The largest NLL gains include very small training sets. With N=1, Borda exactly fits the observed report and the train-only dispersion estimate reaches the cap beta=10. For n=512,r=128,N=1, the selected Sharp center is less accurate but produces nearly uniform predictions: its mean fitted beta is about 0.002. The following saved-fit summaries expose this distinction. They are descriptive diagnostics, not additional tuning or a controlled dispersion ablation.

| n,r,N | Method | Mean fitted beta | beta=10 hits / 100 | Mean test NLL | Mean Kendall error |
|---|---|---:|---:|---:|---:|
| 12,3,4 | global_borda | 5.6969 | 48 | 7.7441 | 24.2 |
| 12,3,4 | efficient_per_setting | 1.4255 | 4 | 2.383 | 27.27 |
| 12,3,4 | sharp_per_setting | 0.24474 | 0 | 1.7832 | 32.51 |
| 512,128,1 | global_borda | 10 | 100 | 30656 | 49249 |
| 512,128,1 | efficient_per_setting | 10 | 100 | 30656 | 49249 |
| 512,128,1 | sharp_per_setting | 0.0020017 | 0 | 496.49 | 65072 |
| 2048,32,4226 | global_borda | 0.75083 | 0 | 39.584 | 27017 |
| 2048,32,4226 | efficient_per_setting | 0.76327 | 0 | 39.168 | 21986 |
| 2048,32,4226 | sharp_per_setting | 0.75083 | 0 | 39.584 | 27017 |

Predictive improvements are not confined to N=1: among the 53 settings with N>=20, Efficient has 14 lower-NLL means (13 Holm-supported), and Sharp has 11 (seven Holm-supported). These counts reuse the original 90-setting Holm adjustment. Nevertheless, the result is specific to the declared train-only beta fit on [0,10]; it does not establish that Sharp recovers the center better or remains preferable under another dispersion-fitting rule.

## Comparisons with the proof and original S4 configurations

All references below are refitted on the same new training draws; these are paired comparisons within S4-T, not subtraction of unrelated means from the old report.

| Per-setting method | Reference | Outcome | Complete pairs / 90 | Lower / equal / higher mean |
|---|---|---|---:|---:|
| efficient | efficient_proof | nll | 90/90 | 20 / 67 / 3 |
| efficient | efficient_proof | kendall | 90/90 | 6 / 67 / 17 |
| efficient | efficient_S4_locked | nll | 90/90 | 37 / 50 / 3 |
| efficient | efficient_S4_locked | kendall | 90/90 | 23 / 50 / 17 |
| sharp | sharp_proof | nll | 60/90 | 38 / 9 / 13 |
| sharp | sharp_proof | kendall | 60/90 | 39 / 9 / 12 |
| sharp | sharp_S4_locked | nll | 81/90 | 51 / 21 / 9 |
| sharp | sharp_S4_locked | kendall | 81/90 | 38 / 21 / 22 |

## What was selected

The search reuses the original anchored grid; values are not combined in a full Cartesian product. A controls the stopping threshold, c_width scales stage windows, K scales stage report batches, and c_terminal scales Sharp terminal W*. The [parameter table](results/selected_parameters.md) gives the numerical choices for all 82 groups. The unchanged [grid definition](../section44/design.py) and [saved protocol](results/protocol.json) enumerate every candidate.

Selection allows zero depth and explicitly recorded Borda fallbacks. Therefore a tuned method may equal Borda because it selected that branch, not because a multilevel hierarchy independently matched it. Exact-sieve resource failures are never replaced by Borda.

| Family | Selected candidate | Number of (n,r,N) groups |
|---|---|---:|
| efficient | anchor | 31 |
| efficient | anchor_A1 | 30 |
| efficient | anchor_A2 | 7 |
| efficient | anchor_A8 | 1 |
| efficient | anchor_K0.003 | 3 |
| efficient | anchor_K0.03 | 2 |
| efficient | anchor_K0.1 | 1 |
| efficient | anchor_K1.0 | 6 |
| efficient | anchor_width0.03125 | 1 |
| sharp | anchor | 19 |
| sharp | anchor_A1 | 37 |
| sharp | anchor_A128 | 5 |
| sharp | anchor_A16 | 3 |
| sharp | anchor_A2 | 1 |
| sharp | anchor_A256 | 6 |
| sharp | anchor_A64 | 1 |
| sharp | anchor_K0.03 | 3 |
| sharp | anchor_terminal0.015625 | 1 |
| sharp | anchor_terminal0.125 | 1 |
| sharp | anchor_terminal1 | 2 |
| sharp | proof | 2 |
| sharp | wide_anchor_terminal0.125 | 1 |

## Every held-out comparison

Each row is a signal setting; groups repeated across beta/beta0 controls share their candidate. Differences are **method minus Borda**. Brackets are pointwise 95% t intervals across independent confirmation draws. Depth counts successful fits with positive depth, out of 100. The full [CSV](results/paired_comparisons.csv) also gives MCSE, scaled differences and adjusted p values.

| n,r,N; beta/beta0 | Family | Candidate | Positive depth | Test NLL difference [95% CI] | NLL difference / log(r!) | Kendall difference [95% CI] |
|---|---|---|---:|---|---:|---|
| 8,2,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,2,1; 0.8/0.8 | sharp | anchor_A128 | 0 | -1.4812 [-2.7577, -0.2046] | -2.1369 | 0.93 [-0.12307, 1.9831] |
| 8,2,5; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,2,5; 0.8/0.8 | sharp | anchor | 0 | -2.7697 [-3.4276, -2.1119] | -3.9959 | 2.26 [1.1847, 3.3353] |
| 8,2,28; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,2,28; 0.8/0.8 | sharp | anchor | 0 | -0.020783 [-0.056618, 0.015052] | -0.029984 | 3.2 [2.3939, 4.0061] |
| 8,3,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,3,1; 0.8/0.8 | sharp | anchor_A256 | 0 | -8.3548 [-10.537, -6.1724] | -4.6629 | 2.08 [0.95343, 3.2066] |
| 8,3,9; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,3,9; 0.8/0.8 | sharp | anchor_A256 | 0 | -0.39279 [-0.69953, -0.08605] | -0.21922 | 4.73 [3.7875, 5.6725] |
| 8,4,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,4,1; 0.8/0.8 | sharp | anchor | 0 | -21.264 [-24.362, -18.167] | -6.691 | 2.9 [1.9691, 3.8309] |
| 8,4,4; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 8,4,4; 0.8/0.8 | sharp | anchor | 0 | -1.295 [-1.9625, -0.62756] | -0.40749 | 5.76 [4.6688, 6.8512] |
| 12,2,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 12,2,3; 0.8/0.8 | sharp | anchor | 0 | -3.4775 [-4.4397, -2.5153] | -5.017 | 4.14 [2.4977, 5.7823] |
| 12,2,13; 0.8/0.8 | efficient | anchor_A2 | 100 | -0.93723 [-1.2954, -0.57904] | -1.3521 | 1.62 [0.39076, 2.8492] |
| 12,2,13; 0.8/0.8 | sharp | anchor | 0 | -1.1471 [-1.5485, -0.74578] | -1.6549 | 5.96 [4.3637, 7.5563] |
| 12,2,66; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 12,2,66; 0.8/0.8 | sharp | anchor | 0 | -0.017743 [-0.036378, 0.00089201] | -0.025597 | 10.68 [9.0653, 12.295] |
| 12,3,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 12,3,1; 0.8/0.8 | sharp | anchor | 0 | -10.831 [-12.962, -8.6991] | -6.0448 | 2.84 [1.5044, 4.1756] |
| 12,3,4; 0.8/0.8 | efficient | anchor_A2 | 100 | -5.3611 [-6.7786, -3.9436] | -2.9921 | 3.07 [2.0672, 4.0728] |
| 12,3,4; 0.8/0.8 | sharp | anchor_A128 | 0 | -5.9609 [-7.4014, -4.5205] | -3.3269 | 8.31 [6.4968, 10.123] |
| 12,3,22; 0.8/0.8 | efficient | anchor_A8 | 100 | -0.047255 [-0.1045, 0.0099869] | -0.026374 | 7.83 [6.4707, 9.1893] |
| 12,3,22; 0.8/0.8 | sharp | anchor | 0 | -0.084891 [-0.15834, -0.011438] | -0.047378 | 13.43 [11.695, 15.165] |
| 12,4,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 12,4,1; 0.8/0.8 | sharp | anchor | 0 | -23.566 [-26.739, -20.392] | -7.4151 | 6.34 [4.6923, 7.9877] |
| 12,4,2; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 12,4,2; 0.8/0.8 | sharp | anchor | 0 | -16.447 [-19.659, -13.235] | -5.1752 | 8.16 [6.2367, 10.083] |
| 12,4,11; 0.8/0.8 | efficient | anchor | 100 | -0.057964 [-0.18469, 0.068767] | -0.018239 | 6.57 [5.3077, 7.8323] |
| 12,4,11; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,2,6; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,2,6; 0.8/0.8 | sharp | anchor_A128 | 0 | -3.3326 [-4.0682, -2.5971] | -4.808 | 6.74 [3.7094, 9.7706] |
| 16,2,24; 0.8/0.8 | efficient | anchor_A2 | 100 | -0.22484 [-0.33208, -0.1176] | -0.32438 | 9.46 [7.2491, 11.671] |
| 16,2,24; 0.8/0.8 | sharp | anchor | 0 | -0.29331 [-0.40364, -0.18299] | -0.42316 | 13.48 [10.831, 16.129] |
| 16,2,120; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,2,120; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,3,2; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,3,2; 0.8/0.8 | sharp | anchor | 0 | -11.75 [-13.722, -9.7777] | -6.5576 | 6.66 [4.7858, 8.5342] |
| 16,3,8; 0.8/0.8 | efficient | anchor_A2 | 100 | -1.2043 [-1.7097, -0.69894] | -0.67215 | 9.44 [7.3231, 11.557] |
| 16,3,8; 0.8/0.8 | sharp | anchor_A256 | 0 | -1.3723 [-1.8847, -0.85991] | -0.7659 | 17.48 [14.439, 20.521] |
| 16,3,40; 0.8/0.8 | efficient | anchor_A2 | 100 | 0.035506 [-0.01257, 0.083583] | 0.019816 | 18.98 [16.892, 21.068] |
| 16,3,40; 0.8/0.8 | sharp | anchor | 0 | 0.039489 [-0.0095937, 0.088571] | 0.022039 | 26.2 [23.446, 28.954] |
| 16,4,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 16,4,1; 0.8/0.8 | sharp | anchor | 0 | -25.473 [-28.701, -22.246] | -8.0154 | 5.66 [3.5944, 7.7256] |
| 16,4,4; 0.8/0.8 | efficient | anchor_A2 | 100 | -5.3756 [-7.256, -3.4953] | -1.6915 | 8.13 [6.5017, 9.7583] |
| 16,4,4; 0.8/0.8 | sharp | anchor_A128 | 0 | -5.8002 [-7.7349, -3.8654] | -1.8251 | 17.52 [14.877, 20.163] |
| 16,4,20; 0.8/0.8 | efficient | anchor | 100 | 0.066977 [-0.021152, 0.15511] | 0.021075 | 18.19 [16.168, 20.212] |
| 16,4,20; 0.8/0.8 | sharp | anchor_A2 | 100 | 0.056637 [-0.027822, 0.1411] | 0.017821 | 27.18 [24.446, 29.914] |
| 32,3,8; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,3,8; 0.8/0.8 | sharp | anchor | 0 | -4.1259 [-5.2281, -3.0237] | -2.3027 | 46.19 [40.334, 52.046] |
| 32,3,33; 0.8/0.8 | efficient | anchor_K0.003 | 100 | -0.15386 [-0.2247, -0.083034] | -0.085874 | 60.48 [53.86, 67.1] |
| 32,3,33; 0.8/0.8 | sharp | anchor | 0 | -0.21241 [-0.28515, -0.13967] | -0.11855 | 93.99 [85.508, 102.47] |
| 32,3,165; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,3,165; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,8,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,8,1; 0.8/0.8 | sharp | proof | 0 | -104.58 [-111.67, -97.487] | -9.8617 | 46.73 [39.082, 54.378] |
| 32,8,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,8,3; 0.8/0.8 | sharp | anchor_terminal0.125 | 100 | -12.189 [-15.96, -8.4168] | -1.1494 | 73.2 [67.544, 78.856] |
| 32,8,17; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 32,8,17; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,2,63; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,2,63; 0.8/0.8 | sharp | anchor_A16 | 0 | -0.89914 [-1.0144, -0.78388] | -1.2972 | 526.91 [470.33, 583.49] |
| 128,2,190; 0.8/0.8 | efficient | anchor_A2 | 100 | -0.16628 [-0.18891, -0.14364] | -0.23989 | 449.97 [405.02, 494.92] |
| 128,2,190; 0.8/0.8 | sharp | anchor_terminal0.015625 | 0 | -0.23792 [-0.26123, -0.21462] | -0.34325 | 825.61 [765.36, 885.86] |
| 128,2,381; 0.8/0.8 | efficient | anchor_K0.003 | 100 | -0.0808 [-0.092474, -0.069126] | -0.11657 | 938.54 [881.06, 996.02] |
| 128,2,381; 0.8/0.8 | sharp | anchor | 0 | -0.098298 [-0.10985, -0.086744] | -0.14181 | 1250.8 [1189.9, 1311.6] |
| 128,3,135; 0.8/0.8 | efficient | anchor_width0.03125 | 100 | -0.23014 [-0.26607, -0.1942] | -0.12844 | 1037.2 [981.12, 1093.2] |
| 128,3,135; 0.8/0.8 | sharp | anchor_A16 | 0 | -0.26536 [-0.30135, -0.22936] | -0.1481 | 1404.5 [1342.3, 1466.7] |
| 128,3,541; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,3,541; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,3,2709; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,3,2709; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,4,67; 0.8/0.8 | efficient | anchor_K0.003 | 100 | -0.52167 [-0.59506, -0.44828] | -0.16415 | 1140.4 [1089.6, 1191.3] |
| 128,4,67; 0.8/0.8 | sharp | anchor_A16 | 0 | -0.59994 [-0.67498, -0.5249] | -0.18878 | 1504.5 [1444.1, 1564.8] |
| 128,4,270; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,4,270; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,4,1354; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,4,1354; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,14; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,14; 0.8/0.8 | sharp | anchor_A256 | 0 | -4.7028 [-5.2192, -4.1865] | -0.44347 | 1584.5 [1524.2, 1644.8] |
| 128,8,15; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,15; 0.8/0.8 | sharp | anchor_A64 | 0 | -4.1347 [-4.7243, -3.5451] | -0.3899 | 1601 [1551.3, 1650.7] |
| 128,8,46; 0.8/0.8 | efficient | anchor_K0.1 | 100 | 0.14296 [0.019382, 0.26653] | 0.013481 | 463.72 [438.8, 488.64] |
| 128,8,46; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.4/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.4/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.8/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.8/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 1.6/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 1.6/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 1.6/1.6 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,58; 1.6/1.6 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,93; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,93; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,290; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,8,290; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,3; 0.8/0.8 | sharp | anchor_terminal1 | 100 | -75.945 [-89.857, -62.032] | -2.476 | 1132 [1067, 1197] |
| 128,16,7; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,7; 0.8/0.8 | sharp | anchor_K0.03 | 100 | -14.503 [-15.938, -13.069] | -0.47285 | 1261.1 [1225.5, 1296.7] |
| 128,16,13; 0.8/0.8 | efficient | anchor_K0.03 | 100 | -0.90072 [-1.4759, -0.32552] | -0.029366 | 1131.7 [1095, 1168.5] |
| 128,16,13; 0.8/0.8 | sharp | anchor_K0.03 | 100 | -0.64723 [-1.2647, -0.029794] | -0.021102 | 1615.7 [1571.5, 1659.9] |
| 128,16,22; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,22; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,45; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,45; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,67; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,16,67; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,32,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,32,1; 0.8/0.8 | sharp | anchor_A256 | 0 | -1839.3 [-1893.9, -1784.7] | -22.552 | 955.82 [925.63, 986.01] |
| 128,32,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,32,3; 0.8/0.8 | sharp | anchor_terminal1 | 100 | -84.972 [-93.098, -76.846] | -1.0419 | 1718.2 [1673.2, 1763.2] |
| 128,32,16; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 128,32,16; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,2180; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,2180; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,8721; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,8721; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,43605; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,3,43605; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,4,1090; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,4,1090; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,4,4360; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,4,4360; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,4,21802; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.0047434 [-0.0060149, -0.0034719] | -0.0014925 | -363.64 [-415.16, -312.12] |
| 512,4,21802; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,8,233; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,8,233; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,8,934; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,8,934; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,8,4672; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.021769 [-0.026048, -0.017489] | -0.0020528 | -371.7 [-412.04, -331.36] |
| 512,8,4672; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,16,54; 0.8/0.8 | efficient | anchor_K0.03 | 100 | -1.0239 [-1.3567, -0.69103] | -0.033382 | 19169 [18886, 19452] |
| 512,16,54; 0.8/0.8 | sharp | anchor_K0.03 | 100 | -0.61099 [-0.9721, -0.24988] | -0.01992 | 28751 [28420, 29081] |
| 512,16,218; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,16,218; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,16,1090; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.13814 [-0.15446, -0.12182] | -0.0045039 | -414.68 [-444.71, -384.65] |
| 512,16,1090; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,13; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,13; 0.8/0.8 | sharp | wide_anchor_terminal0.125 | 100 | -62.813 [-65.793, -59.832] | -0.77016 | 21278 [20970, 21586] |
| 512,32,52; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,52; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.4/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.4/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.8/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.8/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 1.6/0.4 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 1.6/0.4 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 1.6/1.6 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,32,263; 1.6/1.6 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,128,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,128,1; 0.8/0.8 | sharp | anchor_A128 | 0 | -30160 [-30573, -29746] | -60.756 | 15824 [15580, 16068] |
| 512,128,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,128,3; 0.8/0.8 | sharp | proof | 0 | -1254.6 [-1318.4, -1190.8] | -2.5273 | 36695 [36250, 37141] |
| 512,128,16; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 512,128,16; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,8,3743; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,8,3743; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,8,14972; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.02274 [-0.025311, -0.02017] | -0.0021444 | -5405.6 [-5720, -5091.2] |
| 2048,8,14972; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,8,74861; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.0095454 [-0.010668, -0.0084228] | -0.00090012 | -2373.9 [-2603.8, -2144] |
| 2048,8,74861; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,32,211; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,32,211; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,32,845; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,32,845; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,32,4226; 0.8/0.8 | efficient | anchor_K1.0 | 100 | -0.41562 [-0.43043, -0.40081] | -0.005096 | -5030.9 [-5149.4, -4912.4] |
| 2048,32,4226; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,512,1; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,512,1; 0.8/0.8 | sharp | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,512,3; 0.8/0.8 | efficient | anchor | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,512,3; 0.8/0.8 | sharp | anchor_A256 | 100 | -15373 [-16122, -14624] | -5.7233 | 3.3887e+05 [3.3659e+05, 3.4115e+05] |
| 2048,512,16; 0.8/0.8 | efficient | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |
| 2048,512,16; 0.8/0.8 | sharp | anchor_A1 | 0 | 0 [0, 0] | 0 | 0 [0, 0] |

## Training, selection and uncertainty

Each calibration draw contains N training reports and ceil(N/3) validation reports, at least one. Each confirmation draw contains a fresh N-report training set and an independent ceil(N/3)-report test set, sharing that draw's latent center. Sampling roles are disjoint; there is no reuse of calibration observations in confirmation and no train-plus-validation refit. The three roles have relative sizes N:ceil(N/3):ceil(N/3), but they are implemented as separate calibration and confirmation phases, not one reused three-way partition. No old S4 observations are split or reused. Tiny-N counts are rounded explicitly.

The original 25 Efficient and 35 Sharp anchored candidates are unchanged. For each candidate, train-only beta is the constrained conditional MLE on [0,10]. Validation ranks candidates by mean whole-ranking NLL, giving each signal cell in a group equal weight. All 20 calibration fits per signal must succeed; there is no positive-depth requirement. Ties use candidate name. The selection is shared across signal controls, so no true beta or beta0 is used as a selection key. The supplied beta0 remains an input to the original schedule.

For metric X, calculate D_b = X_method,b - X_reference,b for each independent confirmation draw. The mean is sum(D_b)/100, MCSE is sample_sd(D_b)/10, and the pointwise interval is mean(D) ± t_(99,0.975) MCSE. Draws are independent Monte Carlo replicates; this motivates the approximate Student-t interval. Intervals condition on the locked constants and omit variability from repeating the selection stage. Holm adjustment controls familywise error within the stated complete-cell comparison family, conditional on valid pointwise p values.

## Interpretation limits

- Results describe the tested grid, generator, supplied bounds and computational budgets. They do not establish an optimal tuning rule or a minimax rate.
- Selection has 20 independent training/validation draws per signal setting, so this is simulation-based group calibration, not ordinary tuning from one real dataset.
- Relative to original S4, both the selection target (validation NLL rather than oracle center risk) and the activity requirement change, along with the grouping of constants. Differences from the original locked configuration cannot be attributed solely to per-setting tuning.
- Borda-equivalent branches remain labeled. Improvement in computation or positive depth does not by itself establish lower prediction or center error.
- The candidate grid is anchored rather than Cartesian. A failure to beat Borda does not exclude other constants or the separately proposed adaptive-eta algorithms.

The empirical constants do not automatically inherit the original uniform risk guarantees.

## Reproduction and files

The preregistered [protocol commit](https://github.com/hyj55/mallowsmodel/commit/2d604ab212cdff13231fa02e56b2206ad474fcaa) predates outcome generation. The [parameter-selection commit](https://github.com/hyj55/mallowsmodel/commit/ac2c1dd68f351870eafe3245f18b4c3f8fc30a93) predates confirmation generation. `results/protocol.json` gives every setting and candidate. `selection.json` records one choice per family/group. `calibration_candidates.json` retains rejected candidates. `calibration_fits.csv.gz` and `confirmation_fits.csv.gz` give logical method-level rows; identical computations have explicit shared fit keys. `summary.csv` and `paired_comparisons.csv` contain all aggregate results.

Lossless draw archives retain fitted orders, data hashes, plan/branch and failure receipts. Raw reports regenerate exactly from root seed 202611040 and the saved stream coordinates. The verification program checks original S4 preservation, selection replay, summaries and a deterministic training/holdout replay sample.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONINTMAXSTRDIGITS=0
python -m pytest -q experiments/section44_per_setting/test_experiment.py
python experiments/section44_per_setting/run.py calibrate
python experiments/section44_per_setting/run.py confirm
python experiments/section44_per_setting/report.py
python experiments/section44_per_setting/verify.py
```
