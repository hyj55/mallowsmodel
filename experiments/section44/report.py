"""Export all independent S4 draws, pointwise intervals and figures."""
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from experiments.section44.core import coordinates, kendall_fast
from experiments.section44.design import (ROOT_SEED,CONFIRMATION_REPEATS,CALIBRATION_REPEATS,
    confirmation_cells,calibration_cells)
from experiments.section44.run import OUTPUT,PRIVATE,HERE,read_records,write_json,sha


def interval(x):
    x=np.asarray(x,float);mean=float(x.mean())
    if len(x)<2:return dict(mean=mean,mcse=None,ci_low=None,ci_high=None)
    se=float(x.std(ddof=1)/math.sqrt(len(x)));half=t.ppf(.975,len(x)-1)*se
    return dict(mean=mean,mcse=se,ci_low=mean-half,ci_high=mean+half)


def flatten(record):
    c=record['cell'];J=c['n']*(c['n']-1)/2
    for name,model in record['models'].items():
        blocks=model.get('blocks',[])
        complete=model['status']=='ok'
        yield dict(cell=c['id'],panel=c['panel'],panels=';'.join(c.get('panels',[c['panel']])),
            phase=record['phase'],repeat=record['repeat'],n=c['n'],r=c['r'],N=c['N'],beta=c['beta'],beta0=c['beta0'],
            method=name,status=model['status'],branch=model.get('branch'),depth=model.get('depth'),
            kendall=model['kendall'],normalized_kendall=model['kendall']/J if complete else None,
            seconds=model['seconds'],zero_items=record['zero_items'],input_bytes=record['input_bytes'],
            pilot_reports=model.get('used',0),W_star=model.get('W_star'),terminal_blocks=len(blocks) or model.get('terminal_nodes'),
            max_sieve_items=max((b['items'] for b in blocks),default=None),
            sieve_pairs=sum(b['pairs'] for b in blocks) if blocks else None,
            pilot_tail_fraction=model.get('pilot_diagnostics',{}).get('fraction_displacement_gt_W'),
            pilot_kendall=model.get('pilot_diagnostics',{}).get('kendall'),
            stage_zero_fraction=float(np.mean([s['zero_items']/c['n'] for s in model.get('stages',[])]))
                                if model.get('stages') else None,
            **record['coordinates'])


def summaries(df,B):
    rows=[]
    for (cell,method),g in df.groupby(['cell','method'],sort=True):
        complete=g[g.status=='ok']; full=len(complete)==B
        out={k:g.iloc[0][k] for k in ('cell','method','panel','panels','n','r','N','beta','beta0',
                                     'lambda_','mu','Vcov','expected_unseen','coverage_shape','information_shape','Nr')}
        out.update(expected=B,observed=len(g),complete=len(complete),
                   active_fits=int(((g.depth>0)&(g.status=='ok')).sum()),
                   fallback_fits=int((g.branch=='borda_fallback').sum()),
                   sieve_fits=int(((g.branch=='exact_sieve')&(g.status=='ok')).sum()),
                   depth_min=g.depth.min(),depth_max=g.depth.max(),
                   observed_zero_items_mean=float(g.zero_items.mean()),
                   seconds_mean=float(g.seconds.mean()),seconds_median=float(g.seconds.median()))
        for col in ('pilot_reports','W_star','max_sieve_items','pilot_kendall','pilot_tail_fraction','stage_zero_fraction'):
            out[col+'_mean']=float(g[col].mean()) if g[col].notna().any() else None
        for metric in ('kendall','normalized_kendall'):
            stats=interval(complete[metric]) if full else dict.fromkeys(['mean','mcse','ci_low','ci_high'])
            out.update({metric+'_'+k:v for k,v in stats.items()})
        out['conditional_completed_kendall_mean']=float(complete.kendall.mean()) if len(complete) else None
        ref=min(float(out['n'])**2,float(out['coverage_shape'])+float(out['n'])/float(out['lambda_']))
        out['combined_reference_shape']=ref
        out['kendall_over_information_shape']=out['kendall_mean']/float(out['information_shape']) if full else None
        out['kendall_over_combined_reference_shape']=out['kendall_mean']/ref if full else None
        out['all_observed_errors_zero']=bool(full and (complete.kendall==0).all())
        out['zero_error_probability_upper95']=1-.05**(1/B) if out['all_observed_errors_zero'] else None
        out['unavailable_reasons']=';'.join(sorted(set(g.loc[g.status!='ok','status'])))
        rows.append(out)
    return pd.DataFrame(rows)


