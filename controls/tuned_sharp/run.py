"""Single-allocation supplement for every unresolved E0/L0/S0 Sharp cell."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd

from controls.tuned_sharp.model import (SEED, block_grid, fit_block, pilot_order,
                                      validation_order, pilot_partition)
from src.manuscript_estimators import score_order
from src.predictive_models import sm_fit
from src.predictive_study import empirical_context, synthetic_context, array_hash
from src.repeated_holdout import load_tasks, restore_fit, save_fit, json_value
from src.models import kendall

PUBLIC = ROOT / 'results/tuned_block_sieve'
PRIVATE = ROOT / 'results/private/tuned_block_sieve/runs'
BASE_SHA = '80e246692d741eba54b06f380614f3396cb8d9f9'
CODE = ('controls/tuned_sharp/model.py', 'controls/tuned_sharp/run.py',
        'src/manuscript_estimators.py', 'src/sieve_budget_retry.py',
        'src/resource_sieve.py', 'src/predictive_models.py', 'src/predictive_study.py',
        'src/repeated_holdout.py', 'src/models.py', 'src/strict_models.py')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def signature():
    return {p: digest(ROOT/p) for p in CODE}


def selected_sources():
    with gzip.open(ROOT/'results/predictive/predictors.jsonl.gz', 'rt') as stream:
        records = [json.loads(line) for line in stream]
    return sorted([r for r in records if r['repeat'] == 0
                   and r['models']['sm_sharp']['status'] == 'sieve_resource_budget'],
                  key=lambda r: (r['study'], r['dataset'], r['n'], r['N']))


def case_id(record):
    study = 'E0' if record['study'] == 'P0' else record['study']
    return f"{study}-{record['dataset']}-n{record['n']}-N{record['N']}"


def get_context(source, tasks):
    if source['study'] == 'S0':
        context = synthetic_context(source['generator'], source['n'], source['N'], 0)
        units = {k: np.arange(len(v)) for k, v in context['data'].items()}
    else:
        task = tasks[source['dataset']]
        context = empirical_context(task, 0, None if source['study'] == 'P0' else source['N'])
        units = {k: task.units[ids] for k, ids in context['parts'].items()}
    assert {k: array_hash(v) for k, v in context['data'].items()} == source['data_sha256']
    return context, units


def seed_for(context, phase):
    return int(np.random.SeedSequence([SEED, context['split_key'], context['n'],
                                      context['N'], phase]).generate_state(1)[0])


def paired_interval(loss, reference, units, seed):
    _, inverse = np.unique(units, return_inverse=True)
    count = np.bincount(inverse)
    sums = np.bincount(inverse, weights=np.asarray(loss)-np.asarray(reference))
    rng = np.random.default_rng(seed)
    # Batched to keep the synthetic 4000-report bootstrap small.
    samples = []
    for _ in range(20):
        ids = rng.integers(0, len(count), size=(100, len(count)))
        samples.extend((sums[ids].sum(axis=1)/count[ids].sum(axis=1)).tolist())
    return list(map(float, np.quantile(samples, [.025, .975])))


def execute(source, context, units):
    name = case_id(source)
    path = PRIVATE / (name+'.json.gz')
    hashes = signature()
    if path.exists():
        with gzip.open(path, 'rt') as stream: record = json.load(stream)
        assert record['code_sha256'] == hashes
        return record
    started = time.perf_counter()
    d, n = context['data'], context['n']
    seed_train, seed_final = seed_for(context, 0), seed_for(context, 1)
    candidates = []
    for blocks in block_grid(n):
        fit = fit_block(d['inner'], n, units['inner'], blocks, seed_train)
        row = dict(blocks=blocks, status=fit.status, model=save_fit(fit),
                   validation_nll=float(fit.nll(d['validation']).mean())
                   if fit.status == 'ok' else None)
        candidates.append(row)
        print(name, 'candidate', blocks, fit.status, row['validation_nll'], flush=True)
    selected, final, refits = None, None, []
    for candidate in validation_order(candidates):
        fit = fit_block(d['development'], n, units['development'],
                        candidate['blocks'], seed_final)
        refits.append(dict(blocks=candidate['blocks'], model=save_fit(fit), status=fit.status))
        if fit.status == 'ok':
            selected, final = candidate['blocks'], fit
            break
    # Independently saved comparators already use these exact development/test rows.
    models = {m: restore_fit(source['models'][m]) for m in
              ('pl', 'sm_likelihood', 'sm_fotakis', 'sm_efficient_fallback')}
    priority = np.random.default_rng(SEED).permutation(n)
    order = score_order(d['development'], np.arange(n), n, context['r'], priority)
    models['global_borda'] = sm_fit('global_borda', d['development'], order,
                                    dict(training_pool='all_development', tie_seed=SEED))
    order, pi, si = pilot_order(d['development'], n, units['development'], seed_final)
    models['pilot_borda'] = sm_fit('pilot_borda', d['development'], order,
        dict(training_pool='pilot_half_for_center', pilot_reports=len(pi),
             terminal_reports=len(si), seed=seed_final))
    if final is not None:
        models['borda_block_sieve'] = final
    losses = {m: f.nll(d['test']) for m, f in models.items() if f.status == 'ok'}
    # Score the frozen models only after validation selection/refit is complete.
    scores = []
    for method, fit in models.items():
        row = dict(method=method, status=fit.status, beta=fit.beta,
                   nll=float(losses[method].mean()) if method in losses else None,
                   kendall=kendall(fit.order, context['truth']) if method in losses
                   and context['truth'] is not None else None,
                   certified=fit.metadata.get('certified'))
        if method in losses:
            row['delta_vs_pl'] = float((losses[method]-losses['pl']).mean())
        scores.append(row)
    comparisons = []
    if final is not None:
        for method in losses:
            if method == 'borda_block_sieve': continue
            delta = losses['borda_block_sieve']-losses[method]
            ci = paired_interval(losses['borda_block_sieve'], losses[method], units['test'],
                                 seed_for(context, 2)) if context['identified_units'] or source['study']=='S0' else None
            comparisons.append(dict(reference=method, delta=float(delta.mean()),
                ci_low=ci[0] if ci else None, ci_high=ci[1] if ci else None,
                ci_kind='conditional_test_unit_percentile' if ci else 'unavailable_unknown_dependence'))
    record = dict(case=name, source_study=source['study'], dataset=source['dataset'], n=n,
        r=context['r'], N=context['N'], repeat=0, train_count=len(d['inner']),
        validation_count=len(d['validation']), test_count=len(d['test']),
        selected_blocks=selected, status='ok' if final is not None else 'all_candidates_unavailable',
        data_sha256=source['data_sha256'], code_sha256=hashes, base_commit=BASE_SHA,
        source_model_status=source['models']['sm_sharp']['status'],
        identified_units=context['identified_units'], unit_description=context['unit_description'],
        test_units=len(np.unique(units['test'])), seed_train=seed_train, seed_final=seed_final,
        grid=block_grid(n), candidates=candidates, refits=refits,
        models={m: save_fit(f) for m, f in models.items()}, scores=scores,
        comparisons=comparisons, parts=context['parts'], units=units,
        losses=losses, seconds=time.perf_counter()-started)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.temporary')
    with gzip.open(temporary, 'wt') as stream: json.dump(json_value(record), stream, allow_nan=False)
    temporary.replace(path)
    return record


def export(records):
    PUBLIC.mkdir(parents=True, exist_ok=True)
    score_rows, candidate_rows, comparison_rows, models = [], [], [], []
    for record in records:
        base = {k: record[k] for k in ('case','source_study','dataset','n','r','N',
                'train_count','validation_count','test_count','test_units','selected_blocks')}
        for row in record['scores']: score_rows.append(dict(base, **row))
        for row in record['candidates']:
            candidate_rows.append(dict(base, blocks=row['blocks'], status=row['status'],
                validation_nll=row['validation_nll'],
                reason=row['model']['metadata'].get('reason',''),
                max_block=int(np.ceil(record['n']/row['blocks']))))
        for row in record['comparisons']: comparison_rows.append(dict(base, **row))
        models.append({k:v for k,v in record.items() if k not in ('parts','units','losses')})
    for name, rows in [('scores',score_rows),('candidates',candidate_rows),('comparisons',comparison_rows)]:
        pd.DataFrame(rows).to_csv(PUBLIC/(name+'.csv'), index=False, float_format='%.12g')
    payload = '\n'.join(json.dumps(json_value(r),sort_keys=True,allow_nan=False) for r in models)+'\n'
    with (PUBLIC/'models.jsonl.gz').open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as stream:
            stream.write(payload.encode())
    manifest = dict(base_commit=BASE_SHA, records=len(records), code_sha256=signature(),
        inputs={p:digest(ROOT/p) for p in ('results/predictive/predictors.jsonl.gz',
            'results/predictive/repeat_scores.csv.gz')},
        outputs={p.name:digest(p) for p in PUBLIC.iterdir() if p.name in
                 ('scores.csv','candidates.csv','comparisons.csv','models.jsonl.gz')})
    (PUBLIC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case', default=None)
    args=parser.parse_args()
    sources=selected_sources()
    assert len(sources)==19
    tasks={t.name:t for t in load_tasks()}
    records=[]
    for source in sources:
        if args.case and args.case not in case_id(source): continue
        context,units=get_context(source,tasks)
        records.append(execute(source,context,units))
        print('COMPLETE',case_id(source),records[-1]['selected_blocks'],flush=True)
    if not args.case: export(records)


if __name__ == '__main__': main()
