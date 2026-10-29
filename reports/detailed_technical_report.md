# Statistical inference on observed LendingClub repayment outcomes

**NullPointer - CSE558 Data Science, IIIT-Delhi, Monsoon 2026**

Satyam Singh (2024514), Satguru Saran (2024510), Krishiv Vats (2024308). Emails and individual contributions must be supplied by the group; no allocation is invented.

## Part A - Framing and scope

LendingClub's historical accepted-loan records support questions about how origination descriptors relate to observed repayment outcomes. The purpose is not to build a classifier or to show that every non-paid account defaulted. Basic exploratory data analysis (EDA) asks what statuses, distributions and missingness patterns exist. The inferential question instead quantifies how large the terminal-outcome differences are, whether uncertainty excludes zero, and whether a declared meaningful threshold is exceeded. This is the project's contribution relative to status-count EDA, not a claim of research novelty in the wider literature.

The primary question compares issued rates between Charged Off and Fully Paid loans. Supporting questions compare debt-to-income ratio (DTI) means, grade association and term-specific charge-off proportions. One loan is one observation. Descriptive statements apply to this file; inference is conditional on an assumed independent historical sampling mechanism; no predictive performance or causal effects are claimed.

## Part B - Dataset and full-file audit

The user supplied the local file `accepted_2007_to_2018Q4.csv` (1,675,133,810 bytes). UTF-8 parsing was successful. SHA-256: `3eae03c28fd9d2e8a076ebeb73507e8d4d0f44d90500decdb0936e0933d1f36a`. Issue dates run from 2007-06-01 00:00:00 through 2018-12-01 00:00:00. The audit scanned every row in chunks of 50,000 and inspected every source column, while retaining only selected columns for inference. Only a five-row sample was printed during initial inspection. The accumulated memory of string chunks was 18,820,062,428 bytes; this is a summed representation cost, not measured peak RSS. The encoded matrix uses 120,967,200 bytes. Hardware needs depend on string storage and temporary copies; allow several GB of free memory and disk space for the raw file.

| Metric | Supplied profile | Full CSV audit |
| --- | --- | --- |
| rows | 314,168 | 2,260,701 |
| columns | 162 | 151 |
| duplicate_rows | 0 | 0 |
| unique_ids | 314,168 | 2,260,701 |
| rows_with_missing | 314,168 | 2,260,701 |

The supplied profile is not interchangeable with the CSV. Its 115 numeric plus 36 text columns total 151; its report also lists date-derived `__parsed` fields, which may explain the difference from 162. This explanation is plausible, not a verified reconstruction of the profiling run. Its issue dates cover April-December 2015, so it may describe a subset; the actual row count and full date coverage govern this analysis. No discrepancy is silently corrected to match the PDF.

| Status | Full CSV count |
| --- | --- |
| Fully Paid | 1,076,751 |
| Charged Off | 268,559 |
| Current | 878,317 |
| Late (31-120 days) | 21,467 |
| In Grace Period | 8,436 |
| Late (16-30 days) | 4,349 |
| Default | 40 |
| <missing> | 33 |
| Does not meet the credit policy. Status:Fully Paid | 1,988 |
| Does not meet the credit policy. Status:Charged Off | 761 |

The entire per-column missingness/type inventory is in outputs/tables/missingness.csv. Exact duplicate candidates are found using stable hashes and, when present, compared as full rows; no matching-feature loans are dropped automatically. IDs are checked separately. The full audit reports 0 duplicate rows and 0 repeated nonmissing IDs. A unique ID is not proof that borrowers are independent.

## Part C - Preparation and before/after reconciliation

Source rows 2,260,701 = terminal rows 1,345,310 + excluded other/missing-status rows 915,391. Current, late, grace-period, Default and ambiguous statuses are not relabelled as completed successful or failed repayments. Historical policy-status variants, if present, are also excluded rather than silently merged. This deliberately narrow outcome definition must be kept in mind when generalising.