def paired(df):
    rows=[]
    for cell,g in df.groupby('cell',sort=True):
        names=sorted(g.method.unique())
        references=[n for n in ('borda','exact_kemeny','efficient_proof','sharp_proof') if n in names]
        for reference in references:
            ref=g[g.method==reference].set_index('repeat')
            for method in names:
                if method==reference:continue
                a=g[g.method==method].set_index('repeat')
                common=a.join(ref[['status','kendall']],rsuffix='_ref')
                available=(common.status=='ok')&(common.status_ref=='ok')
                full=int(available.sum())==CONFIRMATION_REPEATS
                out=dict(cell=cell,method=method,reference=reference,expected=CONFIRMATION_REPEATS,
                         complete_pairs=int(available.sum()))
                if full:
                    d=(common.kendall-common.kendall_ref).to_numpy()
                    out.update(interval(d));out['fraction_lower']=float(np.mean(d<0));out['fraction_equal']=float(np.mean(d==0))
                    seed=int.from_bytes(hashlib.sha256((cell+method+reference).encode()).digest()[:4],'little')
                    rng=np.random.default_rng(np.random.SeedSequence([ROOT_SEED,2,seed]))
                    ids=rng.integers(0,len(d),size=(2000,len(d)))
                    lo,hi=np.quantile(d[ids].mean(axis=1),[.025,.975])
                    out.update(bootstrap_low=float(lo),bootstrap_high=float(hi))
                else:
                    out.update(dict.fromkeys(['mean','mcse','ci_low','ci_high','fraction_lower','fraction_equal',
                                              'bootstrap_low','bootstrap_high']))
                rows.append(out)
    return pd.DataFrame(rows)


def export_draws(phase):
    name='calibration' if phase==0 else 'confirmation'
    folder=PRIVATE/name
    flat=[];count=0
    for cell_folder in sorted(folder.iterdir()):
        if not cell_folder.is_dir():continue
        target=OUTPUT/'draws'/name/(cell_folder.name+'.jsonl.gz')
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('wb') as raw:
            with gzip.GzipFile(fileobj=raw,mode='wb',filename='',mtime=0) as stream:
                for path in sorted(cell_folder.glob('*.json.gz')):
                    with gzip.open(path,'rt') as f:record=json.load(f)
                    # Repeated hashes/configs compress well; retain complete fitted orders,
                    # schedules, individual block receipts and generating-center identities.
                    stream.write((json.dumps(record,separators=(',',':'),allow_nan=False)+'\n').encode())
                    flat.extend(flatten(record));count+=1
    expected=(len(calibration_cells())*CALIBRATION_REPEATS if phase==0 else
              len(confirmation_cells())*CONFIRMATION_REPEATS)
    assert count==expected,(name,count,expected)
    return pd.DataFrame(flat)


COLORS={'borda':'#242424','efficient_proof':'#999999','efficient_calibrated':'#0072B2',
        'sharp_proof':'#D55E00','sharp_calibrated':'#009E73','exact_kemeny':'#CC79A7',
        'majority_2_17':'#E69F00'}
LABELS={'borda':'Global Borda','efficient_proof':'Efficient: proof constants',
        'efficient_calibrated':'Efficient: calibrated','sharp_proof':'Sharp: proof constants',
        'sharp_calibrated':'Sharp: calibrated','exact_kemeny':'Exact Kemeny','majority_2_17':'Majority (Thm 2.17)'}


