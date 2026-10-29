"""Create three useful, executable notebooks; no row-level data is embedded."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
intro="""from pathlib import Path
import json
import pandas as pd
root = Path.cwd()
if not (root / 'outputs').exists(): root = root.parent
assert (root / 'outputs/results.json').exists(), 'Run scripts/run_all.py first'
def read(name): return json.loads((root / 'outputs' / name).read_text(encoding='utf-8'))
"""
def md(text):return dict(cell_type='markdown',metadata={},source=text.splitlines(keepends=True))
def code(text):return dict(cell_type='code',metadata={},source=text.splitlines(keepends=True),execution_count=None,outputs=[])
def save(name,cells):
    for i,cell in enumerate(cells):cell['id']=name[:2]+'-'+str(i).zfill(3)
<<<<<<< HEAD
    for cell in cells:
        if cell['cell_type']=='markdown':
            text=''.join(cell['source']).replace('../figures/eda/income_transform.png','../figures/eda/income_and_loan_amount.png').replace('../figures/eda/missingness.png','../figures/eda/loan_purposes.png')
            text=text.replace('![Income scales]','![Logged income and requested loan amounts]').replace('![Missingness]','![Stated borrowing purposes]').replace('The figure displays only the 20 most incomplete fields; the CSV table contains all fields.','The purpose bars compare common reasons for borrowing. Missingness remains available in the complete audit table.')
            cell['source']=text.splitlines(keepends=True)
=======
>>>>>>> origin/main
    p=ROOT/'notebooks'/name;p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(dict(cells=cells,metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3.14'}},nbformat=4,nbformat_minor=5),indent=2),encoding='utf-8')
save('01_data_audit.ipynb',[
    md('# 1. Data audit\nNullPointer / CSE558. Run the full chunked CSV analysis with `python scripts/run_all.py --data PATH` first. This notebook inspects its actual saved audit without loading millions of raw rows into notebook output.'),
    code(intro),
    code("a=read('dataset_audit.json')\nprint({k:a[k] for k in ['rows','columns','file_bytes','file_sha256','duplicate_rows','duplicate_ids','issue_date_min','issue_date_max']})\nassert sum(a['status_counts'].values()) == a['rows']\nprint(pd.Series(a['status_counts']).to_string())"),
    md('## Profile discrepancy\nThe profile was not a substitute for the full CSV. Its 314,168 rows and 162 columns differ from the actual audit. Derived dates may explain its column inventory, but that profiling run is not independently reconstructible.'),
    code("print(pd.read_csv(root/'outputs/tables/profile_comparison.csv').to_string(index=False))\nm=pd.read_csv(root/'outputs/tables/missingness.csv')\nassert len(m)==a['columns']\nprint(m.sort_values('missing_count',ascending=False).head(20).to_string(index=False))"),
    md('## Interpretation\nMissingness may be structural for joint applications and hardship/settlement programs. ID uniqueness is not borrower independence. The raw file is read-only; source size/mtime are checked and its SHA-256 is recorded. See the full feature audit before using variables as origination predictors.')])
save('02_data_preparation_and_eda.ipynb',[
    md('# 2. Preparation and EDA\nTest-specific complete cases differ from the encoded-size representation. No imputation and no automatic outlier deletion.'),code(intro),
    code("a=read('dataset_audit.json'); c=read('preparation.json'); e=read('encoded_size.json')\nassert c['rows_before']==c['terminal_rows']+c['excluded_nonterminal']\nassert e['rows_before']==e['rows']+e['excluded_missing']\nassert e['cells']==e['rows']*e['columns']\nprint(json.dumps(c,indent=2))\nprint(f\"Actual size: {e['rows']:,} x {e['columns']} = {e['cells']:,}\")\nprint('Features:',e['feature_names'])"),
    md('![Status](../figures/eda/status.png)\nAll source statuses are visible; Current is not relabelled as Fully Paid.\n\n![Boxplots](../figures/eda/outcome_boxplots.png)\nFliers are suppressed for readability only; full values enter the tests.'),
    code("print(pd.read_csv(root/'outputs/tables/outliers.csv').to_string(index=False))\nprint(pd.read_csv(root/'outputs/tables/numeric_summary.csv').to_string(index=False))"),
    md('![Income scales](../figures/eda/income_transform.png)\nLog1p changes visual scale and permits zero income; it does not prove normality.\n\n![Missingness](../figures/eda/missingness.png)\nThe figure displays only the 20 most incomplete fields; the CSV table contains all fields.'),
    code("print(pd.read_csv(root/'outputs/tables/grade_outcome.csv').to_string(index=False))\nprint(pd.read_csv(root/'outputs/tables/term_outcome.csv').to_string(index=False))"),
    md('![Category proportions](../figures/eda/category_rates.png)\nObserved terminal proportions depend on maturity and selection.\n\n![Scatter](../figures/eda/income_dti.png)\nThe seeded scatter sample is descriptive; all eligible rows are used in hypothesis tests.')])
save('03_statistical_inference.ipynb',[
    md('# 3. Statistical inference\nRead reports/analysis_plan.md first. Four alpha=.05 tests; thresholds were fixed before comparing groups. Computations below independently verify statistics from actual saved sufficient summaries.'),code(intro),
    code("from scipy import stats\nimport numpy as np\nr=read('results.json')\nfor v in r[:2]:\n    ref=stats.ttest_ind_from_stats(v['mean_a'],v['sd_a'],v['n_a'],v['mean_b'],v['sd_b'],v['n_b'],equal_var=False)\n    assert np.isclose(ref.statistic,v['statistic'])\n    assert v['ci_low'] < v['estimate'] < v['ci_high']\n    print(v['test'], 'difference:',v['estimate'], '95% CI:',[v['ci_low'],v['ci_high']], 'p:',v['p_display'])"),
    code("table=pd.read_csv(root/'outputs/tables/grade_outcome.csv',index_col=0)\nchi,p,df,expected=stats.chi2_contingency(table.values,correction=False)\nassert np.isclose(chi,r[2]['statistic']) and df==r[2]['df']\nassert expected.min()>=5\nprint('Grade chi-square:',chi,'df:',df,'Cramers V:',r[2]['estimate'],'CI:',[r[2]['ci_low'],r[2]['ci_high']])"),
    code("term=r[3]\nassert np.isclose(term['statistic']**2,term['chi2_crosscheck'])\nprint('60 months:',term['events_a'],'/',term['n_a'],'=',term['proportion_a'])\nprint('36 months:',term['events_b'],'/',term['n_b'],'=',term['proportion_b'])\nprint('Difference in percentage points:',100*term['estimate'])\nprint('95% CI in percentage points:',[100*term['ci_low'],100*term['ci_high']])"),
    code("for v in r:\n    print(v['test'],v['decision'],'Holm p:',v['holm_p_display'],'Threshold:',v['threshold'],v['units'],'Practical:',v['practical'])\ns=read('sensitivity.json')\nfor key,v in s.items():\n    print(key,'capped sensitivity difference:',v['result']['estimate'],'CI:',[v['result']['ci_low'],v['result']['ci_high']])"),
    md('## Defensible conclusion\nCompare intervals with practical thresholds, not just zero. Underflowed p-values are reported as bounds, never as zero. Holm-adjusted decisions do not remove selection, censoring, dependence or confounding. Capped sensitivity changes the estimand. The chi-square cross-check for term is not a fifth test. Bootstrap uncertainty for Cramer\'s V assumes IID observations. See the technical report for formulas and alternative tests.')])
print('Three notebooks created.')
