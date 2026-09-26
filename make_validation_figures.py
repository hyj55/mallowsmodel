"""Scientific figures from frozen summaries; no fitting or observation changes."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, ScalarFormatter
import pandas as pd

ROOT = Path(__file__).resolve().parent


def run():
    data = pd.read_csv(ROOT/'results/validation_extension/synthetic_diagnostic_summary.csv')
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.hashsalt': 'validation-extension'})
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.5))

    def line(ax, rows, metric, label, color, marker):
        rows = rows.sort_values('M')
        ax.errorbar(rows.M, rows[metric],
                    yerr=[rows[metric]-rows[metric+'_lo'], rows[metric+'_hi']-rows[metric]],
                    color=color, marker=marker, linewidth=1.7, capsize=3, label=label)

    sm = data[data.generator.eq('sm')]
    for N, diagnostic, label, color, marker in [
        (28, 'fitted', 'Estimated center, N=28', '#ba5b2b', 'o'),
        (28, 'oracle', 'True center, N=28', '#4576a8', 's'),
        (448, 'fitted', 'Estimated center, N=448', '#327e66', '^')]:
        line(axes[0], sm[sm.N.eq(N)&sm.diagnostic.eq(diagnostic)],
             'positive', label, color, marker)
    axes[0].set_title('A  Detecting a true SM effect', loc='left', fontweight='bold')
    axes[0].set_ylabel('Positive-effect detection rate')
    axes[0].set_ylim(-.03, 1.05)
    axes[0].legend(loc='upper left', fontsize=8.5, frameon=False)

    mix = data[data.family.eq('confounding')]
    for diagnostic, label, color, marker in [
        ('pooled', 'Pooled', '#7c5aa0', 'o'),
        ('group_adjusted', 'Within groups', '#327e66', 's')]:
        line(axes[1], mix[mix.setting.eq(.45)&mix.diagnostic.eq(diagnostic)],
             'positive', label, color, marker)
    axes[1].set_title('B  PL groups, associated displays', loc='left', fontweight='bold')
    axes[1].set_ylabel('Positive-effect detection rate')
    axes[1].set_ylim(-.03, 1.05)
    axes[1].legend(title=r'$\rho=0.45$', loc='upper left', fontsize=9, frameon=False)

    severe = mix[mix.setting.eq(.9)&mix.diagnostic.eq('group_adjusted')]
    line(axes[2], severe, 'reject_zero', 'Within groups', '#a43d48', 'o')
    axes[2].axhline(.05, color='#666666', linestyle='--', linewidth=1, label='Nominal 5%')
    axes[2].set_title('C  Poor overlap breaks calibration', loc='left', fontweight='bold')
    axes[2].set_ylabel('Two-sided rejection of true zero')
    axes[2].set_ylim(0, .46)
    axes[2].legend(title=r'$\rho=0.90$', loc='upper right', fontsize=9, frameon=False)
    for row in severe.itertuples():
        alignment = 'left' if row.M == 60 else 'right' if row.M == 1000 else 'center'
        axes[2].annotate(f'{row.available}/200 available', (row.M, row.reject_zero_hi),
                         xytext=(0, 8), textcoords='offset points', ha=alignment, fontsize=8)

    for ax in axes:
        ax.set_xscale('log')
        ax.set_xticks([60, 200, 1000])
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.set_xlim(45, 1350)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_xlabel('Independent diagnostic reports (M)')
        ax.grid(axis='y', alpha=.18)
    fig.subplots_adjust(left=.06, right=.985, top=.9, bottom=.23, wspace=.32)
    fig.text(.06, .07, '200 independent training repetitions per cell; pointwise 95% Wilson intervals. '
             'Rates condition on availability.\n'
             'Budgets are nested within repetitions. Panel A: N=28 has 193/200 available; N=448 has 200/200.',
             fontsize=9, color='#444444')
    out = ROOT/'figures/validation_extension'
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out/'context_validation.png', dpi=180)
    fig.savefig(out/'context_validation.svg', metadata={'Date': None})
    plt.close(fig)


if __name__ == '__main__':
    run()
