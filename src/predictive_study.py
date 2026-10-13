"""Design, scoring and evidence records for P0/L0/S0 and the B0 sieve supplement."""
import gzip
import hashlib
import json
from pathlib import Path
import time

import numpy as np

from .models import pair_counts, kendall, sample_sm, sample_pl
from .repeated_holdout import (ROOT, load_tasks, split_task, save_fit, restore_fit,
                               json_value, source_inventory)
from .predictive_models import fit_candidates, METHODS

PROTOCOL_COMMIT = '052eeac57a58f8cb851ba7feac8578d18b053f3f'
CURVE_SEED = 202610130
SIMULATION_SEED = 202610131
BOOTSTRAP_SEED = 202610132
BUDGETS = (20,50,100,300,1000,3000)
SIMULATION_CELLS = ((10,20),(10,100),(10,500),(6,100),(16,100),(32,100))
CORE = ('src/resource_sieve.py','src/predictive_models.py','src/predictive_study.py',
        'run_predictive_study.py','src/models.py','src/strict_models.py',
        'src/manuscript_estimators.py','src/group_sensitivity.py','src/repeated_holdout.py',
        'src/data.py','src/validation_extension.py','run_strict_real.py',
        'docs/protocols/PREDICTIVE_COMPARISON_20261013.md')
PRIVATE = ROOT / 'results/private/predictive'
PUBLIC = ROOT / 'results/predictive'


def code_hashes():
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in CORE}


def signature():
    return hashlib.sha256(json.dumps(code_hashes(),sort_keys=True).encode()).hexdigest()


def array_hash(array):
    a = np.asarray(array,dtype='<i8')
    return hashlib.sha256(str(a.shape).encode()+a.tobytes()).hexdigest()


def curve_parts(task, repeat, budget):
    outer = split_task(task,repeat)
    development = np.sort(np.r_[outer['fit'],outer['discovery']])
    # Both Sushi tasks have the same source respondent rows and split_key.
    rng = np.random.default_rng(np.random.SeedSequence([CURVE_SEED,task.split_key,repeat]))
    order = rng.permutation(development)[:budget]
    assert len(order) == budget
    k = int(.75*budget)
    return dict(inner=order[:k],validation=order[k:],development=order,test=outer['confirmation'])


def primary_parts(task, repeat):
    p = split_task(task,repeat)
    return dict(inner=p['fit'],validation=p['discovery'],
                development=np.sort(np.r_[p['fit'],p['discovery']]),test=p['confirmation'])


def empirical_context(task, repeat, budget=None):
    parts = primary_parts(task,repeat) if budget is None else curve_parts(task,repeat,budget)
    data = {key:task.y[ids] for key,ids in parts.items()}
    identified = not task.unit_description.startswith('anonymous') and 'expanded' not in task.unit_description
    # PrefLib encodes anonymous frequencies, irrespective of the descriptor text.
    if task.name.startswith(('00024','00025')):
        identified = False
    return dict(dataset=task.name, study='P0' if budget is None else 'L0', repeat=repeat,
        n=task.n, r=task.y.shape[1], N=len(parts['development']), data=data,
        parts=parts, units=task.units[parts['test']], truth=task.truth,
        estimator_seed=task.estimator_seed, identified_units=identified,
        unit_description=task.unit_description, split_key=task.split_key)


def synthetic_context(generator,n,N,repeat):
    index = 0 if generator == 'sm' else 1
    streams = np.random.SeedSequence([SIMULATION_SEED,index,n,N,repeat]).spawn(3)
    center = np.random.default_rng(streams[0]).permutation(n)
    theta = np.empty(n); theta[center] = np.linspace(1,-1,n)
    if generator == 'sm':
        development = sample_sm(np.random.default_rng(streams[1]),N,n,3,center,.8)
        test = sample_sm(np.random.default_rng(streams[2]),4000,n,3,center,.8)
    else:
        development = sample_pl(np.random.default_rng(streams[1]),N,n,3,theta)
        test = sample_pl(np.random.default_rng(streams[2]),4000,n,3,theta)
    k = int(.75*N)
    return dict(dataset='synthetic_'+generator,study='S0',repeat=repeat,n=n,r=3,N=N,
        data=dict(inner=development[:k],validation=development[k:],development=development,test=test),
        parts=dict(inner=list(range(k)),validation=list(range(k,N)),development=list(range(N)),test=list(range(4000))),
        units=np.arange(4000),truth=center,estimator_seed=202610133,
        identified_units=False,unit_description='independent_simulated_report',
        generator=generator,generating_beta=.8 if generator=='sm' else None,
        generating_theta=theta if generator=='pl' else None,split_key=10000+index)


