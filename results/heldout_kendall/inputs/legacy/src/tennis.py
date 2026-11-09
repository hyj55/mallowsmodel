"""Pinned Sackmann ATP acquisition and chronological, prior-catalog splits."""
import hashlib
import json
import urllib.request
import numpy as np
import pandas as pd
from .data import ROOT

COMMIT='83733587353df8a41f2fd4f516147d5aa83f5a8d'
BASE='https://raw.githubusercontent.com/Aneeshers/tennis-sackmann-archive/'+COMMIT+'/'

def download_tennis():
    folder=ROOT/'data/raw/tennis';folder.mkdir(parents=True,exist_ok=True)
    manifest_path=ROOT/'data/tennis_sources.json'
    old=json.loads(manifest_path.read_text()) if manifest_path.exists() else None
    paths=[f'atp/atp_matches_{y}.csv' for y in range(2009,2020)]
    paths+=['atp/UPSTREAM_README.md','atp/matches_data_dictionary.txt','LICENSE']
    expected={x['file']:x for x in old['files']} if old else {}
    entries=[]
    for member in paths:
        name=member.split('/')[-1];path=folder/name
        if not path.exists():
            path.write_bytes(urllib.request.urlopen(BASE+member,timeout=90).read())
        b=path.read_bytes();digest=hashlib.sha256(b).hexdigest()
        if name in expected:
            assert digest==expected[name]['sha256'] and len(b)==expected[name]['bytes']
        entries.append(dict(file=name,url=BASE+member,bytes=len(b),sha256=digest))
    manifest=dict(original_source='https://github.com/JeffSackmann/tennis_atp',
        mirror='Aneeshers/tennis-sackmann-archive',commit=COMMIT,files=entries)
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    license_path=ROOT/'data/licenses/ATP-CC-BY-NC-SA-4.0.txt'
    license_path.parent.mkdir(parents=True,exist_ok=True)
    license_path.write_bytes((folder/'LICENSE').read_bytes())
    return folder

def season(year,folder=None):
    folder=download_tennis() if folder is None else folder
    df=pd.read_csv(folder/f'atp_matches_{year}.csv')
    valid=df[['winner_id','loser_id','tourney_date','score']].notna().all(axis=1)
    valid &= df.winner_id!=df.loser_id
    valid &= ~df.score.fillna('').str.upper().str.contains(r'W/O|RET|DEF|ABD|ABN|UNF',regex=True)
    out=df.loc[valid].copy()
    out['date']=pd.to_datetime(out.tourney_date.astype(str),format='%Y%m%d')
    out=out.sort_values(['date','tourney_id','match_num'],kind='stable')
    return out,dict(year=year,source_rows=len(df),retained_completed=len(out),
                   excluded_invalid_or_uncompleted=int((~valid).sum()))

def chronological_year(year,folder=None):
    folder=download_tennis() if folder is None else folder
    previous,_=season(year-1,folder);df,audit=season(year,folder)
    catalog=np.unique(previous[['winner_id','loser_id']].to_numpy().astype(int))
    lookup={int(v):i for i,v in enumerate(catalog)}
    inside=df.winner_id.isin(catalog)&df.loser_id.isin(catalog)
    audit.update(catalog_n=len(catalog),excluded_out_of_catalog=int((~inside).sum()),
        excluded_out_of_catalog_test=int(((~inside)&(df.date>=f'{year}-07-01')).sum()))
    df=df.loc[inside].copy()
    y=np.array([[lookup[int(a)],lookup[int(b)]] for a,b in df[['winner_id','loser_id']].to_numpy()])
    train_mask=(df.date<f'{year}-07-01').to_numpy()
    inner_mask=(df.date<f'{year}-04-01').to_numpy()
    train,test=y[train_mask],y[~train_mask]
    seen=np.bincount(train.ravel(),minlength=len(catalog))>0;test_seen=seen[test].all(axis=1)
    audit.update(N_train=len(train),N_test_all=len(test),N_test_seen=int(test_seen.sum()),
        N_test_cold=int((~test_seen).sum()),unseen_training_players=int((~seen).sum()),catalog_ids=catalog.tolist())
    return dict(n=len(catalog),train=train,test=test,test_seen=test_seen,inner_train=y[inner_mask],
        inner_valid=y[train_mask&~inner_mask],groups=df.loc[~train_mask,'tourney_id'].to_numpy(),
        surface=df.loc[~train_mask,'surface'].fillna('unknown').to_numpy(),audit=audit)
