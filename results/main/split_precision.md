# Precision of five random allocations

[Main results](README.md) · [Numeric precision table](split_precision.csv) · [Uncertainty definitions](../../docs/uncertainty.md)

The empirical repeated-partition budget is B=5, using fixed IDs 0–4. Five is a computation choice, not a guarantee of small error and not a preregistered significance threshold. The allocation indices are selected without ranking their outcomes. The displayed mean averages separately fitted models' losses; it is not the loss of an ensemble.

```math
\overline{\Delta}=\frac{1}{5}\sum_{b=1}^{5}\Delta_b,\qquad
s_\Delta^2=\frac{1}{4}\sum_{b=1}^{5}(\Delta_b-\overline{\Delta})^2,\qquad
\widehat{\mathrm{MCSE}}=\frac{s_\Delta}{\sqrt{5}}.
```

Conditional on fixed data and independently randomized allocations, this estimates the standard error of Monte Carlo integration over allocations. It is not a population CI. Five draws give a noisy variance estimate with four degrees of freedom; apparent precision is not guaranteed to persist in further allocations. Compare MCSE with the model difference, not with an absolute label such as "small". Interpolated split quantiles retained in machine tables are descriptive and especially unstable with five values. The table below uses observed min/max instead.

| Component | Role of the five allocations |
|---|---|
| P0 | Average main NLL/delta; MCSE; finite-fit and exact-center counts |
| E0/B0 | Supplementary estimator means and availability; B0 aliases are not extra repetitions |
| L0 | Each training budget averages five aligned outer tests; budgets are nested and dependent |
| P1 | Five confirmation scores and descriptive diagnostics per task; no inner bootstrap |
| G1 | Five within-group splits per training fraction and five whole-group holdouts |
| Full-data features | One full-data feature value is joined to the five-allocation P0 mean |

The 2,000 bootstrap draws **inside** an eligible P0/E0/L0 split are a different resampling operation and remain 2,000. Simulations generate fresh datasets and keep their independent-repetition designs. Fixed diagnostic allocations and chronological forecasts are not converted into random five-fold or five-shuffle experiments.

Raw and scaled differences appear together below. Scaling divides the difference, MCSE, SD and range endpoints by the task's fixed log(r!); it does not add repetitions or change the uncertainty target. Numeric CSV ratios are not multiplied by 100.

| Task | Mean delta | Delta / log(r!) | MCSE | Scaled MCSE | Smallest split delta | Largest split delta |
|---|---|---|---|---|---|---|
| Dots 2013, gap 3 | -0.02170 | -0.00683 | 0.00576 | 0.00181 | -0.03338 | -0.00066 |
| Dots 2013, gap 5 | -0.00998 | -0.00314 | 0.00413 | 0.00130 | -0.01899 | 0.00544 |
| Dots 2013, gap 7 | -0.00189 | -0.00059 | 0.00541 | 0.00170 | -0.01241 | 0.01803 |
| Dots 2013, gap 9 | -0.04415 | -0.01389 | 0.00337 | 0.00106 | -0.05398 | -0.03505 |
| Puzzle, minimum 11 steps | -0.01042 | -0.00328 | 0.00294 | 0.00092 | -0.01678 | -0.00197 |
| Puzzle, minimum 5 steps | -0.06934 | -0.02182 | 0.00523 | 0.00165 | -0.08849 | -0.05774 |
| Puzzle, minimum 7 steps | -0.02090 | -0.00658 | 0.01363 | 0.00429 | -0.07048 | 0.00933 |
| Puzzle, minimum 9 steps | -0.01530 | -0.00481 | 0.00906 | 0.00285 | -0.04358 | 0.01294 |
| Beans | 0.01333 | 0.00744 | 0.01001 | 0.00559 | -0.01041 | 0.04992 |
| Dots 2024 A r2 | 0.04426 | 0.06385 | 0.01430 | 0.02063 | -0.00344 | 0.08493 |
| Dots 2024 A r3 | 0.12868 | 0.07182 | 0.02169 | 0.01210 | 0.06809 | 0.19688 |
| Dots 2024 A r5 | 0.04176 | 0.00872 | 0.03857 | 0.00806 | -0.06567 | 0.14993 |
| Dots 2024 A r6 | 0.08479 | 0.01289 | 0.04061 | 0.00617 | -0.03252 | 0.19261 |
| Dots 2024 B r2 | 0.13836 | 0.19961 | 0.01780 | 0.02568 | 0.09140 | 0.17874 |
| Dots 2024 B r3 | 0.11545 | 0.06443 | 0.01852 | 0.01034 | 0.06331 | 0.17217 |
| Dots 2024 B r5 | 0.05113 | 0.01068 | 0.02977 | 0.00622 | -0.04317 | 0.13347 |
| Dots 2024 B r6 | -0.01824 | -0.00277 | 0.04181 | 0.00636 | -0.17815 | 0.05570 |
| PatrasIQ cost | 0.33462 | 0.05086 | 0.04120 | 0.00626 | 0.23510 | 0.48620 |
| PatrasIQ population | 0.10186 | 0.01548 | 0.06354 | 0.00966 | -0.10239 | 0.21020 |
| Sounds | 0.00761 | 0.01098 | 0.00724 | 0.01044 | -0.00846 | 0.03151 |
| Sushi A | 0.02711 | 0.00179 | 0.00870 | 0.00058 | 0.00606 | 0.05124 |
| Sushi B | -0.00398 | -0.00026 | 0.00657 | 0.00044 | -0.02350 | 0.01349 |
| Wheat | 0.14126 | 0.07884 | 0.02133 | 0.01190 | 0.09595 | 0.21042 |