Numeric fields are parsed after inspecting units/format; trailing percent symbols are supported. Whitespace is stripped from categorical labels. Exact change counts and parse failures appear in outputs/preparation.json. Missing outcomes are not imputed. Test-specific complete-case filters preserve all other usable terminal loans; the encoded representation has its own stricter complete-case rule, which does not reduce every test to the encoded sample.

- int_rate: 268,559 in group A and 1,076,751 in group B; 0 terminal rows excluded for this test.
- dti: 268,488 in group A and 1,076,448 in group B; 374 terminal rows excluded for this test.
- grade: 1,345,310 total; 0 terminal rows excluded for this test.
- term: 324,567 in group A and 1,020,743 in group B; 0 terminal rows excluded for this test.

Joint, hardship and settlement fields may be structurally missing when their conditions do not apply; the code preserves source missingness and does not infer missing-at-random from it. Whole-column mean/zero imputation would invent values and narrow uncertainty, so it is not used. No missingness mechanism is proved by the observed data.

| Field | interquartile range (IQR) flags | Flag % | Lower fence | Upper fence |
| --- | --- | --- | --- | --- |
| loan_amnt | 35,215 | 1.55773 | -10,000 | 38,000 |
| int_rate | 41,099 | 1.818 | -0.26 | 25.74 |
| dti | 21,580 | 0.955308 | -7.01 | 43.39 |
| annual_inc | 110,041 | 4.86764 | -24,500 | 163,500 |
| fico_range_low | 74,846 | 3.31079 | 615 | 775 |
| revol_util | 114 | 0.00504678 | -25.35 | 126.25 |

IQR fences flag unusual observations rather than establish data errors. Primary means retain extremes. DTI sentinel-like values need historical documentation; capping is restricted to sensitivity analysis. Annual income uses log1p only for a descriptive scale comparison: zeros map to zero, negatives are excluded from that chart and not silently logged. The transformation does not prove normality. Tests remain on the original percentage-point scale.

Before encoding: 1,345,310 terminal rows and 12 selected attributes. After representation-specific complete-case filtering: 1,344,080 rows, with 1,230 excluded for missing selected attributes. Actual one-hot matrix: **1,344,080 x 40 = 53,763,200 instance-attribute cells**, meeting the 3,000,000 requirement. Numeric features are loan amount, rate, DTI, income, lower FICO band and utilisation. Nominal indicators represent grade, term, tenure, verification, purpose and application type. Grade order matters for plots but no equal-spacing score is imposed. IDs, outcome and repayment variables are absent. This is a meaningful feature representation, not a blind expansion of employer text or IDs to inflate size.

## Part D - EDA and figure interpretation

1. `status.png` shows all source status counts, including unresolved and missing labels. It makes denominator selection visible, but does not estimate lifetime default probability.
2. `outcome_boxplots.png` compares rate and DTI medians/IQRs by terminal outcome. Fliers are hidden for legibility; every eligible value remains in the tests and full extrema are in numeric_summary.csv. Boxplots do not by themselves establish mean significance.
3. `category_rates.png` shows observed terminal charge-off percentages by grade and term. Group counts are provided in the adjacent saved contingency tables. Patterns may reflect underwriting, borrower mix and outcome maturity rather than causal grade/term effects.
4. `income_and_loan_amount.png` pairs log(1+income) with the requested-loan-amount histogram. It shows income on a compressed scale and the sizes of requested loans; no Gaussianity is claimed.
5. `income_dti.png` is a reproducible 5,000-or-smaller random descriptive sample, seed 558. It visualises possible leverage/outliers without dumping millions of observations; all statistical tests use full eligible groups.
6. `loan_purposes.png` shows how many loans were requested for each stated purpose. `group_mean_comparison.png` contrasts the two outcome groups on original-scale average rate and debt burden. Missingness remains fully audited in the tables.

## Part E - Theory

## Statistical theory and implementation

For two independent groups A and B, estimate delta = mean(A)-mean(B). A denotes Charged Off for numeric comparisons and 60 months for the term comparison. Sample means describe these groups; a population estimand requires an assumed repeatable sampling mechanism. All tests are observational.

