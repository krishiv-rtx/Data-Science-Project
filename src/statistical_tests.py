"""Tests operate on observed arrays/counts; no example values are project results."""
import numpy as np
from scipy import stats

def p_text(p):
    return '< 2.23e-308 (floating-point underflow)' if p == 0 else f'{p:.6g}'

def welch(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float)
    a=a[np.isfinite(a)]; b=b[np.isfinite(b)]
    if min(len(a),len(b))<2: raise ValueError('Welch requires at least two observations per group')
    va,vb=a.var(ddof=1),b.var(ddof=1); aa,bb=va/len(a),vb/len(b)
    se=np.sqrt(aa+bb)
    if se == 0: raise ValueError('Undefined standard error')
    df=(aa+bb)**2/(aa**2/(len(a)-1)+bb**2/(len(b)-1))
    estimate=a.mean()-b.mean(); t=estimate/se; p=2*stats.t.sf(abs(t),df)
    margin=stats.t.ppf(.975,df)*se
    return dict(n_a=len(a),n_b=len(b),mean_a=a.mean(),mean_b=b.mean(),sd_a=np.sqrt(va),sd_b=np.sqrt(vb),
        estimate=estimate,se=se,statistic=t,df=df,p=float(p),ci_low=estimate-margin,ci_high=estimate+margin)

def proportions(xa,na,xb,nb):
    if min(na,nb)<=0 or not (0<=xa<=na and 0<=xb<=nb): raise ValueError('Invalid binomial counts')
    pa,pb=xa/na,xb/nb; pooled=(xa+xb)/(na+nb)
    expected=[na*pooled,na*(1-pooled),nb*pooled,nb*(1-pooled)]
    if min(expected)<5: raise ValueError('Normal approximation has expected count below 5')
    se0=np.sqrt(pooled*(1-pooled)*(1/na+1/nb)); z=(pa-pb)/se0
    se=np.sqrt(pa*(1-pa)/na+pb*(1-pb)/nb); margin=stats.norm.ppf(.975)*se
    cross=stats.chi2_contingency([[xa,na-xa],[xb,nb-xb]],correction=False)
    return dict(n_a=na,n_b=nb,events_a=xa,events_b=xb,proportion_a=pa,proportion_b=pb,
        estimate=pa-pb,se=se,statistic=z,df=None,p=float(2*stats.norm.sf(abs(z))),
        ci_low=pa-pb-margin,ci_high=pa-pb+margin,min_expected=min(expected),chi2_crosscheck=cross.statistic)

def grade_test(table, seed=558, bootstrap=1000):
    table=np.asarray(table,dtype=int)
    if table.ndim!=2 or table.shape[1]!=2 or (table<0).any(): raise ValueError('Expected grade by binary outcome counts')
    chi,p,df,expected=stats.chi2_contingency(table,correction=False)
    if expected.min()<5: raise ValueError('Sparse contingency table requires another method')
    n=table.sum(); v=np.sqrt(chi/n) # min(r-1,c-1)=1
    rng=np.random.default_rng(seed); vals=[]
    for _ in range(bootstrap):
        sim=rng.multinomial(int(n),(table/n).ravel()).reshape(table.shape)
        vals.append(np.sqrt(stats.chi2_contingency(sim,correction=False).statistic/n))
    lo,hi=np.quantile(vals,[.025,.975])
    return dict(n=int(n),estimate=v,statistic=chi,df=int(df),p=float(p),ci_low=lo,ci_high=hi,
        min_expected=float(expected.min()),bootstrap_replicates=bootstrap,
        ci_method='IID multinomial percentile bootstrap of Cramers V; extension',expected=expected.tolist())

def holm(ps):
    ps=np.asarray(ps); order=np.argsort(ps); sorted_adj=np.maximum.accumulate(ps[order]*(len(ps)-np.arange(len(ps))))
    out=np.empty(len(ps)); out[order]=np.minimum(sorted_adj,1); return out.tolist()
