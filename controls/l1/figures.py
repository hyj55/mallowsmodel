"""Plot the fixed-test regularization control from its current five-fit summaries."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
f=pd.read_csv(ROOT/'results/regularized_learning/real_summary.csv')
fig,axes=plt.subplots(1,3,figsize=(13,4.3))
for ax,(task,g) in zip(axes,f.groupby('dataset',sort=False)):
    for delta,lo,hi,label in [('delta','ci_low','ci_high','SM'),('calibrated_delta','calibrated_ci_low','calibrated_ci_high','SM with validation shrinkage')]:
        ax.errorbar(g.N,g[delta],yerr=[g[delta]-g[lo],g[hi]-g[delta]],marker='o',capsize=3,label=label)
    ax.axhline(0,color='gray',lw=.8);ax.set_xscale('log');ax.set_title(task.replace('_',' ').title())
    ax.set_xlabel('Development reports N');ax.grid(alpha=.2)
axes[0].set_ylabel('Whole-ranking NLL difference from tuned PL')
axes[1].legend(fontsize=8)
fig.suptitle('L1: five development permutations, one fixed test per task')
fig.text(.5,.01,'Nominal 95% test-report bootstrap intervals conditional on five fitted models; no training-variability CI.\nBeans lacks farmer IDs, so its intervals are descriptive under unverified report independence.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.10,1,.94))
for ext in ['png','svg']:fig.savefig(ROOT/f'figures/regularized_learning.{ext}',dpi=180)
