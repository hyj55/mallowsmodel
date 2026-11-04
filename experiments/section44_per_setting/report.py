"""Build S4-T paired result tables from saved fits; never refit or select."""
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import sys

# Exact resource receipts can contain factorial-sized byte estimates.
sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
from scipy.stats import t

from experiments.section44_per_setting.design import cells, group_key, holdout_size
from experiments.section44_per_setting.run import PRIVATE, OUT, HERE, read_gzip, sha, write_json
from src.manuscript_estimators import proof_constants


def csv_write(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    buf = io.StringIO(newline='')
    w = csv.DictWriter(buf, fieldnames=keys)
    w.writeheader(); w.writerows(rows)
    raw = buf.getvalue().encode()
    if str(path).endswith('.gz'):
        raw = gzip.compress(raw, mtime=0)
    path.write_bytes(raw)


def ci(values):
    x=np.asarray(values,float);n=len(x);mean=float(x.mean())
    se=float(x.std(ddof=1)/np.sqrt(n))
    half=float(t.ppf(.975,n-1))*se
    p=1. if np.all(x==0) else 0. if se==0 else float(2*t.sf(abs(mean/se),n-1))
    return dict(mean=mean,mcse=se,ci_low=mean-half,ci_high=mean+half,p_value=p)


def adjusted(rows):
    # Each outcome/family is a separately identified family of comparisons.
    groups=defaultdict(list)
    for row in rows:
        if row['complete'] and row['method'].endswith('_per_setting') and row['reference']=='global_borda':
            groups[(row['method'],row['metric'])].append(row)
    for group in groups.values():
        ordered=sorted(group,key=lambda a:a['p_value']);previous=0.
        for rank,row in enumerate(ordered):
            previous=max(previous,min(1.,(len(ordered)-rank)*row['p_value']))
            row['holm_p']=previous


def extract():
    rows=[];execution=Counter();execution_values={}
    for phase in ('calibration','confirmation'):
        dest=[]
        for path in sorted((PRIVATE/phase).glob('*/*.json.gz')):
            rec=read_gzip(path);c=rec['cell']
            for name,m in rec['models'].items():
                f=rec['fits'][m['fit_key']]
                row=dict(cell=c['id'],group=rec['group'],repeat=rec['repeat'],method=name,
                         n=c['n'],r=c['r'],N=c['N'],beta_true=c['beta'],beta0=c['beta0'],
                         holdout_count=rec['holdout_count'],status=f['status'],branch=m['branch'],
                         depth=m['depth'],fit_key=m['fit_key'],representative=f['representative'],
                         beta_fit=f.get('beta'),nll=f.get('holdout_nll'),kendall=f.get('kendall'),
                         A=m['config']['A'],c_width=m['config']['c_width'],K=m['config']['K'],
                         c_terminal=m['config']['c_terminal'])
                dest.append(row)
                if phase=='confirmation' and m['family']!='borda':
                    lam=c['N']*c['r']*(c['r']-1)/(c['n']*(c['n']-1))
                    eta=lam if m['family']=='efficient' else (c['r']-1)/(c['n']-1)
                    constants=proof_constants(c['beta0']);cfg=m['config']
                    K=constants['K'] if cfg['K'] is None else cfg['K']
                    w=max(1,math.ceil(cfg['c_width']*(math.sqrt(c['n']/eta)+1/eta)))
                    ell=math.log(constants['CT'])+math.log(8)+math.log1p(lam*c['n'])
                    M=math.ceil(K*eta*ell*c['n']*(c['n']-1)/(c['r']*(c['r']-1)))
                    reason=m.get('fallback_reason') or ('root_A_stop' if m['depth']==0 else 'positive_depth')
                    rejected=sorted({p['status'] for p in m['plan'].get('candidates',[]) if p['status']!='feasible'})
                    if rejected:reason += '; rejected_candidates='+','.join(rejected)
                    if m['plan']['status']=='no_feasible_resolution' and not m['plan'].get('candidates'):
                        reason='no_admissible_eta'
                    if f['status']!='ok':
                        meta=f['metadata'];reason += '; '+str(meta.get('failed_block',{}).get('reason',meta.get('reason',f['status'])))
                    audit={k:row[k] for k in ('cell','method','n','r','N','beta0','status','branch','depth')}
                    audit.update(reason=reason,A=cfg['A'],c_width=cfg['c_width'],K=float(K),
                                 c_terminal=cfg['c_terminal'],lambda_=lam,eta_initial=eta,
                                 eta_selected=m['plan'].get('eta'),m0=c['n'],w1=w,eight_w1=8*w,
                                 M1=M,half_sample=c['N']//2,pilot_reports=m['plan']['used'],
                                 W_star=max(1,math.ceil(cfg['c_terminal']*cfg['A']*(c['n']-1)/(c['r']-1))) if m['family']=='sharp' else None)
                    audit_key=json.dumps(audit,sort_keys=True)
                    execution[audit_key]+=1;execution_values[audit_key]=audit
        csv_write(OUT/(phase+'_fits.csv.gz'),dest)
        if phase=='confirmation':rows=dest
    audit=[dict(execution_values[k],contexts=count) for k,count in execution.items()]
    csv_write(OUT/'execution.csv',audit)
    lines=['# S4-T execution and first-round parameters','',
           '[Main report](../README.md) · [All numeric parameters](execution.csv)','',
           'Rows group identical signal setting, method, status, depth and reason across repetitions. '
           'First-round w1 and M1 use the initial candidate resolution and are formula diagnostics; '
           'they do not mean that a stopped round consumed reports. N is training count. '
           'The CSV also gives beta0, A, K, both window coefficients, initial and selected eta, '
           'lambda, pilot report budget, and Sharp W*. Full candidate schedules remain in draw archives. '
           'Pilot depth and terminal-sieve success are separate: a resource failure can follow either '
           'zero or positive pilot depth. Positive-depth controls are included for context.','',
           '| Setting | Method | Contexts | Status | Depth | Reason | n=m0 | r | N | Initial w1 | Initial M1 | floor(N/2) |',
           '|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|']
    for a in audit:
        lines.append('| '+' | '.join(str(a[k]) for k in ('cell','method','contexts','status','depth','reason','n','r','N','w1','M1','half_sample'))+' |')
    (OUT/'execution.md').write_text('\n'.join(lines)+'\n')
    return rows


def build_tables(rows):
    grouped=defaultdict(list)
    for row in rows:grouped[(row['cell'],row['method'])].append(row)
    summaries=[];comparisons=[]
    for (cell,method),vals in sorted(grouped.items()):
        assert sorted(v['repeat'] for v in vals)==list(range(100)),(cell,method)
        a=vals[0];good=[v for v in vals if v['status']=='ok'];complete=len(good)==100
        out={k:a[k] for k in ('cell','group','method','n','r','N','beta_true','beta0','holdout_count')}
        out.update(complete=complete,available=len(good),expected=100,
                   positive_depth=sum((v['depth'] or 0)>0 and v['status']=='ok' for v in vals),
                   fallbacks=sum(v['branch']=='borda_fallback' for v in vals),
                   failures=json.dumps(dict(Counter(v['status'] for v in vals if v['status']!='ok')),sort_keys=True))
        if complete:
            for metric in ('nll','kendall'):
                out.update({metric+'_'+k:v for k,v in ci([v[metric] for v in good]).items()})
        summaries.append(out)
        if method=='global_borda':continue
        references=['global_borda']
        if method.endswith('_per_setting'):
            family=method.split('_')[0];references += [family+'_proof',family+'_S4_locked']
        for ref in references:
            lookup={v['repeat']:v for v in grouped[(cell,ref)]}
            paired=[(v,lookup[v['repeat']]) for v in vals
                    if v['status']=='ok' and lookup[v['repeat']]['status']=='ok']
            for metric in ('nll','kendall'):
                row={k:out[k] for k in ('cell','group','method','n','r','N','beta_true','beta0')}
                row.update(reference=ref,metric=metric,available=len(paired),complete=len(paired)==100)
                if row['complete']:
                    row.update(ci([v[metric]-b[metric] for v,b in paired]))
                    scale=math.lgamma(a['r']+1) if metric=='nll' else a['n']*(a['n']-1)/2
                    row['scaled_mean']=row['mean']/scale
                comparisons.append(row)
    adjusted(comparisons)
    csv_write(OUT/'summary.csv',summaries)
    csv_write(OUT/'paired_comparisons.csv',comparisons)
    return summaries,comparisons


def fmt(v):
    return 'unavailable' if v is None else f'{v:.5g}'


def interval(row):
    if not row['complete']:return f"unavailable ({row['available']}/100)"
    return f"{fmt(row['mean'])} [{fmt(row['ci_low'])}, {fmt(row['ci_high'])}]"


def count_line(rows,method,ref,metric):
    rr=[r for r in rows if r['method']==method and r['reference']==ref and r['metric']==metric and r['complete']]
    lower=sum(r['mean'] < -1e-10 for r in rr);higher=sum(r['mean'] > 1e-10 for r in rr)
    better=sum(r.get('holm_p',1)<.05 and r['mean']<0 for r in rr)
    worse=sum(r.get('holm_p',1)<.05 and r['mean']>0 for r in rr)
    return dict(complete=len(rr),lower=lower,equal=len(rr)-lower-higher,higher=higher,
                holm_lower=better,holm_higher=worse)


def report(summaries,comparisons):
    selection=json.loads((OUT/'selection.json').read_text())
    lines=['# S4-T: constants selected separately for each training setting','',
           '[Repository](../../README.md) · [Protocol](PROTOCOL.md) · [Original S4](../section44/README.md) · '
           '[Every selected configuration](results/selection.json) · [All candidate scores](results/calibration_candidates.json) · '
           '[Depth and stopping parameters](results/execution.md)', '',
           'This additional simulation asks whether choosing constants separately for each `(n,r,N)` changes '
           'the comparison with global Borda. Original S4 is preserved. Here N is **training** report count. '
           'The same group uses the same selected constants across repetitions and signal controls.', '',
           'There are **82 parameter-selection groups, 90 signal settings, 1,800 independent training/validation '
           'draws and 9,000 independent training/test draws**. Candidate selection uses validation whole-ranking '
           'NLL; confirmation reports both held-out NLL and true-center Kendall error. Lower is better for both.', '',
           '## Results against global Borda','',
           'The tables count settings by the sign of their mean paired difference. They are descriptive, '
           'not independent votes. The last columns use Holm-adjusted two-sided tests within each '
           'method/outcome family. Incomplete settings are excluded from these sign counts and retained below.', '',
           '| Method | Outcome | Complete settings / 90 | Lower / equal / higher mean | Holm 5% lower / higher |',
           '|---|---|---:|---:|---:|']
    result_counts={}
    for family in ('efficient','sharp'):
        for metric in ('nll','kendall'):
            count=count_line(comparisons,family+'_per_setting','global_borda',metric)
            result_counts[family+'_'+metric]=count
            lines.append(f"| {family.title()}, per-setting | {metric} | {count['complete']}/90 | "
                         f"{count['lower']} / {count['equal']} / {count['higher']} | {count['holm_lower']} / {count['holm_higher']} |")
    lines += ['', 'A lower test NLL and a lower center error are different claims. Validation NLL does not '
              'use the true center and does not directly optimize the Kendall error reported by original S4. '
              'The NLL score includes a train-only fitted dispersion, so two different centers can have the '
              'same predictive loss when both fitted dispersions are zero.', '',
              '## Comparisons with the proof and original S4 configurations','',
              'All references below are refitted on the same new training draws; these are paired comparisons '
              'within S4-T, not subtraction of unrelated means from the old report.', '',
              '| Per-setting method | Reference | Outcome | Complete pairs / 90 | Lower / equal / higher mean |',
              '|---|---|---|---:|---:|']
    for family in ('efficient','sharp'):
        for ref in (family+'_proof',family+'_S4_locked'):
            for metric in ('nll','kendall'):
                c=count_line(comparisons,family+'_per_setting',ref,metric)
                lines.append(f"| {family} | {ref} | {metric} | {c['complete']}/90 | {c['lower']} / {c['equal']} / {c['higher']} |")
    lines += ['', '## What was selected','',
              'Selection allows zero depth and explicitly recorded Borda fallbacks. Therefore a tuned method '
              'may equal Borda because it selected that branch, not because a multilevel hierarchy independently '
              'matched it. Exact-sieve resource failures are never replaced by Borda.', '',
              '| Family | Selected candidate | Number of (n,r,N) groups |', '|---|---|---:|']
    for family in ('efficient','sharp'):
        for name,num in sorted(Counter(v[family]['candidate'] for v in selection.values()).items()):
            lines.append(f'| {family} | {name} | {num} |')
    lines += ['', '## Every held-out comparison','',
              'Each row is a signal setting; groups repeated across beta/beta0 controls share their candidate. '
              'Differences are **method minus Borda**. Brackets are pointwise 95% t intervals across independent '
              'confirmation draws. Depth counts successful fits with positive depth, out of 100. The full '
              '[CSV](results/paired_comparisons.csv) also gives MCSE, scaled differences and adjusted p values.', '',
              '| n,r,N; beta/beta0 | Family | Candidate | Positive depth | Test NLL difference [95% CI] | NLL difference / log(r!) | Kendall difference [95% CI] |',
              '|---|---|---|---:|---|---:|---|']
    lookup={(r['cell'],r['method'],r['reference'],r['metric']):r for r in comparisons}
    ss={(r['cell'],r['method']):r for r in summaries}
    for c in sorted(cells(),key=lambda c:(c['n'],c['r'],c['N'],c['beta'],c['beta0'])):
        for family in ('efficient','sharp'):
            method=family+'_per_setting';nll=lookup[(c['id'],method,'global_borda','nll')]
            kd=lookup[(c['id'],method,'global_borda','kendall')]
            label=f"{c['n']},{c['r']},{c['N']}; {c['beta']:g}/{c['beta0']:g}"
            selected=selection[group_key(c)][family]['candidate']
            lines.append(f"| {label} | {family} | {selected} | {ss[(c['id'],method)]['positive_depth']} | "
                         f"{interval(nll)} | {fmt(nll.get('scaled_mean'))} | {interval(kd)} |")
    lines += ['', '## Training, selection and uncertainty','',
              'Each calibration draw contains N training reports and ceil(N/3) validation reports, at least '
              'one. Each confirmation draw contains a fresh N-report training set and an independent '
              'ceil(N/3)-report test set, sharing that draw\'s latent center. Sampling roles are disjoint; '
              'there is no reuse of calibration observations in confirmation and no train-plus-validation '
              'refit. The three roles have relative sizes N:ceil(N/3):ceil(N/3), but they are implemented '
              'as separate calibration and confirmation phases, not one reused three-way partition. '
              'No old S4 observations are split or reused. Tiny-N counts are rounded explicitly.', '',
              'The original 25 Efficient and 35 Sharp anchored candidates are unchanged. For each candidate, '
              'train-only beta is the constrained conditional MLE on [0,10]. Validation ranks candidates by '
              'mean whole-ranking NLL, giving each signal cell in a group equal weight. All 20 calibration '
              'fits per signal must succeed; there is no positive-depth requirement. Ties use candidate name. '
              'The selection is shared across signal controls, so no true beta or beta0 is used as a '
              'selection key. The supplied beta0 remains an input to the original schedule.', '',
              'For metric X, calculate D_b = X_method,b - X_reference,b for each independent confirmation '
              'draw. The mean is sum(D_b)/100, MCSE is sample_sd(D_b)/10, and the pointwise interval is '
              'mean(D) ± t_(99,0.975) MCSE. Draws are independent Monte Carlo replicates; this motivates '
              'the approximate Student-t interval. Intervals condition on the locked constants and omit '
              'variability from repeating the selection stage. Holm adjustment controls familywise error '
              'within the stated complete-cell comparison family, conditional on valid pointwise p values.', '',
              '## Interpretation limits','',
              '- Results describe the tested grid, generator, supplied bounds and computational budgets. '
              'They do not establish an optimal tuning rule or a minimax rate.',
              '- Selection has 20 independent training/validation draws per signal setting, so this is '
              'simulation-based group calibration, not ordinary tuning from one real dataset.',
              '- Relative to original S4, both the selection target (validation NLL rather than oracle center '
              'risk) and the activity requirement change, along with the grouping of constants. Differences '
              'from the original locked configuration cannot be attributed solely to per-setting tuning.',
              '- Borda-equivalent branches remain labeled. Improvement in computation or positive depth '
              'does not by itself establish lower prediction or center error.',
              '- The candidate grid is anchored rather than Cartesian. A failure to beat Borda does not '
              'exclude other constants or the separately proposed adaptive-eta algorithms.', '',
              'The empirical constants do not automatically inherit the original uniform risk guarantees.', '',
              '## Reproduction and files','',
              'The preregistered [protocol commit](https://github.com/hyj55/mallowsmodel/commit/'
              '2d604ab212cdff13231fa02e56b2206ad474fcaa) predates outcome generation. '
              '`results/protocol.json` gives every setting and candidate. `selection.json` records one '
              'choice per family/group. `calibration_candidates.json` retains rejected candidates. '
              '`calibration_fits.csv.gz` and `confirmation_fits.csv.gz` give logical method-level rows; '
              'identical computations have explicit shared fit keys. `summary.csv` and '
              '`paired_comparisons.csv` contain all aggregate results.', '',
              'Lossless draw archives retain fitted orders, data hashes, plan/branch and failure receipts. '
              'Raw reports regenerate exactly from root seed 202611040 and the saved stream coordinates. '
              'The verification program checks original S4 preservation, selection replay, summaries and '
              'a deterministic training/holdout replay sample.', '',
              '```bash',
              'export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONINTMAXSTRDIGITS=0',
              'python -m pytest -q experiments/section44_per_setting/test_experiment.py',
              'python experiments/section44_per_setting/run.py calibrate',
              'python experiments/section44_per_setting/run.py confirm',
              'python experiments/section44_per_setting/report.py',
              'python experiments/section44_per_setting/verify.py',
              '```', '']
    (HERE/'README.md').write_text('\n'.join(lines))
    write_json(OUT/'result_counts.json',result_counts)


def archive():
    # Bounded lossless gzip parts; no large uncompressed scientific artifacts.
    dest=OUT/'draws';dest.mkdir(exist_ok=True)
    entries=[]
    for phase in ('calibration','confirmation'):
        chunks=[];raw_size=0;part=0
        def flush():
            nonlocal chunks,raw_size,part
            if not chunks:return
            data=gzip.compress(b''.join(chunks),mtime=0)
            name=f'{phase}-{part:03}.jsonl.gz';path=dest/name;path.write_bytes(data)
            entries.append(dict(path='draws/'+name,records=len(chunks),bytes=len(data),sha256=sha(path)))
            chunks=[];raw_size=0;part+=1
        for path in sorted((PRIVATE/phase).glob('*/*.json.gz')):
            with gzip.open(path,'rb') as f:raw=f.read()
            if raw_size+len(raw)>12_000_000:flush()
            chunks.append(raw);raw_size+=len(raw)
        flush()
    write_json(OUT/'draw_archives.json',entries)


def main():
    rows=extract()
    assert len(rows)==90*100*7
    summaries,comparisons=build_tables(rows)
    report(summaries,comparisons)
    archive()
    files={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*')
           if p.is_file() and '__pycache__' not in str(p) and p.name!='manifest.json'}
    write_json(OUT/'manifest.json',files)
    print(json.dumps(json.loads((OUT/'result_counts.json').read_text()),indent=2))


if __name__=='__main__':main()
