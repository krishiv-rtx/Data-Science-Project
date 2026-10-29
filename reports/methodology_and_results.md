# Methodology and results

Read analysis_plan.md for hypotheses, thresholds, direction and eligibility fixed before comparisons. Four tests executed on the full local file; observations were not fabricated from the preliminary profile.

<<<<<<< HEAD
| Question | n (CO/FP or total) | Estimate | 95% confidence interval (CI) | Statistic | df | p | Practical conclusion |
=======
| Question | n (CO/FP or total) | Estimate | 95% CI | Statistic | df | p | Practical conclusion |
>>>>>>> origin/main
| --- | --- | --- | --- | --- | --- | --- | --- |
| int_rate | 268,559 / 1,076,751 | 3.08743 | [3.06698, 3.10787] | 295.97 | 390,130 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| dti | 268,488 / 1,076,448 | 2.35957 | [2.31027, 2.40886] | 93.8212 | 390,672 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| grade | 1,345,310 | 0.26191 | [0.260287, 0.26345] | 92,284.3 | 6 | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |
| term | 324,567 / 1,020,743 | 0.164519 | [0.162759, 0.16628] | 204.25 | not applicable | < 2.23e-308 (floating-point underflow) | CI beyond positive threshold |

## Sample accounting

- int_rate: 268,559 in group A and 1,076,751 in group B; 0 terminal rows excluded for this test.
- dti: 268,488 in group A and 1,076,448 in group B; 374 terminal rows excluded for this test.
- grade: 1,345,310 total; 0 terminal rows excluded for this test.
- term: 324,567 in group A and 1,020,743 in group B; 0 terminal rows excluded for this test.

## Statistical theory and implementation

For two independent groups A and B, estimate delta = mean(A)-mean(B). A denotes Charged Off for numeric comparisons and 60 months for the term comparison. Sample means describe these groups; a population estimand requires an assumed repeatable sampling mechanism. All tests are observational.

<<<<<<< HEAD
**Welch t:** Let n_A,n_B be counts and s_A²,s_B² sample variances (divisor n-1). standard error (SE) = sqrt(s_A²/n_A + s_B²/n_B). t = delta/SE under H0 delta=0. Degrees of freedom nu = (u+v)²/[u²/(n_A-1)+v²/(n_B-1)], where u=s_A²/n_A and v=s_B²/n_B. The two-sided p-value is 2*P(T_nu >= |t|); the 95% interval is delta +/- t_(.975,nu)*SE. It allows unequal variances but still requires independent observations and a reasonable mean sampling approximation. It is not a normality test. Large groups do not excuse extreme leverage or selection bias.

**Two-proportion z:** x_A and x_B count Charged Off loans, n_A and n_B include only observed terminal loans of the given term. p_hat_A=x_A/n_A, p_hat_B=x_B/n_B. Under equal proportions use p_pool=(x_A+x_B)/(n_A+n_B). SE0=sqrt[p_pool*(1-p_pool)*(1/n_A+1/n_B)]. z=(p_hat_A-p_hat_B)/SE0; p=2*P(Z>=|z|). The large-sample confidence interval instead uses SE=sqrt[p_hat_A*(1-p_hat_A)/n_A+p_hat_B*(1-p_hat_B)/n_B]. The null-pooled SE is not reused for the interval. Expected successes/failures must be adequate; the implementation rejects expected counts below five. df is not applicable for the standard normal reference. Without continuity correction, z² equals the 2x2 Pearson chi-square statistic, checked in code and tests.

**Chi-square:** O_ij is the observed grade-outcome count; E_ij = row_i_total * column_j_total / N. Sum (O-E)²/E to obtain chi-square. Under independence the approximate reference has (r-1)*(c-1) degrees of freedom, six for seven grades and two outcomes. The p-value is the upper-tail probability. This tail convention detects any association and is not a directional claim that every grade's event rate rises. Cramer's V = sqrt(chi-square/[N*min(r-1,c-1)]); here min=1. V measures association magnitude without a sign. A percentile interval from 1,000 seeded multinomial resamples of the observed cell proportions describes independent and identically distributed (IID) sampling uncertainty; it is an extension and does not correct dependence or selection. Grade-specific proportions remain necessary for interpretation.
=======
**Welch t:** Let n_A,n_B be counts and s_A²,s_B² sample variances (divisor n-1). SE = sqrt(s_A²/n_A + s_B²/n_B). t = delta/SE under H0 delta=0. Degrees of freedom nu = (u+v)²/[u²/(n_A-1)+v²/(n_B-1)], where u=s_A²/n_A and v=s_B²/n_B. The two-sided p-value is 2*P(T_nu >= |t|); the 95% interval is delta +/- t_(.975,nu)*SE. It allows unequal variances but still requires independent observations and a reasonable mean sampling approximation. It is not a normality test. Large groups do not excuse extreme leverage or selection bias.

**Two-proportion z:** x_A and x_B count Charged Off loans, n_A and n_B include only observed terminal loans of the given term. p_hat_A=x_A/n_A, p_hat_B=x_B/n_B. Under equal proportions use p_pool=(x_A+x_B)/(n_A+n_B). SE0=sqrt[p_pool*(1-p_pool)*(1/n_A+1/n_B)]. z=(p_hat_A-p_hat_B)/SE0; p=2*P(Z>=|z|). The large-sample confidence interval instead uses SE=sqrt[p_hat_A*(1-p_hat_A)/n_A+p_hat_B*(1-p_hat_B)/n_B]. The null-pooled SE is not reused for the interval. Expected successes/failures must be adequate; the implementation rejects expected counts below five. df is not applicable for the standard normal reference. Without continuity correction, z² equals the 2x2 Pearson chi-square statistic, checked in code and tests.