**Welch t:** Let n_A,n_B be counts and s_A²,s_B² sample variances (divisor n-1). standard error (SE) = sqrt(s_A²/n_A + s_B²/n_B). t = delta/SE under H0 delta=0. Degrees of freedom nu = (u+v)²/[u²/(n_A-1)+v²/(n_B-1)], where u=s_A²/n_A and v=s_B²/n_B. The two-sided p-value is 2*P(T_nu >= |t|); the 95% interval is delta +/- t_(.975,nu)*SE. It allows unequal variances but still requires independent observations and a reasonable mean sampling approximation. It is not a normality test. Large groups do not excuse extreme leverage or selection bias.

**Two-proportion z:** x_A and x_B count Charged Off loans, n_A and n_B include only observed terminal loans of the given term. p_hat_A=x_A/n_A, p_hat_B=x_B/n_B. Under equal proportions use p_pool=(x_A+x_B)/(n_A+n_B). SE0=sqrt[p_pool*(1-p_pool)*(1/n_A+1/n_B)]. z=(p_hat_A-p_hat_B)/SE0; p=2*P(Z>=|z|). The large-sample confidence interval instead uses SE=sqrt[p_hat_A*(1-p_hat_A)/n_A+p_hat_B*(1-p_hat_B)/n_B]. The null-pooled SE is not reused for the interval. Expected successes/failures must be adequate; the implementation rejects expected counts below five. df is not applicable for the standard normal reference. Without continuity correction, z² equals the 2x2 Pearson chi-square statistic, checked in code and tests.

**Chi-square:** O_ij is the observed grade-outcome count; E_ij = row_i_total * column_j_total / N. Sum (O-E)²/E to obtain chi-square. Under independence the approximate reference has (r-1)*(c-1) degrees of freedom, six for seven grades and two outcomes. The p-value is the upper-tail probability. This tail convention detects any association and is not a directional claim that every grade's event rate rises. Cramer's V = sqrt(chi-square/[N*min(r-1,c-1)]); here min=1. V measures association magnitude without a sign. A percentile interval from 1,000 seeded multinomial resamples of the observed cell proportions describes independent and identically distributed (IID) sampling uncertainty; it is an extension and does not correct dependence or selection. Grade-specific proportions remain necessary for interpretation.

**Holm:** Sort four p-values p_(1)<=...<=p_(4), multiply each by 4,3,2,1 respectively, then apply cumulative maxima and cap at one. Map adjusted values back to original questions. This addresses repeated testing; it does not make overlapping grade/rate associations independent. Intervals remain ordinary marginal intervals.

**Errors and interpretation:** A Type I error here would assert a nonzero difference/association when the corresponding population null holds; a Type II error would miss one. Alpha is a long-run false-positive criterion conditional on assumptions, not the probability H0 is true. A 95% frequentist interval is generated by a procedure with 95% coverage over repeated comparable samples; it does not assign 95% probability to a fixed parameter. A small p-value is not an effect size, causality claim, or practical decision. Failure to reject does not prove equality. Threshold decisions should consider the whole interval. If a p-value numerically underflows, the report uses a bound, never an exact zero claim.

**Alternatives:** Pooled t needs equal population variances, not established here; Welch avoids that unnecessary constraint. Known-sigma z is not warranted with estimated SDs. Paired t needs meaningful pairs, which these outcome groups lack. A rank test addresses a different distributional question and does not generally test equal means or medians. Exact contingency tests may replace asymptotic tests for sparse expected cells. Correlation imposes numeric coding/linear association assumptions that do not suit grade-category independence. These choices were made for estimands, not to obtain small p-values.


## Part F - Actual computed results

| Question | n (CO/FP or total) | Estimate | 95% confidence interval (CI) | Statistic | df | p | Practical conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| int_rate | 268,559 / 1,076,751 | 3.08743 | [3.06698, 3.10787] | 295.97 | 390,130 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| dti | 268,488 / 1,076,448 | 2.35957 | [2.31027, 2.40886] | 93.8212 | 390,672 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| grade | 1,345,310 | 0.26191 | [0.260287, 0.26345] | 92,284.3 | 6 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| term | 324,567 / 1,020,743 | 0.164519 | [0.162759, 0.16628] | 204.25 | not applicable | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |

