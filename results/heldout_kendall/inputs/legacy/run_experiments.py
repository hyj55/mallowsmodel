"""Reproduce the prespecified model comparison. Run from the repository root."""
import argparse
from dataclasses import asdict
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import brentq
from scipy.special import expit, gammaln
from scipy.stats import t as student_t

from src.data import ROOT, audit, load_all, save_manifest
from src.models import (borda, distances, exact_dp, fit_pl, fit_sm, greedy,
                        kendall, kemeny_cost, logz_mean, milp_center, multistart,
                        pair_counts, posest, sample_pl, sample_sm, tune_pl)

SEED = 20260920
OUT = ROOT / "results"
PRIVATE = OUT / "private"
BETA_FACTORS = (0., .25, .5, .75, 1.)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False,
                                   default=lambda x: x.item() if hasattr(x, "item") else str(x))+"\n")


def paired_ci(values, seed=SEED, resamples=2000):
    values = np.asarray(values)
    rng = np.random.default_rng(seed)
    sims = np.empty(resamples)
    for start in range(0, resamples, 100):
        stop = min(start+100, resamples)
        idx = rng.integers(len(values), size=(stop-start, len(values)))
        sims[start:stop] = values[idx].mean(axis=1)
    lo, hi = np.quantile(sims, [.025, .975])
    return float(lo), float(hi)


def outer_split(data):
    # Both Sushi files have aligned respondent rows and therefore share this split.
    perm = np.random.default_rng(SEED).permutation(len(data.y))
    ntest = int(np.ceil(.2*len(perm)))
    return perm[ntest:], perm[:ntest]


def fit_compare(development, test, n, seed, time_limit=10.):
    nin = max(2, int(.8*len(development)))
    train, valid = development[:nin], development[nin:]
    tau, grid_losses = tune_pl(train, valid, n)
    pl = fit_pl(development, n, tau)
    pl_near = fit_pl(development, n, 1e-6)
    sm = fit_sm(development, n, seed, time_limit=time_limit)
    # Large-instance sensitivity only: use insertion for the INNER calibration fit.
    inner_sm = fit_sm(train, n, seed, solver="dp" if n <= 18 else "multistart")
    factor = BETA_FACTORS[int(np.argmin([inner_sm.nll(valid, f).mean() for f in BETA_FACTORS]))]
    losses = np.stack([sm.nll(test), pl.nll(test), sm.nll(test, factor), pl_near.nll(test)])
    unseen = set(range(n))-set(development.ravel())
    record = {"beta": sm.beta, "tau": tau, "sm_beta_factor": factor,
              "sm_D": sm.objective, "sm_gap": sm.metadata["absolute_gap"],
              "sm_certified": sm.metadata["certified"], "sm_solver": sm.metadata["solver"],
              "sm_seconds": sm.metadata["seconds"], "pl_seconds": pl.metadata["seconds"],
              "pl_gradient_max": pl.metadata["gradient_max"], "pl_success": pl.metadata["success"],
              "pl_near_gradient_max": pl_near.metadata["gradient_max"],
              "unseen_items": len(unseen),
              "test_reports_with_unseen": int(np.isin(test, list(unseen)).any(axis=1).sum()),
              "center_kendall_SM_PL": kendall(sm.order, pl.order),
              "SM_nll": float(losses[0].mean()), "PL_nll": float(losses[1].mean()),
              "SM_calibrated_nll": float(losses[2].mean()), "PL_near_mle_nll": float(losses[3].mean()),
              "delta": float((losses[0]-losses[1]).mean())}
    parameters = {"sm_order": sm.order.tolist(), "beta": sm.beta, "pl_theta": pl.theta.tolist(),
                  "tau": tau, "beta_factor": factor, "inner_pl_losses": grid_losses,
                  "sm_optimization": sm.metadata}
    return record, losses, parameters, sm, pl


