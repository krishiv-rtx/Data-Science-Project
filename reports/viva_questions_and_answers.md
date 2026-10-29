# Viva questions and answers

25 categories, each with a main question, follow-up and common mistake. Numerical answers are drawn from this run.

## 1. Objective and novelty

**Q: Why this problem rather than a default classifier?**

The assignment centres on inference. We quantify terminal-outcome differences, uncertainty and practical importance. The contribution beyond status-count exploratory data analysis (EDA) is a declared estimand and a defensible test, not a claim that lending risk has never been studied.

**Follow-up: What is the primary estimand?**

Mean issued rate among Charged Off loans minus that among Fully Paid loans.

**Avoid:** Calling a familiar dataset itself novel.

## 2. Dataset and provenance

**Q: What exactly did you analyse?**

The local CSV contains 2,260,701 parsed records and 151 source columns; 33 are verified summary/footer records. Its hash is in the audit. The profile describes a smaller 314,168-row collection, so our results come from the CSV.

**Follow-up: Where was it originally downloaded?**

The original URL, date and licence were not supplied; the filename does not prove them.

**Avoid:** Claiming a Kaggle source without evidence.

## 3. Types and schema

**Q: Why is a numeric-looking ID not a numeric feature?**

Its magnitude does not represent a borrower attribute. We keep IDs for uniqueness checks, while grade is ordinal and purpose is nominal.

**Follow-up: Why not code grade A-G as 1-7?**

That imposes equal spacing if used quantitatively; our independence test uses category counts.

**Avoid:** Confusing storage dtype with analytical meaning.

## 4. Missingness

**Q: Why not fill every missing value with a mean?**

Special-program fields can be structurally absent, and unconditional imputation would invent measurements and understate uncertainty. Tests use their own complete cases.

**Follow-up: Is deletion unbiased?**

Not necessarily; excluded cases may differ. Complete-case rules are transparent but do not prove missing-at-random.

**Avoid:** Claiming that a large retained sample eliminates missingness bias.

## 5. Outliers and interquartile range (IQR)

**Q: Why not delete all outliers?**

The IQR rule flags unusual values, not errors. Primary tests retain observations; cap and nonnegative-debt-to-income ratio (DTI) sensitivities disclose their changed estimands.

**Follow-up: What is the fence?**

Q1 minus 1.5 IQR and Q3 plus 1.5 IQR, where IQR=Q3-Q1.

**Avoid:** Choosing exclusions to improve p-values.

## 6. Encoding

**Q: How is the course size requirement met?**

The actual representation has 1,344,080 complete-case rows and 40 columns: 53,763,200 cells. It uses six numeric descriptors and one-hot categories, excluding ID, status and repayment fields.

**Follow-up: Does every test use that sample?**

No. Each test uses its own required-variable complete cases; the matrix is for representation auditing.

**Avoid:** Multiplying raw dimensions and calling it post-encoding size.

## 7. Log transformations

**Q: Why use log1p for income?**

Income is highly skewed; log(1+income) makes scale differences visible and admits zero. It is only an EDA transformation, not a declaration of Gaussianity.

**Follow-up: Does the mean difference then mean dollars?**

No. A comparison on a log scale would have a different estimand; our core tests retain original rate/DTI scales.

**Avoid:** Interpreting a log-scale mean as an arithmetic dollar mean.

## 8. Leakage

**Q: Why exclude recoveries and last-payment amounts?**

They arise during or after repayment and are unavailable at origination. Including them in origination prediction could reveal the outcome.

**Follow-up: Is grade known at application?**

Not necessarily; issued grade/rate are origination descriptors. We do not make application-time prediction claims.

**Avoid:** Treating every CSV column as a prospective predictor.

## 9. EDA

**Q: What does the status plot establish?**

It describes observed records and the size of the unresolved population. It motivates explicit denominator selection.

**Follow-up: Can a boxplot prove a significant difference?**

No; it depicts distributions. Tests and intervals quantify the specified mean contrast under assumptions.

**Avoid:** Inferring p-values from appearance.

## 10. Hypotheses

**Q: Why must H0 carry equality?**

The reference distribution is evaluated at the equality null here: zero mean/proportion difference, or independence. H1 represents the research alternative.

**Follow-up: When were hypotheses fixed?**

After a small schema sample and the preliminary profile, before computing full-data group comparisons; this is not independent preregistration.

**Avoid:** Claiming hypotheses were chosen before any exposure to the dataset.

## 11. Direction

**Q: Why two-sided comparisons?**

The scientific questions ask whether differences exist without selecting a sign after observing results.

**Follow-up: Why is chi-square upper-tailed?**

Squaring departures makes large values evidence against independence in any direction; it does not imply one grade direction.

**Avoid:** Switching to one-sided after seeing a favourable sign.

## 12. z and t tests

**Q: Why a t reference for means with a huge sample?**

Population variances are unknown. Welch uses estimated spreads and Satterthwaite degrees of freedom; it approaches normal behaviour at large df without needing known sigma.

**Follow-up: Does the CLT cure confounding?**

No. It concerns sampling distributions, not selection, confounding or dependence.

**Avoid:** Using large n as a universal validity argument.

## 13. Welch versus pooled

**Q: What if group variances differ?**

Welch directly allows unequal variances and unequal group sizes. Pooled t assumes equal population variances.

