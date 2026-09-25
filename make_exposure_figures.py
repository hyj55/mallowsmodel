"""Export scientific figures from the saved exposure summaries."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.data import ROOT
OUT=ROOT/'figures';DATA=ROOT/'results/exposure'
COLORS={'sharp':'#d17a18','efficient':'#2878a5','mle':'#8e59aa','pl':'#319568'}
LABELS={'sharp':'Section 2: exact sieve','efficient':'Section 3: Borda / depth 0','mle':'Exact center MLE','pl':'Regularized PL'}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','savefig.dpi':180})
def save(fig,name):
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight')
    svg=OUT/(name+'.svg');fig.savefig(svg,bbox_inches='tight')
    svg.write_text('\n'.join(x.rstrip() for x in svg.read_text().splitlines())+'\n');plt.close(fig)
def small():
    df=pd.read_csv(DATA/'small_summary.csv');fig,axes=plt.subplots(2,3,figsize=(13,7),sharey=True)
    for row,dgp in enumerate(['SM','PL']):
        for col,r in enumerate([2,4,8]):
            ax=axes[row,col];sub=df[(df.dgp==dgp)&(df.r==r)]
            for method in ['sharp','efficient','mle','pl']:
                g=sub[sub.method==method].sort_values('N');x=g.N if r==8 else g.lambda_
                ax.plot(x,g.risk_normalized,'o-',ms=3,color=COLORS[method],label=LABELS[method])
                ax.fill_between(x,g.risk_normalized_lo,g.risk_normalized_hi,color=COLORS[method],alpha=.08)
            ax.set_xscale('log');ax.set_ylim(0,.65);ax.grid(alpha=.15)
            ax.set_xlabel('N (full rankings: lambda = N)' if r==8 else 'Pair exposure lambda')
            if r<8:ax.axvline(1,color='gray',ls=':',lw=1)
            ax.set_title(f'Truth {dgp}: n=8, r={r}')
            if col==0:ax.set_ylabel('Mean Kendall error / 28')
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc='lower center',ncol=4,bbox_to_anchor=(.5,-.02),frameon=False)
    fig.suptitle('Center recovery: 30 independent datasets per design',y=1.02)
    fig.tight_layout();save(fig,'exposure_small_centers')
def coverage():
    df=pd.read_csv(DATA/'coverage_summary.csv');df=df[(df.dgp=='SM')&(df.method=='efficient')]
    fig,axes=plt.subplots(1,2,figsize=(11,4.1))
    for r,color in [(2,'#2878a5'),(8,'#d17a18'),(32,'#8e59aa')]:
        g=df[df.r==r].sort_values('lambda_')
        axes[0].errorbar(g.lambda_,g.risk_normalized,
            yerr=[g.risk_normalized-g.risk_normalized_lo,g.risk_normalized_hi-g.risk_normalized],
            marker='o',ms=4,color=color,label=f'r={r}',capsize=2)
        axes[1].plot(g.lambda_,g.unseen_items/64,'o-',color=color,label=f'r={r}')
        for j,(_,v) in enumerate(g.iterrows()):
            if j==0 or .9<=v.lambda_<=1.05:
                axes[1].annotate(f'mu={v.mu:.3g}',(v.lambda_,v.unseen_items/64),xytext=(4,12 if r!=8 else -18),
                                 textcoords='offset points',fontsize=8,color=color)
    for ax in axes:
        ax.set_xscale('log');ax.set_xlabel('Actual pair exposure lambda')
        ax.axvline(1,ls=':',color='gray');ax.grid(alpha=.15);ax.legend(frameon=False)
    axes[0].set_ylabel('Mean Kendall error / 2016');axes[0].set_title('Section 3 equals Borda here')
    axes[1].set_ylim(-.06,.84);axes[1].set_ylabel('Fraction of unseen items')
    axes[1].set_title('Similar lambda can conceal different coverage')
    fig.suptitle('Uniform SM: n=64, beta=0.8',y=1.02);fig.tight_layout();save(fig,'exposure_coverage')
def tennis():
    bins=pd.read_csv(DATA/'tennis_strength_bins.csv');df=pd.read_csv(DATA/'tennis_by_year.csv')
    same=pd.read_csv(DATA/'tennis_same_order_by_year.csv')
    fig,axes=plt.subplots(1,2,figsize=(11.5,4.2));x=np.arange(len(bins))
    axes[0].errorbar(x,bins.observed,yerr=[bins.observed-bins.lo,bins.hi-bins.observed],
                    fmt='o-',color='#222222',capsize=3,label='Observed favorite wins')
    axes[0].plot(x,bins.PL,'s--',color=COLORS['pl'],label='PL')
    axes[0].plot(x,bins.SM_same_order,'^--',color=COLORS['efficient'],label='Same-order SM, shrunk beta')
    axes[0].set_xticks(x,bins.gap_bin);axes[0].set_xlabel('Training PL log-worth gap')
    axes[0].set_ylabel('Win probability');axes[0].set_ylim(.48,.95);axes[0].legend(frameon=False,fontsize=8)
    for method,color,label in [('efficient_shrunk',COLORS['efficient'],'Section 3, shrunk beta'),
                              ('insertion_shrunk',COLORS['mle'],'Insertion, shrunk beta')]:
        g=df[(df.target=='seen')&(df.method==method)]
        axes[1].plot(g.year,g.delta,'o-',color=color,label=label)
    g=same[same.method=='same_order_shrunk']
    axes[1].plot(g.year,g.delta,'s--',color='#555555',label='Same PL order, shrunk beta')
    axes[1].axhline(0,color='gray',lw=1);axes[1].set_xlabel('Test season')
    axes[1].set_ylabel('SM minus PL log loss');axes[1].legend(frameon=False,fontsize=8)
    axes[0].set_title('Probability structure');axes[1].set_title('Chronological prediction')
    for ax in axes:ax.grid(alpha=.15)
    fig.tight_layout();save(fig,'exposure_tennis')
if __name__=='__main__':
    OUT.mkdir(exist_ok=True);small();coverage();tennis()
