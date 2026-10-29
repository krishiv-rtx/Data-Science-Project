"""Conservative time-availability classification, not guessed exact definitions."""
from .config import NUMERIC,CATEGORICAL

def classify(name):
    if name=='loan_status':return 'outcome','After origination','Exclude from features; defines terminal groups'
    if name in ['id','member_id','url','zip_code','emp_title','desc','title']:
        return 'identifier/text','Not a quantitative measure','Exclude; privacy, cardinality, or uncertain meaning'
    if name.startswith(('last_','next_','out_prncp','total_pymnt','total_rec_','hardship','settlement','debt_settlement','recoveries','collection_recovery','payment_plan','orig_projected','deferral')):
        return 'repayment process','After origination or uncertain future information','Exclude from origination features'
    if name in NUMERIC+CATEGORICAL:
        return 'selected descriptor','Origination candidate; exact vintage definition caveat','Use descriptively; no application-time predictive claim'
    return 'unselected','Not independently verified','Exclude from selected representation pending authoritative dictionary'