def draw_figures(summary,pairs,resources):
    folder=HERE/'figures';folder.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'svg.fonttype':'none','svg.hashsalt':'section44','savefig.bbox':'tight'})
    fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for ax,(n,r) in zip(axs.flat,[(16,3),(128,8),(512,8),(2048,32)]):
        g=summary[(summary.n==n)&(summary.r==r)&(summary.beta==.8)&(summary.beta0==.8)]
        for method in ['borda','efficient_calibrated','sharp_calibrated','sharp_proof','exact_kemeny']:
            a=g[(g.method==method)&(g.complete==g.expected)].sort_values('N')
            if len(a):ax.errorbar(a.N,a.normalized_kendall_mean,yerr=a.normalized_kendall_ci_high-a.normalized_kendall_mean,
                label=LABELS[method],color=COLORS[method],marker='o',capsize=2)
        ax.set(xscale='log',xlabel='Training reports N',ylabel='Mean Kendall error / choose(n,2)',title=f'n={n}, r={r}')
    handles,labels=axs.flat[0].get_legend_handles_labels()
    bylabel={}
    for ax in axs.flat:
        hs,ls=ax.get_legend_handles_labels();bylabel.update(zip(ls,hs))
    fig.legend(bylabel.values(),bylabel.keys(),loc='outside lower center',ncol=3)
    fig.suptitle('S4 independent confirmation: center risk (pointwise 95% t intervals)')
    fig.savefig(folder/'risk.svg',metadata={'Date':None});fig.savefig(folder/'risk.png',dpi=150);plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    for family,ax in zip(('efficient','sharp'),axs):
        q=pairs[(pairs.method==family+'_calibrated')&(pairs.reference=='borda')].copy()
        q=q.merge(summary[summary.method==family+'_calibrated'][['cell','n','r','active_fits','complete']],on='cell')
        q=q[q.complete==100]
        q['scaled']=q['mean']/(q.n*(q.n-1)/2)
        scatter=ax.scatter(q.active_fits/100,q.scaled,c=np.log2(q.n),cmap='viridis',vmin=3,vmax=11,alpha=.8,s=35)
        ax.axhline(0,color='#777',lw=1)
        ax.set(xlabel='Fraction of confirmation fits with positive depth',
               ylabel='Paired normalized risk difference vs Borda',title=family.capitalize()+' calibrated')
    fig.suptitle('Positive depth alone does not imply lower error; negative difference favors calibration')
    bar=fig.colorbar(scatter,ax=axs,ticks=[3,5,7,9,11],label='Catalogue size n')
    bar.ax.set_yticklabels(['8','32','128','512','2048'])
    fig.savefig(folder/'depth_risk.svg',metadata={'Date':None});fig.savefig(folder/'depth_risk.png',dpi=150);plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,n in zip(axs,(128,512)):
        q=summary[(summary.n==n)&(summary.r<summary.n)&(summary.lambda_>.9)&(summary.lambda_<=1)&
                  (summary.beta==.8)&(summary.beta0==.8)]
        for method in ('borda','efficient_calibrated','sharp_calibrated'):
            a=q[(q.method==method)&(q.complete==100)].sort_values('Vcov')
            ax.errorbar(a.Vcov,a.normalized_kendall_mean,yerr=a.normalized_kendall_ci_high-a.normalized_kendall_mean,
                        color=COLORS[method],marker='o',label=LABELS[method],capsize=2)
        ax.set(xscale='log',xlabel='Nonappearance exponent V_cov',ylabel='Mean normalized Kendall error',
               title=f'n={n}, realized pair exposure 0.9 < lambda <= 1')
    fig.legend(*axs[0].get_legend_handles_labels(),loc='outside lower center',ncol=3)
    fig.suptitle('Similar pair exposure does not fix item coverage; r and N change along each curve')
    fig.savefig(folder/'coverage.svg',metadata={'Date':None});fig.savefig(folder/'coverage.png',dpi=150);plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    for ax,r in zip(axs,(3,8)):
        q=summary[(summary.r==r)&summary.panels.str.contains('bounded_r_R10')&
                  (summary.lambda_>.15)&(summary.lambda_<=.201)&(summary.beta==.8)&(summary.beta0==.8)]
        for method in ('borda','efficient_calibrated','sharp_calibrated'):
            a=q[(q.method==method)&(q.complete==100)].sort_values('n')
            ax.errorbar(a.n,a.kendall_over_information_shape,
                yerr=(a.kendall_ci_high-a.kendall_mean)/a.information_shape,
                marker='o',capsize=2,color=COLORS[method],label=LABELS[method])
        ax.set(xscale='log',xlabel='Catalogue size n',ylabel='Mean Kendall error / min(n^2, n/lambda)',
               title=f'Fixed r={r}, R=10; target lambda=0.2')
    fig.legend(*axs[0].get_legend_handles_labels(),loc='outside lower center',ncol=3)
    fig.suptitle('Fixed-report-size rate comparison; finite points do not establish an asymptotic order')
    fig.savefig(folder/'bounded_r.svg',metadata={'Date':None});fig.savefig(folder/'bounded_r.png',dpi=150);plt.close(fig)

    fig,axs=plt.subplots(1,3,figsize=(13,4.3),layout='constrained')
    for ax,n in zip(axs,(8,32,128)):
        q=summary[(summary.n==n)&(summary.r==n)]
        for method in ('borda','majority_2_17','exact_kemeny'):
            a=q[q.method==method].sort_values('N')
            positive=a[a.kendall_mean>0]
            if len(positive):ax.plot(positive.N,positive.kendall_mean/n,'o-',color=COLORS[method],label=LABELS[method])
            z=a[a.kendall_mean==0]
            if len(z):ax.scatter(z.N,np.full(len(z),1e-5),marker='v',color=COLORS[method])
        a=q[q.method=='majority_2_17'].sort_values('N')
        if len(a):
            N=a.N.to_numpy();shape=(1/np.cosh(.8/2))**N/np.sqrt(N+1)
            ax.plot(N,shape/shape[0]*a.iloc[0].kendall_mean/n,'--',color='#777',lw=1,
                    label='sech(beta/2)^N / sqrt(N+1), anchored at N=1')
        ax.set(yscale='log',xlabel='Full rankings N',ylabel='Mean Kendall error / n',title=f'n = r = {n}')
        ax.text(.03,.03,'Triangles: 0 observed errors\n(plotted at 1e-5, not a positive estimate)',transform=ax.transAxes,fontsize=8)
    hs,ls=axs[0].get_legend_handles_labels();fig.legend(hs,ls,loc='outside lower center',ncol=3)
    fig.suptitle('Separate full-ranking endpoint; 100 independent draws per point')
    fig.savefig(folder/'full_ranking.svg',metadata={'Date':None});fig.savefig(folder/'full_ranking.png',dpi=150);plt.close(fig)

    if len(resources):
        fig,axs=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
        for method in ('borda','efficient_calibrated','sharp_calibrated','exact_kemeny'):
            a=resources[(resources.method==method)&(resources.status=='ok')]
            axs[0].scatter(a.Nr,a.fit_seconds_with_tracing,color=COLORS[method],s=20,alpha=.65,label=LABELS[method])
            axs[1].scatter(a.Nr,a.peak_traced_working_bytes/2**20,color=COLORS[method],s=20,alpha=.65)
        axs[0].set(xscale='log',yscale='log',xlabel='Observed item occurrences Nr',ylabel='Fit seconds with allocation tracing')
        axs[1].set(xscale='log',yscale='log',xlabel='Observed item occurrences Nr',ylabel='Peak traced working allocation (MiB)')
        fig.legend(*axs[0].get_legend_handles_labels(),loc='outside lower center',ncol=4)
        fig.suptitle('Completed cold-packing profiles on draw 0; input excluded from working memory')
        fig.savefig(folder/'resources.svg',metadata={'Date':None});fig.savefig(folder/'resources.png',dpi=150);plt.close(fig)


