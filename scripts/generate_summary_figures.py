"""Regenerate status/category/effect figures from computed aggregate outputs."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'outputs/dataset_audit.json').read_text());results=json.loads((ROOT/'outputs/results.json').read_text())
plt.rcParams.update({'font.size':10,'figure.dpi':150,'axes.spines.top':False,'axes.spines.right':False})
counts=pd.Series(a['status_counts']).sort_values()
labels={'Does not meet the credit policy. Status:Fully Paid':'Outside policy: Fully Paid','Does not meet the credit policy. Status:Charged Off':'Outside policy: Charged Off','<missing>':'Non-loan metadata'}
fig,ax=plt.subplots(figsize=(8,4.6));ax.barh([labels.get(k,k) for k in counts.index],counts.values,color='#247b86')
for y,n in enumerate(counts.values):ax.text(n+10000,y,f'{n:,}',va='center',fontsize=8)
ax.set(xlabel='Records',title=f'Source statuses (n={a["rows"]:,}; includes 33 non-loan rows)',xlim=(0,max(counts)*1.2));fig.tight_layout();fig.savefig(ROOT/'figures/eda/status.png');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(10,4))
grade=pd.read_csv(ROOT/'outputs/tables/grade_outcome.csv',index_col=0)
term=pd.read_csv(ROOT/'outputs/tables/term_outcome.csv',index_col=0)
for ax,frame,event,total,title in [(axes[0],grade,'Charged Off',grade.sum(axis=1),'Grade'),(axes[1],term,'sum',term['count'],'Term')]:
    ax.bar(range(len(frame)),frame[event]/total*100,color='#247b86')
    ax.set_xticks(range(len(frame)),[f'{k}\nn={n:,}' for k,n in zip(frame.index,total)],fontsize=7)
    ax.set(ylabel='Observed charge-off (%)',title=title+' among terminal outcomes')
fig.tight_layout();fig.savefig(ROOT/'figures/eda/category_rates.png');plt.close(fig)
fig,axes=plt.subplots(2,2,figsize=(10,5))
for ax,r in zip(axes.flat,results):
    factor=100 if r['test']=='term' else 1
    ax.errorbar(r['estimate']*factor,0,xerr=[[(r['estimate']-r['ci_low'])*factor],[(r['ci_high']-r['estimate'])*factor]],fmt='o',capsize=6,color='#247b86')
    ax.axvline(r['threshold']*factor,color='#b6762d',linestyle='--',label='Practical threshold')
    ax.axvline(0,color='gray',linewidth=.7);ax.set_yticks([])
    ax.set(title=r['test']+' estimate and 95% CI',xlabel='Percentage points' if r['test']!='grade' else "Cramer's V")
    ax.legend(fontsize=8)
fig.tight_layout();fig.savefig(ROOT/'figures/inference/effect_intervals.png');plt.close(fig)
print('Aggregate status, category and effect-interval figures regenerated.')