### int_rate: Welch t

| Quantity | Computed value |
| --- | --- |
| n_a | 268,559 |
| n_b | 1,076,751 |
| mean_a | 15.7107 |
| mean_b | 12.6233 |
| sd_a | 4.91039 |
| sd_b | 4.52723 |
| estimate | 3.08743 |
| se | 0.0104316 |
| statistic | 295.97 |
| df | 390,130 |
| p | not applicable |
| ci_low | 3.06698 |
| ci_high | 3.10787 |
| test | int_rate |
| method | Welch t |
| units | percentage points |
| threshold | 1 |
| excluded | 0 |
| p_display | < 2.23e-308 (floating-point underflow) |
| holm_p_display | < 2.23e-308 (floating-point underflow) |
| holm_reject | 1 |
| decision | Reject H0 |
| practical | CI beyond positive threshold |
| p_underflow | 1 |

Decision: Reject H0 at alpha=.05. Holm decision: reject. Practical comparison: CI beyond positive threshold. These are unadjusted associations among terminal outcomes.

### dti: Welch t

| Quantity | Computed value |
| --- | --- |
| n_a | 268,488 |
| n_b | 1,076,448 |
| mean_a | 20.1712 |
| mean_b | 17.8116 |
| sd_a | 11.8317 |
| sd_b | 10.9359 |
| estimate | 2.35957 |
| se | 0.0251496 |
| statistic | 93.8212 |
| df | 390,672 |
| p | not applicable |
| ci_low | 2.31027 |
| ci_high | 2.40886 |
| test | dti |
| method | Welch t |
| units | percentage points |
| threshold | 2 |
| excluded | 374 |
| p_display | < 2.23e-308 (floating-point underflow) |
| holm_p_display | < 2.23e-308 (floating-point underflow) |
| holm_reject | 1 |
| decision | Reject H0 |
| practical | CI beyond positive threshold |
| p_underflow | 1 |

Decision: Reject H0 at alpha=.05. Holm decision: reject. Practical comparison: CI beyond positive threshold. These are unadjusted associations among terminal outcomes.

### grade: Chi-square independence

| Quantity | Computed value |
| --- | --- |
| n | 1,345,310 |
| estimate | 0.26191 |
| statistic | 92,284.3 |
| df | 6 |
| p | not applicable |
| ci_low | 0.260287 |
| ci_high | 0.26345 |
| min_expected | 1,822.99 |
| bootstrap_replicates | 1,000 |
| ci_method | IID multinomial percentile bootstrap of Cramers V; extension |
| test | grade |
| method | Chi-square independence |
| units | Cramers V |
| threshold | 0.1 |
| excluded | 0 |
| p_display | < 2.23e-308 (floating-point underflow) |
| holm_p_display | < 2.23e-308 (floating-point underflow) |
| holm_reject | 1 |
| decision | Reject H0 |
| practical | CI beyond positive threshold |
| p_underflow | 1 |

Decision: Reject H0 at alpha=.05. Holm decision: reject. Practical comparison: CI beyond positive threshold. These are unadjusted associations among terminal outcomes.

### term: Two-proportion z

| Quantity | Computed value |
| --- | --- |
| n_a | 324,567 |
| n_b | 1,020,743 |
| events_a | 105,307 |
| events_b | 163,252 |
| proportion_a | 0.324454 |
| proportion_b | 0.159934 |
| estimate | 0.164519 |
| se | 0.000898296 |
| statistic | 204.25 |
| df | not applicable |
| p | not applicable |
| ci_low | 0.162759 |
| ci_high | 0.16628 |
| min_expected | 64,792 |
| chi2_crosscheck | 41,717.9 |
| test | term |
| method | Two-proportion z |
| units | proportion (60 minus 36 months) |
| threshold | 0.02 |
| excluded | 0 |
| p_display | < 2.23e-308 (floating-point underflow) |
| holm_p_display | < 2.23e-308 (floating-point underflow) |
| holm_reject | 1 |
| decision | Reject H0 |
| practical | CI beyond positive threshold |
| p_underflow | 1 |

