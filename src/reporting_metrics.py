"""Report-only scales for saved whole-ranking loss differences; no refitting."""
import math

import numpy as np
import pandas as pd


def uniform_scaled_differences(frame):
    """Append delta / log(r!) and its uncertainty on fixed-r result rows.

    Each row must describe reports of one size r. These summaries cannot be
    applied to a mixed-size task by substituting its average report size.
    Preserve raw values, unavailable entries, infinities and interval targets.
    """
    out = frame.copy()
    r = pd.to_numeric(out['r'], errors='raise')
    if not (np.isfinite(r).all() and (r >= 2).all() and (r == np.floor(r)).all()):
        raise ValueError('Uniform scaling requires a fixed integer report size r >= 2 per row')
    fields = [c for c in out if c == 'delta' or c.startswith('delta_')]
    if 'uniform_nll' in out or any(c.startswith('delta_uniform') for c in fields):
        raise ValueError('Uniform-scaled columns already exist')
    out['uniform_nll'] = r.map(lambda size: math.lgamma(int(size) + 1))
    for field in fields:
        out['delta_uniform' + field[len('delta'):]] = out[field] / out.uniform_nll
    return out
