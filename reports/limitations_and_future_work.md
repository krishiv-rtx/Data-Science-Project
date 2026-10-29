# Limitations and future work

Accepted-loan selection excludes rejected applications. Terminal-outcome selection favours mature loans and early defaults; recent 60-month loans are particularly likely to remain unresolved. Therefore term differences are not causal effects and are not lifetime portfolio default probabilities. Grade and interest rate reflect overlapping underwriting information, so their tests are not independent evidence of separate mechanisms. Income, vintage and borrower characteristics can confound all unadjusted comparisons.

Loans may share borrowers or economic shocks. Unique loan IDs do not verify independent borrowers, and no reliable borrower identifier is established. Standard errors, bootstrap intervals and p-values assume independent sampling and can be too optimistic. The dataset is a historical selected collection, not a probability sample; treat inference as model-based and conditional on this collection rather than automatically representative of future lending.

Complete-case exclusion can be selective. debt-to-income ratio (DTI) extremes can affect mean comparisons; retained-extreme primary results and capped sensitivity results target different quantities. A large sample improves some approximations but cannot remove bias, confounding or dependence. Marginal 95% intervals are not simultaneous; Holm controls family-wise error only under valid individual p-values. Thresholds are declared analytical judgments, not authoritative lending standards.

The exact original download URL, original access date, redistribution licence and version-specific dictionary were not supplied. The local SHA-256 identifies the file, not its original source. Lecture PDFs, quizzes and practice problems were not provided, so exact lecture mapping and the requested 80% syllabus claim cannot be verified. No identities, emails, contributions, sources, or statistics were invented.

Future work: obtain the historical dictionary and course resources; confirm extraction/as-of date; follow fixed origination cohorts through a common horizon; account for censoring using suitable survival methods; investigate borrower clustering; assess missingness by vintage and outcome; and only then consider adjusted association models. A leakage-safe classifier would require a declared prediction time and temporal validation, and is intentionally outside this midterm's core scope.


## Reading help

[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.
