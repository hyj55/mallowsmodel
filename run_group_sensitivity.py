"""Frozen repeated within-group and whole-group-holdout empirical experiments."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import json
from pathlib import Path
import platform
import time

import numpy as np
import pandas as pd
import scipy

from src.group_sensitivity import (ROOT, METHODS, SCHEMES, SPLIT_PLAN, SEED,
    load_group_tasks, within_split, holdout_split, matched_training,
    fit_candidates, group_score, paired_contrast)

PRIVATE = ROOT / 'results/private/group_sensitivity'
PUBLIC = ROOT / 'results/group_sensitivity'


def json_value(value):
    if isinstance(value, dict):
        return {str(k): json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [json_value(v) for v in value]
    if isinstance(value, (np.integer, np.bool_)):
        return value.item()
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else str(float(value))
    return value


def fit_json(fit):
    return json_value(dict(status=fit.status, order=fit.order, beta=fit.beta,
                           theta=fit.theta, metadata=fit.metadata))


def run_task(task, quick=False):
    start = time.perf_counter()
    directory = PRIVATE / task.name
    directory.mkdir(parents=True, exist_ok=True)
    cache, scores, contrasts, audit = {}, [], [], []
    context_count = 0
    plan = ((70, 2),) if quick else SPLIT_PLAN
    log = gzip.open(directory / 'fits.jsonl.gz', 'wt')

    def fit(ids, context):
        nonlocal context_count
        a = task.y[ids]
        unique, counts = np.unique(a, axis=0, return_counts=True)
        key = unique.tobytes(), counts.tobytes()
        if key not in cache:
            cache[key] = fit_candidates(a, task.n)
        fitted = cache[key]
        context_count += 1
        log.write(json.dumps(dict(context, train_ids=ids.tolist(),
            fits={m: fit_json(v) for m, v in fitted.items()}), allow_nan=False) + '\n')
        for method, value in fitted.items():
            meta = value.metadata
            audit.append(dict(context, method=method, status=value.status,
                n_train=len(ids), unseen=meta.get('unseen'), item_min=meta.get('item_min'),
                pair_min=meta.get('pair_min'), p=meta.get('p'), lambda_=meta.get('lambda_'),
                mu=meta.get('mu'), coverage_ratio=meta.get('coverage_ratio'),
                branch=meta.get('branch', meta.get('algorithm', '')), depth=meta.get('depth')))
        return fitted

    def evaluate(fitted, ids, n_train, context):
        loss = {method: fitted[method].nll(task.y[ids]) for method in METHODS}
        for method in METHODS:
            record = dict(context, method=method, n_train=n_train,
                          **group_score(loss[method], fitted[method], len(ids)))
            mask = np.isfinite(loss[method]) & np.isfinite(loss['pl'])
            record.update(n_paired=int(mask.sum()) if method != 'pl' else 0,
                delta_sum=float((loss[method][mask] - loss['pl'][mask]).sum()) if method != 'pl' else 0.)
            scores.append(record)
        return loss

    for percent, repetitions in plan:
        for repeat in range(repetitions):
            train, test = within_split(task.groups, task.index, percent, repeat)
            if np.intersect1d(train, test).size or len(train) + len(test) != len(task.y):
                raise AssertionError('Invalid split')
            base = dict(dataset=task.name, design='within', percent=percent, repeat=repeat)
            pooled = fit(train, dict(base, scheme='pooled', group=-1))
            for g, name in enumerate(task.group_names):
                tr = train[task.groups[train] == g]
                te = test[task.groups[test] == g]
                matched = matched_training(train, len(tr), task.index, percent, repeat, g)
                if len(tr) != len(matched) or not np.isin(matched, train).all():
                    raise AssertionError('Invalid matched budget')
                ctx = dict(base, group=g, group_name=name)
                fitted = {'pooled': pooled,
                    'local': fit(tr, dict(base, scheme='local', group=g)),
                    'matched_pool': fit(matched, dict(base, scheme='matched_pool', group=g))}
                loss = {scheme: evaluate(fitted[scheme], te, len(train) if scheme == 'pooled' else len(tr),
                                         dict(ctx, scheme=scheme)) for scheme in SCHEMES}
                for method in METHODS[:-1]:
                    if all(fitted[s][method].status != 'ok' for s in SCHEMES):
                        continue
                    for reference in ('pooled', 'matched_pool'):
                        contrasts.append(dict(ctx, sm_method=method, reference=reference,
                            n_test=len(te), **paired_contrast(loss['local'][method], loss['local']['pl'],
                                                             loss[reference][method], loss[reference]['pl'])))
            if repeat % 20 == 0:
                print(task.name, 'within', percent, repeat, 'cache', len(cache), flush=True)
    for repeat in range(2 if quick else 100):
        train, test = holdout_split(task.groups, task.index, repeat)
        if np.intersect1d(task.groups[train], task.groups[test]).size:
            raise AssertionError('A group crossed the holdout boundary')
        base = dict(dataset=task.name, design='group_holdout', percent=70, repeat=repeat, scheme='pooled')
        fitted = fit(train, dict(base, group=-1))
        for g in np.unique(task.groups[test]):
            te = test[task.groups[test] == g]
            evaluate(fitted, te, len(train), dict(base, group=int(g), group_name=task.group_names[g]))
    log.close()
    frames = {'group_scores': pd.DataFrame(scores), 'contrasts': pd.DataFrame(contrasts),
              'fit_audit': pd.DataFrame(audit)}
    for name, frame in frames.items():
        frame.to_csv(directory / (name + '.csv.gz'), index=False, float_format='%.15g')
    elapsed = time.perf_counter() - start
    manifest = dict(dataset=task.name, quick=quick, source=task.source, n=task.n, r=task.y.shape[1],
        reports=len(task.y), groups=len(task.group_names), unit=task.unit,
        min_reports_per_group=int(np.bincount(task.groups).min()),
        max_reports_per_group=int(np.bincount(task.groups).max()),
        seed=SEED, split_plan=plan, holdout_repetitions=2 if quick else 100,
        fit_contexts=context_count, distinct_training_histograms=len(cache),
        candidate_fit_attempts=len(audit), elapsed_seconds=elapsed)
    (directory / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('FINISHED', task.name, round(elapsed, 1), 'seconds', flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--datasets', nargs='*')
    parser.add_argument('--quick', action='store_true', help='Development run in a separate private directory')
    parser.add_argument('--summarize-only', action='store_true')
    args = parser.parse_args()
    global PRIVATE
    if args.quick:
        PRIVATE = ROOT / 'results/private/group_sensitivity_quick'
    PRIVATE.mkdir(parents=True, exist_ok=True)
    if not args.summarize_only:
        tasks = load_group_tasks()
        if args.datasets:
            tasks = [t for t in tasks if t.name in args.datasets]
            if len(tasks) != len(args.datasets):
                raise ValueError('Unknown dataset name')
        # Workers get their destination explicitly via initializer; macOS uses spawn.
        with ProcessPoolExecutor(max_workers=args.workers, initializer=worker_directory,
                                 initargs=(str(PRIVATE),)) as pool:
            futures = {pool.submit(run_task, task, args.quick): task.name for task in tasks}
            for future in as_completed(futures):
                future.result()
    if not args.quick:
        from src.group_sensitivity_summary import publish_summaries
        publish_summaries(PRIVATE, PUBLIC)


def worker_directory(path):
    global PRIVATE
    PRIVATE = Path(path)


if __name__ == '__main__':
    main()
