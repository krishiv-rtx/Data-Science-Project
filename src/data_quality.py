"""Targeted quality flags supplement the whole-schema missingness audit."""
import json
from .config import ROOT
from .statistical_tests import welch,p_text

def extra_checks(d,audit,write_output=True):
    footer=d.id.fillna('').str.strip().str.startswith('Total amount funded in policy code') & d.loan_status.isna() & d.loan_amnt.isna()
    separator=d.id.fillna('').str.strip().eq('Loans that do not meet the credit policy') & d.loan_status.isna() & d.loan_amnt.isna()
    audit['verified_footer_rows']=int(footer.sum())
    audit['verified_separator_rows']=int(separator.sum())
    audit['verified_nonloan_rows']=int((footer|separator).sum())
    audit['loan_records']=len(d)-int((footer|separator).sum())
    audit.pop('nonfooter_records',None)
    checks={'verified_footer_rows':int(footer.sum()),'verified_separator_rows':int(separator.sum()),'negative_dti':int((d.dti<0).sum()),
        'dti_equal_999':int(d.dti.eq(999).sum()),'revol_util_above_100':int((d.revol_util>100).sum()),
        'negative_income':int((d.annual_inc<0).sum()),'zero_income':int(d.annual_inc.eq(0).sum()),
        'negative_loan_amount':int((d.loan_amnt<0).sum())}
    t=d[d.loan_status.isin(['Fully Paid','Charged Off'])]
    checks['terminal_negative_dti']=int((t.dti<0).sum())
    a=t.loc[t.loan_status.eq('Charged Off') & t.dti.ge(0),'dti'].dropna()
    b=t.loc[t.loan_status.eq('Fully Paid') & t.dti.ge(0),'dti'].dropna()
    r=welch(a,b);r.pop('p');r.pop('statistic');r.pop('df')
    checks['dti_nonnegative_sensitivity']={'rule':'Exclude negative DTI only; primary remains unchanged; descriptive sensitivity, not an additional declared test','summary':r}
    if write_output:(ROOT/'outputs/quality_flags.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    return checks

def clean_underflow(obj):
    if isinstance(obj,dict):
        if obj.get('p')==0:
            obj['p']=None;obj['p_display']=p_text(0);obj['p_underflow']=True
        for v in obj.values():clean_underflow(v)
    elif isinstance(obj,list):
        for v in obj:clean_underflow(v)
    return obj
