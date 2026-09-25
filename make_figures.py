"""Standalone scientific figures from saved aggregate outputs; no source data needed."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT/"figures"
OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 160, "savefig.dpi": 220})
BLUE, ORANGE = "#245c96", "#c35b2b"


def save(fig, name):
    fig.savefig(OUT/f"{name}.png", bbox_inches="tight")
    fig.savefig(OUT/f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def main():
    real = pd.read_csv(ROOT/"results/real_summary.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, dataset, title in zip(axes, ["beans", "sushi_a", "sushi_b"],
                                  ["Beans: n=10, r=3", "Sushi A: n=10, r=10", "Sushi B: n=100, r=10"]):
        d = real[real.dataset == dataset]
        ax.axhline(0, color="#808080", lw=.8)
        ax.fill_between(d.N, d.ci_low, d.ci_high, color=BLUE, alpha=.12)
        ax.plot(d.N, d.delta, "o-", color=BLUE, ms=4, label="SM MLE - ridge PL")
        ax.plot(d.N, d.calibrated_delta, "s--", color=ORANGE, ms=4, label="Calibrated SM - ridge PL")
        ax.set_xscale("log")
        ax.set_xlabel("Total development reports N")
        ax.set_title(title)
        ax.grid(axis="y", alpha=.18)
    axes[0].set_ylabel("Whole-ranking NLL difference (nats)\nPositive: PL better; negative: SM better")
    axes[1].legend(loc="upper right", frameon=False, fontsize=8)
    fig.text(.5, -.01, "Bands: pointwise 95% test-report bootstrap intervals, conditional on fitted models. Sushi B center is approximate.",
             ha="center", fontsize=8, color="#444444")
    fig.tight_layout()
    save(fig, "real_learning_curves")

    synthetic = pd.read_csv(ROOT/"results/synthetic_summary.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, dgp, title in zip(axes, ["SM", "PL_equal", "PL_unequal"],
                              ["True selective Mallows", "True PL: equal worth gaps", "True PL: unequal worth gaps"]):
        d = synthetic[synthetic.dgp == dgp]
        ax.axhline(0, color="#808080", lw=.8)
        ax.fill_between(d.N, d.ci_low, d.ci_high, color=BLUE, alpha=.12)
        ax.plot(d.N, d.delta, "o-", color=BLUE, ms=4, label="SM MLE - ridge PL")
        ax.plot(d.N, d.SM_calibrated_nll-d.PL_nll, "s--", color=ORANGE, ms=4,
                label="Calibrated SM - ridge PL")
        ax.set_xscale("log")
        ax.set_xlabel("Total development reports N")
        ax.set_title(title)
        ax.grid(axis="y", alpha=.18)
    axes[0].set_ylabel("Whole-ranking NLL difference (nats)")
    axes[1].legend(frameon=False, fontsize=8)
    fig.text(.5, -.01, "n=10, r=3; 30 independent repetitions; matched expected inversion count; bands are replicate-based 95% intervals.",
             ha="center", fontsize=8, color="#444444")
    fig.tight_layout()
    save(fig, "synthetic_learning_curves")

    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    for dgp, color, marker in [("SM", BLUE, "o"), ("PL_unequal", ORANGE, "s")]:
        d = synthetic[synthetic.dgp == dgp]
        ax.plot(d.N, d.SM_center_error, marker+"-", color=color, label=f"SM fit, true {dgp}")
        ax.plot(d.N, d.PL_center_error, marker+"--", color=color, label=f"PL fit, true {dgp}")
    ax.set(xscale="log", xlabel="Total development reports N", ylabel="Mean central Kendall error (out of 45)")
    ax.grid(axis="y", alpha=.18)
    ax.legend(frameon=False, fontsize=8, ncol=2)
    fig.tight_layout()
    save(fig, "central_rank_error")


if __name__ == "__main__":
    main()
