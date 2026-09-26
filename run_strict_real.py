"""Original reports, frozen grouped split, literal estimators, disjoint diagnostics."""
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from src.strict_models import fit_sm_strict, fit_pl_mm, StrictFit
from src.strict_features import discovery_choices
from src.models import kendall, pair_counts
from src.diagnostics import pair_arrays, context_slope, shell_decomposition
from download_strict_data import RAW

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results/strict_features'
SEED = 202609251


def load_tasks():
    tasks = []
    for path in sorted(RAW.glob('*.soc')):
        records, title = [], ''
        for line in path.read_text().splitlines():
            if line.startswith('# TITLE:'):
                title = line.split(':', 1)[1].strip()
            if not line or line.startswith('#'):
                continue
            count, order = line.split(':')
            order = [int(x)-1 for x in order.split(',')]
            assert sorted(order) == list(range(4))
            records.extend([order]*int(count))
        y = np.asarray(records, int)
        tasks.append(dict(name=path.stem, title=title, family='preflib', n=4, r=4,
                          y=y, group=np.arange(len(y)), truth=np.arange(4),
                          grouping='anonymous_upstream_aggregated_records'))
    for arm in ['A', 'B']:
        by_size = {r: [] for r in [2, 3, 5, 6]}
        group = {r: [] for r in by_size}
        sources = sorted(RAW.glob(f'*ratingsrankings{arm}*.json'))
        for file_number, path in enumerate(sources):
            data = json.loads(path.read_text())
            assert len(data) == 240
            for block in range(60):
                records = data[4*block:4*block+4]
                assert sorted(x['frames'] for x in records) == [2, 3, 5, 6]
                for row in records:
                    r = row['frames']
                    local = np.array(row['rankings'], int)
                    shown = np.array(row['groundtruth'], int)
                    assert sorted(local) == list(range(1, r+1))
                    assert len(set(shown)) == r and np.all((shown >= 50) & (shown <= 79))
                    # The export replaced largest count by label 1. List
                    # positions still encode the participant's reported order.
                    y = np.sort(shown)[::-1][local-1]-50
                    assert set(y) == set(shown-50)
                    by_size[r].append(y)
                    group[r].append(file_number*60+block)
        for r in by_size:
            tasks.append(dict(name=f'dots2024_{arm}_r{r}', title=f'2024 dots arm {arm}, r={r}',
                family='dots2024', arm=arm, n=30, r=r, y=np.asarray(by_size[r]),
                group=np.asarray(group[r]), truth=np.arange(30),
                grouping='source_export_participant_blocks'))
    assert len(tasks) == 16
    return tasks


def split_task(task, task_index):
    key = 100+ord(task['arm']) if task['family'] == 'dots2024' else task_index
    unique = np.unique(task['group'])
    shuffled = np.random.default_rng(np.random.SeedSequence([SEED, 19, key])).permutation(unique)
    a, b = int(.6*len(unique)), int(.8*len(unique))
    parts = [np.flatnonzero(np.isin(task['group'], s)) for s in [shuffled[:a], shuffled[a:b], shuffled[b:]]]
    assert len(set(np.concatenate(parts))) == len(task['y'])
    return parts


def ci(values, seed, resamples=2000, unit_identified=True):
    values = np.asarray(values, float)
    if not unit_identified or not np.isfinite(values).all():
        return np.nan, np.nan
    rng = np.random.default_rng(seed)
    sampled = rng.integers(len(values), size=(resamples, len(values)))
    return tuple(np.quantile(values[sampled].mean(axis=1), [.025, .975]))