**Follow-up: Why not first test variances and switch methods?**

A preselected Welch procedure avoids a data-dependent selection rule and does not need that extra assumption.

**Avoid:** Treating a nonsignificant variance test as proof of equality.

## 14. Two proportions

**Q: What are the two term denominators?**

Terminal loans in the 60-month and 36-month groups. Charged Off is the event; Current is excluded, not counted as no event.

**Follow-up: Why pooled standard error (SE) for z but not the confidence interval (CI)?**

The test imposes equal proportions under H0; the interval estimates the unconstrained difference using separate group proportions.

**Avoid:** Using all originated loans as denominator while excluding unresolved events.

## 15. Chi-square

**Q: Why six degrees of freedom for grade?**

Seven grade rows and two outcome columns give (7-1)*(2-1)=6, with margins constraining independent cell variation.

**Follow-up: Why inspect expected counts?**

The chi-square reference is an approximation that can be poor in sparse cells. We verify the actual minimum expected count.

**Avoid:** Applying a count-table test to arbitrary continuous measurements.

## 16. P-values

**Q: What does an extremely small p-value mean?**

Under H0 and the working sampling assumptions, a statistic at least this extreme is very unlikely. It does not measure the probability H0 is true.

**Follow-up: Why report a bound instead of zero?**

The numerical survival function underflows; mathematical tail probability is not zero.

**Avoid:** Saying p is the chance results happened by random chance without conditioning on a null.

## 17. Confidence intervals

**Q: What does 95% confidence mean?**

A repeated-sampling procedure would cover the fixed parameter in 95% of comparable samples if its assumptions hold.

**Follow-up: What is SE versus standard deviation (SD)?**

SD describes individual variation; SE describes uncertainty in an estimator. The mean-difference SE combines each variance divided by its sample size.

**Avoid:** Assigning 95% probability to a fixed parameter after calculating the interval.

## 18. Practical significance

**Q: Can a tiny p-value coexist with a negligible difference?**

Yes. Large samples can detect small effects precisely. Compare effect size and the full interval with the declared practical threshold.

**Follow-up: Where did our thresholds come from?**

Transparent scale/decision examples chosen by the analyst, not verified industry standards; the grade V threshold is especially conventional.

**Avoid:** Equating rejection with business importance.

## 19. Multiple testing

**Q: Why apply Holm?**

Four related hypotheses increase the chance of at least one false rejection. Holm adjusts ordered p-values to control family-wise error if individual p-values are valid.

**Follow-up: Are the CIs simultaneous?**

No. They remain marginal 95% intervals and are labelled accordingly.

**Avoid:** Assuming Holm removes confounding or makes hypotheses independent.

## 20. Assumptions and robustness

**Q: What is the weakest assumption?**

Independent, representative sampling is not established. Loans can share borrowers and economic conditions, and the accepted/terminal selections are strong.

**Follow-up: What does cap sensitivity tell us?**

Whether extreme upper-tail values materially drive a mean contrast, while changing the estimand to a capped-variable mean.

**Avoid:** Claiming robustness because p stays small alone.

## 21. Alternative methods

**Q: Why not Mann-Whitney instead of Welch?**

It changes the question to ranks/distributions; it is not generally a test of equal means or medians. Our primary estimand is the original-scale mean difference.

**Follow-up: When use Fisher exact?**

For sparse count tables where the asymptotic expected-cell condition fails, with an appropriate exact design.

**Avoid:** Listing alternatives without explaining their estimands.

## 22. Actual results

**Q: What are the main computed effects?**

Rate difference is 3.087 percentage points; DTI difference 2.360; grade Cramer's V 0.262; term difference 16.452 percentage points. All declared tests reject under their working assumptions, and their intervals exceed the chosen positive thresholds.

**Follow-up: Does term cause these extra charge-offs?**

No. The 60-month and 36-month terminal groups differ in borrower mix and maturity. The result is conditional association.

**Avoid:** Confusing proportion units .1645 with .1645 percentage points.

## 23. Limitations and causality

**Q: Why cannot this prove a causal effect?**

There is no random assignment or credible causal identification design. Underwriting, borrower risk and economic vintage may affect both descriptors and outcomes.

**Follow-up: What would improve the design?**

Common-horizon cohorts, explicit censoring methods, borrower-cluster information and carefully justified adjustment or a causal design.

**Avoid:** Adding regression and declaring causality automatically.

## 24. Reproducibility

**Q: How can a reviewer reproduce the results?**

Install requirements, point run_all.py at the raw CSV, generate reports, run tests/notebooks, then compile the template. The audit records the file hash and deterministic seeds.

**Follow-up: Are notebook outputs invented?**

No; their plain-Python cells were executed sequentially in fresh processes and actual stdout was saved. They inspect and cross-check results from the full-data pipeline.

**Avoid:** Calling an unexecuted notebook validated.

## 25. Professor challenges

**Q: What remains incomplete despite the calculations?**

Exact original provenance and course mapping. Lecture/quiz/practice files were absent, and personal emails, contributions and code URL must be filled accurately before submission.

**Follow-up: What if a test had failed to reject?**

Report that evidence is insufficient to reject at the chosen level; discuss the CI and detectable practical range rather than claiming equality.

**Avoid:** Hiding missing materials or inventing lecture numbers.



## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
