# Attribute guide in everyday language

## Attributes used in this project

| Attribute | Plain meaning | What it signifies |
| --- | --- | --- |
| id | Loan identifier | Tracks a loan; has no numerical risk interpretation. |
| loan_status | Recorded loan outcome | Defines Fully Paid and Charged Off groups; Current is unresolved. |
| issue_d | Loan issue month | Shows loan vintage and helps explain maturity differences. |
| loan_amnt | Requested loan amount, in dollars | Shows the size of the loan, not the amount repaid. |
| int_rate | Issued annual interest rate, in percent | The price charged for borrowing; tested between outcome groups. |
| dti | Debt-to-income ratio, in percent | A debt-burden measure; higher means more debt relative to income. |
| annual_inc | Reported annual income, dollars per year | Borrower income scale; zero/extreme values need context. |
| fico_range_low | Lower end of the origination credit-score band | An approximate credit-score range endpoint, not the exact score. |
| revol_util | Revolving credit utilisation, in percent | How much of available revolving credit is used; unusually large values need review. |
| grade | Recorded loan grade, A through G | An ordered underwriting label, not an equally spaced number. |
| term | Scheduled loan duration, in months | The comparison uses 36-month and 60-month loans. |
| home_ownership | Reported housing situation | For example, rent, mortgage or own; a category, not wealth itself. |
| verification_status | Recorded income-verification category | Describes verification status; does not guarantee truthful income. |
| purpose | Stated reason for borrowing | For example, debt consolidation; self-reported category. |
| application_type | Individual or joint application | Helps interpret why joint-applicant fields may be missing. |
| charged_off | Derived 1 for Charged Off, 0 for Fully Paid | Defined only in the selected terminal-outcome sample. |

## Complete source inventory

All source fields are listed below with their observed missing counts and analytical decision. For unused fields without a verified historical definition, the expanded name is a reading aid only; it must not be presented as a certified definition. See the detailed selected-attribute table above for the variables actually used.

