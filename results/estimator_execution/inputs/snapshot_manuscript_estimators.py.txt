"""Literal manuscript Algorithms 2.1/3.1/3.2. Exact sieve limited to m<=8."""
from functools import lru_cache
from itertools import permutations
import math
import numpy as np
from .models import pair_counts, validate_rankings

def exposure(n,r,N):
    lam=N*r*(r-1)/(n*(n-1)); mu=N*r/n
    return dict(n=n,r=r,N=N,mu=mu,lambda_=lam,
        coverage_ratio=mu/math.log(math.e*r),
        Vcov=float('inf') if r==n else -N*math.log1p(-r/n),
        lambda_region='below_1' if lam<1 else ('at_1' if lam==1 else 'above_1'),
        mu_region='below_1' if mu<1 else ('below_log_er' if mu<math.log(math.e*r) else 'above_log_er'),
        unseen_term=n*n*(1-r/n)**N,reference_shape=min(n*(n-1)/2,n/lam))

def proof_constants(beta0):
    if beta0<=0: raise ValueError('beta0 must be positive')
    rho=np.tanh(beta0/2); cstar=2+2048/beta0**2; tstar=min(1/8,beta0/64)
    b0=min(1/(8*cstar),tstar/8)
    return dict(A=256,K=max(8.,4/(b0*rho*rho)),CT=12/rho)

def schedule(n,r,N,eta,beta0=.8):
    c=proof_constants(beta0); lam=N*r*(r-1)/(n*(n-1)); m=n; stages=[]
    while eta*m>c['A']:
        s=len(stages)+1; width=math.ceil(math.sqrt(m/eta)+1/eta)
        next_m=min(m,8*width)
        if next_m>=m: raise RuntimeError('Noncontracting schedule')
        ell=math.log(c['CT'])+s*math.log(8)+math.log1p(lam*m)
        batch=math.ceil(c['K']*eta*ell*n*(n-1)/(r*(r-1)))
        stages.append(dict(width=width,batch=batch,cap=next_m));m=next_m
    return stages

def block_scores(y,labels,n,r):
    labels=np.asarray(labels); mask=np.zeros(n,bool);mask[labels]=True
    inside=mask[y]; k=inside.sum(axis=1);rank=inside.cumsum(axis=1)
    q=(k[:,None]+1-2*rank)*inside
    sums=np.bincount(y.ravel(),weights=q.ravel(),minlength=n)
    counts=np.bincount(y.ravel(),minlength=n)
    scores=np.divide((n-1)*sums,(r-1)*counts,out=np.zeros(n),where=counts>0)
    return np.clip(scores[labels],-len(labels),len(labels))

def score_order(y,labels,n,r,priority):
    labels=np.asarray(labels)
    return labels[np.lexsort((priority[labels],-block_scores(y,labels,n,r)))]

def padded_blocks(order,width):
    for a in range(0,len(order),2*width):
        b=min(len(order),a+2*width)
        left,right=max(0,a-3*width),min(len(order),b+3*width)
        yield order[left:right],order[a:b],left

def hierarchy(y,n,stages,priority,terminal_scores=True):
    r=y.shape[1];nodes=[(np.arange(n),np.arange(n))]
    offsets=np.zeros(n,dtype=int);used=0
    for stage in stages:
        batch=y[used:used+stage['batch']]
        if len(batch)!=stage['batch']: raise ValueError('Insufficient fresh reports')
        used+=len(batch);children=[]
        for labels,active in nodes:
            order=score_order(batch,labels,n,r,priority)
            for child,core,left in padded_blocks(order,stage['width']):
                active_child=core[np.isin(core,active)]
                if len(active_child):
                    offsets[active_child]+=left;children.append((child,active_child))
        nodes=children
    anchors=np.zeros(n,int)
    for labels,active in nodes:
        order=(score_order(y[used:],labels,n,r,priority) if terminal_scores
               else labels[np.argsort(priority[labels])])
        rank=np.zeros(n,int);rank[order]=np.arange(len(order))
        anchors[active]=offsets[active]+rank[active]
    return np.lexsort((priority,anchors)),used,len(nodes)

