import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from .config import ROOT, NUMERIC

def figures(d,t):
    out=ROOT/'figures/eda'; out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'figure.dpi':140,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,4)); d.loan_status.fillna('Missing').value_counts().plot.barh(ax=ax,color='#247b86')
    ax.set(xlabel='Loans',title=f'Observed status (all {len(d):,} CSV rows)'); fig.tight_layout(); fig.savefig(out/'status.png'); plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    for c,ax in zip(['int_rate','dti'],axes):
        groups=[t.loc[t.loan_status.eq(s),c].dropna().to_numpy() for s in ['Fully Paid','Charged Off']]
        ax.boxplot(groups,tick_labels=['Fully Paid','Charged Off'],showfliers=False)
        ax.set(title=c+' by terminal outcome',ylabel='Percentage points')
    fig.suptitle('Boxplot fliers hidden for readability; all values retained in tests',fontsize=10)
    fig.tight_layout(); fig.savefig(out/'outcome_boxplots.png'); plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    for col,ax in zip(['grade','term'],axes):
        g=t.groupby(col).charged_off.agg(['mean','size']).sort_index()
        ax.bar(g.index.astype(str),100*g['mean'],color='#247b86'); ax.set(ylabel='Observed charge-off (%)',title=col+' among terminal outcomes')
    fig.tight_layout(); fig.savefig(out/'category_rates.png'); plt.close(fig)
    income=d.annual_inc.dropna(); income=income[income>=0]
    fig,axes=plt.subplots(1,2,figsize=(9,3.5))
    axes[0].hist(income,bins=60,color='#247b86'); axes[0].set(xlabel='Annual income (USD), full range',ylabel='Loans')
    axes[1].hist(np.log1p(income),bins=60,color='#b6762d'); axes[1].set(xlabel='log(1 + annual income)',ylabel='Loans')
    fig.suptitle(f'Income scale sensitivity (n={len(income):,}); no distributional normality claimed')
    fig.tight_layout(); fig.savefig(out/'income_transform.png'); plt.close(fig)
    sample=t[['annual_inc','dti']].dropna().sample(n=min(5000,len(t[['annual_inc','dti']].dropna())),random_state=558)
    fig,ax=plt.subplots(figsize=(6,4)); ax.scatter(sample.annual_inc,sample.dti,s=5,alpha=.2)
    ax.set(xlabel='Annual income (USD)',ylabel='DTI (percentage points)',title=f'Seeded descriptive scatter (n={len(sample):,})')
    fig.tight_layout(); fig.savefig(out/'income_dti.png'); plt.close(fig)
