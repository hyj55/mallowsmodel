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
OUT = ROOT / "results/regularized_learning"
PRIVATE = ROOT / "results/private/regularized_learning"
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
                  "sm_optimization": sm.metadata, "pl_near_theta": pl_near.theta.tolist(),
                  "inner_sm_order": inner_sm.order.tolist(), "inner_beta": inner_sm.beta,
                  "inner_validation_nll": [float(inner_sm.nll(valid, f).mean()) for f in BETA_FACTORS]}
    return record, losses, parameters, sm, pl


def real_experiments():
    all_data = load_all()
    write_json(OUT/"data_audit.json", [audit(d) for d in all_data])
    save_manifest(OUT)
    records, summaries, params = [], [], {}
    for data in all_data:
        pool, test_idx = outer_split(data)
        if data.name == "beans":
            budgets, repetitions = [20, 50, 100, 200, 400, len(pool)], 5
        elif data.name == "sushi_a":
            budgets, repetitions = [20, 50, 100, 300, 1000, 3000], 5
        else:
            budgets, repetitions = [100, 300, 1000, 3000], 5
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


def main():
    OUT.mkdir(parents=True,exist_ok=True);PRIVATE.mkdir(parents=True,exist_ok=True)
    write_json(OUT/'environment.json',dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__,seed=SEED,repetitions=5))
    real_experiments()


if __name__=='__main__':main()
