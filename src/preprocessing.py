import numpy as np
import pandas as pd
from .config import NUMERIC, CATEGORICAL, TERMINAL

def prepare(frame):
    d = frame.copy(); changes = {}
    for c in ['loan_status'] + CATEGORICAL:
        changes[c+'_whitespace'] = int((d[c].notna() & d[c].ne(d[c].str.strip())).sum())
        d[c] = d[c].str.strip()
    for c in NUMERIC:
        original = d[c]
        d[c] = pd.to_numeric(original.str.rstrip('%'), errors='coerce').astype(float)
        changes[c+'_parse_failures'] = int((original.notna() & d[c].isna()).sum())
    d['issue_date'] = pd.to_datetime(d.issue_d, format='%b-%Y', errors='coerce')
    changes['issue_date_parse_failures'] = int((d.issue_d.notna() & d.issue_date.isna()).sum())
    terminal = d[d.loan_status.isin(TERMINAL)].copy()
    terminal['charged_off'] = terminal.loan_status.eq('Charged Off').astype(int)
    changes.update(rows_before=len(d), terminal_rows=len(terminal), excluded_nonterminal=len(d)-len(terminal))
    return d, terminal, changes

def iqr_summary(series):
    s = series.dropna(); q1,q3 = s.quantile([.25,.75]); spread=q3-q1
    lower,upper=q1-1.5*spread,q3+1.5*spread
    flags=(s<lower)|(s>upper)
    return {'n':len(s),'q1':q1,'q3':q3,'lower':lower,'upper':upper,'flagged':int(flags.sum()),'percent':100*flags.mean()}

def encode(terminal):
    # No missing-value imputation: complete cases for this descriptive representation only.
    eligible=terminal[NUMERIC+CATEGORICAL].replace([np.inf,-np.inf],np.nan).dropna()
    matrix=pd.get_dummies(eligible, columns=CATEGORICAL, dtype='uint8')
    return {'rows_before':len(terminal),'columns_before':len(NUMERIC+CATEGORICAL),
        'rows':len(matrix),'columns':len(matrix.columns),'cells':int(matrix.size),
        'meets_3m':bool(matrix.size>=3_000_000),'excluded_missing':len(terminal)-len(matrix),
        'feature_names':list(matrix.columns),'memory_bytes':int(matrix.memory_usage(deep=True).sum())}