| Source field | Meaning / reading aid | Missing source records | Use and caution |
| --- | --- | --- | --- |
| id | Loan identifier; Tracks a loan; has no numerical risk interpretation. | 0 | Exclude; privacy, cardinality, or uncertain meaning |
| member_id | member id (name-based reading aid; exact vintage definition unverified) | 2260701 | Exclude; privacy, cardinality, or uncertain meaning |
| loan_amnt | Requested loan amount, in dollars; Shows the size of the loan, not the amount repaid. | 33 | Use descriptively; no application-time predictive claim |
| funded_amnt | funded amount (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| funded_amnt_inv | funded amount investor (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| term | Scheduled loan duration, in months; The comparison uses 36-month and 60-month loans. | 33 | Use descriptively; no application-time predictive claim |
| int_rate | Issued annual interest rate, in percent; The price charged for borrowing; tested between outcome groups. | 33 | Use descriptively; no application-time predictive claim |
| installment | installment (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| grade | Recorded loan grade, A through G; An ordered underwriting label, not an equally spaced number. | 33 | Use descriptively; no application-time predictive claim |
| sub_grade | sub grade (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| emp_title | employment title (name-based reading aid; exact vintage definition unverified) | 167002 | Exclude; privacy, cardinality, or uncertain meaning |
| emp_length | employment length (name-based reading aid; exact vintage definition unverified) | 146940 | Exclude from selected representation pending authoritative dictionary |
| home_ownership | Reported housing situation; For example, rent, mortgage or own; a category, not wealth itself. | 33 | Use descriptively; no application-time predictive claim |
| annual_inc | Reported annual income, dollars per year; Borrower income scale; zero/extreme values need context. | 37 | Use descriptively; no application-time predictive claim |
| verification_status | Recorded income-verification category; Describes verification status; does not guarantee truthful income. | 33 | Use descriptively; no application-time predictive claim |
| issue_d | Loan issue month; Shows loan vintage and helps explain maturity differences. | 33 | Exclude from selected representation pending authoritative dictionary |
| loan_status | Recorded loan outcome; Defines Fully Paid and Charged Off groups; Current is unresolved. | 33 | Exclude from features; defines terminal groups |
| pymnt_plan | payment plan (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| url | url (name-based reading aid; exact vintage definition unverified) | 33 | Exclude; privacy, cardinality, or uncertain meaning |
| desc | desc (name-based reading aid; exact vintage definition unverified) | 2134636 | Exclude; privacy, cardinality, or uncertain meaning |
| purpose | Stated reason for borrowing; For example, debt consolidation; self-reported category. | 33 | Use descriptively; no application-time predictive claim |
| title | title (name-based reading aid; exact vintage definition unverified) | 23359 | Exclude; privacy, cardinality, or uncertain meaning |
| zip_code | zip code (name-based reading aid; exact vintage definition unverified) | 34 | Exclude; privacy, cardinality, or uncertain meaning |
| addr_state | addr state (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| dti | Debt-to-income ratio, in percent; A debt-burden measure; higher means more debt relative to income. | 1744 | Use descriptively; no application-time predictive claim |
| delinq_2yrs | delinquency 2yrs (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| earliest_cr_line | earliest cr line (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| fico_range_low | Lower end of the origination credit-score band; An approximate credit-score range endpoint, not the exact score. | 33 | Use descriptively; no application-time predictive claim |
| fico_range_high | credit score range high (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| inq_last_6mths | credit inquiries last 6mths (name-based reading aid; exact vintage definition unverified) | 63 | Exclude from selected representation pending authoritative dictionary |
| mths_since_last_delinq | months since last delinquency (name-based reading aid; exact vintage definition unverified) | 1158535 | Exclude from selected representation pending authoritative dictionary |
| mths_since_last_record | months since last record (name-based reading aid; exact vintage definition unverified) | 1901545 | Exclude from selected representation pending authoritative dictionary |
| open_acc | open account (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| pub_rec | pub received (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| revol_bal | revolving credit balance (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| revol_util | Revolving credit utilisation, in percent; How much of available revolving credit is used; unusually large values need review. | 1835 | Use descriptively; no application-time predictive claim |
| total_acc | total account (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| initial_list_status | initial list status (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| out_prncp | out principal (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| out_prncp_inv | out principal investor (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| total_pymnt | total payment (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| total_pymnt_inv | total payment investor (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| total_rec_prncp | total received principal (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| total_rec_int | total received interest (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| total_rec_late_fee | total received late fee (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| recoveries | recoveries (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| collection_recovery_fee | collection recovery fee (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| last_pymnt_d | last payment date (name-based reading aid; exact vintage definition unverified) | 2460 | Exclude from origination features |
| last_pymnt_amnt | last payment amount (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| next_pymnt_d | next payment date (name-based reading aid; exact vintage definition unverified) | 1345343 | Exclude from origination features |
| last_credit_pull_d | last credit pull date (name-based reading aid; exact vintage definition unverified) | 105 | Exclude from origination features |
| last_fico_range_high | last credit score range high (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| last_fico_range_low | last credit score range low (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| collections_12_mths_ex_med | collections 12 months ex med (name-based reading aid; exact vintage definition unverified) | 178 | Exclude from selected representation pending authoritative dictionary |
| mths_since_last_major_derog | months since last major derogatory credit event (name-based reading aid; exact vintage definition unverified) | 1679926 | Exclude from selected representation pending authoritative dictionary |
| policy_code | policy code (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| application_type | Individual or joint application; Helps interpret why joint-applicant fields may be missing. | 33 | Use descriptively; no application-time predictive claim |
| annual_inc_joint | annual income joint (name-based reading aid; exact vintage definition unverified) | 2139991 | Exclude from selected representation pending authoritative dictionary |
| dti_joint | dti joint (name-based reading aid; exact vintage definition unverified) | 2139995 | Exclude from selected representation pending authoritative dictionary |
| verification_status_joint | verification status joint (name-based reading aid; exact vintage definition unverified) | 2144971 | Exclude from selected representation pending authoritative dictionary |
| acc_now_delinq | account now delinquency (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| tot_coll_amt | total collection amount (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| tot_cur_bal | total current balance (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| open_acc_6m | open account 6m (name-based reading aid; exact vintage definition unverified) | 866163 | Exclude from selected representation pending authoritative dictionary |
| open_act_il | open act installment loan (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| open_il_12m | open installment loan 12m (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| open_il_24m | open installment loan 24m (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| mths_since_rcnt_il | months since recent installment loan (name-based reading aid; exact vintage definition unverified) | 909957 | Exclude from selected representation pending authoritative dictionary |
| total_bal_il | total balance installment loan (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| il_util | installment loan utilisation (name-based reading aid; exact vintage definition unverified) | 1068883 | Exclude from selected representation pending authoritative dictionary |
| open_rv_12m | open rv 12m (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| open_rv_24m | open rv 24m (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| max_bal_bc | max balance bankcard (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| all_util | all utilisation (name-based reading aid; exact vintage definition unverified) | 866381 | Exclude from selected representation pending authoritative dictionary |
| total_rev_hi_lim | total rev high limit (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| inq_fi | credit inquiries fi (name-based reading aid; exact vintage definition unverified) | 866162 | Exclude from selected representation pending authoritative dictionary |
| total_cu_tl | total cu trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 866163 | Exclude from selected representation pending authoritative dictionary |
| inq_last_12m | credit inquiries last 12m (name-based reading aid; exact vintage definition unverified) | 866163 | Exclude from selected representation pending authoritative dictionary |
| acc_open_past_24mths | account open past 24mths (name-based reading aid; exact vintage definition unverified) | 50063 | Exclude from selected representation pending authoritative dictionary |
| avg_cur_bal | avg current balance (name-based reading aid; exact vintage definition unverified) | 70379 | Exclude from selected representation pending authoritative dictionary |
| bc_open_to_buy | bankcard open to buy (name-based reading aid; exact vintage definition unverified) | 74968 | Exclude from selected representation pending authoritative dictionary |
| bc_util | bankcard utilisation (name-based reading aid; exact vintage definition unverified) | 76104 | Exclude from selected representation pending authoritative dictionary |
| chargeoff_within_12_mths | chargeoff within 12 months (name-based reading aid; exact vintage definition unverified) | 178 | Exclude from selected representation pending authoritative dictionary |
| delinq_amnt | delinquency amount (name-based reading aid; exact vintage definition unverified) | 62 | Exclude from selected representation pending authoritative dictionary |
| mo_sin_old_il_acct | months sin old installment loan acct (name-based reading aid; exact vintage definition unverified) | 139104 | Exclude from selected representation pending authoritative dictionary |
| mo_sin_old_rev_tl_op | months sin old rev trade line (credit account) opened (name-based reading aid; exact vintage definition unverified) | 70310 | Exclude from selected representation pending authoritative dictionary |
| mo_sin_rcnt_rev_tl_op | months sin recent rev trade line (credit account) opened (name-based reading aid; exact vintage definition unverified) | 70310 | Exclude from selected representation pending authoritative dictionary |
| mo_sin_rcnt_tl | months sin recent trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| mort_acc | mort account (name-based reading aid; exact vintage definition unverified) | 50063 | Exclude from selected representation pending authoritative dictionary |
| mths_since_recent_bc | months since recent bankcard (name-based reading aid; exact vintage definition unverified) | 73445 | Exclude from selected representation pending authoritative dictionary |
| mths_since_recent_bc_dlq | months since recent bankcard delinquency (name-based reading aid; exact vintage definition unverified) | 1741000 | Exclude from selected representation pending authoritative dictionary |
| mths_since_recent_inq | months since recent credit inquiries (name-based reading aid; exact vintage definition unverified) | 295468 | Exclude from selected representation pending authoritative dictionary |
| mths_since_recent_revol_delinq | months since recent revolving credit delinquency (name-based reading aid; exact vintage definition unverified) | 1520342 | Exclude from selected representation pending authoritative dictionary |
| num_accts_ever_120_pd | number accounts ever 120 pd (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_actv_bc_tl | number actv bankcard trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_actv_rev_tl | number actv rev trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_bc_sats | number bankcard sats (name-based reading aid; exact vintage definition unverified) | 58623 | Exclude from selected representation pending authoritative dictionary |
| num_bc_tl | number bankcard trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_il_tl | number installment loan trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_op_rev_tl | number opened rev trade line (credit account) (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_rev_accts | number rev accounts (name-based reading aid; exact vintage definition unverified) | 70310 | Exclude from selected representation pending authoritative dictionary |
| num_rev_tl_bal_gt_0 | number rev trade line (credit account) balance gt 0 (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_sats | number sats (name-based reading aid; exact vintage definition unverified) | 58623 | Exclude from selected representation pending authoritative dictionary |
| num_tl_120dpd_2m | number trade line (credit account) 120dpd 2m (name-based reading aid; exact vintage definition unverified) | 153690 | Exclude from selected representation pending authoritative dictionary |
| num_tl_30dpd | number trade line (credit account) 30dpd (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_tl_90g_dpd_24m | number trade line (credit account) 90g days past due 24m (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| num_tl_op_past_12m | number trade line (credit account) opened past 12m (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| pct_tl_nvr_dlq | percentage trade line (credit account) nvr delinquency (name-based reading aid; exact vintage definition unverified) | 70464 | Exclude from selected representation pending authoritative dictionary |
| percent_bc_gt_75 | percent bankcard gt 75 (name-based reading aid; exact vintage definition unverified) | 75412 | Exclude from selected representation pending authoritative dictionary |
| pub_rec_bankruptcies | pub received bankruptcies (name-based reading aid; exact vintage definition unverified) | 1398 | Exclude from selected representation pending authoritative dictionary |
| tax_liens | tax liens (name-based reading aid; exact vintage definition unverified) | 138 | Exclude from selected representation pending authoritative dictionary |
| tot_hi_cred_lim | total high cred limit (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| total_bal_ex_mort | total balance ex mort (name-based reading aid; exact vintage definition unverified) | 50063 | Exclude from selected representation pending authoritative dictionary |
| total_bc_limit | total bankcard limit (name-based reading aid; exact vintage definition unverified) | 50063 | Exclude from selected representation pending authoritative dictionary |
| total_il_high_credit_limit | total installment loan high credit limit (name-based reading aid; exact vintage definition unverified) | 70309 | Exclude from selected representation pending authoritative dictionary |
| revol_bal_joint | revolving credit balance joint (name-based reading aid; exact vintage definition unverified) | 2152681 | Exclude from selected representation pending authoritative dictionary |
| sec_app_fico_range_low | secondary applicant credit score range low (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_fico_range_high | secondary applicant credit score range high (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_earliest_cr_line | secondary applicant earliest cr line (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_inq_last_6mths | secondary applicant credit inquiries last 6mths (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_mort_acc | secondary applicant mort account (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_open_acc | secondary applicant open account (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_revol_util | secondary applicant revolving credit utilisation (name-based reading aid; exact vintage definition unverified) | 2154517 | Exclude from selected representation pending authoritative dictionary |
| sec_app_open_act_il | secondary applicant open act installment loan (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_num_rev_accts | secondary applicant number rev accounts (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_chargeoff_within_12_mths | secondary applicant chargeoff within 12 months (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_collections_12_mths_ex_med | secondary applicant collections 12 months ex med (name-based reading aid; exact vintage definition unverified) | 2152680 | Exclude from selected representation pending authoritative dictionary |
| sec_app_mths_since_last_major_derog | secondary applicant months since last major derogatory credit event (name-based reading aid; exact vintage definition unverified) | 2224759 | Exclude from selected representation pending authoritative dictionary |
| hardship_flag | hardship flag (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| hardship_type | hardship type (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_reason | hardship reason (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_status | hardship status (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| deferral_term | deferral term (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_amount | hardship amount (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_start_date | hardship start date (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_end_date | hardship end date (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| payment_plan_start_date | payment plan start date (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_length | hardship length (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_dpd | hardship days past due (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_loan_status | hardship loan status (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| orig_projected_additional_accrued_interest | orig projected additional accrued interest (name-based reading aid; exact vintage definition unverified) | 2252050 | Exclude from origination features |
| hardship_payoff_balance_amount | hardship payoff balance amount (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| hardship_last_payment_amount | hardship last payment amount (name-based reading aid; exact vintage definition unverified) | 2249784 | Exclude from origination features |
| disbursement_method | disbursement method (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from selected representation pending authoritative dictionary |
| debt_settlement_flag | debt settlement flag (name-based reading aid; exact vintage definition unverified) | 33 | Exclude from origination features |
| debt_settlement_flag_date | debt settlement flag date (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
| settlement_status | settlement status (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
| settlement_date | settlement date (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
| settlement_amount | settlement amount (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
| settlement_percentage | settlement percentage (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
| settlement_term | settlement term (name-based reading aid; exact vintage definition unverified) | 2226455 | Exclude from origination features |
