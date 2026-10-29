"""Refresh targeted flags without repeating the full 151-column audit."""
from pathlib import Path
import sys,argparse,json
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.config import ROOT
from src.data_quality import extra_checks,clean_underflow
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);args=ap.parse_args()
columns=['id','loan_status','loan_amnt','dti','annual_inc','revol_util']
d=pd.read_csv(args.data,usecols=columns,dtype={'id':'string','loan_status':'string'})
a=json.loads((ROOT/'outputs/dataset_audit.json').read_text())
checks=extra_checks(d,a)
(ROOT/'outputs/dataset_audit.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
p=ROOT/'outputs/sensitivity.json';p.write_text(json.dumps(clean_underflow(json.loads(p.read_text())),indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
