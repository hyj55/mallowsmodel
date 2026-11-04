"""S4-T: independently selected constants for each (n, r, training N)."""
from experiments.section44.design import candidate_grid, confirmation_cells

ROOT_SEED = 202611040
CALIBRATION_REPEATS = 20
CONFIRMATION_REPEATS = 100
BASE_COMMIT = 'c6d71925c8e31d8b0b9d3c3ab64ca9cc1c283674'


def group_key(c):
    return f"n{c['n']}-r{c['r']}-N{c['N']}"


def holdout_size(N):
    return max(1, (N + 2) // 3)


def cells():
    return [c for c in confirmation_cells() if c['r'] < c['n'] and
            c['N'] * c['r'] * (c['r'] - 1) <= c['n'] * (c['n'] - 1)]


def protocol():
    return dict(
        experiment='S4-T', base_commit=BASE_COMMIT, root_seed=ROOT_SEED,
        calibration_repeats=CALIBRATION_REPEATS,
        confirmation_repeats=CONFIRMATION_REPEATS, cells=cells(),
        candidates=candidate_grid(), selection_key=['n', 'r', 'N'],
        selection=('One candidate per family and (n,r,N), minimizing equal-cell mean '
                   'validation whole-ranking NLL across 20 independent training/validation '
                   'draws per signal cell. Signal/beta0 controls sharing (n,r,N) share the '
                   'same candidate. Every planned calibration fit must complete; zero depth '
                   'and the inherited Borda fallback are eligible. Exact ties use candidate ID. '
                   'No true-center error or confirmation outcome is used for selection.'),
        partitions=('N is the number of fitting reports, matching S4. Validation and test '
                    'sets each have ceil(N/3), at least one, independent reports under the '
                    'same center as their training set. Calibration generates training and '
                    'validation only. Confirmation uses 100 fresh independent training/test '
                    'draws; it does not rerun selection. No validation-to-training refit: '
                    'the fitting budget remains N. These are disjoint sampling roles, '
                    'not folds of a fixed dataset; tiny-N rounding is explicit.'),
        fitting=('Unchanged S4 center algorithms and candidate configurations. Conditional '
                 'on each fitted center, train-only profile beta on [0,10], as in P0. '
                 'Truth beta is never supplied to likelihood fitting; beta0 remains the '
                 'supplied simulation bound used by the center schedule.'),
        comparators=['global_borda', 'efficient_proof', 'sharp_proof',
                     'efficient_S4_locked', 'sharp_S4_locked',
                     'efficient_per_setting', 'sharp_per_setting'],
        primary_outcomes=['test_whole_ranking_NLL', 'Kendall_error_to_true_center'],
        uncertainty=('Paired differences per independent confirmation draw, 100 draws per '
                     'cell. Mean, MCSE, pointwise t95 interval. Holm correction separately '
                     'by outcome and per-setting family across complete cells. Intervals '
                     'condition on the selected constants, not on repeating selection.'),
        resources=dict(sieve_seconds_per_packing=30, sieve_memory_bytes=512 << 20,
                       total_terminal_seconds=120, workers=3),
        failure_policy=('Retain every attempt; no reroll, approximate sieve or test-driven '
                        'replacement. A candidate with any calibration failure is ineligible. '
                        'A confirmation failure makes its unconditional cell mean unavailable.'),
        scope=('All 90 partial-ranking signal settings of S4 with lambda<=1, grouped into '
               '82 (n,r,N) keys. Original S4 files/results remain unchanged. Same anchored '
               '25 Efficient / 35 Sharp candidates; not a Cartesian grid or the proposed '
               'adaptive-eta algorithm. No mandatory positive-depth selection filter.'),
    )
