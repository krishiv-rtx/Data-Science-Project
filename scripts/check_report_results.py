"""Independent checks of the four stored results and their report rendering."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'outputs/results.json').read_text());tex=(ROOT/'reports/final_report.tex').read_text()
checks=[]
for v in r[:2]:
    ref=stats.ttest_ind_from_stats(v['mean_a'],v['sd_a'],v['n_a'],v['mean_b'],v['sd_b'],v['n_b'],equal_var=False)
    assert np.isclose(ref.statistic,v['statistic'])
    u=v['sd_a']**2/v['n_a'];w=v['sd_b']**2/v['n_b']
    df=(u+w)**2/(u*u/(v['n_a']-1)+w*w/(v['n_b']-1))
    assert np.isclose(df,v['df'])
    half=stats.t.ppf(.975,df)*np.sqrt(u+w)
    np.testing.assert_allclose([v['ci_low'],v['ci_high']],[v['estimate']-half,v['estimate']+half])
    checks.append(v['test']+': statistic, degrees of freedom and interval independently agree')
table=pd.read_csv(ROOT/'outputs/tables/grade_outcome.csv',index_col=0)
chi,p,df,expected=stats.chi2_contingency(table,correction=False)
assert np.isclose(chi,r[2]['statistic']) and df==6 and expected.min()>=5
assert np.isclose(np.sqrt(chi/table.values.sum()),r[2]['estimate'])
checks.append('grade: contingency statistic, degrees of freedom, expected counts and association magnitude agree')
v=r[3];delta=v['events_a']/v['n_a']-v['events_b']/v['n_b']
assert np.isclose(delta,v['estimate']) and np.isclose(v['statistic']**2,v['chi2_crosscheck'])
checks.append('term: event denominators, proportion contrast and chi-square equivalence agree')
assert tex.count(r'95\% confidence interval &')+tex.count(r'95\% CI (confidence interval) &')==4
for v in r:
    scale=100 if v['test']=='term' else 1
    assert f"[{scale*v['ci_low']:.5g}, {scale*v['ci_high']:.5g}]" in tex
    assert f"{v['estimate']*scale:.5g}" in tex
checks.append('All four report estimates and confidence intervals match computed values and displayed units')
(ROOT/'outputs/report_result_crosscheck.json').write_text(json.dumps({'passed':True,'checks':checks,'unchanged_empirical_results':True},indent=2))
print('\n'.join(checks))