**Chi-square:** O_ij is the observed grade-outcome count; E_ij = row_i_total * column_j_total / N. Sum (O-E)²/E to obtain chi-square. Under independence the approximate reference has (r-1)*(c-1) degrees of freedom, six for seven grades and two outcomes. The p-value is the upper-tail probability. This tail convention detects any association and is not a directional claim that every grade's event rate rises. Cramer's V = sqrt(chi-square/[N*min(r-1,c-1)]); here min=1. V measures association magnitude without a sign. A percentile interval from 1,000 seeded multinomial resamples of the observed cell proportions describes IID sampling uncertainty; it is an extension and does not correct dependence or selection. Grade-specific proportions remain necessary for interpretation.
>>>>>>> origin/main

**Holm:** Sort four p-values p_(1)<=...<=p_(4), multiply each by 4,3,2,1 respectively, then apply cumulative maxima and cap at one. Map adjusted values back to original questions. This addresses repeated testing; it does not make overlapping grade/rate associations independent. Intervals remain ordinary marginal intervals.

**Errors and interpretation:** A Type I error here would assert a nonzero difference/association when the corresponding population null holds; a Type II error would miss one. Alpha is a long-run false-positive criterion conditional on assumptions, not the probability H0 is true. A 95% frequentist interval is generated by a procedure with 95% coverage over repeated comparable samples; it does not assign 95% probability to a fixed parameter. A small p-value is not an effect size, causality claim, or practical decision. Failure to reject does not prove equality. Threshold decisions should consider the whole interval. If a p-value numerically underflows, the report uses a bound, never an exact zero claim.

**Alternatives:** Pooled t needs equal population variances, not established here; Welch avoids that unnecessary constraint. Known-sigma z is not warranted with estimated SDs. Paired t needs meaningful pairs, which these outcome groups lack. A rank test addresses a different distributional question and does not generally test equal means or medians. Exact contingency tests may replace asymptotic tests for sparse expected cells. Correlation imposes numeric coding/linear association assumptions that do not suit grade-category independence. These choices were made for estimands, not to obtain small p-values.


## Auditable per-test calculations

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


## Sensitivity checks

**int_rate sensitivity:** upper cap 26.3; estimate 3.03701, CI [3.0172, 3.05681]. Primary observations are unchanged. This tests capped-variable means, not the original estimand.

**dti sensitivity:** upper cap 38.47; estimate 2.29075, CI [2.25446, 2.32705]. Primary observations are unchanged. This tests capped-variable means, not the original estimand.

Issue-year/term rates are in outputs/tables/cohort_term_rates.csv. These stratified descriptions expose composition but do not eliminate censoring. Pooled primary comparisons remain the declared questions.

Accepted-loan selection excludes rejected applications. Terminal-outcome selection favours mature loans and early defaults; recent 60-month loans are particularly likely to remain unresolved. Therefore term differences are not causal effects and are not lifetime portfolio default probabilities. Grade and interest rate reflect overlapping underwriting information, so their tests are not independent evidence of separate mechanisms. Income, vintage and borrower characteristics can confound all unadjusted comparisons.

Loans may share borrowers or economic shocks. Unique loan IDs do not verify independent borrowers, and no reliable borrower identifier is established. Standard errors, bootstrap intervals and p-values assume independent sampling and can be too optimistic. The dataset is a historical selected collection, not a probability sample; treat inference as model-based and conditional on this collection rather than automatically representative of future lending.

<<<<<<< HEAD
Complete-case exclusion can be selective. debt-to-income ratio (DTI) extremes can affect mean comparisons; retained-extreme primary results and capped sensitivity results target different quantities. A large sample improves some approximations but cannot remove bias, confounding or dependence. Marginal 95% intervals are not simultaneous; Holm controls family-wise error only under valid individual p-values. Thresholds are declared analytical judgments, not authoritative lending standards.
=======
Complete-case exclusion can be selective. DTI extremes can affect mean comparisons; retained-extreme primary results and capped sensitivity results target different quantities. A large sample improves some approximations but cannot remove bias, confounding or dependence. Marginal 95% intervals are not simultaneous; Holm controls family-wise error only under valid individual p-values. Thresholds are declared analytical judgments, not authoritative lending standards.
>>>>>>> origin/main

The exact original download URL, original access date, redistribution licence and version-specific dictionary were not supplied. The local SHA-256 identifies the file, not its original source. Lecture PDFs, quizzes and practice problems were not provided, so exact lecture mapping and the requested 80% syllabus claim cannot be verified. No identities, emails, contributions, sources, or statistics were invented.


## Additional source-quality review

The source contains 32 total-funded footer records and 1 policy-section separator, all with missing loan amount/status; these are not loans and are excluded from every test. There are 2,260,668 loan records. Two observed DTI values are negative and 135 equal 999; their exact semantics are unverified. Primary inference retains them transparently. Excluding the two negative DTI values gives difference 2.35953, CI [2.31024, 2.40882], leaving the interpretation unchanged. There are 1,667 zero incomes and 7,343 utilisation values above 100; these are flagged, not automatically deleted. No negative income was observed.
<<<<<<< HEAD


## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
=======
>>>>>>> origin/main
