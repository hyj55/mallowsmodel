"""Exploratory Kemeny solver: add violated transitivity constraints on demand.

The feasible set is the same as models.milp_center. This changes computation,
not the selective likelihood. Every retained lower bound comes from a solved
relaxation; every reported order is checked against the original objective.
"""
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from .models import _linear_order_constraints, kemeny_cost, multistart


def cutting_plane_center(w, seed=0, time_limit=60.):
    t0 = time.perf_counter()
    n = len(w)
    order = multistart(w, seed)
    upper = kemeny_cost(w, order)
    ii, jj, all_constraints = _linear_order_constraints(n)
    a = all_constraints.A
    c = (w[jj, ii]-w[ii, jj]).astype(float)
    base = int(w[ii, jj].sum())
    lower = int(np.minimum(w, w.T)[ii, jj].sum())
    active = np.zeros(a.shape[0], dtype=bool)
    x = (c < 0).astype(float)
    integer_phase = False
    iterations = 0
    status = "time limit"
    while time.perf_counter()-t0 < time_limit:
        ax = a@x
        violated = (ax < -1e-7) | (ax > 1+1e-7)
        active |= violated
        remaining = time_limit-(time.perf_counter()-t0)
        if remaining <= 0:
            break
        constraint = LinearConstraint(a[active], 0, 1)
        result = milp(c, integrality=np.ones(len(c)) if integer_phase else np.zeros(len(c)),
                      bounds=Bounds(0, 1), constraints=constraint,
                      options={"time_limit": remaining, "mip_rel_gap": 0.})
        iterations += 1
        status = str(result.message)
        bound = getattr(result, "mip_dual_bound", None)
        if result.status == 0:
            bound = result.fun
        if bound is not None and np.isfinite(bound):
            lower = max(lower, int(np.ceil(base+bound-1e-5)))
        if result.x is None:
            break
        x = result.x
        ax = a@x
        valid = np.all((ax >= -1e-6) & (ax <= 1+1e-6))
        integral = np.max(np.abs(x-np.round(x))) < 1e-6
        if valid and integral:
            wins = np.zeros(n)
            np.add.at(wins, ii, np.round(x))
            np.add.at(wins, jj, 1-np.round(x))
            if len(np.unique(wins)) != n:
                raise RuntimeError("Nontransitive solution")
            candidate = np.argsort(-wins)
            cost = kemeny_cost(w, candidate)
            if cost < upper:
                order, upper = candidate, cost
            if lower == upper:
                break
        if valid and not integral:
            integer_phase = True
        if result.status != 0:
            break
    if lower > upper:
        raise RuntimeError("Lower bound exceeds feasible objective")
    return order, {"lower_bound": lower, "upper_bound": upper,
                   "absolute_gap": upper-lower, "certified": upper == lower,
                   "seconds": time.perf_counter()-t0, "active_constraints": int(active.sum()),
                   "iterations": iterations, "status": status}
