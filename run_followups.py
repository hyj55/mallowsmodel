"""Exploratory follow-ups motivated by the primary results; test data never tune fits."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import LinearConstraint, minimize

from src.data import load_beans, load_sushi
from src.models import SMFit, distances, fit_beta, pair_counts, pl_nll, pl_objective
from src.cutting_plane import cutting_plane_center
from run_experiments import OUT, SEED, fit_compare, outer_split, paired_ci, write_json


def fit_pl_with_order(y, order, tau, initial):
    """Convex ridge PL objective subject to the SAME order as the fitted SM."""
    n = len(order)
    a = np.zeros((n-1, n))
    for k in range(n-1):
        a[k, order[k]], a[k, order[k+1]] = 1, -1
    start = np.empty(n)
    start[order] = np.sort(initial)[::-1]
    def averaged_objective(theta):
        value, gradient = pl_objective(theta, y, tau)
        return value/len(y), gradient/len(y)
    result = minimize(averaged_objective, start, jac=True, method="SLSQP",
                      constraints=[LinearConstraint(a, 0, np.inf), LinearConstraint(np.ones((1,n)), 0, 0)],
                      options={"ftol": 1e-10, "maxiter": 1000})
    if not result.success or (a@result.x).min() < -1e-6:
        raise RuntimeError(f"Ordered PL optimization failed: {result.message}")
    return result.x


def same_order_followup():
    parameters = json.loads((OUT/"fitted_parameters.json").read_text())
    rows, summary = [], []
    for data, size in [(load_beans(), 673), (load_sushi("a"), 3000)]:
        diffs, reverse_diffs = [], []
        pool, test_idx = outer_split(data)
        for rep in range(5):
            tag = f"{data.name}_N{size}_rep{rep}"
            p = parameters[tag]
            train_idx = np.random.default_rng(SEED+11+rep).permutation(pool)[:size]
            y, test = data.y[train_idx], data.y[test_idx]
            order, theta = np.array(p["sm_order"]), np.array(p["pl_theta"])
            ordered_theta = fit_pl_with_order(y, order, p["tau"], theta)
            sm_nll = SMFit(order, p["beta"], 0, {}).nll(test)
            original_pl_nll = pl_nll(test, theta)
            ordered_nll = pl_nll(test, ordered_theta)
            pl_order = np.argsort(-theta)
            sm_on_pl = SMFit(pl_order, fit_beta(distances(y, pl_order).sum(), len(y), y.shape[1]), 0, {})
            sm_on_pl_nll = sm_on_pl.nll(test)
            delta = sm_nll-ordered_nll
            rev = sm_on_pl_nll-original_pl_nll
            diffs.append(delta)
            reverse_diffs.append(rev)
            rows.append({"dataset": data.name, "N": size, "replicate": rep,
                         "SM_nll": sm_nll.mean(), "PL_same_SM_order_nll": ordered_nll.mean(),
                         "same_SM_order_delta": delta.mean(), "SM_on_PL_order_nll": sm_on_pl_nll.mean(),
                         "PL_nll": original_pl_nll.mean(), "same_PL_order_delta": rev.mean()})
        for setting, values in [("same_SM_order", diffs), ("same_PL_order", reverse_diffs)]:
            v = np.mean(values, axis=0)
            lo, hi = paired_ci(v)
            summary.append({"dataset": data.name, "N": size, "setting": setting,
                            "delta": v.mean(), "ci_low": lo, "ci_high": hi})
    pd.DataFrame(rows).to_csv(OUT/"same_order_replicates.csv", index=False)
    pd.DataFrame(summary).to_csv(OUT/"same_order_summary.csv", index=False)
    print(pd.DataFrame(summary).round(5).to_string(index=False), flush=True)


def beans_year_transfer():
    data = load_beans()
    mask = np.char.endswith(data.groups.astype(str), "15")
    train = data.y[mask]
    test = data.y[~mask]
    rows, losses = [], []
    for rep in range(5):
        rng = np.random.default_rng(SEED+110000+rep)
        development = train[rng.permutation(len(train))]
        row, loss, _, _, _ = fit_compare(development, test, data.n, SEED+110000+rep)
        row.update(dataset="beans_2015_to_2016", replicate=rep, N=len(train), test_reports=len(test))
        rows.append(row)
        losses.append(loss)
    avg = np.mean(losses, axis=0)
    delta = avg[0]-avg[1]
    lo, hi = paired_ci(delta)
    clo, chi = paired_ci(avg[2]-avg[1])
    summary = {"dataset": "beans_2015_to_2016", "N": len(train), "test_reports": len(test),
               "SM_nll": avg[0].mean(), "PL_nll": avg[1].mean(), "delta": delta.mean(),
               "ci_low": lo, "ci_high": hi, "SM_calibrated_nll": avg[2].mean(),
               "calibrated_delta": (avg[2]-avg[1]).mean(), "calibrated_ci_low": clo, "calibrated_ci_high": chi}
    pd.DataFrame(rows).to_csv(OUT/"beans_transfer_replicates.csv", index=False)
    write_json(OUT/"beans_transfer_summary.json", summary)
    print(summary, flush=True)


def outer_fold_stability():
    """Five disjoint test folds; descriptive fold variation, not iid fold CIs."""
    rows, summaries = [], []
    for data in [load_beans(), load_sushi("a")]:
        rng = np.random.default_rng(SEED+220000)
        folds = np.array_split(rng.permutation(len(data.y)), 5)
        weighted = []
        for fold in range(5):
            test_idx = folds[fold]
            pool = np.concatenate([f for j, f in enumerate(folds) if j != fold])
            pool = rng.permutation(pool)[:min(3000, len(pool))]
            record, losses, _, _, _ = fit_compare(data.y[pool], data.y[test_idx], data.n, SEED+fold)
            record.update(dataset=data.name, fold=fold, N=len(pool), test_reports=len(test_idx))
            rows.append(record)
            weighted.append(losses[0]-losses[1])
        values = np.concatenate(weighted)
        summaries.append({"dataset": data.name, "pooled_delta": values.mean(),
                          "fold_delta_min": min(x.mean() for x in weighted),
                          "fold_delta_max": max(x.mean() for x in weighted),
                          "test_reports": len(values), "note": "Descriptive stability; no independent-fold CI"})
    pd.DataFrame(rows).to_csv(OUT/"outer_fold_replicates.csv", index=False)
    pd.DataFrame(summaries).to_csv(OUT/"outer_fold_summary.csv", index=False)
    print(pd.DataFrame(summaries).to_string(index=False), flush=True)


def cutting_plane_audit():
    data = load_sushi("b")
    pool, test = outer_split(data)
    pool = np.random.default_rng(SEED+11).permutation(pool)
    rows = []
    for size in [100, 3000]:
        y = data.y[pool[:size]]
        order, certificate = cutting_plane_center(pair_counts(y, data.n), SEED+size, time_limit=60.)
        beta = fit_beta(certificate["upper_bound"], size, 10)
        fit = SMFit(order, beta, certificate["upper_bound"], certificate)
        row = {"N": size, **certificate, "order": order.tolist(), "beta": beta,
               "test_nll": float(fit.nll(data.y[test]).mean())}
        rows.append(row)
        write_json(OUT/"cutting_plane_pilot.json", rows)
        print({k:v for k,v in row.items() if k != "order"}, flush=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutting-plane", action="store_true", help="Also run two 60-second bound audits")
    args = parser.parse_args()
    same_order_followup()
    beans_year_transfer()
    outer_fold_stability()
    if args.cutting_plane:
        cutting_plane_audit()