def benchmark(data):
    pool, _ = outer_split(data)
    pool = np.random.default_rng(SEED+11).permutation(pool)
    max_n = min(3000, len(pool))
    budgets = [min(50 if data.n == 10 else 100, max_n), max_n]
    rows = []
    for size in budgets:
        w = pair_counts(data.y[pool[:size]], data.n)
        candidates = {}
        for name, method in [("borda", borda), ("posest", posest), ("greedy", greedy), ("multistart", multistart)]:
            t0 = time.perf_counter()
            order = method(w, seed=SEED)
            candidates[name] = (kemeny_cost(w, order), time.perf_counter()-t0)
        t0 = time.perf_counter()
        if data.n <= 18:
            order = exact_dp(w, SEED)
            certificate = {"certified": True, "lower_bound": kemeny_cost(w, order)}
            method_name = "exact_dp"
        else:
            order, certificate = milp_center(w, SEED, time_limit=20.)
            method_name = "milp_20s"
        cost = kemeny_cost(w, order)
        candidates[method_name] = (cost, time.perf_counter()-t0)
        for name, (value, seconds) in candidates.items():
            rows.append({"dataset": data.name, "N": size, "algorithm": name,
                         "D": value, "seconds_center_only": seconds,
                         "reference_D": cost, "reference_certified": certificate["certified"],
                         "excess_over_best": value-cost,
                         "gap_to_lower_bound": value-certificate["lower_bound"]})
    return rows


def real_experiments():
    all_data = load_all()
    write_json(OUT/"data_audit.json", [audit(d) for d in all_data])
    save_manifest(OUT)
    algo = []
    for data in all_data:
        print(f"Algorithm benchmark: {data.name}", flush=True)
        algo += benchmark(data)
        pd.DataFrame(algo).to_csv(OUT/"algorithm_benchmark.csv", index=False)
    records, summaries, params = [], [], {}
    for data in all_data:
        pool, test_idx = outer_split(data)
        if data.name == "beans":
            budgets, repetitions = [20, 50, 100, 200, 400, len(pool)], 5
        elif data.name == "sushi_a":
            budgets, repetitions = [20, 50, 100, 300, 1000, 3000], 5
        else:
            budgets, repetitions = [100, 300, 1000, 3000], 3
        by_budget = {size: [] for size in budgets}
        for rep in range(repetitions):
            train_idx = np.random.default_rng(SEED+11+rep).permutation(pool)
            for size in budgets:
                seed = SEED+100*rep+size
                print(f"Real: {data.name}, rep={rep}, N={size}", flush=True)
                record, losses, parameter, _, _ = fit_compare(data.y[train_idx[:size]],
                                                             data.y[test_idx], data.n, seed)
                record.update(dataset=data.name, N=size, replicate=rep, test_reports=len(test_idx))
                records.append(record)
                by_budget[size].append(losses)
                params[f"{data.name}_N{size}_rep{rep}"] = parameter
                # Only likelihoods, indices and fitted parameters; ignored by git / zip.
                np.savez_compressed(PRIVATE/f"{data.name}_N{size}_rep{rep}.npz", losses=losses,
                                    train_indices=train_idx[:size], test_indices=test_idx)
                pd.DataFrame(records).to_csv(OUT/"real_replicates.csv", index=False)
                write_json(OUT/"fitted_parameters.json", params)
        for size, fits in by_budget.items():
            a = np.stack(fits)  # repetition, model, test report
            avg = a.mean(axis=0)
            delta = avg[0]-avg[1]
            lo, hi = paired_ci(delta)
            cal_delta = avg[2]-avg[1]
            clo, chi = paired_ci(cal_delta)
            near_delta = avg[0]-avg[3]
            nlo, nhi = paired_ci(near_delta)
            rep_delta = (a[:, 0]-a[:, 1]).mean(axis=1)
            summaries.append({"dataset": data.name, "N": size, "repetitions": len(fits),
                              "test_reports": len(test_idx), "SM_nll": avg[0].mean(),
                              "PL_nll": avg[1].mean(), "delta": delta.mean(), "ci_low": lo, "ci_high": hi,
                              "SM_calibrated_nll": avg[2].mean(), "calibrated_delta": cal_delta.mean(),
                              "calibrated_ci_low": clo, "calibrated_ci_high": chi,
                              "PL_near_mle_nll": avg[3].mean(), "near_mle_delta": near_delta.mean(),
                              "near_mle_ci_low": nlo, "near_mle_ci_high": nhi,
                              "repeat_delta_min": rep_delta.min(), "repeat_delta_max": rep_delta.max(),
                              "uniform_nll": gammaln(data.y.shape[1]+1)})
        pd.DataFrame(summaries).to_csv(OUT/"real_summary.csv", index=False)
    return summaries


def matched_pl_theta(n, r, beta, shape):
    # Expected inversion count of uniform subsets depends only on pair marginals.
    if shape == "equal":
        raw = np.linspace(1, -1, n)
    elif shape == "unequal":
        raw = np.r_[3., np.linspace(.4, -.4, n-1)]
    else:
        raise ValueError(shape)
    gaps = np.array([raw[i]-raw[j] for i, j in combinations(range(n), 2)])
    target = logz_mean(r, beta)[1]
    inclusion = r*(r-1)/(n*(n-1))
    scale = brentq(lambda a: inclusion*expit(-a*gaps).sum()-target, 0, 200)
    theta = scale*(raw-raw.mean())
    return theta, scale


