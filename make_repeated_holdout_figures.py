"""Render recorded partition averages, without fitting or resampling."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def label(name):
    if name.startswith('00024-'):
        return 'Dots 2013: 200x'+str([3,5,7,9][int(name[-1])-1])
    if name.startswith('00025-'):
        return 'Puzzle: '+['11/14/17/20','5/8/11/14','7/10/13/16','9/12/15/18'][int(name[-1])-1]
    return name.replace('dots2024_', 'Dots 2024 ').replace('_r', ', r=').replace('_', ' ').title().replace('R=', 'r=')


def main():
    data = pd.read_csv(ROOT / 'results/repeated_holdout/scores.csv')
    data = data[data.split.eq('confirmation') & data.method.eq('mle')].copy()
    assert len(data) == 23 and data.repetitions.eq(30).all()
    groups = [data[data.study.ne('strict_features')], data[data.dataset.str.startswith('000')],
              data[data.dataset.str.startswith('dots2024')]]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.8), gridspec_kw={'wspace':.75})
    for ax, rows, title in zip(axes, groups, ['Other real tasks', 'PrefLib tasks', 'Dots 2024 tasks']):
        for i, (_, row) in enumerate(rows.iterrows()):
            full = row.paired_delta_finite_repeats == 30
            mean = row.paired_delta_mean if full else row.paired_delta_finite_conditional_mean
            se = row.paired_delta_partition_mcse if full else row.paired_delta_finite_conditional_partition_mcse
            if np.isfinite(mean):
                ax.errorbar(mean, i, xerr=se if np.isfinite(se) else None, fmt='o',
                    color='#126b89' if full else '#9a6500',
                    markerfacecolor='#126b89' if full else 'white', capsize=3, markersize=6)
            else:
                ax.text(.02, i, 'No finite paired mean', transform=ax.get_yaxis_transform(),
                        color='#9a6500', fontsize=8)
        labels = [label(r.dataset) + (f' [{int(r.paired_delta_finite_repeats)}/30]' if r.paired_delta_finite_repeats != 30 else '')
                  for _, r in rows.iterrows()]
        ax.set_yticks(range(len(rows)), labels, fontsize=9)
        ax.set_ylim(len(rows)-.4, -.6)
        ax.axvline(0, color='#999999', lw=.8, zorder=0)
        ax.grid(axis='x', alpha=.15)
        ax.set_title(title, fontsize=12)
        ax.set_xlabel('Mean confirmation NLL(SM) - NLL(PL)\nnegative favors SM', fontsize=9)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('Repeated holdout: exact SM versus unpenalized PL', fontsize=16, y=.98)
    fig.text(.04, .025,
        '30 new partitions per task. Bars: ±1 partition Monte Carlo SE conditional on these data; not population confidence intervals.\n'
        'Solid: all 30 paired losses finite. Hollow: finite-repeat conditional mean only; bracket = retained repeat count.\n'
        'Whole-ranking losses have different report lengths across tasks; effect magnitudes are not a universal task ranking.', fontsize=9)
    fig.subplots_adjust(top=.88, bottom=.23, left=.13, right=.985)
    out = ROOT / 'figures/repeated_holdout'; out.mkdir(parents=True, exist_ok=True)
    for extension in ('png', 'svg'):
        fig.savefig(out / ('confirmation_means.'+extension), dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
