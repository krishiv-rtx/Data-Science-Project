import unittest,tempfile
from pathlib import Path
import pandas as pd
from src.config import SELECTED
from src.data_loading import load_and_audit
from src.data_quality import extra_checks,clean_underflow

class AuditTests(unittest.TestCase):
    def test_nonloan_metadata_and_negative_dti(self):
        d=pd.DataFrame({'id':['1','2','3','4','Total amount funded in policy code 1: 100','Loans that do not meet the credit policy'],
            'loan_status':['Fully Paid','Fully Paid','Charged Off','Charged Off',None,None],
            'loan_amnt':[100,100,100,100,None,None],'dti':[1.,2.,3.,4.,None,None],
            'annual_inc':[10,10,10,10,None,None],'revol_util':[1,2,3,4,None,None]})
        audit={};flags=extra_checks(d,audit,write_output=False)
        self.assertEqual(audit['verified_nonloan_rows'],2)
        self.assertEqual(audit['loan_records'],4)
        self.assertEqual(flags['negative_dti'],0)
    def test_underflow_is_not_reported_as_zero(self):
        r=clean_underflow({'nested':{'p':0.0},'nonzero':{'p':.2}})
        self.assertIsNone(r['nested']['p']);self.assertIn('<',r['nested']['p_display'])
        self.assertEqual(r['nonzero']['p'],.2)
    def test_duplicate_detection_crosses_chunks(self):
        # Synthetic fixture is solely a software test, never empirical project evidence.
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'fixture.csv'
            d=pd.DataFrame([{c:'1' for c in SELECTED}]*3)
            d.loc[1,'id']='2';d.to_csv(p,index=False)
            _,a=load_and_audit(p,chunk_size=1)
            self.assertEqual(a['rows'],3)
            self.assertEqual(a['duplicate_rows'],1)
            self.assertEqual(a['duplicate_ids'],1)
            self.assertEqual(a['columns'],len(SELECTED))
