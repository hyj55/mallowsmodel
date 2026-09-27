"""Export repeated-split scientific figures. Whiskers are split ranges, not CIs."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'figures/group_sensitivity'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    table = pd.read_csv(ROOT / 'results/group_sensitivity/contrasts.csv')
    table = table[(table.percent == 70) & (table.sm_method == 'sm_mle')]
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.4), sharex='col')
    for row, family in enumerate(['puzzle', 'dots']):
        names = [f'{family}-{v}' for v in ([5, 7, 9, 11] if family == 'puzzle' else [3, 5, 7, 9])]
        for col, reference in enumerate(['pooled', 'matched_pool']):
            ax = axes[row, col]
            data = table[table.reference == reference].set_index('dataset').loc[names]
            for offset, model, color in [(-.12, 'sm', '#2676b8'), (.12, 'pl', '#c76824')]:
                center = data[model + '_change_median'].to_numpy()
                lo, hi = data[model + '_change_p05'].to_numpy(), data[model + '_change_p95'].to_numpy()
                ax.errorbar(center, np.arange(4) + offset, xerr=np.stack([center-lo, hi-center]),
                            fmt='o', capsize=3, color=color, label='SM exact center' if model == 'sm' else 'PL')
            ax.axvline(0, color='#777777', linewidth=.8)
            ax.set_yticks(np.arange(4), [n.replace('-', ' ').title() for n in names])
            ax.invert_yaxis()
            ax.grid(axis='x', alpha=.2)
            ax.set_title('Local minus pooled (all training)' if reference == 'pooled' else 'Local minus pooled (same training count)')
            if row == 1:
                ax.set_xlabel('NLL change (nats/report); negative favors local fitting')
    axes[0, 0].legend(loc='best', frameon=False)
    fig.suptitle('Does fitting the actual stimulus set improve prediction?', fontsize=15, y=.99)
    fig.text(.5, .012, '100 repeated 70/30 splits. Dots: medians; whiskers: 5th–95th split percentiles, NOT confidence intervals.\n'
             'Both families and fitting schemes use the same four-way finite prediction mask in each comparison.',
             ha='center', fontsize=9)
    fig.tight_layout(rect=[0, .075, 1, .955])
    for extension in ['svg', 'png']:
        fig.savefig(OUT / ('local_prediction_changes.' + extension), dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    names = ['puzzle-5','puzzle-7','puzzle-9','puzzle-11','dots-3','dots-5','dots-7','dots-9']
    for offset, ref, color, label in [(-.13,'pooled','#6856a5','Versus full pooled training'),
                                     (.13,'matched_pool','#218c7a','Versus matched training count')]:
        data = table[table.reference == ref].set_index('dataset').loc[names]
        center = data.interaction_median.to_numpy()
        lo, hi = data.interaction_p05.to_numpy(), data.interaction_p95.to_numpy()
        ax.errorbar(center, np.arange(len(names)) + offset, xerr=np.stack([center-lo,hi-center]),
                    fmt='o', color=color, capsize=3, label=label)
    ax.axvline(0, color='#777777', linewidth=.8)
    ax.set_yticks(np.arange(len(names)), [n.replace('-', ' ').title() for n in names]); ax.invert_yaxis()
    ax.grid(axis='x', alpha=.2)
    fig.suptitle('Does local fitting change the relative SM–PL advantage?', fontsize=14, y=.985)
    ax.set_xlabel('Change in (SM NLL - PL NLL); negative shifts the comparison toward SM')
    fig.legend(*ax.get_legend_handles_labels(), frameon=False, loc='upper center',
               bbox_to_anchor=(.5, .945), ncol=2, fontsize=9)
    fig.text(.5,.015,'Exact SM center. Paired four-way finite cases. Whiskers are 5th–95th split ranges, NOT confidence intervals.',
             ha='center',fontsize=8.5)
    fig.tight_layout(rect=[0,.05,1,.89])
    for extension in ['svg','png']:
        fig.savefig(OUT / ('relative_model_changes.' + extension), dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
