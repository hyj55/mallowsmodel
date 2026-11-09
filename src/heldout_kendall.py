"""Report-level Kendall loss, independent of dispersion and test-time tuning."""
import math
import numpy as np
from .models import distances, logz_mean


def report_loss(y, order, mass=None):
    """Restrict the saved catalogue order to each display; never reorder reports.

    With mass, return a population expectation, not an unweighted support mean.
    An infinite probabilistic loss does not make a finite order unavailable.
    """
    y = np.asarray(y, dtype=int)
    if order is None:
        return dict(test_kendall_mean=math.nan, test_kendall_sum=math.nan,
                    evaluation_count=len(y), evaluation_target='population' if mass is not None else 'test_reports')
    order = np.asarray(order, dtype=int)
    if sorted(order.tolist()) != list(range(len(order))):
        raise ValueError('A complete strict catalogue order is required')
    d = distances(y, order)
    if mass is None:
        mean, total = float(d.mean()), int(d.sum())
    else:
        mass = np.asarray(mass, float)
        if mass.shape != d.shape or (mass < 0).any() or not np.isclose(mass.sum(), 1):
            raise ValueError('Population masses must be nonnegative and sum to one')
        mean, total = float(mass @ d), math.nan
    return dict(test_kendall_mean=mean, test_kendall_sum=total,
                evaluation_count=len(y), evaluation_target='population' if mass is not None else 'test_reports')


def beta_audit(beta, beta0=None, beta_true=None, config=None):
    """A plug-in estimate is not a test of the population lower-bound assumption."""
    b = float(beta) if beta is not None else math.nan
    out = dict(beta_fit=b, algorithm_beta0=beta0, beta_true=beta_true,
               beta_fit_below_beta0=None if beta0 is None or math.isnan(b) else bool(b < beta0),
               true_beta_below_beta0=None if beta0 is None or beta_true is None else bool(beta_true < beta0))
    if beta0 is None:
        out['constant_beta0_status'] = 'not_an_input'
    elif config is None:
        out['constant_beta0_status'] = 'supplied_input_not_inferred'
    else:
        # The proof map has A=256, width coefficient=1, terminal coefficient=8.
        # In addition b0<=1/64 and rho<1 imply K(beta0)>256 for finite beta0.
        changed = config['A'] != 256 or config['c_width'] != 1 or config.get('c_terminal', 8) != 8
        K = config.get('K')
        out['constant_beta0_status'] = ('no_common_proof_inverse' if changed or (K is not None and K <= 256)
                                         else 'supplied_input_not_inferred')
        out['K_below_proof_infimum'] = None if K is None else K < 256
    return out


def mean_nll(y, saved, mass=None):
    from .repeated_holdout import restore_fit
    f = dict(saved)
    f.setdefault('method', 'pl' if f.get('theta') is not None else 'sm')
    f.setdefault('metadata', {})
    f.setdefault('status', 'ok')
    f.setdefault('theta', None)
    f.setdefault('beta', math.nan)
    v = restore_fit(f).nll(y)
    return float(np.mean(v) if mass is None else np.asarray(mass) @ v)
