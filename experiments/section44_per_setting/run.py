"""Resumable S4-T selection/confirmation with independent training and holdouts."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np

from experiments.section44.core import PROOF, digest_array, kendall_fast
from experiments.section44.design import candidate_grid
from experiments.section44_per_setting.design import (cells, protocol, group_key,
    CALIBRATION_REPEATS, CONFIRMATION_REPEATS)
from experiments.section44_per_setting.engine import (generate, computational_plan,
    perform_fit, score, clean, stable_hash)

HERE = Path(__file__).resolve().parent
OUT = HERE/'results'
PRIVATE = ROOT/'results/private/section44_per_setting'
CODE = ['experiments/section44_per_setting/'+p for p in ('design.py','engine.py','run.py')]+[
    'experiments/section44/core.py','experiments/section44/design.py',
    'src/manuscript_estimators.py','src/models.py','src/resource_sieve.py','src/sieve_budget_retry.py']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(clean(value), indent=2, sort_keys=True, allow_nan=False)+'\n')


def write_gzip(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    with tmp.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as f:
            f.write((json.dumps(clean(value), separators=(',', ':'), allow_nan=False)+'\n').encode())
    tmp.replace(path)


def read_gzip(path):
    with gzip.open(path, 'rt') as f:
        return json.load(f)


def initialize():
    p = protocol()
    path = OUT/'protocol.json'
    if path.exists():
        assert json.loads(path.read_text()) == p, 'Protocol changed after registration'
    else:
        write_json(path, p)
    old = {str(f.relative_to(ROOT)):sha(f) for f in (ROOT/'experiments/section44').rglob('*')
           if f.is_file() and '__pycache__' not in str(f)}
    if not (OUT/'original_s4_hashes.json').exists():
        write_json(OUT/'original_s4_hashes.json', old)
    else:
        assert json.loads((OUT/'original_s4_hashes.json').read_text()) == old
    signature = dict(protocol=sha(path), code={p:sha(ROOT/p) for p in CODE})
    path = OUT/'producer.json'
    if path.exists():
        assert json.loads(path.read_text())['signature'] == signature, 'Producer changed'
    else:
        write_json(path, dict(signature=signature, python=sys.version, numpy=np.__version__,
                             platform=platform.platform(), protocol_commit='2d604ab212cdff13231fa02e56b2206ad474fcaa'))
    return signature


def methods(c, phase, selected=None):
    rows = [('global_borda', 'borda', PROOF.asdict())]
    if phase == 0:
        for name, entry in candidate_grid().items():
            for family in entry['families']:
                rows.append((family+'__'+name, family, entry['config']))
    else:
        locked = json.loads((ROOT/'experiments/section44/results/selection.json').read_text())
        for family in ('efficient', 'sharp'):
            rows += [(family+'_proof', family, PROOF.asdict()),
                     (family+'_S4_locked', family, locked[family]['config']),
                     (family+'_per_setting', family, selected[group_key(c)][family]['config'])]
    return rows


def execute(c, phase, index, repeat, signature, selected):
    folder = 'calibration' if phase == 0 else 'confirmation'
    path = PRIVATE/folder/c['id']/f'{repeat:03}.json.gz'
    selection_hash = sha(OUT/'selection.json') if phase else None
    if path.exists():
        result = read_gzip(path)
        assert result['signature'] == signature and result['selection_sha256'] == selection_hash
        return result
    start = time.perf_counter()
    truth, train, holdout, seed = generate(c, phase, index, repeat)
    result = dict(cell=c, group=group_key(c), phase=phase, repeat=repeat, index=index,
                  signature=signature, selection_sha256=selection_hash,
                  train_sha256=digest_array(train), holdout_sha256=digest_array(holdout),
                  truth_sha256=digest_array(truth), truth=truth.tolist(),
                  estimator_seed=seed, holdout_count=len(holdout), models={}, fits={})
    predictions = {}
    # Separate caches per worker avoid concurrent writes to packing receipts.
    cache = PRIVATE/('packing-'+str(os.getpid()))
    for name, family, config in methods(c, phase, selected):
        p, key, logical = computational_plan(c, family, config)
        entry = dict(fit_key=key, family=family, config=config, plan=p, **logical)
        result['models'][name] = entry
        if key in result['fits']:
            continue
        before = time.perf_counter()
        order, meta = perform_fit(c, family, config, train, seed, cache)
        saved = dict(status=meta['status'], representative=name, metadata=meta,
                     seconds=time.perf_counter()-before, order=None)
        if order is not None:
            saved['order'] = order.tolist()
            order_key = digest_array(order)
            if order_key not in predictions:
                predictions[order_key] = score(train, holdout, order)
            saved.update(predictions[order_key])
            # True-center risk is deliberately absent from calibration scores.
            if phase:
                saved['kendall'] = kendall_fast(order, truth)
        result['fits'][key] = saved
    result['seconds'] = time.perf_counter()-start
    write_gzip(path, result)
    return result


def select_records(records):
    by_group = {}
    for rec in records:
        by_group.setdefault(rec['group'], []).append(rec)
    selections, audit = {}, []
    for group, draws in sorted(by_group.items()):
        expected_cells = {c['id'] for c in cells() if group_key(c) == group}
        assert {r['cell']['id'] for r in draws} == expected_cells
        for cell in expected_cells:
            assert sorted(r['repeat'] for r in draws if r['cell']['id']==cell) == list(range(CALIBRATION_REPEATS))
        selections[group] = {}
        for family in ('efficient', 'sharp'):
            eligible = []
            for name, cfg in candidate_grid().items():
                if family not in cfg['families']:
                    continue
                key = family+'__'+name
                fitted = [(rec['models'][key], rec['fits'][rec['models'][key]['fit_key']]) for rec in draws]
                complete = sum(f['status']=='ok' for _,f in fitted)
                # Equal repeats per cell make this exactly the equal-cell mean.
                value = float(np.mean([f['holdout_nll'] for _,f in fitted])) if complete == len(draws) else None
                row = dict(group=group, family=family, candidate=name, config=cfg['config'],
                           expected=len(draws), complete=complete, validation_nll=value,
                           positive_depth=sum((m.get('depth') or 0)>0 for m,_ in fitted),
                           fallback=sum(m['branch']=='borda_fallback' for m,_ in fitted),
                           eligible=value is not None)
                audit.append(row)
                if row['eligible']:
                    eligible.append(row)
            if not eligible:
                raise RuntimeError(f'No eligible candidate: {group}/{family}')
            selections[group][family] = min(eligible, key=lambda x:(x['validation_nll'],x['candidate']))
    assert len(selections) == len({group_key(c) for c in cells()})
    return selections, audit


def select():
    records = [read_gzip(p) for p in sorted((PRIVATE/'calibration').glob('*/*.json.gz'))]
    selected, audit = select_records(records)
    write_json(OUT/'selection.json', selected)
    write_json(OUT/'calibration_candidates.json', audit)


def run_cell(args):
    c, phase, index, signature, selected = args
    B = CALIBRATION_REPEATS if phase == 0 else CONFIRMATION_REPEATS
    for repeat in range(B):
        rec = execute(c, phase, index, repeat, signature, selected)
        if repeat % 10 == 0 or repeat == B-1:
            print(('calibrate' if phase==0 else 'confirm'), c['id'], repeat+1, '/', B,
                  f"last={rec['seconds']:.2f}s unique={len(rec['fits'])}", flush=True)
    return c['id']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['initialize','calibrate','select','confirm'])
    ap.add_argument('--workers', type=int, default=3)
    args = ap.parse_args()
    signature = initialize()
    if args.phase == 'initialize':
        print('Initialized', len(cells()), 'signal cells', flush=True)
        return
    if args.phase == 'select':
        select()
        return
    phase = int(args.phase == 'confirm')
    selected = json.loads((OUT/'selection.json').read_text()) if phase else None
    work = [(c, phase, i, signature, selected) for i,c in enumerate(cells())]
    # Largest n first exposes expensive resource requirements early, without
    # changing any candidate, random stream or outcome-dependent stopping.
    work.sort(key=lambda a:(-a[0]['n'], -a[0]['N'], a[0]['id']))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(run_cell, w) for w in work]
        for f in as_completed(futures):
            print('Completed', f.result(), flush=True)
    if phase == 0:
        select()


if __name__ == '__main__':
    main()
