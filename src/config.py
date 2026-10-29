from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 558
ALPHA = 0.05
NUMERIC = ['loan_amnt', 'int_rate', 'dti', 'annual_inc', 'fico_range_low', 'revol_util']
CATEGORICAL = ['grade', 'term', 'home_ownership', 'verification_status', 'purpose', 'application_type']
SELECTED = ['id', 'loan_status', 'issue_d'] + NUMERIC + CATEGORICAL
TERMINAL = ['Fully Paid', 'Charged Off']
# Analytical judgement, not industry standards; fixed before outcome comparisons.
PRACTICAL = {'int_rate': 1.0, 'dti': 2.0, 'term': 0.02, 'grade_cramers_v': 0.1}
