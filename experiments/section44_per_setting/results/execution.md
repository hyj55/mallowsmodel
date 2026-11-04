# S4-T execution and first-round parameters

[Main report](../README.md) · [All numeric parameters](execution.csv)

Rows group identical signal setting, method, status, depth and reason across repetitions. First-round w1 and M1 use the initial candidate resolution and are formula diagnostics; they do not mean that a stopped round consumed reports. N is training count. The CSV also gives beta0, A, K, both window coefficients, initial and selected eta, lambda, pilot report budget, and Sharp W*. Full candidate schedules remain in draw archives. Pilot depth and terminal-sieve success are separate: a resource failure can follow either zero or positive pilot depth. Positive-depth controls are included for context.

| Setting | Method | Contexts | Status | Depth | Reason | n=m0 | r | N | Initial w1 | Initial M1 | floor(N/2) |
|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|
| n12-r2-N13-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 12 | 2 | 13 | 13 | 62237456 | 6 |
| n12-r2-N13-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 2 | 13 | 1 | 27 | 6 |
| n12-r2-N13-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 12 | 2 | 13 | 1 | 1 | 6 |
| n12-r2-N13-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 12 | 2 | 13 | 23 | 28724980 | 6 |
| n12-r2-N13-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 2 | 13 | 2 | 5 | 6 |
| n12-r2-N13-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 2 | 13 | 2 | 1 | 6 |
| n12-r2-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 12 | 2 | 3 | 39 | 12706504 | 1 |
| n12-r2-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 12 | 2 | 3 | 3 | 6 | 1 |
| n12-r2-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 12 | 2 | 3 | 3 | 1 | 1 |
| n12-r2-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 2 | 3 | 23 | 25413008 | 1 |
| n12-r2-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 2 | 3 | 2 | 4 | 1 |
| n12-r2-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 2 | 3 | 2 | 1 | 1 |
| n12-r2-N66-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 12 | 2 | 66 | 5 | 379305996 | 33 |
| n12-r2-N66-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 12 | 2 | 66 | 1 | 161 | 33 |
| n12-r2-N66-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 12 | 2 | 66 | 1 | 6 | 33 |
| n12-r2-N66-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 12 | 2 | 66 | 23 | 34482364 | 33 |
| n12-r2-N66-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 2 | 66 | 2 | 5 | 33 |
| n12-r2-N66-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 2 | 66 | 2 | 1 | 33 |
| n12-r3-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 12 | 3 | 1 | 39 | 4235502 | 0 |
| n12-r3-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 12 | 3 | 1 | 3 | 2 | 0 |
| n12-r3-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 12 | 3 | 1 | 3 | 1 | 0 |
| n12-r3-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 3 | 1 | 14 | 16942005 | 0 |
| n12-r3-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 3 | 1 | 1 | 3 | 0 |
| n12-r3-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 3 | 1 | 1 | 1 | 0 |
| n12-r3-N22-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 12 | 3 | 22 | 5 | 126435332 | 11 |
| n12-r3-N22-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 12 | 3 | 22 | 1 | 54 | 11 |
| n12-r3-N22-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 12 | 3 | 22 | 1 | 2 | 11 |
| n12-r3-N22-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 12 | 3 | 22 | 14 | 22988243 | 11 |
| n12-r3-N22-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 3 | 22 | 1 | 4 | 11 |
| n12-r3-N22-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 3 | 22 | 1 | 1 | 11 |
| n12-r3-N4-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 12 | 3 | 4 | 14 | 18992218 | 2 |
| n12-r3-N4-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 3 | 4 | 1 | 9 | 2 |
| n12-r3-N4-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 12 | 3 | 4 | 1 | 1 | 2 |
| n12-r3-N4-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 3 | 4 | 14 | 18992218 | 2 |
| n12-r3-N4-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 3 | 4 | 1 | 3 | 2 |
| n12-r3-N4-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 3 | 4 | 1 | 1 | 2 |
| n12-r4-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 1 | 23 | 4450053 | 0 |
| n12-r4-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 1 | 2 | 2 | 0 |
| n12-r4-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 1 | 2 | 1 | 0 |
| n12-r4-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 4 | 1 | 11 | 13350158 | 0 |
| n12-r4-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 4 | 1 | 1 | 2 | 0 |
| n12-r4-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 4 | 1 | 1 | 1 | 0 |
| n12-r4-N11-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 12 | 4 | 11 | 5 | 63217666 | 5 |
| n12-r4-N11-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 12 | 4 | 11 | 1 | 27 | 5 |
| n12-r4-N11-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=noncontracting | 12 | 4 | 11 | 1 | 1 | 5 |
| n12-r4-N11-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 4 | 11 | 11 | 17241182 | 5 |
| n12-r4-N11-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 4 | 11 | 1 | 3 | 5 |
| n12-r4-N11-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 12 | 4 | 11 | 1 | 1 | 5 |
| n12-r4-N2-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 2 | 14 | 9496109 | 1 |
| n12-r4-N2-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 2 | 1 | 5 | 1 |
| n12-r4-N2-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 12 | 4 | 2 | 1 | 1 | 1 |
| n12-r4-N2-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 12 | 4 | 2 | 11 | 14244164 | 1 |
| n12-r4-N2-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 12 | 4 | 2 | 1 | 3 | 1 |
| n12-r4-N2-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 12 | 4 | 2 | 1 | 1 | 1 |
| n128-r16-N13-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 13 | 32 | 80952524 | 6 |
| n128-r16-N13-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 16 | 13 | 2 | 35 | 6 |
| n128-r16-N13-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 128 | 16 | 13 | 2 | 4 | 6 |
| n128-r16-N13-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 13 | 42 | 49816938 | 6 |
| n128-r16-N13-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 16 | 13 | 3 | 8 | 6 |
| n128-r16-N13-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 128 | 16 | 13 | 3 | 3 | 6 |
| n128-r16-N22-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 22 | 23 | 144959677 | 11 |
| n128-r16-N22-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 16 | 22 | 2 | 62 | 11 |
| n128-r16-N22-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 16 | 22 | 2 | 3 | 11 |
| n128-r16-N22-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 22 | 42 | 52712610 | 11 |
| n128-r16-N22-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 16 | 22 | 3 | 8 | 11 |
| n128-r16-N22-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 16 | 22 | 3 | 1 | 11 |
| n128-r16-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 3 | 77 | 15819994 | 1 |
| n128-r16-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 3 | 5 | 7 | 1 |
| n128-r16-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 3 | 5 | 1 | 1 |
| n128-r16-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 3 | 42 | 42186650 | 1 |
| n128-r16-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 16 | 3 | 3 | 6 | 1 |
| n128-r16-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 128 | 16 | 3 | 3 | 1 | 1 |
| n128-r16-N45-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 45 | 16 | 318979489 | 22 |
| n128-r16-N45-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 16 | 45 | 1 | 135 | 22 |
| n128-r16-N45-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 16 | 45 | 1 | 5 | 22 |
| n128-r16-N45-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 45 | 42 | 56707465 | 22 |
| n128-r16-N45-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 16 | 45 | 3 | 8 | 22 |
| n128-r16-N45-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 16 | 45 | 3 | 1 | 22 |
| n128-r16-N67-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 67 | 13 | 493671479 | 33 |
| n128-r16-N67-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 16 | 67 | 1 | 209 | 33 |
| n128-r16-N67-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 16 | 67 | 1 | 7 | 33 |
| n128-r16-N67-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 67 | 42 | 58945849 | 33 |
| n128-r16-N67-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 16 | 67 | 3 | 9 | 33 |
| n128-r16-N67-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 16 | 67 | 3 | 1 | 33 |
| n128-r16-N7-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 7 | 45 | 40678008 | 3 |
| n128-r16-N7-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 7 | 3 | 18 | 3 |
| n128-r16-N7-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 16 | 7 | 3 | 1 | 3 |
| n128-r16-N7-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 16 | 7 | 42 | 46489152 | 3 |
| n128-r16-N7-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 16 | 7 | 3 | 7 | 3 |
| n128-r16-N7-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 128 | 16 | 7 | 3 | 2 | 3 |
| n128-r2-N190-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 2 | 190 | 117 | 932725574 | 95 |
| n128-r2-N190-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 2 | 190 | 8 | 395 | 95 |
| n128-r2-N190-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 128 | 2 | 190 | 8 | 14 | 95 |
| n128-r2-N190-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 2 | 190 | 255 | 314181246 | 95 |
| n128-r2-N190-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 2 | 190 | 16 | 45 | 95 |
| n128-r2-N190-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 2 | 190 | 16 | 5 | 95 |
| n128-r2-N381-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 2 | 381 | 74 | 2022226807 | 190 |
| n128-r2-N381-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 128 | 2 | 381 | 5 | 855 | 190 |
| n128-r2-N381-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 128 | 2 | 381 | 5 | 9 | 190 |
| n128-r2-N381-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 2 | 381 | 255 | 339691643 | 190 |
| n128-r2-N381-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 2 | 381 | 16 | 48 | 190 |
| n128-r2-N381-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 2 | 381 | 16 | 5 | 190 |
| n128-r2-N63-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 2 | 63 | 258 | 278189226 | 31 |
| n128-r2-N63-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 2 | 63 | 17 | 118 | 31 |
| n128-r2-N63-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 2 | 63 | 17 | 4 | 31 |
| n128-r2-N63-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 2 | 63 | 255 | 282604928 | 31 |
| n128-r2-N63-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 2 | 63 | 16 | 40 | 31 |
| n128-r2-N63-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 2 | 63 | 16 | 4 | 31 |
| n128-r3-N135-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 3 | 135 | 71 | 721575834 | 67 |
| n128-r3-N135-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 128 | 3 | 135 | 5 | 305 | 67 |
| n128-r3-N135-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 128 | 3 | 135 | 3 | 11 | 67 |
| n128-r3-N135-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 3 | 135 | 154 | 228053597 | 67 |
| n128-r3-N135-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 3 | 135 | 10 | 33 | 67 |
| n128-r3-N135-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 3 | 135 | 10 | 4 | 67 |
| n128-r3-N2709-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 3 | 2709 | 13 | 19981070965 | 1354 |
| n128-r3-N2709-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 3 | 2709 | 1 | 8446 | 1354 |
| n128-r3-N2709-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 3 | 2709 | 1 | 282 | 1354 |
| n128-r3-N2709-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 3 | 2709 | 154 | 314701254 | 1354 |
| n128-r3-N2709-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 3 | 2709 | 10 | 45 | 1354 |
| n128-r3-N2709-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 3 | 2709 | 10 | 5 | 1354 |
| n128-r3-N541-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 3 | 541 | 31 | 3383489244 | 270 |
| n128-r3-N541-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 128 | 3 | 541 | 2 | 1431 | 270 |
| n128-r3-N541-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 3 | 541 | 2 | 48 | 270 |
| n128-r3-N541-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 3 | 541 | 154 | 266843268 | 270 |
| n128-r3-N541-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 3 | 541 | 10 | 38 | 270 |
| n128-r3-N541-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 3 | 541 | 10 | 4 | 270 |
| n128-r32-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 1 | 63 | 5470997 | 0 |
| n128-r32-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 1 | 4 | 3 | 0 |
| n128-r32-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 1 | 4 | 1 | 0 |
| n128-r32-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 32 | 1 | 27 | 21883987 | 0 |
| n128-r32-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 32 | 1 | 2 | 4 | 0 |
| n128-r32-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 32 | 1 | 2 | 1 | 0 |
| n128-r32-N16-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 32 | 16 | 13 | 117745006 | 8 |
| n128-r32-N16-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 32 | 16 | 1 | 50 | 8 |
| n128-r32-N16-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 32 | 16 | 1 | 2 | 8 |
| n128-r32-N16-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 32 | 16 | 27 | 29436252 | 8 |
| n128-r32-N16-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 32 | 16 | 2 | 5 | 8 |
| n128-r32-N16-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 32 | 16 | 2 | 1 | 8 |
| n128-r32-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 3 | 32 | 18584761 | 1 |
| n128-r32-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 3 | 2 | 8 | 1 |
| n128-r32-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 32 | 3 | 2 | 1 | 1 |
| n128-r32-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 32 | 3 | 27 | 24779682 | 1 |
| n128-r32-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 32 | 3 | 2 | 4 | 1 |
| n128-r32-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 128 | 32 | 3 | 2 | 1 | 1 |
| n128-r4-N1354-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 4 | 1354 | 13 | 9986495507 | 677 |
| n128-r4-N1354-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 4 | 1354 | 1 | 4221 | 677 |
| n128-r4-N1354-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 4 | 1354 | 1 | 141 | 677 |
| n128-r4-N1354-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 4 | 1354 | 116 | 236017620 | 677 |
| n128-r4-N1354-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 4 | 1354 | 8 | 34 | 677 |
| n128-r4-N1354-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 4 | 1354 | 8 | 4 | 677 |
| n128-r4-N270-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 4 | 270 | 31 | 1688276355 | 135 |
| n128-r4-N270-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 128 | 4 | 270 | 2 | 714 | 135 |
| n128-r4-N270-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 4 | 270 | 2 | 24 | 135 |
| n128-r4-N270-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 4 | 270 | 116 | 200092013 | 135 |
| n128-r4-N270-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 4 | 270 | 8 | 29 | 135 |
| n128-r4-N270-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 4 | 270 | 8 | 3 | 135 |
| n128-r4-N67-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 4 | 67 | 72 | 357809921 | 33 |
| n128-r4-N67-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 128 | 4 | 67 | 5 | 152 | 33 |
| n128-r4-N67-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 128 | 4 | 67 | 5 | 2 | 33 |
| n128-r4-N67-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 4 | 67 | 116 | 170894291 | 33 |
| n128-r4-N67-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 128 | 4 | 67 | 8 | 25 | 33 |
| n128-r4-N67-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 4 | 67 | 8 | 3 | 33 |
| n128-r8-N14-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 14 | 73 | 74550460 | 7 |
| n128-r8-N14-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 14 | 5 | 32 | 7 |
| n128-r8-N14-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 14 | 5 | 2 | 7 |
| n128-r8-N14-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 14 | 67 | 85200526 | 7 |
| n128-r8-N14-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 8 | 14 | 5 | 13 | 7 |
| n128-r8-N14-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 8 | 14 | 5 | 2 | 7 |
| n128-r8-N15-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 15 | 70 | 80510624 | 7 |
| n128-r8-N15-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 15 | 5 | 35 | 7 |
| n128-r8-N15-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 128 | 8 | 15 | 5 | 2 | 7 |
| n128-r8-N15-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 15 | 67 | 85877999 | 7 |
| n128-r8-N15-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 128 | 8 | 15 | 5 | 13 | 7 |
| n128-r8-N15-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 128 | 8 | 15 | 5 | 2 | 7 |
| n128-r8-N290-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 290 | 13 | 2138809088 | 145 |
| n128-r8-N290-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 8 | 290 | 1 | 905 | 145 |
| n128-r8-N290-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 290 | 1 | 31 | 145 |
| n128-r8-N290-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 128 | 8 | 290 | 67 | 118003261 | 145 |
| n128-r8-N290-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 290 | 5 | 17 | 145 |
| n128-r8-N290-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 290 | 5 | 2 | 145 |
| n128-r8-N46-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 46 | 35 | 280460449 | 23 |
| n128-r8-N46-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 46 | 3 | 119 | 23 |
| n128-r8-N46-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 8 | 46 | 3 | 40 | 23 |
| n128-r8-N46-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 46 | 67 | 97551461 | 23 |
| n128-r8-N46-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 46 | 5 | 14 | 23 |
| n128-r8-N46-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 46 | 5 | 2 | 23 |
| n128-r8-N58-b0.4-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 31 | 5774051282 | 29 |
| n128-r8-N58-b0.4-lo0.4 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 58 | 2 | 165 | 29 |
| n128-r8-N58-b0.4-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 58 | 2 | 6 | 29 |
| n128-r8-N58-b0.4-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 67 | 1592841733 | 29 |
| n128-r8-N58-b0.4-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 58 | 5 | 16 | 29 |
| n128-r8-N58-b0.4-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 58 | 5 | 2 | 29 |
| n128-r8-N58-b0.8-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 31 | 5774051282 | 29 |
| n128-r8-N58-b0.8-lo0.4 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 58 | 2 | 165 | 29 |
| n128-r8-N58-b0.8-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 58 | 2 | 6 | 29 |
| n128-r8-N58-b0.8-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 67 | 1592841733 | 29 |
| n128-r8-N58-b0.8-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 58 | 5 | 16 | 29 |
| n128-r8-N58-b0.8-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 58 | 5 | 2 | 29 |
| n128-r8-N58-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 31 | 362764470 | 29 |
| n128-r8-N58-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 58 | 2 | 154 | 29 |
| n128-r8-N58-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 58 | 2 | 6 | 29 |
| n128-r8-N58-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 67 | 100072958 | 29 |
| n128-r8-N58-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 58 | 5 | 15 | 29 |
| n128-r8-N58-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 58 | 5 | 2 | 29 |
| n128-r8-N58-b1.6-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 31 | 5774051282 | 29 |
| n128-r8-N58-b1.6-lo0.4 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 58 | 2 | 165 | 29 |
| n128-r8-N58-b1.6-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 58 | 2 | 6 | 29 |
| n128-r8-N58-b1.6-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 67 | 1592841733 | 29 |
| n128-r8-N58-b1.6-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 58 | 5 | 16 | 29 |
| n128-r8-N58-b1.6-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 58 | 5 | 2 | 29 |
| n128-r8-N58-b1.6-lo1.6 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 31 | 27862387 | 29 |
| n128-r8-N58-b1.6-lo1.6 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 128 | 8 | 58 | 2 | 144 | 29 |
| n128-r8-N58-b1.6-lo1.6 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 58 | 2 | 5 | 29 |
| n128-r8-N58-b1.6-lo1.6 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 58 | 67 | 7686176 | 29 |
| n128-r8-N58-b1.6-lo1.6 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 58 | 5 | 14 | 29 |
| n128-r8-N58-b1.6-lo1.6 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 58 | 5 | 2 | 29 |
| n128-r8-N93-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 93 | 24 | 611899199 | 46 |
| n128-r8-N93-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 128 | 8 | 93 | 2 | 259 | 46 |
| n128-r8-N93-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 128 | 8 | 93 | 2 | 9 | 46 |
| n128-r8-N93-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 128 | 8 | 93 | 67 | 105272981 | 46 |
| n128-r8-N93-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 128 | 8 | 93 | 5 | 15 | 46 |
| n128-r8-N93-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 128 | 8 | 93 | 5 | 2 | 46 |
| n16-r2-N120-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 2 | 120 | 5 | 712496119 | 60 |
| n16-r2-N120-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 16 | 2 | 120 | 1 | 302 | 60 |
| n16-r2-N120-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 16 | 2 | 120 | 1 | 11 | 60 |
| n16-r2-N120-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 16 | 2 | 120 | 31 | 47499742 | 60 |
| n16-r2-N120-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 2 | 120 | 2 | 7 | 60 |
| n16-r2-N120-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 16 | 2 | 120 | 2 | 1 | 60 |
| n16-r2-N24-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 2 | 24 | 14 | 118682654 | 12 |
| n16-r2-N24-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 2 | 24 | 1 | 51 | 12 |
| n16-r2-N24-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 16 | 2 | 24 | 1 | 2 | 12 |
| n16-r2-N24-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 16 | 2 | 24 | 31 | 39560885 | 12 |
| n16-r2-N24-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 2 | 24 | 2 | 6 | 12 |
| n16-r2-N24-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 2 | 24 | 2 | 1 | 12 |
| n16-r2-N6-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 16 | 2 | 6 | 38 | 26062318 | 3 |
| n16-r2-N6-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 16 | 2 | 6 | 3 | 12 | 3 |
| n16-r2-N6-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 16 | 2 | 6 | 3 | 1 | 3 |
| n16-r2-N6-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 16 | 2 | 6 | 31 | 34749758 | 3 |
| n16-r2-N6-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 2 | 6 | 2 | 5 | 3 |
| n16-r2-N6-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 2 | 6 | 2 | 1 | 3 |
| n16-r3-N2-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 16 | 3 | 2 | 38 | 8687440 | 1 |
| n16-r3-N2-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 16 | 3 | 2 | 3 | 4 | 1 |
| n16-r3-N2-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 16 | 3 | 2 | 3 | 1 | 1 |
| n16-r3-N2-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 16 | 3 | 2 | 19 | 23166505 | 1 |
| n16-r3-N2-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 3 | 2 | 2 | 4 | 1 |
| n16-r3-N2-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 3 | 2 | 2 | 1 | 1 |
| n16-r3-N40-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 3 | 40 | 5 | 237498707 | 20 |
| n16-r3-N40-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 16 | 3 | 40 | 1 | 101 | 20 |
| n16-r3-N40-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=noncontracting | 16 | 3 | 40 | 1 | 4 | 20 |
| n16-r3-N40-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 16 | 3 | 40 | 19 | 31666495 | 20 |
| n16-r3-N40-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 3 | 40 | 2 | 5 | 20 |
| n16-r3-N40-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 3 | 40 | 2 | 1 | 20 |
| n16-r3-N8-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 3 | 8 | 14 | 39560885 | 4 |
| n16-r3-N8-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 3 | 8 | 1 | 17 | 4 |
| n16-r3-N8-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 16 | 3 | 8 | 1 | 1 | 4 |
| n16-r3-N8-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 16 | 3 | 8 | 19 | 26373924 | 4 |
| n16-r3-N8-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 3 | 8 | 2 | 4 | 4 |
| n16-r3-N8-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 3 | 8 | 2 | 1 | 4 |
| n16-r4-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 16 | 4 | 1 | 38 | 4343720 | 0 |
| n16-r4-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 16 | 4 | 1 | 3 | 2 | 0 |
| n16-r4-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 16 | 4 | 1 | 3 | 1 | 0 |
| n16-r4-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 16 | 4 | 1 | 14 | 17374879 | 0 |
| n16-r4-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 4 | 1 | 1 | 3 | 0 |
| n16-r4-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 4 | 1 | 1 | 1 | 0 |
| n16-r4-N20-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 4 | 20 | 5 | 118749354 | 10 |
| n16-r4-N20-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 16 | 4 | 20 | 1 | 51 | 10 |
| n16-r4-N20-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=noncontracting | 16 | 4 | 20 | 1 | 2 | 10 |
| n16-r4-N20-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 16 | 4 | 20 | 14 | 23749871 | 10 |
| n16-r4-N20-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 4 | 20 | 1 | 4 | 10 |
| n16-r4-N20-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 16 | 4 | 20 | 1 | 1 | 10 |
| n16-r4-N4-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 16 | 4 | 4 | 14 | 19780443 | 2 |
| n16-r4-N4-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 4 | 4 | 1 | 9 | 2 |
| n16-r4-N4-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 16 | 4 | 4 | 1 | 1 | 2 |
| n16-r4-N4-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 16 | 4 | 4 | 14 | 19780443 | 2 |
| n16-r4-N4-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 16 | 4 | 4 | 1 | 3 | 2 |
| n16-r4-N4-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 16 | 4 | 4 | 1 | 1 | 2 |
| n2048-r32-N211-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 2048 | 32 | 211 | 223 | 1522972747 | 105 |
| n2048-r32-N211-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 2048 | 32 | 211 | 14 | 644 | 105 |
| n2048-r32-N211-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 2048 | 32 | 211 | 14 | 22 | 105 |
| n2048-r32-N211-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 2048 | 32 | 211 | 434 | 461944341 | 105 |
| n2048-r32-N211-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 2048 | 32 | 211 | 28 | 66 | 105 |
| n2048-r32-N211-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 32 | 211 | 28 | 7 | 105 |
| n2048-r32-N4226-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 2048 | 32 | 4226 | 47 | 39465024556 | 2113 |
| n2048-r32-N4226-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 2 | positive_depth; rejected_candidates=sample_budget | 2048 | 32 | 4226 | 3 | 16681 | 2113 |
| n2048-r32-N4226-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 32 | 4226 | 3 | 55603 | 2113 |
| n2048-r32-N4226-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 2048 | 32 | 4226 | 434 | 597671929 | 2113 |
| n2048-r32-N4226-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 2048 | 32 | 4226 | 28 | 85 | 2113 |
| n2048-r32-N4226-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 32 | 4226 | 28 | 9 | 2113 |
| n2048-r32-N845-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 2048 | 32 | 845 | 107 | 6926888841 | 422 |
| n2048-r32-N845-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 32 | 845 | 7 | 2928 | 422 |
| n2048-r32-N845-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 2048 | 32 | 845 | 7 | 98 | 422 |
| n2048-r32-N845-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 2048 | 32 | 845 | 434 | 524640102 | 422 |
| n2048-r32-N845-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 2048 | 32 | 845 | 28 | 74 | 422 |
| n2048-r32-N845-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 32 | 845 | 28 | 8 | 422 |
| n2048-r512-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 1 | 198 | 7374865 | 0 |
| n2048-r512-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 1 | 13 | 4 | 0 |
| n2048-r512-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 1 | 13 | 1 | 0 |
| n2048-r512-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 1 | 95 | 29499458 | 0 |
| n2048-r512-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 1 | 6 | 5 | 0 |
| n2048-r512-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 1 | 6 | 1 | 0 |
| n2048-r512-N16-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 2048 | 512 | 16 | 47 | 149401508 | 8 |
| n2048-r512-N16-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 2048 | 512 | 16 | 3 | 64 | 8 |
| n2048-r512-N16-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 2048 | 512 | 16 | 3 | 3 | 8 |
| n2048-r512-N16-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 16 | 95 | 37350377 | 8 |
| n2048-r512-N16-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 16 | 6 | 6 | 8 |
| n2048-r512-N16-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 512 | 16 | 6 | 1 | 8 |
| n2048-r512-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 3 | 110 | 24452848 | 1 |
| n2048-r512-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 3 | 7 | 11 | 1 |
| n2048-r512-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 2048 | 512 | 3 | 7 | 1 | 1 |
| n2048-r512-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 3 | 95 | 32603797 | 1 |
| n2048-r512-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 2048 | 512 | 3 | 6 | 5 | 1 |
| n2048-r512-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 2048 | 512 | 3 | 6 | 1 | 1 |
| n2048-r8-N14972-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 2048 | 8 | 14972 | 107 | 122735421624 | 7486 |
| n2048-r8-N14972-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 8 | 14972 | 7 | 51877 | 7486 |
| n2048-r8-N14972-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 8 | 14972 | 7 | 172922 | 7486 |
| n2048-r8-N14972-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 2048 | 8 | 14972 | 1067 | 2098601920 | 7486 |
| n2048-r8-N14972-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 1 | positive_depth; working_array_memory_budget | 2048 | 8 | 14972 | 67 | 296 | 7486 |
| n2048-r8-N14972-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 8 | 14972 | 67 | 30 | 7486 |
| n2048-r8-N3743-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 2048 | 8 | 3743 | 223 | 27020244008 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 8 | 3743 | 14 | 11421 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 2048 | 8 | 3743 | 14 | 381 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 2048 | 8 | 3743 | 1067 | 1848031650 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | sharp_S4_locked | 27 | resource_limit | 1 | positive_depth; working_array_memory_budget | 2048 | 8 | 3743 | 67 | 261 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 8 | 3743 | 67 | 27 | 1871 |
| n2048-r8-N3743-b0.8-lo0.8 | sharp_S4_locked | 73 | ok | 1 | positive_depth | 2048 | 8 | 3743 | 67 | 261 | 1871 |
| n2048-r8-N74861-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 2048 | 8 | 74861 | 47 | 699099027001 | 37430 |
| n2048-r8-N74861-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 2 | positive_depth; rejected_candidates=sample_budget | 2048 | 8 | 74861 | 3 | 295488 | 37430 |
| n2048-r8-N74861-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 2048 | 8 | 74861 | 3 | 984959 | 37430 |
| n2048-r8-N74861-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 2048 | 8 | 74861 | 1067 | 2390688756 | 37430 |
| n2048-r8-N74861-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 1 | positive_depth; working_array_memory_budget | 2048 | 8 | 74861 | 67 | 337 | 37430 |
| n2048-r8-N74861-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 2048 | 8 | 74861 | 67 | 34 | 37430 |
| n32-r3-N165-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 32 | 3 | 165 | 7 | 1057133287 | 82 |
| n32-r3-N165-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 32 | 3 | 165 | 1 | 447 | 82 |
| n32-r3-N165-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 32 | 3 | 165 | 1 | 15 | 82 |
| n32-r3-N165-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 32 | 3 | 165 | 38 | 68339930 | 82 |
| n32-r3-N165-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 32 | 3 | 165 | 3 | 10 | 82 |
| n32-r3-N165-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 32 | 3 | 165 | 3 | 1 | 82 |
| n32-r3-N33-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 32 | 3 | 33 | 18 | 176414216 | 16 |
| n32-r3-N33-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 32 | 3 | 33 | 2 | 75 | 16 |
| n32-r3-N33-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 32 | 3 | 33 | 2 | 1 | 16 |
| n32-r3-N33-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 32 | 3 | 33 | 38 | 57022777 | 16 |
| n32-r3-N33-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 32 | 3 | 33 | 3 | 9 | 16 |
| n32-r3-N33-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 32 | 3 | 33 | 3 | 1 | 16 |
| n32-r3-N8-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 32 | 3 | 8 | 47 | 36723920 | 4 |
| n32-r3-N8-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 32 | 3 | 8 | 3 | 16 | 4 |
| n32-r3-N8-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 32 | 3 | 8 | 3 | 1 | 4 |
| n32-r3-N8-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 32 | 3 | 8 | 38 | 48965227 | 4 |
| n32-r3-N8-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 32 | 3 | 8 | 3 | 7 | 4 |
| n32-r3-N8-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 32 | 3 | 8 | 3 | 1 | 4 |
| n32-r8-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 1 | 42 | 4658956 | 0 |
| n32-r8-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 1 | 3 | 2 | 0 |
| n32-r8-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 1 | 3 | 1 | 0 |
| n32-r8-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 32 | 8 | 1 | 17 | 18635821 | 0 |
| n32-r8-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 32 | 8 | 1 | 2 | 3 | 0 |
| n32-r8-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 32 | 8 | 1 | 17 | 18635821 | 0 |
| n32-r8-N17-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 32 | 8 | 17 | 7 | 108459109 | 8 |
| n32-r8-N17-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 32 | 8 | 17 | 1 | 46 | 8 |
| n32-r8-N17-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 32 | 8 | 17 | 1 | 2 | 8 |
| n32-r8-N17-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 32 | 8 | 17 | 17 | 25519791 | 8 |
| n32-r8-N17-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 32 | 8 | 17 | 2 | 4 | 8 |
| n32-r8-N17-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 32 | 8 | 17 | 2 | 1 | 8 |
| n32-r8-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 3 | 20 | 15738663 | 1 |
| n32-r8-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 3 | 2 | 7 | 1 |
| n32-r8-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 32 | 8 | 3 | 2 | 1 | 1 |
| n32-r8-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 32 | 8 | 3 | 17 | 20984883 | 1 |
| n32-r8-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 32 | 8 | 3 | 2 | 3 | 1 |
| n32-r8-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 32 | 8 | 3 | 2 | 1 | 1 |
| n512-r128-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 1 | 107 | 6404206 | 0 |
| n512-r128-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 1 | 7 | 3 | 0 |
| n512-r128-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 1 | 7 | 1 | 0 |
| n512-r128-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 128 | 1 | 50 | 25616821 | 0 |
| n512-r128-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 512 | 128 | 1 | 4 | 4 | 0 |
| n512-r128-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 512 | 128 | 1 | 4 | 1 | 0 |
| n512-r128-N16-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 128 | 16 | 24 | 133624717 | 8 |
| n512-r128-N16-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 512 | 128 | 16 | 2 | 57 | 8 |
| n512-r128-N16-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 128 | 16 | 2 | 2 | 8 |
| n512-r128-N16-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 128 | 16 | 50 | 33406180 | 8 |
| n512-r128-N16-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 512 | 128 | 16 | 4 | 5 | 8 |
| n512-r128-N16-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 128 | 16 | 4 | 1 | 8 |
| n512-r128-N3-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 3 | 58 | 21508210 | 1 |
| n512-r128-N3-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 3 | 4 | 10 | 1 |
| n512-r128-N3-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 512 | 128 | 3 | 4 | 1 | 1 |
| n512-r128-N3-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 128 | 3 | 50 | 28677614 | 1 |
| n512-r128-N3-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 512 | 128 | 3 | 4 | 5 | 1 |
| n512-r128-N3-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 512 | 128 | 3 | 50 | 28677614 | 1 |
| n512-r16-N1090-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 16 | 1090 | 24 | 9107635880 | 545 |
| n512-r16-N1090-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 16 | 1090 | 2 | 3850 | 545 |
| n512-r16-N1090-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 16 | 1090 | 2 | 12832 | 545 |
| n512-r16-N1090-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 16 | 1090 | 167 | 267380136 | 545 |
| n512-r16-N1090-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 16 | 1090 | 11 | 38 | 545 |
| n512-r16-N1090-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 16 | 1090 | 11 | 4 | 545 |
| n512-r16-N218-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 16 | 218 | 56 | 1573699218 | 109 |
| n512-r16-N218-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 16 | 218 | 4 | 666 | 109 |
| n512-r16-N218-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 16 | 218 | 4 | 23 | 109 |
| n512-r16-N218-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 16 | 218 | 167 | 231001721 | 109 |
| n512-r16-N218-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 16 | 218 | 11 | 33 | 109 |
| n512-r16-N218-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 16 | 218 | 11 | 4 | 109 |
| n512-r16-N54-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 16 | 54 | 122 | 337438128 | 27 |
| n512-r16-N54-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 512 | 16 | 54 | 8 | 143 | 27 |
| n512-r16-N54-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth | 512 | 16 | 54 | 8 | 15 | 27 |
| n512-r16-N54-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 16 | 54 | 167 | 199963335 | 27 |
| n512-r16-N54-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 512 | 16 | 54 | 11 | 29 | 27 |
| n512-r16-N54-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 512 | 16 | 54 | 11 | 9 | 27 |
| n512-r3-N2180-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 3 | 2180 | 122 | 13636224634 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 3 | 2180 | 8 | 5764 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 3 | 2180 | 8 | 193 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 2180 | 618 | 1067545415 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | sharp_S4_locked | 98 | ok | 0 | root_A_stop | 512 | 3 | 2180 | 39 | 151 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 3 | 2180 | 39 | 16 | 1090 |
| n512-r3-N2180-b0.8-lo0.8 | sharp_S4_locked | 2 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 2180 | 39 | 151 | 1090 |
| n512-r3-N43605-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 3 | 43605 | 24 | 364350755485 | 21802 |
| n512-r3-N43605-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 3 | 43605 | 2 | 154000 | 21802 |
| n512-r3-N43605-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 3 | 43605 | 2 | 5134 | 21802 |
| n512-r3-N43605-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 43605 | 618 | 1426041256 | 21802 |
| n512-r3-N43605-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 43605 | 39 | 201 | 21802 |
| n512-r3-N43605-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 3 | 43605 | 39 | 21 | 21802 |
| n512-r3-N8721-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 3 | 8721 | 56 | 62955890468 | 4360 |
| n512-r3-N8721-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 3 | 8721 | 4 | 26610 | 4360 |
| n512-r3-N8721-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 3 | 8721 | 4 | 887 | 4360 |
| n512-r3-N8721-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 8721 | 618 | 1232022931 | 4360 |
| n512-r3-N8721-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 3 | 8721 | 39 | 174 | 4360 |
| n512-r3-N8721-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 3 | 8721 | 39 | 18 | 4360 |
| n512-r32-N13-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 512 | 32 | 13 | 123 | 81191163 | 6 |
| n512-r32-N13-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 512 | 32 | 13 | 8 | 35 | 6 |
| n512-r32-N13-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 512 | 32 | 13 | 8 | 2 | 6 |
| n512-r32-N13-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 13 | 109 | 99927586 | 6 |
| n512-r32-N13-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | sample_budget; rejected_candidates=sample_budget | 512 | 32 | 13 | 7 | 15 | 6 |
| n512-r32-N13-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 1 | positive_depth | 512 | 32 | 13 | 14 | 5 | 6 |
| n512-r32-N263-b0.4-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 32 | 263 | 24 | 34361759920 | 131 |
| n512-r32-N263-b0.4-lo0.4 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 32 | 263 | 2 | 981 | 131 |
| n512-r32-N263-b0.4-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 263 | 2 | 33 | 131 |
| n512-r32-N263-b0.4-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 263 | 109 | 2090449273 | 131 |
| n512-r32-N263-b0.4-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 263 | 7 | 20 | 131 |
| n512-r32-N263-b0.4-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 263 | 7 | 2 | 131 |
| n512-r32-N263-b0.8-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 32 | 263 | 24 | 34361759920 | 131 |
| n512-r32-N263-b0.8-lo0.4 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 32 | 263 | 2 | 981 | 131 |
| n512-r32-N263-b0.8-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 263 | 2 | 33 | 131 |
| n512-r32-N263-b0.8-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 263 | 109 | 2090449273 | 131 |
| n512-r32-N263-b0.8-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 263 | 7 | 20 | 131 |
| n512-r32-N263-b0.8-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 263 | 7 | 2 | 131 |
| n512-r32-N263-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 32 | 263 | 24 | 2197028442 | 131 |
| n512-r32-N263-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 32 | 263 | 2 | 929 | 131 |
| n512-r32-N263-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 263 | 2 | 31 | 131 |
| n512-r32-N263-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 263 | 109 | 133659525 | 131 |
| n512-r32-N263-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 263 | 7 | 19 | 131 |
| n512-r32-N263-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 263 | 7 | 2 | 131 |
| n512-r32-N263-b1.6-lo0.4 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 32 | 263 | 24 | 34361759920 | 131 |
| n512-r32-N263-b1.6-lo0.4 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 32 | 263 | 2 | 981 | 131 |
| n512-r32-N263-b1.6-lo0.4 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 263 | 2 | 33 | 131 |
| n512-r32-N263-b1.6-lo0.4 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 263 | 109 | 2090449273 | 131 |
| n512-r32-N263-b1.6-lo0.4 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 263 | 7 | 20 | 131 |
| n512-r32-N263-b1.6-lo0.4 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 263 | 7 | 2 | 131 |
| n512-r32-N263-b1.6-lo1.6 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 32 | 263 | 24 | 171612576 | 131 |
| n512-r32-N263-b1.6-lo1.6 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 32 | 263 | 2 | 885 | 131 |
| n512-r32-N263-b1.6-lo1.6 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 263 | 2 | 30 | 131 |
| n512-r32-N263-b1.6-lo1.6 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 263 | 109 | 10440309 | 131 |
| n512-r32-N263-b1.6-lo1.6 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 263 | 7 | 18 | 131 |
| n512-r32-N263-b1.6-lo1.6 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 263 | 7 | 2 | 131 |
| n512-r32-N52-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 52 | 57 | 374860003 | 26 |
| n512-r32-N52-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 512 | 32 | 52 | 4 | 159 | 26 |
| n512-r32-N52-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 32 | 52 | 4 | 6 | 26 |
| n512-r32-N52-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 32 | 52 | 109 | 115341540 | 26 |
| n512-r32-N52-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 32 | 52 | 7 | 17 | 26 |
| n512-r32-N52-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 32 | 52 | 7 | 2 | 26 |
| n512-r4-N1090-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 4 | 1090 | 122 | 6818112317 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 4 | 1090 | 8 | 2882 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 4 | 1090 | 8 | 97 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 1090 | 466 | 800659062 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | sharp_S4_locked | 96 | ok | 0 | root_A_stop | 512 | 4 | 1090 | 30 | 113 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 4 | 1090 | 30 | 12 | 545 |
| n512-r4-N1090-b0.8-lo0.8 | sharp_S4_locked | 4 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 1090 | 30 | 113 | 545 |
| n512-r4-N21802-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 4 | 21802 | 24 | 182170845696 | 10901 |
| n512-r4-N21802-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 4 | 21802 | 2 | 76998 | 10901 |
| n512-r4-N21802-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 4 | 21802 | 2 | 256660 | 10901 |
| n512-r4-N21802-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 21802 | 466 | 1069528862 | 10901 |
| n512-r4-N21802-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 21802 | 30 | 151 | 10901 |
| n512-r4-N21802-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 4 | 21802 | 30 | 16 | 10901 |
| n512-r4-N4360-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 4 | 4360 | 56 | 31473984357 | 2180 |
| n512-r4-N4360-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 4 | 4360 | 4 | 13304 | 2180 |
| n512-r4-N4360-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 4 | 4360 | 4 | 444 | 2180 |
| n512-r4-N4360-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 4360 | 466 | 924006881 | 2180 |
| n512-r4-N4360-b0.8-lo0.8 | sharp_S4_locked | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 4 | 4360 | 30 | 131 | 2180 |
| n512-r4-N4360-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 4 | 4360 | 30 | 14 | 2180 |
| n512-r8-N233-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 8 | 233 | 122 | 1457059857 | 116 |
| n512-r8-N233-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=sample_budget | 512 | 8 | 233 | 8 | 616 | 116 |
| n512-r8-N233-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 8 | 233 | 8 | 21 | 116 |
| n512-r8-N233-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 512 | 8 | 233 | 267 | 400222450 | 116 |
| n512-r8-N233-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 8 | 233 | 17 | 57 | 116 |
| n512-r8-N233-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 8 | 233 | 17 | 6 | 116 |
| n512-r8-N4672-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop; rejected_candidates=sample_budget | 512 | 8 | 4672 | 24 | 39037904663 | 2336 |
| n512-r8-N4672-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 8 | 4672 | 2 | 16501 | 2336 |
| n512-r8-N4672-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 8 | 4672 | 2 | 55001 | 2336 |
| n512-r8-N4672-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 8 | 4672 | 267 | 534765818 | 2336 |
| n512-r8-N4672-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 8 | 4672 | 17 | 76 | 2336 |
| n512-r8-N4672-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 8 | 4672 | 17 | 8 | 2336 |
| n512-r8-N934-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 512 | 8 | 934 | 56 | 6742161904 | 467 |
| n512-r8-N934-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 1 | positive_depth; rejected_candidates=sample_budget | 512 | 8 | 934 | 4 | 2850 | 467 |
| n512-r8-N934-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_feasible_resolution; rejected_candidates=noncontracting | 512 | 8 | 934 | 4 | 95 | 467 |
| n512-r8-N934-b0.8-lo0.8 | sharp_proof | 100 | resource_limit | 0 | root_A_stop; working_array_memory_budget | 512 | 8 | 934 | 267 | 461989681 | 467 |
| n512-r8-N934-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 1 | positive_depth | 512 | 8 | 934 | 17 | 66 | 467 |
| n512-r8-N934-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | noncontracting; rejected_candidates=noncontracting | 512 | 8 | 934 | 17 | 7 | 467 |
| n8-r2-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 8 | 2 | 1 | 43 | 4104901 | 0 |
| n8-r2-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 8 | 2 | 1 | 3 | 2 | 0 |
| n8-r2-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 8 | 2 | 1 | 3 | 1 | 0 |
| n8-r2-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 2 | 1 | 15 | 16419601 | 0 |
| n8-r2-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 2 | 1 | 1 | 3 | 0 |
| n8-r2-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 2 | 1 | 1 | 1 | 0 |
| n8-r2-N28-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 8 | 2 | 28 | 4 | 153609642 | 14 |
| n8-r2-N28-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 2 | 28 | 1 | 65 | 14 |
| n8-r2-N28-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 2 | 28 | 1 | 3 | 14 |
| n8-r2-N28-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 2 | 28 | 15 | 21944235 | 14 |
| n8-r2-N28-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 2 | 28 | 1 | 4 | 14 |
| n8-r2-N28-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 2 | 28 | 1 | 1 | 14 |
| n8-r2-N5-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 13 | 22781546 | 2 |
| n8-r2-N5-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 1 | 10 | 2 |
| n8-r2-N5-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 1 | 1 | 2 |
| n8-r2-N5-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 15 | 18225237 | 2 |
| n8-r2-N5-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 1 | 3 | 2 |
| n8-r2-N5-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 2 | 5 | 1 | 1 | 2 |
| n8-r3-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 8 | 3 | 1 | 18 | 4365902 | 0 |
| n8-r3-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 8 | 3 | 1 | 2 | 2 | 0 |
| n8-r3-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 8 | 3 | 1 | 2 | 1 | 0 |
| n8-r3-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 3 | 1 | 9 | 11642406 | 0 |
| n8-r3-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 3 | 1 | 1 | 2 | 0 |
| n8-r3-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 3 | 1 | 1 | 1 | 0 |
| n8-r3-N9-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 8 | 3 | 9 | 4 | 49168447 | 4 |
| n8-r3-N9-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 3 | 9 | 1 | 21 | 4 |
| n8-r3-N9-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 3 | 9 | 1 | 1 | 4 |
| n8-r3-N9-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 3 | 9 | 9 | 14568429 | 4 |
| n8-r3-N9-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 3 | 9 | 1 | 3 | 4 |
| n8-r3-N9-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 3 | 9 | 1 | 1 | 4 |
| n8-r4-N1-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | no_admissible_eta | 8 | 4 | 1 | 11 | 4635255 | 0 |
| n8-r4-N1-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | no_admissible_eta | 8 | 4 | 1 | 1 | 2 | 0 |
| n8-r4-N1-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | no_admissible_eta | 8 | 4 | 1 | 1 | 1 | 0 |
| n8-r4-N1-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 4 | 1 | 7 | 9270509 | 0 |
| n8-r4-N1-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 4 | 1 | 1 | 2 | 0 |
| n8-r4-N1-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 4 | 1 | 1 | 1 | 0 |
| n8-r4-N4-b0.8-lo0.8 | efficient_proof | 100 | ok | 0 | root_A_stop | 8 | 4 | 4 | 5 | 21558681 | 2 |
| n8-r4-N4-b0.8-lo0.8 | efficient_S4_locked | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 4 | 4 | 1 | 10 | 2 |
| n8-r4-N4-b0.8-lo0.8 | efficient_per_setting | 100 | ok | 0 | root_A_stop; rejected_candidates=noncontracting | 8 | 4 | 4 | 1 | 1 | 2 |
| n8-r4-N4-b0.8-lo0.8 | sharp_proof | 100 | ok | 0 | root_A_stop | 8 | 4 | 4 | 7 | 10779341 | 2 |
| n8-r4-N4-b0.8-lo0.8 | sharp_S4_locked | 100 | ok | 0 | root_A_stop | 8 | 4 | 4 | 1 | 2 | 2 |
| n8-r4-N4-b0.8-lo0.8 | sharp_per_setting | 100 | ok | 0 | root_A_stop | 8 | 4 | 4 | 1 | 1 | 2 |