Decision: Reject H0 at alpha=.05. Holm decision: reject. Practical comparison: CI beyond positive threshold. These are unadjusted associations among terminal outcomes.


**int_rate sensitivity:** upper cap 26.3; estimate 3.03701, CI [3.0172, 3.05681]. Primary observations are unchanged. This tests capped-variable means, not the original estimand.

**dti sensitivity:** upper cap 38.47; estimate 2.29075, CI [2.25446, 2.32705]. Primary observations are unchanged. This tests capped-variable means, not the original estimand.

## Part G - Syllabus connection

The supplied guidelines explicitly request preparation, EDA and 3-5 hypothesis tests with alternative-test comparisons, intervals and practical thresholds. The template illustrates Welch's procedure. The exact lecture and quiz mapping cannot be verified because those files were absent. See syllabus_mapping.md for a clear evidence boundary. Holm and the bootstrap interval are explicitly labelled extensions; they support the core introductory inference instead of replacing it.

## Part H - Critical interpretation

Accepted-loan selection excludes rejected applications. Terminal-outcome selection favours mature loans and early defaults; recent 60-month loans are particularly likely to remain unresolved. Therefore term differences are not causal effects and are not lifetime portfolio default probabilities. Grade and interest rate reflect overlapping underwriting information, so their tests are not independent evidence of separate mechanisms. Income, vintage and borrower characteristics can confound all unadjusted comparisons.

Loans may share borrowers or economic shocks. Unique loan IDs do not verify independent borrowers, and no reliable borrower identifier is established. Standard errors, bootstrap intervals and p-values assume independent sampling and can be too optimistic. The dataset is a historical selected collection, not a probability sample; treat inference as model-based and conditional on this collection rather than automatically representative of future lending.

Complete-case exclusion can be selective. DTI extremes can affect mean comparisons; retained-extreme primary results and capped sensitivity results target different quantities. A large sample improves some approximations but cannot remove bias, confounding or dependence. Marginal 95% intervals are not simultaneous; Holm controls family-wise error only under valid individual p-values. Thresholds are declared analytical judgments, not authoritative lending standards.

The exact original download URL, original access date, redistribution licence and version-specific dictionary were not supplied. The local SHA-256 identifies the file, not its original source. Lecture PDFs, quizzes and practice problems were not provided, so exact lecture mapping and the requested 80% syllabus claim cannot be verified. No identities, emails, contributions, sources, or statistics were invented.

## Part I - Conclusions and reproducibility

For each question the table above answers both statistical and practical significance. The result does not establish that changing interest, DTI, grade or term would change a borrower's outcome. The strength of this workflow is its audit trail: source file identity, exact eligibility rules, calculated matrix size, reusable tested formulas and reports generated from JSON outputs. The principal unresolved scientific weaknesses are selection, maturity, unverified dependence and historical provenance.

Run scripts/run_all.py for the full scan and figures, scripts/generate_reports.py for this document and the LaTeX source, and scripts/compile_report.py for PDF compilation. The notebooks independently execute their code from top to bottom against saved audit outputs; the raw scan itself runs in the command-line pipeline. Outputs are not hypothetical or reconstructed from a chart. See README.md for exact commands, missing course inputs and compilation requirements.


## Additional source-quality review

The source contains 32 total-funded footer records and 1 policy-section separator, all with missing loan amount/status; these are not loans and are excluded from every test. There are 2,260,668 loan records. Two observed DTI values are negative and 135 equal 999; their exact semantics are unverified. Primary inference retains them transparently. Excluding the two negative DTI values gives difference 2.35953, CI [2.31024, 2.40882], leaving the interpretation unchanged. There are 1,667 zero incomes and 7,343 utilisation values above 100; these are flagged, not automatically deleted. No negative income was observed.


## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
