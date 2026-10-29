import unittest
import numpy as np
from scipy import stats
from src.statistical_tests import welch,proportions,grade_test,holm

class StatisticalTests(unittest.TestCase):
    def test_welch_matches_scipy_and_direction(self):
        a=[1,4,7,10,20]; b=[1,2,3,4,5,6]
        r=welch(a,b); ref=stats.ttest_ind(a,b,equal_var=False)
        self.assertAlmostEqual(r['statistic'],ref.statistic)
        self.assertAlmostEqual(r['p'],ref.pvalue)
        self.assertAlmostEqual(r['df'],ref.df)
        reverse=welch(b,a)
        self.assertAlmostEqual(r['ci_low'],-reverse['ci_high'])
    def test_z_squared_equals_chi_square(self):
        r=proportions(30,100,20,120)
        self.assertAlmostEqual(r['statistic']**2,r['chi2_crosscheck'])
        self.assertGreater(r['ci_high'],r['estimate'])
        self.assertLess(r['ci_low'],r['estimate'])
    def test_invalid_counts(self):
        with self.assertRaises(ValueError):proportions(11,10,5,20)
        with self.assertRaises(ValueError):proportions(0,10,0,10)
    def test_grade_df_and_reproducible_interval(self):
        table=[[30,70],[50,50],[70,30]]
        a=grade_test(table,bootstrap=50);b=grade_test(table,bootstrap=50)
        self.assertEqual(a['df'],2)
        self.assertEqual(a['ci_low'],b['ci_low'])
        self.assertTrue(0 <= a['estimate'] <= 1)
    def test_holm_reference(self):
        np.testing.assert_allclose(holm([.01,.04,.03]),[.03,.06,.06])

if __name__=='__main__':unittest.main()
