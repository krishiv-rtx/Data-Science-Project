import unittest
import pandas as pd
from src.preprocessing import prepare,encode,iqr_summary
from src.config import NUMERIC,CATEGORICAL

class PreprocessingTests(unittest.TestCase):
    def example(self):
        d={c:['1','2','3'] for c in NUMERIC}
        d.update({c:['A','B','A'] for c in CATEGORICAL})
        d.update(id=['1','2','3'],loan_status=[' Fully Paid ','Charged Off','Current'],issue_d=['Jan-2015']*3)
        return pd.DataFrame(d,dtype='string')
    def test_outcomes_are_not_imputed(self):
        d,t,change=prepare(self.example())
        self.assertEqual(len(t),2);self.assertEqual(list(t.charged_off),[0,1])
        self.assertEqual(change['excluded_nonterminal'],1)
    def test_encoded_size_real_matrix(self):
        _,t,_=prepare(self.example());r=encode(t)
        self.assertEqual(r['cells'],r['rows']*r['columns'])
        self.assertNotIn('id',r['feature_names']);self.assertNotIn('charged_off',r['feature_names'])
    def test_iqr_flags_dont_remove(self):
        x=pd.Series([1,2,3,4,100]);r=iqr_summary(x)
        self.assertEqual(r['flagged'],1);self.assertEqual(len(x),5)
