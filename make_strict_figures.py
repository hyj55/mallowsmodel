"""Scientific figures from saved results; no model fitting."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT/'results/strict_features'
OUT = ROOT/'figures/strict_features'
BLUE, GREEN, GRAY = '#2966a3', '#00846f', '#67737e'
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT/(name+'.png'), dpi=180, bbox_inches='tight')
    fig.savefig(OUT/(name+'.svg'), bbox_inches='tight')
    plt.close(fig)


def transitions():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4), layout='constrained')
    for ax, part, xlabel, title in zip(axes, ['bridge', 'shell'],
            ['Mixture weight: SM (0) to PL (1)', 'Within-shell tilt h (0 = SM)'],
            ['A. Average inversion noise fixed', 'B. Every shell mass fixed']):
        df = pd.read_csv(DATA/f'{part}_summary.csv')
        for shape, color in [('equal', BLUE), ('alternating', GREEN)]:
            g = df[(df.method == 'mle') & (df.N == 448) & (df.r == 3) &
                   (df['shape'] == shape)].sort_values('value')
            ax.errorbar(g.value, g.delta, yerr=[g.delta-g.delta_lo, g.delta_hi-g.delta],
                        color=color, marker='o', markersize=4, capsize=3,
                        label=shape.capitalize()+' PL gaps')
        ax.axhline(0, color=GRAY, lw=1, linestyle='--')
        ax.set(xlabel=xlabel, title=title, ylim=(-.075, .09))
        ax.grid(axis='y', alpha=.15)
        ax.text(.02, .92, 'PL predicts better', transform=ax.transAxes, color=GRAY)
        ax.text(.02, .04, 'SM predicts better', transform=ax.transAxes, color=GRAY)
    axes[0].set_ylabel('Conditional NLL(SM MLE) − NLL(PL)\n(nats / whole ranking)')
    axes[1].legend(loc='center right', frameon=False, fontsize=9)
    fig.suptitle('n = 8, r = 3, N = 448; 40 independent training samples per point\n'
                 'Exact population test loss; pointwise 95% paired-replicate intervals', fontsize=11)
    save(fig, 'feature_transitions')


def real_results():
    df = pd.read_csv(DATA/'real_results.csv'); df = df[df.method == 'mle']
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.4), layout='constrained')
    for ax, mask, title in [(axes[0], ~df.dataset.str.startswith('dots2024'), 'Full rankings: n = r = 4'),
                           (axes[1], df.dataset.str.startswith('dots2024'), 'Partial rankings: n = 30, N = 180')]:
        g = df[mask].reset_index(drop=True)
        for i, row in g.iterrows():
            if np.isfinite(row.delta):
                color = GREEN if row.delta < 0 else BLUE
                ax.errorbar(row.delta, i, xerr=[[row.delta-row.delta_lo], [row.delta_hi-row.delta]],
                            fmt='o', color=color, capsize=3, markersize=5)
            else:
                ax.text(.02, i, 'PL: no unique finite MLE', fontsize=8, va='center', color=GRAY)
        labels = [x.replace('00024-0000000', 'Dots ').replace('00025-0000000', 'Puzzle ')
                   .replace('dots2024_', '').replace('_r', ', r=') for x in g.dataset]
        ax.set(yticks=np.arange(len(g)), yticklabels=labels, title=title,
               xlabel='SM − PL confirmation NLL (nats / ranking)')
        ax.invert_yaxis(); ax.axvline(0, color=GRAY, lw=1, linestyle='--')
        ax.grid(axis='x', alpha=.15)
    fig.suptitle('All 16 prespecified real tasks; negative differences favor SM\n'
                 'Pointwise 95% intervals; left: anonymous-record working bootstrap', fontsize=11)
    save(fig, 'real_confirmation')


def budgets():
    df = pd.read_csv(DATA/'followup_budget_replicates.csv')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
    for selector, label, color in [('pair', 'Pairwise log-loss selector', BLUE),
                                   ('context', 'Context-only selector', GREEN)]:
        g = df[df.selector == selector].groupby('budget').agg(
            accuracy=('correct', 'mean'), regret=('regret', 'mean'))
        for ax, column in zip(axes, ['accuracy', 'regret']):
            ax.plot(g.index, g[column], '-o', color=color, label=label)
            ax.set_xscale('log'); ax.set_xticks([20, 60, 200, 1000], ['20', '60', '200', '1000'])
            ax.set_xlabel('Additional independent discovery reports')
            ax.grid(alpha=.15)
    axes[0].set(ylabel='Fraction choosing the smaller population NLL', ylim=(0, 1))
    axes[1].set_ylabel('Mean selection regret (nats / ranking)')
    axes[0].legend(frameon=False, fontsize=9, loc='lower right')
    fig.suptitle('Exploratory budget sensitivity: same 200 training fits and exact test laws\n'
                 'Context at 20 reports: 64/200 abstentions; its plotted means condition on selection', fontsize=11)
    save(fig, 'discovery_budget')


if __name__ == '__main__':
    transitions(); real_results(); budgets()
