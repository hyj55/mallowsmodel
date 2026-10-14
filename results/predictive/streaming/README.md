# Exact-sieve memory and search audit

[Construction and proof](../../../docs/sieve_computation.md#bounded-memory-exact-search) · [Predictive results](../README.md)

This directory records implementation attempts for the 530 unavailable Sharp contexts. They share ten distinct catalogue-size / integer-radius packings. A packing is independent of the selected pair orientations, so its construction is attempted once and mapped to every dependent context. Sharp/global-sieve aliases are not counted twice. These are computational checks, not additional statistical experiments or changed train/test splits.

| File | Contents |
|---|---|
| [packings.json](packings.json) | Actual search receipts, retained-prefix sizes, resolved lexicographic positions, time, managed array allocation, native peak RSS, and code fingerprints |
| [contexts.csv](contexts.csv) | All 530 affected contexts, their unchanged estimator seeds, shared construction, and availability before and after the audit |
| [benchmarks.json](benchmarks.json) | Complete construction checks, including the original 29,086-candidate reference and forced disk eviction/reloading |
| [manifest.json](manifest.json) | Code and input/output hashes; verifies that predictive parameters, score tables, and primary study manifest are unchanged |

`packing_so_far` describes an accepted **prefix** of the sieve when `complete=false`. It is not a usable substitute for the full packing. `resolved_permutations` counts lexicographically earlier permutations already accepted or proved covered, including those skipped as whole prefixes. Dividing by `total_permutations` describes search position; it is not a reliable runtime forecast because later search costs differ.

`allocated_working_bytes` accounts for managed candidate blocks, the read buffer, scratch allowance and reserve. `native_peak_rss_bytes` is measured for the C++ search subprocess; it excludes the Python process and compilation. The packed disk index is temporary and reconstructed from the canonical saved candidate rows on resume. Candidate rows and checkpoints remain local under `results/private/streaming_sieve`; only audit receipts and aggregate status mappings are published.

Reproduce with `python benchmark_streaming_sieve.py --seconds 120 --workers 2`. Validate the saved public evidence without starting any search using `python validate_streaming_sieve.py`. Additional runtime can be given with `--resume`; the exact construction and its seed remain unchanged.

## Measured outcome

**Zero of the ten shared packings completed; all 530 dependent Sharp fits remain unavailable.** Each construction received 120 seconds with a 4-GiB managed-array limit. The two simulation cases with the smaller covering-count lower bounds, (16,19) and (32,158), then resumed for another 480 seconds each, for approximately 600 seconds cumulatively. All stopped on the time budget, after actually starting the search. These are not additional training/test repetitions.

| Contexts sharing the packing | n | Integer radius | Affected fits | Cumulative seconds | Retained candidate prefix | Accounted work memory, MB |
|---|---:|---:|---:|---:|---:|---:|
| Wheat (P0) | 16 | 4 | 30 | 120 | 38,457 | 3.335 |
| Simulation n=16 (S0) | 16 | 19 | 40 | 600 | 1,034 | 2.139 |
| Dots2024, both arms and all report sizes (P0) | 30 | 54 | 240 | 120 | 5 | 2.121 |
| Simulation n=32 (S0) | 32 | 158 | 40 | 600 | 3 | 2.124 |
| PatrasIQ cost (P0) | 36 | 72 | 30 | 120 | 3 | 2.129 |
| PatrasIQ population (P0) | 48 | 172 | 30 | 120 | 3 | 2.150 |
| Sushi B, N=4000 (P0) | 100 | 123 | 30 | 120 | 4 | 2.290 |
| Sushi B, N=3000 (L0) | 100 | 165 | 30 | 120 | 4 | 2.290 |
| Sushi B, N=1000 (L0) | 100 | 495 | 30 | 120 | 4 | 2.290 |
| Sushi B, N=300 (L0) | 100 | 1650 | 30 | 120 | 3 | 2.290 |

Work-memory accounting includes the fixed reserve; it is not total process RSS. In particular, Wheat now starts construction using a few MB rather than being refused by a factorial pre-allocation. This does not remove its lower bound of 5,619,873,728 retained orders: its 38,457-order prefix is unfinished. Disk spill bounds the candidate cache, but retaining and checking billions of orders remains substantial work. The results do not establish a universal impossibility of a different exact solver.

The completed computational checks are:

| n | Radius | Complete candidates | Accounted work memory, MB | Native seconds | Check |
|---:|---:|---:|---:|---:|---|
| 10 | 4 | 29,086 | 2.623 | 36.431 | All orders match the original reference SHA256 |
| 12 | 40 | 4 | 2.105 | 2.534 | Complete packing without factorial allocation |
| 16 | 100 | 2 | 2.106 | 0.014 | Complete packing without factorial allocation |
| 9 | 4 | 3,838 | 2.106 | 2.528 | Forced disk spill; all orders equal original enumeration |

The forced-spill check performs 14 block writes and 240,559 block reads under a 2,108,000-byte array budget. The ten-item reference uses about 2.62 MB of accounted work memory versus 76.50 MB in the saved ball-cover receipt, but takes about 36.43 seconds versus that receipt's 6.06 seconds. These timings were collected under different load and are not a controlled speed comparison; the new engine is not uniformly faster. The existing ball-cover and parity-DP implementations remain available. The twelve- and sixteen-item rows here are computational checks, not recovered empirical or synthetic study fits.

To reproduce the committed two-stage budget schedule after the initial command above:

```bash
python benchmark_streaming_sieve.py --resume --cases 16:19 32:158 --seconds 480 --workers 2
```

Elapsed time and the length of an unfinished prefix can vary across machines and loads. A completed ordered packing, its minimizing objective, and its tie rule do not change. All existing predictive parameter files, NLL scores, split summaries and data-feature joins are unchanged.
