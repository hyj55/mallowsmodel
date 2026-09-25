"""Frozen exploratory additions. Reuses original training samples."""
import argparse
import json
import numpy as np
import pandas as pd
from run_strict_simulations import grid, SEED, OUT, finite_summary
from run_strict_real import load_tasks, split_task, diagnostic_profiles
from src.strict_features import draw_small, small_law, discovery_choices
from src.strict_models import fit_sm_strict, fit_pl_mm, StrictFit, profile_beta_unbounded
from src.models import distances
from src.diagnostics import pair_arrays, context_slope


def budgets():
    old = pd.read_csv(OUT/'bridge_selection_replicates.csv')
    rows = []
    for cell, (n, r, N, family, value, shape) in enumerate(grid('bridge')):
        if (n, r, N, shape) != (8, 3, 448, 'equal'):
            continue
        print('BUDGET', value, flush=True)
        for rep in range(40):
            trng, drng, _, _ = [np.random.default_rng(x) for x in
                np.random.SeedSequence([SEED, 0, cell, rep]).spawn(4)]
            truth = trng.permutation(n)
            train = draw_small(trng, N, truth, family, value, shape, r)
            discovery = draw_small(drng, 1000, truth, family, value, shape, r)
            sm, pl = fit_sm_strict(train, n), fit_pl_mm(train, n)
            canonical, probability, _ = small_law(n, r, family, value, shape)
            losses = {'sm': float(probability@sm.nll(truth[canonical])),
                      'pl': float(probability@pl.nll(truth[canonical]))}
            previous = old[(old.cell == cell) & (old.rep == rep)].iloc[0]
            assert np.allclose([losses['sm'], losses['pl']],
                               [previous.sm_nll, previous.pl_nll], atol=1e-12)
            for budget in [20, 60, 200, 1000]:
                choice = discovery_choices(discovery[:budget], sm, pl)
                for selector in ['pair', 'context']:
                    selected = choice[selector+'_choice']
                    if budget == 1000:
                        assert selected == previous[selector+'_choice']
                    loss = losses.get(selected, np.nan)
                    rows.append(dict(cell=cell, rep=rep, value=value, budget=budget,
                        selector=selector, choice=selected, sm_nll=losses['sm'],
                        pl_nll=losses['pl'], selected_nll=loss,
                        correct=float(loss <= min(losses.values())+1e-12)
                                if np.isfinite(loss) else np.nan,
                        regret=loss-min(losses.values()),
                        context_eligible=choice.get('context_eligible_cells', 0)))
    df = pd.DataFrame(rows)
    df.to_csv(OUT/'followup_budget_replicates.csv', index=False)
    summaries = []
    for key, g in df.groupby(['value', 'budget', 'selector']):
        row = dict(zip(['value', 'budget', 'selector'], key))
        row.update(repetitions=len(g), abstentions=int((g.choice == 'abstain').sum()))
        for metric in ['correct', 'regret']:
            row.update(finite_summary(g[metric], metric))
        summaries.append(row)
    pd.DataFrame(summaries).to_csv(OUT/'followup_budget_summary.csv', index=False)
    differences = []
    for (value, selector), g in df.groupby(['value', 'selector']):
        p = g.pivot(index='rep', columns='budget', values='regret')
        for budget in [20, 60, 200]:
            differences.append(dict(value=value, selector=selector, budget=budget,
                **finite_summary(p[budget]-p[1000], 'excess_regret_over_1000')))
    pd.DataFrame(differences).to_csv(OUT/'followup_budget_paired.csv', index=False)
    print('Verified all 200 training fits and 1000-report selector replays', flush=True)


def objective():
    fitted = json.loads((OUT/'real_parameters.json').read_text())
    contexts, profiles = [], []
    for index, task in enumerate(load_tasks()):
        fit_idx, disc_idx, test_idx = split_task(task, index)
        train = task['y'][fit_idx]
        saved = fitted[task['name']]['pl']
        if saved['status'] != 'ok':
            for split in ['discovery', 'confirmation']:
                contexts.append(dict(dataset=task['name'], split=split,
                    status='pl_fit_unavailable', reference='external_objective_order'))
            continue
        pl = StrictFit('pl', np.asarray(saved['order']),
                      theta=np.asarray(saved['theta']), metadata=saved['metadata'])
        beta = profile_beta_unbounded(distances(train, task['truth']).sum(),
                                      len(train), task['r'])
        sm = StrictFit('objective_reference_only', task['truth'], beta=beta, metadata={})
        for split, indices in [('discovery', disc_idx), ('confirmation', test_idx)]:
            y = task['y'][indices]
            context = context_slope(pair_arrays(y, sm.order, beta, pl.theta),
                                    resamples=2000, seed=SEED+index+2)
            contexts.append(dict(dataset=task['name'], split=split,
                reference='external_objective_order', reference_beta=beta, **context))
            profiles.extend(diagnostic_profiles(y, train, sm, pl, task, split))
    pd.DataFrame(contexts).to_csv(OUT/'real_objective_context.csv', index=False)
    pd.DataFrame(profiles).to_csv(OUT/'real_objective_gap_profiles.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', choices=['budgets', 'objective'], required=True)
    args = parser.parse_args()
    (budgets if args.part == 'budgets' else objective)()