def paired_bootstrap(losses,units,seed,resamples=2000):
    """Cluster resampling of reports; report-weighted ratio, paired across fits."""
    _,inverse = np.unique(units,return_inverse=True)
    count = np.bincount(inverse)
    rng = np.random.default_rng(seed)
    samples = rng.integers(0,len(count),size=(resamples,len(count)))
    denominator = count[samples].sum(axis=1)
    pl_sum = np.bincount(inverse,weights=losses['pl'])
    output = {}
    for method,loss in losses.items():
        if not np.isfinite(loss).all():
            continue
        sums = np.bincount(inverse,weights=loss)
        nll = sums[samples].sum(axis=1)/denominator
        delta = (sums-pl_sum)[samples].sum(axis=1)/denominator
        output[method] = dict(nll_ci_low=float(np.quantile(nll,.025)),nll_ci_high=float(np.quantile(nll,.975)),
                             delta_ci_low=float(np.quantile(delta,.025)),delta_ci_high=float(np.quantile(delta,.975)))
    return output


def evaluate(context,fits):
    test = context['data']['test']; development = context['data']['development']
    losses = {m:fits[m].nll(test) for m in METHODS}
    assert np.isfinite(losses['pl']).all() and np.isfinite(losses['sm_likelihood']).all()
    intervals = {}
    if context['identified_units']:
        seed = np.random.SeedSequence([BOOTSTRAP_SEED,context['split_key'],context['repeat'],context['N']])
        intervals = paired_bootstrap(losses,context['units'],seed)
    w = pair_counts(development,context['n']); i,j = np.triu_indices(context['n'],1)
    counts = np.bincount(development.ravel(),minlength=context['n'])
    base = {k:context[k] for k in ('dataset','study','repeat','n','r','N')}
    base.update(n_test=len(test),test_units=len(np.unique(context['units'])),
        lambda_=context['N']*context['r']*(context['r']-1)/(context['n']*(context['n']-1)),
        mu=context['N']*context['r']/context['n'],unseen_items=int((counts==0).sum()),
        missing_pairs=int(((w+w.T)[i,j]==0).sum()),R_bound=10)
    scores = []
    for method in METHODS:
        fit = fits[method]; meta = fit.metadata
        row = dict(base,method=method,status=fit.status,nll=float(losses[method].mean()),
            delta=float((losses[method]-losses['pl']).mean()),beta=fit.beta,
            tau=meta.get('tau',np.nan),certified=meta.get('certified',False),
            objective_gap=meta.get('objective_gap',np.nan),branch=meta.get('branch',meta.get('path','')),
            alias_of=meta.get('alias_of',''),kendall=kendall(fit.order,context['truth'])
                if context['truth'] is not None and fit.status=='ok' else np.nan,
            ci_kind='conditional_test_unit_percentile' if method in intervals else
                'independent_repetitions_in_summary' if context['study']=='S0' else 'unavailable',
            bootstrap_units=len(np.unique(context['units'])) if method in intervals else 0)
        row.update(intervals.get(method,dict(nll_ci_low=np.nan,nll_ci_high=np.nan,
                                           delta_ci_low=np.nan,delta_ci_high=np.nan)))
        scores.append(row)
    return scores,losses


def execute(context,code_signature,path):
    path = Path(path)
    if path.exists():
        with gzip.open(path,'rt') as stream:
            record = json.load(stream)
        if record['code_signature'] != code_signature:
            raise ValueError('Code changed since cached fit; do not silently mix runs: '+str(path))
        return 'cached'
    started = time.perf_counter()
    d = context['data']
    fits = fit_candidates(d['inner'],d['validation'],d['development'],context['n'],context['estimator_seed'])
    scores,losses = evaluate(context,fits)
    record = {k:v for k,v in context.items() if k not in ('data','units')}
    record.update(code_signature=code_signature,protocol_commit=PROTOCOL_COMMIT,
        data_sha256={k:array_hash(v) for k,v in d.items()},
        models={m:save_fit(f) for m,f in fits.items()},scores=scores,losses=losses,
        seconds=time.perf_counter()-started)
    path.parent.mkdir(parents=True,exist_ok=True)
    temp = path.with_suffix('.temporary')
    with gzip.open(temp,'wt') as stream:
        json.dump(json_value(record),stream,allow_nan=False)
    temp.replace(path)
    return {m:f.status for m,f in fits.items()}


def read_records(directory=PRIVATE):
    records = []
    for path in sorted(Path(directory).glob('*/*.json.gz')):
        with gzip.open(path,'rt') as stream:
            record = json.load(stream)
        for row in record['scores']:
            for key,value in row.items():
                if value in ('nan','inf','-inf'):
                    row[key] = float(value)
        records.append(record)
    return records
