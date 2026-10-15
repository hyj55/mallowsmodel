"""Publication plots from saved aggregate tables; no fitting or resampling."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from summarize_predictive_study import task_label

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'figures/predictive'
COLORS={'pl':'#315c9e','sm_likelihood':'#cf6336','sm_sharp':'#258576',
        'sm_fotakis':'#9462ad','sm_efficient_fallback':'#777777'}
LABELS={'pl':'PL, tuned ridge','sm_likelihood':'SM, likelihood center','sm_sharp':'SM, Sharp / global sieve',
        'sm_fotakis':'SM, Fotakis','sm_efficient_fallback':'SM, efficient fallback'}


def save(fig,name):
    fig.savefig(OUT/(name+'.png'),dpi=180,bbox_inches='tight')
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight')
    plt.close(fig)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    primary=pd.read_csv(ROOT/'results/predictive/primary.csv')
    p=primary[primary.method.eq('sm_likelihood')].sort_values('delta_mean')
    fig,ax=plt.subplots(figsize=(9,8))
    y=np.arange(len(p))
    for k,(_,row) in enumerate(p.iterrows()):
        color='#258576' if row.delta_mean<0 else '#cf6336'
        ax.errorbar(row.delta_mean,k,xerr=row.delta_mcse,fmt='o',color=color,capsize=3,
            mfc=color if row.certified_centers==5 else 'white')
    labels=[f'{task_label(r.dataset)}  (n={r.n}, r={r.r}; exact {r.certified_centers}/5)' for _,r in p.iterrows()]
    ax.set_yticks(y,labels);ax.axvline(0,color='black',lw=.8);ax.invert_yaxis()
    ax.set_xlabel('Mean whole-ranking NLL: SM minus PL (nats/report)')
    ax.set_title('Primary prediction: 5 grouped outer allocations\nBars: ±1 partition MCSE, not population confidence intervals',pad=15)
    ax.grid(axis='x',alpha=.2);save(fig,'primary')
    learning=pd.read_csv(ROOT/'results/predictive/learning.csv')
    fig,axes=plt.subplots(2,2,figsize=(12,8),sharex='col')
    for col,dataset in enumerate(('sushi_a','sushi_b')):
        for method in ('pl','sm_likelihood','sm_sharp','sm_fotakis'):
            d=learning[(learning.dataset==dataset)&(learning.method==method)].sort_values('N')
            for row,metric in ((0,'nll'),(1,'delta')):
                axes[row,col].errorbar(d.N,d[metric+'_mean'],yerr=d[metric+'_mcse'],
                    marker='o',ms=4,color=COLORS[method],label=LABELS[method],capsize=2)
        axes[0,col].set_title(dataset.replace('_',' ').title())
        axes[1,col].axhline(0,color='black',lw=.7)
        for ax in axes[:,col]:
            ax.set_xscale('log');ax.grid(alpha=.2)
        axes[1,col].set_xlabel('Development reports N; fixed r=10 and R=10')
    axes[0,0].set_ylabel('Whole-ranking test NLL');axes[1,0].set_ylabel('SM minus PL NLL')
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2)
    fig.suptitle('Sushi learning curves: 5 aligned outer splits\nBars: ±1 partition MCSE; missing points indicate unavailable fits',y=1.02)
    fig.tight_layout(rect=(0,.10,1,1));save(fig,'learning')
    sim=pd.read_csv(ROOT/'results/predictive/synthetic.csv')
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for col,generator in enumerate(('synthetic_sm','synthetic_pl')):
        for row,(fixed,value,x) in enumerate((('n',10,'N'),('N',100,'n'))):
            ax=axes[row,col]
            for method in ('pl','sm_likelihood','sm_sharp','sm_efficient_fallback'):
                d=sim[(sim.dataset==generator)&(sim[fixed]==value)&(sim.method==method)].sort_values(x)
                ax.errorbar(d[x],d.nll_mean,yerr=[d.nll_mean-d.nll_ci_low,d.nll_ci_high-d.nll_mean],
                    marker='o',ms=4,color=COLORS[method],label=LABELS[method],capsize=3)
            ax.grid(alpha=.2);ax.set_xlabel(('Training reports N (n=10)' if x=='N' else 'Catalogue items n (N=100)'))
            if x=='N':ax.set_xscale('log')
            ax.set_title(generator.replace('synthetic_','').upper()+' generator')
    for ax in axes[:,0]:ax.set_ylabel('Whole-ranking test NLL')
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='lower center',ncol=2)
    fig.suptitle('Controlled curves: fixed r=3 and R=10\nBars: 95% t intervals across 20 independent training/test draws',y=1.02)
    fig.tight_layout(rect=(0,.10,1,1));save(fig,'synthetic')
    print('Saved primary, empirical learning and controlled-curve PNG/PDF figures')


if __name__=='__main__':
    main()
