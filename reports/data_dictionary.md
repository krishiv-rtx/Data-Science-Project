# Data dictionary and temporal audit

Source types are inferred by a full chunked scan; all source values are first loaded as strings for stable cross-chunk hashing, then selected numeric fields are parsed. Float64/int categorical analytical roles differ from the raw storage representation. Exact original download metadata and vintage dictionary remain unverified. These working descriptions combine supplied profile evidence and basic domain semantics; ambiguous unused fields are not guessed.

| Variable | Meaning | Units / type | Missing source rows | Use / caveat |
| --- | --- | --- | --- | --- |
| int_rate | Issued annual interest rate | percentage points / Continuous | 33 | Origination descriptor, not necessarily known at application |
| dti | Debt-to-income ratio | percentage points / Continuous | 1,744 | Exact historical denominator requires vintage documentation; do not assume all debts included |
| loan_amnt | Requested/listed loan principal | USD / Continuous monetary | 33 | Not a repayment amount |
| annual_inc | Reported annual income | USD/year / Continuous monetary | 37 | Self-report/verification limitations; zero and extreme values require interpretation |
| fico_range_low | Lower end of origination FICO band | score points / Discrete ordered | 33 | Not exact FICO; do not use last_fico fields as substitutes |
| revol_util | Revolving credit utilisation | percentage points / Continuous | 1,835 | Values above 100 may reflect source conventions |
| grade | Recorded credit grade | A-G / Ordinal category | 33 | Order A-G; no equal spacing assumption |
| term | Scheduled term | months / Category | 33 | Whitespace stripped; only 36/60 used for term test |
| home_ownership | Reported housing tenure | category / Nominal | 33 | Do not encode as a numeric quantity |
| verification_status | Income verification label | category / Nominal | 33 | Not proof of accuracy or absence of risk |
| purpose | Stated loan purpose | category / Nominal | 33 | Self-reported; no causal interpretation |
| application_type | Individual/joint application label | category / Nominal | 33 | Joint-specific missingness can be structural |
| loan_status | Observed repayment status | category / Nominal outcome | 33 | Fully Paid/Charged Off only for primary inference |
| issue_d | Issue month | calendar month / Date | 33 | Parsed using %b-%Y; monthly resolution |
| id | Loan identifier | none / Identifier | 0 | Used for integrity, never as a numeric feature |

## Derived variables

- `issue_date`: issue_d parsed with `%b-%Y`; failed parses become missing and are counted.
- `charged_off`: 1 iff loan_status is exactly Charged Off, 0 iff Fully Paid; undefined outside the terminal sample. This is an observed terminal outcome, not lifetime default risk for all loans.
- Grade and term tables: counts of unique loan records in each category by terminal outcome. Grade order A through G is maintained.
- One-hot columns: one column per observed category of grade, term, home_ownership, verification_status, purpose and application_type; no dropped reference level, because no regression is fitted. Each value is 0 or 1. Exact columns are in outputs/encoded_size.json.
- Numeric representation: six numeric columns preserved on original scales, with complete-case rows only. No scaling or imputation. There is no predictive model.
- `log1p(annual_inc)`: natural logarithm of 1 + income for nonnegative observed values, including zero. It is a descriptive chart only; no mean comparison uses this scale. Negative incomes are not logged.
<<<<<<< HEAD
- interquartile range (IQR) flags: below Q1-1.5*(Q3-Q1) or above Q3+1.5*(Q3-Q1), calculated per numeric field on nonmissing source values. No deletion follows a flag.
- Capped sensitivity values: min(x, pooled terminal 99th percentile); only sensitivity comparisons use them.

The complete 151-or-other-source-column inventory is outputs/tables/feature_audit.csv; its row count follows the actual file. Selected numeric/categorical variables appear in exploratory data analysis (EDA) or size auditing. Only int_rate, dti, grade, term and loan_status enter tests. No field is certified for application-time prediction. Identifiers and repayment-process variables are excluded from the encoded representation. ID uniqueness cannot establish borrower uniqueness.


## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
=======
- IQR flags: below Q1-1.5*(Q3-Q1) or above Q3+1.5*(Q3-Q1), calculated per numeric field on nonmissing source values. No deletion follows a flag.
- Capped sensitivity values: min(x, pooled terminal 99th percentile); only sensitivity comparisons use them.

The complete 151-or-other-source-column inventory is outputs/tables/feature_audit.csv; its row count follows the actual file. Selected numeric/categorical variables appear in EDA or size auditing. Only int_rate, dti, grade, term and loan_status enter tests. No field is certified for application-time prediction. Identifiers and repayment-process variables are excluded from the encoded representation. ID uniqueness cannot establish borrower uniqueness.
>>>>>>> origin/main