def efficient_center(y,n,seed=0,beta0=.8):
    y=validate_rankings(y,n);N,r=y.shape;meta=exposure(n,r,N)
    priority=np.random.default_rng(seed).permutation(n)
    low=(r-1)/(n-1);eta=min(meta['lambda_'],1.);candidates=[]
    while eta>=low:candidates.append(eta);eta/=2
    if meta['mu']>=1 and (not candidates or candidates[-1]!=low):candidates.append(low)
    for eta in candidates:
        stages=schedule(n,r,N,eta,beta0)
        if sum(s['batch'] for s in stages)<=N//2:
            order,used,leaves=hierarchy(y,n,stages,priority)
            return order,dict(depth=len(stages),eta=eta,pilot_reports=used,
                terminal_blocks=leaves,branch='hierarchy',outside_lambda=meta['lambda_']>1)
    return score_order(y,np.arange(n),n,r,priority),dict(depth=0,eta=None,
        pilot_reports=0,terminal_blocks=1,branch='borda_fallback',outside_lambda=meta['lambda_']>1)

@lru_cache(maxsize=8)
def permutation_table(m):
    if m>8:raise ValueError('Exact sieve limited to blocks of size <=8; no MLE substitution')
    orders=np.array(list(permutations(range(m))),dtype=np.int16)
    ranks=np.argsort(orders,axis=1);i,j=np.triu_indices(m,1)
    bits=ranks[:,i]>ranks[:,j]
    masks=(bits.astype(np.uint64)<<np.arange(len(i),dtype=np.uint64)).sum(axis=1,dtype=np.uint64)
    return orders,masks,bits

@lru_cache(maxsize=128)
def permutation_sieve(m,radius):
    orders,masks,_=permutation_table(m)
    if radius<1:return np.arange(len(orders))
    remaining=np.arange(len(orders));keep=[]
    while len(remaining):
        first=remaining[0];keep.append(first)
        remaining=remaining[np.bitwise_count(masks[remaining]^masks[first])>radius]
    return np.asarray(keep)

def extract_pairs(y,labels,rng):
    allowed=set(map(int,labels));pairs=[]
    for row in y:
        displayed=sorted(allowed.intersection(map(int,row)))
        if len(displayed)<2:continue
        a,b=rng.choice(displayed,size=2,replace=False)
        rank={int(item):j for j,item in enumerate(row)}
        pairs.append([a,b] if rank[a]<rank[b] else [b,a])
    return np.asarray(pairs,dtype=int).reshape(-1,2)

def sieve_order(pairs,labels):
    labels=np.sort(labels);m,k=len(labels),len(pairs)
    if m<=1 or k==0:return labels,dict(sieve_size=1,pairs=k,radius=None)
    phi=m*(m*(m-1)//2)/k;keep=permutation_sieve(m,math.floor(phi))
    lookup={int(item):i for i,item in enumerate(labels)}
    local=np.array([[lookup[int(a)],lookup[int(b)]] for a,b in pairs])
    w=pair_counts(local,m);orders,_,bits=permutation_table(m);i,j=np.triu_indices(m,1)
    losses=bits[keep].astype(np.int64)@(w[i,j]-w[j,i])+w[j,i].sum()
    winner=keep[np.argmin(losses)]
    return labels[orders[winner]],dict(sieve_size=len(keep),pairs=k,radius=phi)

def sharp_center(y,n,seed=0,beta0=.8):
    y=validate_rankings(y,n);N,r=y.shape;priority=np.random.default_rng(seed).permutation(n)
    stages=schedule(n,r,N,(r-1)/(n-1),beta0)
    if sum(s['batch'] for s in stages)>N//2:
        return score_order(y,np.arange(n),n,r,priority),dict(depth=0,
            branch='borda_fallback',pilot_reports=0,sieve_size=0,pairs=0)
    pilot,used,_=hierarchy(y,n,stages,priority,terminal_scores=False)
    width=math.ceil(8*256*(n-1)/(r-1));anchors=np.zeros(n,int);blocks=[]
    rng=np.random.default_rng(seed+173)
    for labels,core,left in padded_blocks(pilot,width):
        pairs=extract_pairs(y[used:],labels,rng);order,info=sieve_order(pairs,labels)
        rank=np.zeros(n,int);rank[order]=np.arange(len(order));anchors[core]=left+rank[core]
        blocks.append(info)
    return np.lexsort((priority,anchors)),dict(depth=len(stages),branch='exact_sieve',
        pilot_reports=used,sieve_size=sum(x['sieve_size'] for x in blocks),
        pairs=sum(x['pairs'] for x in blocks),blocks=blocks)
