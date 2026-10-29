"""Run from project root. Never prints raw observations or modifies the source."""
import argparse
from pathlib import Path
import sys,json,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from src.config import ROOT, NUMERIC, PRACTICAL
from src.data_loading import load_and_audit
from src.preprocessing import prepare,iqr_summary,encode
from src.statistical_tests import welch,proportions,grade_test,holm,p_text
from src.eda import figures
from src.data_quality import extra_checks,clean_underflow

def dump(path,obj):
    Path(path).write_text(json.dumps(clean_underflow(obj),indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--data',type=Path,default=ROOT/'data/raw/accepted_2007_to_2018Q4.csv'); args=ap.parse_args()
    started=time.time()
    for p in ['outputs/tables','outputs/logs','data/processed','figures/eda','figures/inference','reports']:(ROOT/p).mkdir(parents=True,exist_ok=True)
    raw,audit=load_and_audit(args.data); dump(ROOT/'outputs/dataset_audit.json',audit)
    if audit['duplicate_ids'] or audit['missing_ids']: raise ValueError('Identifier integrity needs manual review before inference')
    d,t,changes=prepare(raw); del raw
    extra_checks(d,audit)
    expected={'grade':set('ABCDEFG'),'term':{'36 months','60 months'}}
    for c,allowed in expected.items():
        unexpected=set(t[c].dropna().unique())-allowed
        if unexpected: raise ValueError(f'Unexpected {c}: {unexpected}')
    encoded=encode(t); dump(ROOT/'outputs/encoded_size.json',encoded); dump(ROOT/'outputs/preparation.json',changes)
    pd.DataFrame({'column':audit['column_names'],'missing_count':[audit['missing_counts'][c] for c in audit['column_names']],
        'missing_percent':[100*audit['missing_counts'][c]/audit['rows'] for c in audit['column_names']],
        'inferred_type':[audit['inferred_types'][c] for c in audit['column_names']]}).to_csv(ROOT/'outputs/tables/missingness.csv',index=False)
    pd.DataFrame({c:iqr_summary(d[c]) for c in NUMERIC}).T.to_csv(ROOT/'outputs/tables/outliers.csv')
    d[NUMERIC].describe(percentiles=[.01,.25,.5,.75,.99]).T.to_csv(ROOT/'outputs/tables/numeric_summary.csv')
    t.groupby('loan_status')[NUMERIC].agg(['count','mean','std','median','min','max','skew']).to_csv(ROOT/'outputs/tables/group_summaries.csv')
    results=[]; sensitivity={}
    for c in ['int_rate','dti']:
        a=t.loc[t.charged_off.eq(1),c].dropna(); b=t.loc[t.charged_off.eq(0),c].dropna()
        r=welch(a,b); r.update(test=c,method='Welch t',units='percentage points',threshold=PRACTICAL[c],excluded=len(t)-len(a)-len(b)); results.append(r)
        q=t[c].quantile(.99)
        sensitivity[c]={'rule':'Pooled terminal-sample 99th percentile cap; sensitivity only', 'cap':q,'result':welch(a.clip(upper=q),b.clip(upper=q))}
    table=pd.crosstab(t.grade,t.loan_status).reindex(index=list('ABCDEFG'),columns=['Charged Off','Fully Paid'],fill_value=0)
    table.to_csv(ROOT/'outputs/tables/grade_outcome.csv')
    r=grade_test(table.values); r.update(test='grade',method='Chi-square independence',units='Cramers V',threshold=PRACTICAL['grade_cramers_v'],excluded=len(t)-int(table.values.sum())); results.append(r)
    terms=t.groupby('term').charged_off.agg(['sum','count']); terms.to_csv(ROOT/'outputs/tables/term_outcome.csv')
    r=proportions(int(terms.loc['60 months','sum']),int(terms.loc['60 months','count']),int(terms.loc['36 months','sum']),int(terms.loc['36 months','count']))
    r.update(test='term',method='Two-proportion z',units='proportion (60 minus 36 months)',threshold=PRACTICAL['term'],excluded=len(t)-int(terms['count'].sum())); results.append(r)
    for r,adjusted in zip(results,holm([r['p'] for r in results])):
        r['p_display']=p_text(r['p']); r['holm_p_display']=p_text(adjusted); r['holm_reject']=adjusted<.05
        r['decision']='Reject H0' if r['p']<.05 else 'Fail to reject H0'
        r['practical']='CI beyond positive threshold' if r['ci_low']>r['threshold'] else 'CI beyond negative threshold' if r['ci_high'] < -r['threshold'] else 'CI overlaps practical boundary or negligible region'
        # Keep machine-readable finite underflow information without falsely asserting an exact zero p-value.
        if r['p']==0:r['p']=None;r['p_underflow']=True
    dump(ROOT/'outputs/results.json',results); dump(ROOT/'outputs/sensitivity.json',sensitivity)
    flat=[{k:v for k,v in r.items() if not isinstance(v,list)} for r in results]; pd.DataFrame(flat).to_csv(ROOT/'outputs/tables/hypothesis_tests.csv',index=False)
    cohorts=t.assign(issue_year=t.issue_date.dt.year).groupby(['issue_year','term']).charged_off.agg(['sum','count','mean'])
    cohorts.to_csv(ROOT/'outputs/tables/cohort_term_rates.csv')
    # This compact cache contains aggregates only, so the ZIP does not expose row-level data.
    figures(d,t)
    import matplotlib.pyplot as plt
    m=pd.Series(audit['missing_counts']).sort_values(ascending=False).head(20)/len(d)*100
    fig,ax=plt.subplots(figsize=(8,6)); m.sort_values().plot.barh(ax=ax); ax.set(xlabel='Missing (%)',title='20 most incomplete source fields'); fig.tight_layout(); fig.savefig(ROOT/'figures/eda/missingness.png'); plt.close(fig)
    audit['issue_date_min']=str(d.issue_date.min()); audit['issue_date_max']=str(d.issue_date.max()); dump(ROOT/'outputs/dataset_audit.json',audit)
    summary=dict(completed_tests=len(results),elapsed_seconds=time.time()-started,raw_rows=len(d),terminal_rows=len(t),
        encoded_cells=encoded['cells'],source_file_unchanged=True,random_seed=558,mode='full CSV scan, compact aggregate output')
    dump(ROOT/'outputs/run_summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