def main():
    calibration=export_draws(0); confirmation=export_draws(1)
    for name,frame in [('calibration',calibration),('confirmation',confirmation)]:
        frame.to_csv(OUTPUT/(name+'_fits.csv.gz'),index=False,compression=dict(method='gzip',mtime=0),float_format='%.12g')
    cal_summary=summaries(calibration,CALIBRATION_REPEATS)
    summary=summaries(confirmation,CONFIRMATION_REPEATS)
    comparison=paired(confirmation)
    cal_summary.to_csv(OUTPUT/'calibration_summary.csv',index=False,float_format='%.12g')
    summary.to_csv(OUTPUT/'summary.csv',index=False,float_format='%.12g')
    comparison.to_csv(OUTPUT/'paired_comparisons.csv',index=False,float_format='%.12g')
    receipts=[json.loads(p.read_text()) for p in sorted((PRIVATE/'resource_receipts').glob('*/*.json'))]
    resources=pd.DataFrame(receipts)
    resources.to_csv(OUTPUT/'resource_profiles.csv',index=False,float_format='%.12g')
    draw_figures(summary,comparison,resources)
    write_json(OUTPUT/'counts.json',dict(calibration_draws=len(calibration_cells())*CALIBRATION_REPEATS,
        confirmation_cells=len(confirmation_cells()),confirmation_draws=len(confirmation_cells())*CONFIRMATION_REPEATS,
        calibration_fits=len(calibration),confirmation_fits=len(confirmation),
        confirmation_status=confirmation.status.value_counts().to_dict(),resource_profiles=len(resources)))
    print((OUTPUT/'counts.json').read_text())


if __name__=='__main__':main()