def diagnostic_profiles(y, train, sm, pl, task, split):
    a = pair_arrays(y, sm.order, sm.beta, pl.theta)
    tr = pair_arrays(train, sm.order, sm.beta, pl.theta)
    rows = []
    for h in np.unique(a['gap']):
        cuts = np.quantile(tr['worth_gap'][tr['gap'] == h], [1/3, 2/3])
        bins = np.searchsorted(cuts, a['worth_gap'], side='right')
        for bin_id in range(3):
            mask = (a['gap'] == h) & (bins == bin_id)
            if not mask.any():
                continue
            rows.append(dict(dataset=task['name'], split=split, gap=int(h), bin=bin_id,
                observations=int(mask.sum()), contributing_reports=int(mask.any(axis=1).sum()),
                observed=a['z'][mask].mean(), sm=a['sm'][mask].mean(), pl=a['pl'][mask].mean(),
                lower_cut=cuts[0], upper_cut=cuts[1]))
    return rows


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = load_tasks()
    results, descriptions, splits, predictions, contexts, shells, profiles, selections = ([] for _ in range(8))
    parameters = {}
    for task_index, task in enumerate(tasks):
        print('REAL', task_index+1, task['name'], flush=True)
        fit_idx, discovery_idx, test_idx = split_task(task, task_index)
        train, discovery, test = [task['y'][x] for x in [fit_idx, discovery_idx, test_idx]]
        n, r = task['n'], task['r']
        unit_identified = task['family'] != 'preflib'
        uncertainty = 'conditional_participant_bootstrap' if unit_identified else 'unavailable_assessor_ids'
        for split, indices in [('fit', fit_idx), ('discovery', discovery_idx), ('confirmation', test_idx)]:
            splits.extend(dict(dataset=task['name'], record=int(i), group=int(task['group'][i]), split=split) for i in indices)
        counts = np.bincount(train.ravel(), minlength=n)
        w = pair_counts(train, n)
        descriptions.append(dict(dataset=task['name'], title=task['title'], n=n, r=r,
            reports=len(task['y']), N=len(train), discovery=len(discovery), confirmation=len(test),
            lambda_=len(train)*r*(r-1)/(n*(n-1)), mu=len(train)*r/n,
            unseen=int((counts == 0).sum()), item_min=int(counts.min()), item_max=int(counts.max()),
            observed_pairs=int(((w+w.T)[np.triu_indices(n, 1)] > 0).sum()),
            distinct_sets=len(np.unique(np.sort(task['y'], axis=1), axis=0)),
            grouping=task['grouping'], objective_truth_available=True, reports_dropped=0))
        models = {}; timings = {}
        t0 = time.perf_counter(); models['pl'] = fit_pl_mm(train, n); timings['pl'] = time.perf_counter()-t0
        for method in ['mle', 'sharp', 'efficient', 'borda']:
            t0 = time.perf_counter()
            models[method] = fit_sm_strict(train, n, method, beta0=.1, pair_seed=SEED+task_index)
            timings[method] = time.perf_counter()-t0
        parameters[task['name']] = {}
        pl_loss = models['pl'].nll(test)
        for method, model in models.items():
            loss = model.nll(test); delta = loss-pl_loss
            low, high = ci(delta, SEED+task_index, unit_identified=unit_identified)
            results.append(dict(dataset=task['name'], method=method, status=model.status, uncertainty_status=uncertainty,
                nll=float(loss.mean()), delta=float(delta.mean()), delta_lo=low, delta_hi=high,
                infinite_reports=int(np.isinf(loss).sum()),
                objective_kendall=kendall(model.order, task['truth']) if model.status == 'ok' else np.nan,
                beta=model.beta, seconds=timings[method],
                branch=model.metadata.get('branch', 'hunter_mm' if method == 'pl' else 'unavailable'),
                depth=model.metadata.get('depth', np.nan), certified=model.metadata.get('certified', False)))
            parameters[task['name']][method] = dict(order=model.order.tolist() if model.order is not None else None,
                theta=model.theta.tolist() if model.theta is not None else None,
                beta=str(model.beta) if not np.isfinite(model.beta) else model.beta,
                status=model.status, metadata=model.metadata)
            predictions.extend(dict(dataset=task['name'], method=method, record=int(i),
                group=int(task['group'][i]), nll=float(v)) for i, v in zip(test_idx, loss))
        primary = models['mle']
        choice = discovery_choices(discovery, primary, models['pl'])
        selection = dict(dataset=task['name'], **choice)
        for selector in ['pair', 'context']:
            name = choice[selector+'_choice']
            model = primary if name == 'sm' else models['pl'] if name == 'pl' else None
            selection[selector+'_confirmation_nll'] = float(model.nll(test).mean()) if model is not None else np.nan
        selections.append(selection)
        if primary.status == 'ok' and models['pl'].status == 'ok' and np.isfinite(primary.beta):
            for split, y in [('discovery', discovery), ('confirmation', test)]:
                decomposition = shell_decomposition(y, primary.order, primary.beta, models['pl'].theta)
                for component in ['total', 'shell_mass', 'within_shell']:
                    low, high = ci(decomposition[component], SEED+task_index+1, unit_identified=unit_identified)
                    shells.append(dict(dataset=task['name'], split=split, component=component, uncertainty_status=uncertainty,
                        value=decomposition[component].mean(), ci_low=low, ci_high=high))
                arrays = pair_arrays(y, primary.order, primary.beta, models['pl'].theta)
                c = context_slope(arrays, resamples=2000 if unit_identified else 0, seed=SEED+task_index+2)
                contexts.append(dict(dataset=task['name'], split=split, **c))
                profiles.extend(diagnostic_profiles(y, train, primary, models['pl'], task, split))
        for filename, rows in [('real_results', results), ('real_datasets', descriptions),
                ('real_splits', splits), ('real_predictions', predictions), ('real_context', contexts),
                ('real_shells', shells), ('real_gap_profiles', profiles), ('real_selection', selections)]:
            pd.DataFrame(rows).to_csv(OUT/f'{filename}.csv', index=False)
        (OUT/'real_parameters.json').write_text(json.dumps(parameters, indent=2,
            default=lambda x: x.item() if hasattr(x, 'item') else str(x))+'\n')
        print('  ', {name: model.status for name, model in models.items()}, flush=True)
    (OUT/'real_manifest.json').write_text(json.dumps(dict(seed=SEED, tasks=len(tasks),
        source_reports=sum(len(x['y']) for x in tasks), source_reports_dropped=0,
        protocol_sha256=hashlib.sha256((ROOT/'docs/protocols/STRICT_FEATURE_PROTOCOL.md').read_bytes()).hexdigest()), indent=2)+'\n')
    print('DONE', flush=True)


if __name__ == '__main__':
    run()
