"""Exploratory diagnostics; see docs/protocols/DIAGNOSTIC_PROTOCOL.md.

Reuses saved parameters and reconstructs the original splits from fixed seeds.
Sushi data are downloaded by src.data when absent, never bundled with outputs.
"""
import hashlib
import io
import json
from itertools import permutations
from pathlib import Path
import platform
import zipfile

import numpy as np
import pandas as pd
from scipy.special import logsumexp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.data import RAW, ROOT, load_all
from src.models import distances, logz_mean, pl_nll, sample_sm, sample_pl
from src.diagnostics import (binary_nll, context_slope, pair_arrays,
                             pl_shell_distribution, shell_counts,
                             shell_decomposition, sm_pair_probability)
from run_experiments import OUT, SEED, outer_split, paired_ci, write_json

DIAG_SEED = 20260925
REPS = 2000


def verify():
    rng = np.random.default_rng(DIAG_SEED)
    errors = []
    for r in [3, 4, 5, 6]:
        perm = np.array(list(permutations(range(r))))
        center = rng.permutation(r)
        theta = rng.normal(size=r)
        d = distances(perm, center)
        expected = np.bincount(d, weights=np.exp(-pl_nll(perm, theta)),
                               minlength=r*(r-1)//2+1)
        actual = pl_shell_distribution(center[None,:], theta)[0]
        errors.append(float(np.max(np.abs(expected-actual))))
        assert np.allclose(expected, actual, atol=1e-12)
        assert np.array_equal(np.bincount(d), shell_counts(r))
        for beta in [0., .2, np.log(2), 2.]:
            probability = np.exp(-beta*d - logz_mean(r, beta)[0])
            position = np.argsort(perm, axis=1)
            for i in range(r):
                for j in range(i+1,r):
                    empirical = probability[position[:,center[i]] < position[:,center[j]]].sum()
                    analytical = sm_pair_probability(np.array([j-i]), beta)[0]
                    assert abs(empirical-analytical) < 1e-12
        check = shell_decomposition(perm, center, .8, theta)
        assert np.allclose(check["total"],check["shell_mass"]+check["within_shell"])
    assert np.allclose(sm_pair_probability(np.array([1,2]),np.log(2)), [2/3,16/21])
    return {"exhaustive_sizes": [3,4,5,6], "max_shell_probability_error": max(errors),
            "checks": "pair marginals, shell counts, PL shell DP, loss decomposition, analytic triples"}


def ci_record(values):
    lo, hi = paired_ci(values, seed=DIAG_SEED, resamples=REPS)
    return {"value": float(np.mean(values)), "ci_low": lo, "ci_high": hi}


def gap_bins(train_arrays, test_arrays):
    cuts = np.quantile(train_arrays["worth_gap"][train_arrays["gap"] == 1], [1/3,2/3])
    assignment = np.searchsorted(cuts,test_arrays["worth_gap"],side="right")
    m = test_arrays["z"].shape[0]
    # report x bin x [count, observed successes, predicted SM, predicted PL]
    result = np.zeros((m,3,4))
    for g in range(3):
        mask = (test_arrays["gap"] == 1) & (assignment == g)
        result[:,g,0] = mask.sum(axis=1)
        for k,key in enumerate(["z","sm","pl"],1):
            result[:,g,k] = (mask*test_arrays[key]).sum(axis=1)
    return result, cuts.tolist()


def summarize_bins(records, dataset):
    a = np.mean(records,axis=0)
    rng = np.random.default_rng(DIAG_SEED)
    stats = a.sum(axis=0)
    boot = np.array([a[rng.integers(len(a),size=len(a))].sum(axis=0) for _ in range(REPS)])
    rows = []
    for g in range(3):
        row = {"dataset":dataset,"bin":g+1,"mean_pair_count":stats[g,0]}
        for k,name in enumerate(["observed","sm_predicted","pl_predicted"],1):
            row[name] = stats[g,k]/stats[g,0]
            rates = np.divide(boot[:,g,k],boot[:,g,0],out=np.full(REPS,np.nan),where=boot[:,g,0]>0)
            row[name+"_lo"],row[name+"_hi"] = np.nanquantile(rates,[.025,.975])
        rows.append(row)
    return rows


def main():
    verification = verify()
    OUT.mkdir(exist_ok=True)
    (ROOT/"figures").mkdir(exist_ok=True)
    protocol = ROOT/"docs/protocols/DIAGNOSTIC_PROTOCOL.md"
    write_json(OUT/"diagnostic_manifest.json",{
        "date":"2026-09-25","protocol_sha256":hashlib.sha256(protocol.read_bytes()).hexdigest(),
        "seed":DIAG_SEED,"bootstrap":REPS,"python":platform.python_version(),
        "numpy":np.__version__,"verification":verification,
        "inference":"Exploratory, conditional on original fits; whole-report resampling",
        "joint_likelihood_included":False})
    params = json.loads((OUT/"fitted_parameters.json").read_text())
    datasets = load_all()  # Downloads and verifies Sushi before opening its archive.
    with zipfile.ZipFile(RAW/"sushi3-2016.zip") as z:
        udata = np.loadtxt(io.StringIO(z.read("sushi3-2016/sushi3.udata").decode()),dtype=int)
    decomposition, pair_scores, contexts, context_reps, bins, audits, bin_cutoffs = [],[],[],[],[],[],[]
    for data in datasets:
        pool,test_idx = outer_split(data)
        test = data.y[test_idx]
        largest = 673 if data.name == "beans" else 3000
        repetitions = 3 if data.name == "sushi_b" else 5
        sets,counts = np.unique(np.sort(test,axis=1),axis=0,return_counts=True)
        audits.append({"dataset":data.name,"test_reports":len(test),"unique_sets":len(sets),
                       "max_set_repeats":int(counts.max()),"sets_repeated_at_least_5":int((counts>=5).sum())})
        for size in ([largest,20] if data.name == "beans" else [largest]):
            components,cal_components,scores,bin_records = [],[],[],[]
            context_records = {}
            for rep in range(repetitions):
                p = params[f"{data.name}_N{size}_rep{rep}"]
                center = np.array(p["sm_order"]);theta = np.array(p["pl_theta"])
                decomp = shell_decomposition(test,center,p["beta"],theta)
                components.append(decomp)
                cal = dict(decomp)
                cal_sm = p["beta"]*p["beta_factor"]*distances(test,center)+logz_mean(test.shape[1],p["beta"]*p["beta_factor"])[0]
                cal["total"] = cal_sm-decomp["pl_nll"]
                cal["shell_mass"] = cal_sm-decomp["sym_nll"]
                cal_components.append(cal)
                if size != largest:
                    continue
                pairs = pair_arrays(test,center,p["beta"],theta)
                z = pairs["z"]
                scores.append({"binary_logloss":(binary_nll(z,pairs["sm"])-binary_nll(z,pairs["pl"])).mean(axis=1),
                               "brier":((z-pairs["sm"])**2-(z-pairs["pl"])**2).mean(axis=1)})
                train_idx = np.random.default_rng(SEED+11+rep).permutation(pool)[:size]
                trpairs = pair_arrays(data.y[train_idx],center,p["beta"],theta)
                grouped,cuts = gap_bins(trpairs,pairs)
                bin_records.append(grouped)
                bin_cutoffs.append({"dataset":data.name,"replicate":rep,"cut_1":cuts[0],"cut_2":cuts[1]})
                configs = [("pair",None)]
                if data.name == "beans":
                    configs.append(("pair_x_season",data.groups[test_idx]))
                if data.name == "sushi_b":
                    configs.append(("pair_x_region",udata[test_idx,9]))
                for label,strata in configs:
                    result = context_slope(pairs,strata,resamples=REPS,seed=DIAG_SEED,return_draws=True)
                    draws = result.pop("_draws",None)
                    context_reps.append({"dataset":data.name,"replicate":rep,"stratification":label,**result})
                    context_records.setdefault(label,[]).append((result,draws))
                print(f"Diagnostics {data.name} N={size} replicate={rep} complete",flush=True)
            for fit_name,records in [("main",components),("beta_shrinkage",cal_components)]:
                for component in ["total","shell_mass","within_shell"]:
                    avg = np.mean([d[component] for d in records],axis=0)
                    decomposition.append({"dataset":data.name,"N":size,"fit":fit_name,
                                          "component":component,"repetitions":repetitions,**ci_record(avg)})
            if size != largest:
                continue
            for metric in ["binary_logloss","brier"]:
                pair_scores.append({"dataset":data.name,"metric":metric,
                                    **ci_record(np.mean([d[metric] for d in scores],axis=0))})
            bins += summarize_bins(bin_records,data.name)
            for label,records in context_records.items():
                available = [rec for rec,draws in records if draws is not None]
                row = {"dataset":data.name,"stratification":label,"available_fits":len(available)}
                if len(available) != repetitions:
                    contexts.append({**row,"status":"insufficient_variation_in_some_or_all_fits"})
                    continue
                # Same bootstrap report indices in each fit; do not treat fits as independent.
                estimates = np.array([[d[k] for k in ["observed","sm_predicted","pl_predicted"]] for d in available]).mean(axis=0)
                draws = np.mean([v for _,v in records],axis=0)
                draws = draws[np.isfinite(draws).all(axis=1)]
                row.update(status="ok",valid_bootstraps=len(draws))
                for key in ["eligible_cells","eligible_pairs","pair_observations","reports"]:
                    row[key+"_min"] = min(d[key] for d in available)
                    row[key+"_max"] = max(d[key] for d in available)
                for j,key in enumerate(["observed","sm_predicted","pl_predicted"]):
                    row[key] = estimates[j]
                    row[key+"_lo"],row[key+"_hi"] = np.quantile(draws[:,j],[.025,.975])
                for j,key in [(1,"residual_vs_sm"),(2,"residual_vs_pl")]:
                    row[key] = estimates[0]-estimates[j]
                    row[key+"_lo"],row[key+"_hi"] = np.quantile(draws[:,0]-draws[:,j],[.025,.975])
                contexts.append(row)
        print(pd.DataFrame(decomposition).tail(6).round(5).to_string(index=False),flush=True)
    for name,records in [("shell_decomposition",decomposition),("pair_diagnostics",pair_scores),
                         ("context_effects",contexts),("context_replicates",context_reps),
                         ("adjacent_pair_bins",bins),("diagnostic_coverage",audits),
                         ("diagnostic_bin_cutoffs",bin_cutoffs)]:
        pd.DataFrame(records).to_csv(OUT/f"{name}.csv",index=False)
    controls = positive_controls()
    pd.DataFrame(controls).to_csv(OUT/"diagnostic_controls.csv",index=False)
    make_plot()
    print("SHELL DECOMPOSITION",pd.DataFrame(decomposition).query('fit == "main"').round(5).to_string(index=False),sep="\n")
    print("CONTEXT",pd.DataFrame(contexts).round(5).to_string(index=False),sep="\n")
    print("PAIR SCORES",pd.DataFrame(pair_scores).round(5).to_string(index=False),sep="\n")


def positive_controls():
    # Fixed displayed sets with endpoints 0 and 2; gap 2 versus gap 1.
    rng = np.random.default_rng(DIAG_SEED+1)
    rows = []
    beta = np.log(2)
    theta = np.log([16.,4.,1.,.25])
    size = 10000
    for model in ["SM","PL"]:
        for s in [np.array([0,1,2]),np.array([0,2,3])]:
            if model == "SM":
                local = sample_sm(rng,size,3,3,np.arange(3),beta)
            else:
                local = sample_pl(rng,size,3,3,theta[s])
            y = s[local]
            outcome = (np.argmax(y==0,axis=1)<np.argmax(y==2,axis=1)).mean()
            h = int(np.flatnonzero(s==2)[0])
            theoretical = float(sm_pair_probability(np.array([h]),beta)[0]) if model=="SM" else 16/17
            rows.append({"model":model,"set":"-".join(map(str,s)),"reports":size,
                         "gap":h,"observed_pair_probability":outcome,"theoretical":theoretical})
    return rows


def make_plot():
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    d = pd.read_csv(OUT/"shell_decomposition.csv")
    fig,axes = plt.subplots(1,2,figsize=(10.5,3.7))
    datasets = ["beans","sushi_a","sushi_b"]
    for offset,component,color,label in [(-.16,"shell_mass","#245c96","Inversion-count distribution"),(.16,"within_shell","#c35b2b","Within-shell allocation")]:
        q = d.query('fit == "main" and N != 20 and component == @component').set_index("dataset").loc[datasets]
        x = np.arange(3)+offset
        axes[0].bar(x,q.value,width=.3,color=color,label=label)
        axes[0].errorbar(x,q.value,yerr=np.array([q.value-q.ci_low,q.ci_high-q.value]),fmt="none",color="#172b40",capsize=3,lw=1)
    axes[0].set(xticks=np.arange(3),xticklabels=["Beans","Sushi A","Sushi B*"],ylabel="SM minus PL NLL component (nats)")
    axes[0].axhline(0,color="#888",lw=.8);axes[0].legend(frameon=False,fontsize=8)
    bins = pd.read_csv(OUT/"adjacent_pair_bins.csv").query('dataset == "sushi_a"')
    axes[1].errorbar(bins.bin,bins.observed,yerr=np.array([bins.observed-bins.observed_lo,bins.observed_hi-bins.observed]),fmt="o-",color="#172b40",label="Observed (report bootstrap)",capsize=3)
    axes[1].plot(bins.bin,bins.sm_predicted,"s--",color="#245c96",label="SM")
    axes[1].plot(bins.bin,bins.pl_predicted,"^--",color="#c35b2b",label="PL")
    axes[1].set(xticks=[1,2,3],xticklabels=["Small","Medium","Large"],xlabel="PL worth-gap bin (cutoffs from training)",ylabel="Agreement with fitted SM center",title="Sushi A: adjacent center pairs only")
    axes[1].legend(frameon=False,fontsize=8)
    fig.tight_layout()
    fig.savefig(ROOT/"figures/mechanism_diagnostics.png",dpi=200)
    fig.savefig(ROOT/"figures/mechanism_diagnostics.svg")
    plt.close(fig)


def same_center_sensitivity():
    """Post-diagnostic sensitivity, extending the earlier same-order follow-up."""
    from src.data import load_sushi
    from run_followups import fit_pl_with_order
    parameters = json.loads((OUT/"fitted_parameters.json").read_text())
    data = load_sushi("a")
    pool,test = outer_split(data)
    records = []
    for rep in range(5):
        p = parameters[f"sushi_a_N3000_rep{rep}"]
        train = np.random.default_rng(SEED+11+rep).permutation(pool)[:3000]
        order = np.array(p["sm_order"])
        theta = fit_pl_with_order(data.y[train],order,p["tau"],np.array(p["pl_theta"]))
        records.append(shell_decomposition(data.y[test],order,p["beta"],theta))
    rows = []
    for key in ["total","shell_mass","within_shell"]:
        values = np.mean([x[key] for x in records],axis=0)
        rows.append({"dataset":"sushi_a","N":3000,"fit":"PL_order_constrained_to_SM",
                     "component":key,**ci_record(values)})
    pd.DataFrame(rows).to_csv(OUT/"shell_same_center_sensitivity.csv",index=False)
    addendum = ROOT/"docs/protocols/DIAGNOSTIC_ADDENDUM.md"
    write_json(OUT/"diagnostic_sensitivity_manifest.json",{
        "addendum_sha256":hashlib.sha256(addendum.read_bytes()).hexdigest(),
        "seed":DIAG_SEED,"bootstrap":REPS,"selection":"Post-diagnostic sensitivity; no test tuning"})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--same-center",action="store_true")
    args = parser.parse_args()
    main()
    if args.same_center:
        same_center_sensitivity()
