"""Reconstruct all real scores and replay one simulation replicate per target."""
import hashlib,json,platform
import numpy as np
import pandas as pd
import scipy
from src.data import ROOT,load_beans,load_sushi
from src.models import SMFit,pl_nll,kendall
from src.tennis import chronological_year,download_tennis
from run_exposure import OUT,SEED,compare,draw,matched_theta,estimator_seed,js,mean_ci

def main():
    maximum=0.;replayed=0
    for part in ['small','coverage']:
        frame=pd.read_csv(OUT/f'{part}_replicates.csv')
        assert len(frame)==(4080 if part=='small' else 1440)
        for seed,g in frame[frame.rep==0].groupby('seed'):
            row=g.iloc[0];n,r,N=map(int,[row.n,row.r,row.N]);rng=np.random.default_rng(int(seed))
            truth=rng.permutation(n);theta=matched_theta(n,r,.8,truth)
            train=draw(rng,N,n,r,truth,row.dgp,.8,theta)
            test=draw(rng,2000 if n==8 else 1000,n,r,truth,row.dgp,.8,theta)
            fitseed=estimator_seed(int(seed));assert np.all(g.estimator_seed==fitseed)
            methods=['sharp','efficient','mle'] if part=='small' else ['efficient']
            models,losses,factors=compare(train,test,n,fitseed,methods)
            for _,v in g.iterrows():
                assert kendall(models[v.method].order,truth)==v.risk
                error=abs(losses[v.method].mean()-v.nll);maximum=max(maximum,error)
                assert error<1e-8
                assert abs(losses.get(v.method+'_shrunk',losses[v.method]).mean()-v.nll_shrunk)<1e-8
            replayed+=1
        summary=pd.read_csv(OUT/f'{part}_summary.csv')
        for _,s in summary.iterrows():
            g=frame[(frame.dgp==s.dgp)&(frame.n==s.n)&(frame.r==s.r)&(frame.N==s.N)&(frame.method==s.method)]
            assert len(g)==s.repetitions
            for metric in ['risk','risk_normalized','nll','delta_nll','nll_shrunk','delta_shrunk']:
                m,lo,hi=mean_ci(g[metric])
                np.testing.assert_allclose([m,lo,hi],[s[metric],s[metric+'_lo'],s[metric+'_hi']],atol=1e-10)
        np.testing.assert_allclose(frame.lambda_,frame.N*frame.r*(frame.r-1)/(frame.n*(frame.n-1)))
        np.testing.assert_allclose(frame.mu,frame.N*frame.r/frame.n)
    saved=json.loads((OUT/'real_parameters.json').read_text())
    real=pd.read_csv(OUT/'real_replicates.csv')
    datasets={d.name:d for d in [load_beans(),load_sushi('b')]}
    for key,p in saved.items():
        name,rep,N=key.rsplit('_',2);test=datasets[name].y[p['test_indices']]
        assert not set(p['train_indices']).intersection(p['test_indices'])
        losses={'pl':pl_nll(test,np.array(p['pl_theta']))}
        for method,v in p['sm'].items():
            sm=SMFit(np.array(v['order']),v['beta'],0,{})
            losses[method]=sm.nll(test);losses[method+'_shrunk']=sm.nll(test,v['factor'])
        g=real[(real.dataset==name)&(real.rep==int(rep))&(real.N==int(N))]
        for _,v in g.iterrows():
            error=abs(losses[v.method].mean()-v.nll);maximum=max(maximum,error);assert error<1e-10
    folder=download_tennis()
    saved_tennis=json.loads((OUT/'tennis_parameters.json').read_text())
    sports=pd.read_csv(OUT/'tennis_by_year.csv')
    for year,p in saved_tennis.items():
        d=chronological_year(int(year),folder);test=d['test']
        losses={'pl':pl_nll(test,np.array(p['pl_theta']))}
        for method,v in p['sm'].items():
            sm=SMFit(np.array(v['order']),v['beta'],0,{})
            losses[method]=sm.nll(test);losses[method+'_shrunk']=sm.nll(test,v['factor'])
        for _,v in sports[sports.year==int(year)].iterrows():
            mask=d['test_seen'] if v.target=='seen' else np.ones(len(test),bool);loss=losses[v.method][mask]
            np.testing.assert_allclose([loss.mean(),np.mean((1-np.exp(-loss))**2)],[v.nll,v.brier],atol=1e-10)
            maximum=max(maximum,abs(loss.mean()-v.nll))
    summary=pd.read_csv(OUT/'tennis_summary.csv')
    seen=summary[summary.target=='seen'].set_index('method')
    # Independent references recorded before workspace interruption (rounded).
    np.testing.assert_allclose(seen.loc[['pl','efficient_shrunk','insertion_shrunk'],'nll'],
                               [.63444,.65898,.66392],atol=2e-5,rtol=0)
    same=pd.read_csv(OUT/'tennis_same_order_summary.csv').set_index('method')
    assert abs(same.loc['same_order_shrunk','delta']-.02169)<2e-5
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        ROOT/'src/manuscript_estimators.py',ROOT/'src/tennis.py',ROOT/'run_exposure.py',
        ROOT/'run_exposure_followup.py',ROOT/'docs/protocols/EXPOSURE_PROTOCOL.md',
        ROOT/'docs/protocols/EXPOSURE_FOLLOWUP.md']}
    result=dict(status='passed',synthetic_independent_datasets=1740,replayed_design_replicates=replayed,
        real_saved_fits_reconstructed=len(saved),tennis_seasons_reconstructed=len(saved_tennis),
        max_nll_reconstruction_error=maximum,recorded_tennis_results_recovered=True,
        source_sha256=hashes,python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
        seed=SEED,random_streams='independent data and SeedSequence([data_seed,73471]) estimator')
    js(OUT/'validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
