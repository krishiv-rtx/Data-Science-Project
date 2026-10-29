# Analysis plan fixed before outcome comparisons

NullPointer, CSE558, Monsoon 2026. Written after inspecting five source rows and the supplied profile, before executing group comparisons. This is a transparent analysis plan, not a preregistered independent confirmatory study.

Primary question: among accepted loans observed as Fully Paid or Charged Off, is the mean origination interest-rate difference practically material? Supporting questions address debt-to-income ratio (DTI), grade, and term. One loan is the observational unit. Accepted loans and terminal outcomes define two selection stages; neither all applicants nor all originated loans are represented by terminal-only estimates.

All four tests use alpha=.05 and nondirectional research alternatives. Welch and proportion tests are two-sided; chi-square independence uses the upper tail because departures in any direction increase the statistic. H0 carries equality. Report unadjusted results and Holm-adjusted results for this four-test family. Unadjusted 95% intervals are marginal, not simultaneous.

1. Interest rate: H0 mu_CO - mu_FP = 0; H1 difference != 0. Welch t test. Threshold 1 percentage point: $100 annual simple interest per $10,000 principal illustrates scale, not actual amortized cost or an industry standard.
2. DTI: H0 mu_CO - mu_FP = 0; H1 difference != 0. Welch t test. Threshold 2 percentage points: monthly debt obligations of $100 against monthly income of $5,000 illustrates scale. Subjective analytical criterion.
3. Grade: H0 grade and terminal outcome independent; H1 associated. Chi-square 7 by 2, expected df=6 if all grades present. Cramer's V with an independent and identically distributed (IID) multinomial bootstrap interval, seed 558, 1,000 draws. V=.10 is an exploratory interpretive convention, not a lending decision threshold; grade-specific event proportions supply context. This threshold is weakly grounded and must not be treated as authoritative.
4. Term: H0 p_60 - p_36 = 0; H1 difference != 0. Pooled-null two-proportion z test, unpooled large-sample 95% difference interval. Threshold .02, or 2 additional observed charge-offs per 100 terminal loans. This is a subjective decision-relevance scale, not a causal effect or portfolio loss forecast.

Use test-specific complete cases with no imputation. Check category labels, valid IDs, sample sizes, numeric parsing, finite measurements, spreads, extreme values and expected cells. Retain extremes in primary tests. Cap each numeric test variable at its pooled terminal 99th percentile only as a labelled sensitivity analysis; this changes the estimand. Never delete based on p-values. Report issue-year/term terminal proportions to expose maturity composition. No predictive model is necessary.

Welch avoids the pooled t assumption of equal variances; unknown population standard deviation (SD) rules out a known-sigma z test. Paired tests are invalid without paired units. Mann-Whitney changes the estimand to rank/distribution differences, not generally mean or median differences. Fisher exact is a possible sparse categorical alternative; do not force an asymptotic test if expected counts are too small. The 2x2 chi-square cross-check is the same term finding, not a fifth test. Independence remains an unverified working assumption: repeated borrowers and shared economic conditions can make intervals too narrow.

Encoding uses six numeric and six categorical origination-candidate attributes, one-hot nominal categories, no identifiers, no outcome, no post-outcome fields, and complete cases. Calculate actual matrix rows times columns. This representation is for size and preparation audit, not a fitted predictor. Application-time availability of the issued rate and grade must not be assumed; these are origination descriptors.


## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