def synthetic_experiments(repetitions=30):
    rows, algorithm_rows = [], []
    n, r, beta = 10, 3, .8
    budgets = [20, 50, 100, 300]
    dgps = ["SM", "PL_equal", "PL_unequal"]
    write_json(OUT/"synthetic_settings.json", {
        "n": n, "r": r, "beta": beta, "repetitions": repetitions, "test_reports": 2000,
        "budgets": budgets, "matched_expected_inversions": logz_mean(r, beta)[1],
        "PL_equal_theta_in_center_order": matched_pl_theta(n, r, beta, "equal")[0].tolist(),
        "PL_unequal_theta_in_center_order": matched_pl_theta(n, r, beta, "unequal")[0].tolist()})
    for d, dgp in enumerate(dgps):
        for rep in range(repetitions):
            rng = np.random.default_rng(SEED+10000+1000*d+rep)
            center = rng.permutation(n)
            if dgp == "SM":
                sample = lambda count: sample_sm(rng, count, n, r, center, beta)
                truth = lambda y: beta*distances(y, center)+logz_mean(r, beta)[0]
            else:
                theta = np.zeros(n)
                theta[center] = matched_pl_theta(n, r, beta, dgp.split("_")[1])[0]
                sample = lambda count: sample_pl(rng, count, n, r, theta)
                from src.models import pl_nll
                truth = lambda y: pl_nll(y, theta)
            development, test = sample(max(budgets)), sample(2000)
            oracle = float(truth(test).mean())
            for size in budgets:
                record, _, _, sm, pl = fit_compare(development[:size], test, n, SEED+rep)
                record.update(dgp=dgp, N=size, replicate=rep, oracle_nll=oracle,
                              SM_center_error=kendall(sm.order, center), PL_center_error=kendall(pl.order, center))
                rows.append(record)
                w = pair_counts(development[:size], n)
                for name, method in [("borda", borda), ("posest", posest), ("greedy", greedy), ("multistart", multistart)]:
                    order = method(w, SEED+rep)
                    algorithm_rows.append({"dgp": dgp, "N": size, "replicate": rep, "algorithm": name,
                                           "objective_gap": kemeny_cost(w, order)-sm.objective,
                                           "central_kendall": kendall(order, center)})
            if (rep+1) % 5 == 0:
                print(f"Synthetic: {dgp}, {rep+1}/{repetitions} repetitions", flush=True)
                pd.DataFrame(rows).to_csv(OUT/"synthetic_replicates.csv", index=False)
    df = pd.DataFrame(rows)
    df.to_csv(OUT/"synthetic_replicates.csv", index=False)
    pd.DataFrame(algorithm_rows).to_csv(OUT/"synthetic_algorithms.csv", index=False)
    summary = []
    for (dgp, size), group in df.groupby(["dgp", "N"], sort=False):
        mean = group.delta.mean()
        half = student_t.ppf(.975, len(group)-1)*group.delta.sem()
        summary.append({"dgp": dgp, "N": size, "repetitions": len(group),
                        "SM_nll": group.SM_nll.mean(), "PL_nll": group.PL_nll.mean(),
                        "delta": mean, "ci_low": mean-half, "ci_high": mean+half,
                        "SM_calibrated_nll": group.SM_calibrated_nll.mean(),
                        "SM_center_error": group.SM_center_error.mean(),
                        "PL_center_error": group.PL_center_error.mean(), "oracle_nll": group.oracle_nll.mean()})
    pd.DataFrame(summary).to_csv(OUT/"synthetic_summary.csv", index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=["real", "synthetic", "all"], default="all")
    parser.add_argument("--synthetic-reps", type=int, default=30)
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    PRIVATE.mkdir(exist_ok=True)
    write_json(OUT/"environment.json", {"python": sys.version, "platform": platform.platform(),
               "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__,
               "seed": SEED, "protocol_sha256": hashlib.sha256((ROOT/"docs/protocols/PROTOCOL.md").read_bytes()).hexdigest()})
    t0 = time.perf_counter()
    if args.part in ("real", "all"):
        real_experiments()
    if args.part in ("synthetic", "all"):
        synthetic_experiments(args.synthetic_reps)
    print(f"Finished {args.part} in {time.perf_counter()-t0:.1f} seconds", flush=True)


if __name__ == "__main__":
    main()
