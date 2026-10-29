"""Build reader-friendly descriptive replacements from real source values."""
from pathlib import Path
from collections import Counter
import argparse,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--data');args=ap.parse_args()
cache=ROOT/'outputs/tables/explainer_plot_counts.json'
if args.data:
    purposes=Counter();income=np.zeros(50,dtype=int);amount=np.zeros(40,dtype=int)
    income_edges=np.linspace(0,20,51);amount_edges=np.linspace(0,40000,41)
    n_income=n_amount=0
    for d in pd.read_csv(args.data,usecols=['loan_amnt','annual_inc','purpose'],chunksize=100000):
        valid=d.loan_amnt.notna();purposes.update(d.loc[valid,'purpose'].fillna('Not recorded').value_counts().to_dict())
        inc=pd.to_numeric(d.loc[valid,'annual_inc'],errors='coerce').dropna();inc=inc[inc>=0]
        am=pd.to_numeric(d.loc[valid,'loan_amnt'],errors='coerce').dropna()
        income+=np.histogram(np.log1p(inc),income_edges)[0];amount+=np.histogram(am,amount_edges)[0]
        n_income+=len(inc);n_amount+=len(am)
    cache.write_text(json.dumps({'purpose_counts':dict(purposes),'income_edges':income_edges.tolist(),'income_counts':income.tolist(),'amount_edges':amount_edges.tolist(),'amount_counts':amount.tolist(),'n_income':n_income,'n_amount':n_amount},indent=2))
if not cache.exists():raise SystemExit('Supply --data PATH for the first run; later runs use saved aggregate counts.')
c=json.loads(cache.read_text());plt.rcParams.update({'font.size':11,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False})
purposes=pd.Series(c['purpose_counts']).sort_values()
fig,ax=plt.subplots(figsize=(8,4.5));ax.barh(purposes.index.str.replace('_',' '),purposes.values,color='#247b86')
ax.set(xlabel='Number of loans',title=f'Why did borrowers request loans? (n={int(purposes.sum()):,})');fig.tight_layout();fig.savefig(ROOT/'figures/eda/loan_purposes.png');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(10,4))
for ax,edges,counts,label,title in [(axes[0],c['income_edges'],c['income_counts'],'Natural logarithm of (1 + annual income in dollars)',f'Income on a compressed scale (n={c["n_income"]:,})'),(axes[1],c['amount_edges'],c['amount_counts'],'Requested loan amount (US dollars)',f'How much did borrowers request? (n={c["n_amount"]:,})')]:
    ax.stairs(counts,edges,fill=True,color='#247b86');ax.set(xlabel=label,ylabel='Number of loans',title=title,ylim=(0,None))
fig.tight_layout();fig.savefig(ROOT/'figures/eda/income_and_loan_amount.png');plt.close(fig)
r=json.loads((ROOT/'outputs/results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(9,4))
for ax,v,title in zip(axes,r[:2],['Average issued interest rate','Average debt-to-income ratio']):
    means=[v['mean_b'],v['mean_a']]; bars=ax.bar(['Fully Paid','Charged Off'],means,color=['#247b86','#b6762d'])
    for bar,value in zip(bars,means):ax.text(bar.get_x()+bar.get_width()/2,value+.35,f'{value:.2f}%',ha='center')
    ax.set(ylabel='Group mean (%)',title=title,ylim=(0,max(means)*1.22))
fig.suptitle('How do the two completed-outcome groups compare?');fig.tight_layout();fig.savefig(ROOT/'figures/inference/group_mean_comparison.png');plt.close(fig)
assert sum(c['income_counts'])==c['n_income'];assert sum(c['amount_counts'])==c['n_amount']
print('Three replacement figures generated; histogram totals reconcile with eligible source values.')
