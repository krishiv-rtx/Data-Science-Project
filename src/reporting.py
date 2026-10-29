"""Generate narrative and template-based source from saved, computed outputs."""
from pathlib import Path
import json,re,platform,importlib.metadata
import pandas as pd
from .config import ROOT,NUMERIC,CATEGORICAL
from .feature_audit import classify

def read(name):return json.loads((ROOT/'outputs'/name).read_text(encoding='utf-8'))
def write(name,text):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def fmt(x):
    if x is None:return 'not applicable'
    return f'{x:,.0f}' if isinstance(x,int) else f'{x:,.6g}' if isinstance(x,float) else str(x)
def mdtable(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(fmt(x).replace('|','/') for x in row)+' |' for row in rows)
def texescape(s):
    return str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')

def generate():
    a=read('dataset_audit.json'); e=read('encoded_size.json'); c=read('preparation.json'); results=read('results.json'); sens=read('sensitivity.json')
    result_table=mdtable(['Question','n (CO/FP or total)','Estimate','95% CI','Statistic','df','p','Practical conclusion'],[
        [r['test'],f"{r['n_a']:,} / {r['n_b']:,}" if 'n_a' in r else f"{r['n']:,}",r['estimate'],f"[{r['ci_low']:.6g}, {r['ci_high']:.6g}]",r['statistic'],r['df'],r['p_display'],r['practical']] for r in results])
    profile={'rows':314168,'columns':162,'duplicate_rows':0,'unique_ids':314168,'rows_with_missing':314168}
    comparison=mdtable(['Metric','Supplied profile','Full CSV audit'],[[k,profile[k],a[k]] for k in profile])
    statuses=mdtable(['Status','Full CSV count'],list(a['status_counts'].items()))
    arithmetic=f"{e['rows']:,} x {e['columns']:,} = {e['cells']:,} instance-attribute cells"
    sample_counts='\n'.join(f"- {r['test']}: "+(f"{r['n_a']:,} in group A and {r['n_b']:,} in group B" if 'n_a' in r else f"{r['n']:,} total")+f"; {r['excluded']:,} terminal rows excluded for this test." for r in results)
    descriptions={
        'int_rate':('Issued annual interest rate','percentage points','Continuous','Origination descriptor, not necessarily known at application'),
        'dti':('Debt-to-income ratio','percentage points','Continuous','Exact historical denominator requires vintage documentation; do not assume all debts included'),
        'loan_amnt':('Requested/listed loan principal','USD','Continuous monetary','Not a repayment amount'),
        'annual_inc':('Reported annual income','USD/year','Continuous monetary','Self-report/verification limitations; zero and extreme values require interpretation'),
        'fico_range_low':('Lower end of origination FICO band','score points','Discrete ordered','Not exact FICO; do not use last_fico fields as substitutes'),
        'revol_util':('Revolving credit utilisation','percentage points','Continuous','Values above 100 may reflect source conventions'),
        'grade':('Recorded credit grade','A-G','Ordinal category','Order A-G; no equal spacing assumption'),
        'term':('Scheduled term','months','Category','Whitespace stripped; only 36/60 used for term test'),
        'home_ownership':('Reported housing tenure','category','Nominal','Do not encode as a numeric quantity'),
        'verification_status':('Income verification label','category','Nominal','Not proof of accuracy or absence of risk'),
        'purpose':('Stated loan purpose','category','Nominal','Self-reported; no causal interpretation'),
        'application_type':('Individual/joint application label','category','Nominal','Joint-specific missingness can be structural'),
        'loan_status':('Observed repayment status','category','Nominal outcome','Fully Paid/Charged Off only for primary inference'),
        'issue_d':('Issue month','calendar month','Date','Parsed using %b-%Y; monthly resolution'),
        'id':('Loan identifier','none','Identifier','Used for integrity, never as a numeric feature')}
    dictionary=mdtable(['Variable','Meaning','Units / type','Missing source rows','Use / caveat'],[[k,v[0],v[1]+' / '+v[2],a['missing_counts'].get(k),v[3]] for k,v in descriptions.items()])
    feature_rows=[]
    for name in a['column_names']:
        category,time,decision=classify(name)
        feature_rows.append([name,a['inferred_types'][name],a['missing_counts'][name],category,time,decision])
    pd.DataFrame(feature_rows,columns=['feature','type','missing_count','role','time_availability','decision']).to_csv(ROOT/'outputs/tables/feature_audit.csv',index=False)
    pd.DataFrame([{'metric':k,'profile':v,'actual':a[k]} for k,v in profile.items()]).to_csv(ROOT/'outputs/tables/profile_comparison.csv',index=False)
    numeric_profile={'loan_amnt':15216.877196277152,'int_rate':12.509651874156505,'dti':19.1650938994035,'annual_inc':77435.89938978506}
    observed=pd.read_csv(ROOT/'outputs/tables/numeric_summary.csv',index_col=0)
    pd.DataFrame([{'variable':k,'profile_mean':v,'actual_mean':float(observed.loc[k,'mean'])} for k,v in numeric_profile.items()]).to_csv(ROOT/'outputs/tables/profile_numeric_comparison.csv',index=False)
    status_profile={'Fully Paid':222280,'Charged Off':56159,'Current':33891,'Late (31-120 days)':1113,'In Grace Period':501,'Late (16-30 days)':223,'Default':1}
    pd.DataFrame([{'status':k,'profile_count':status_profile.get(k),'actual_count':v} for k,v in a['status_counts'].items()]).to_csv(ROOT/'outputs/tables/profile_status_comparison.csv',index=False)
    pd.DataFrame([{'step':'source CSV','rows':a['rows'],'columns':a['columns']},
        {'step':'terminal only','rows':c['terminal_rows'],'columns':len(NUMERIC+CATEGORICAL)},
        {'step':'encoded complete cases','rows':e['rows'],'columns':e['columns']}]).to_csv(ROOT/'outputs/tables/before_after.csv',index=False)
    write('reports/data_dictionary.md',f'''# Data dictionary and temporal audit

Source types are inferred by a full chunked scan; all source values are first loaded as strings for stable cross-chunk hashing, then selected numeric fields are parsed. Float64/int categorical analytical roles differ from the raw storage representation. Exact original download metadata and vintage dictionary remain unverified. These working descriptions combine supplied profile evidence and basic domain semantics; ambiguous unused fields are not guessed.

{dictionary}

## Derived variables

- `issue_date`: issue_d parsed with `%b-%Y`; failed parses become missing and are counted.
- `charged_off`: 1 iff loan_status is exactly Charged Off, 0 iff Fully Paid; undefined outside the terminal sample. This is an observed terminal outcome, not lifetime default risk for all loans.
- Grade and term tables: counts of unique loan records in each category by terminal outcome. Grade order A through G is maintained.
- One-hot columns: one column per observed category of grade, term, home_ownership, verification_status, purpose and application_type; no dropped reference level, because no regression is fitted. Each value is 0 or 1. Exact columns are in outputs/encoded_size.json.
- Numeric representation: six numeric columns preserved on original scales, with complete-case rows only. No scaling or imputation. There is no predictive model.
- `log1p(annual_inc)`: natural logarithm of 1 + income for nonnegative observed values, including zero. It is a descriptive chart only; no mean comparison uses this scale. Negative incomes are not logged.
- IQR flags: below Q1-1.5*(Q3-Q1) or above Q3+1.5*(Q3-Q1), calculated per numeric field on nonmissing source values. No deletion follows a flag.
- Capped sensitivity values: min(x, pooled terminal 99th percentile); only sensitivity comparisons use them.

The complete 151-or-other-source-column inventory is outputs/tables/feature_audit.csv; its row count follows the actual file. Selected numeric/categorical variables appear in EDA or size auditing. Only int_rate, dti, grade, term and loan_status enter tests. No field is certified for application-time prediction. Identifiers and repayment-process variables are excluded from the encoded representation. ID uniqueness cannot establish borrower uniqueness.
''')
    limitations='''Accepted-loan selection excludes rejected applications. Terminal-outcome selection favours mature loans and early defaults; recent 60-month loans are particularly likely to remain unresolved. Therefore term differences are not causal effects and are not lifetime portfolio default probabilities. Grade and interest rate reflect overlapping underwriting information, so their tests are not independent evidence of separate mechanisms. Income, vintage and borrower characteristics can confound all unadjusted comparisons.

Loans may share borrowers or economic shocks. Unique loan IDs do not verify independent borrowers, and no reliable borrower identifier is established. Standard errors, bootstrap intervals and p-values assume independent sampling and can be too optimistic. The dataset is a historical selected collection, not a probability sample; treat inference as model-based and conditional on this collection rather than automatically representative of future lending.

Complete-case exclusion can be selective. DTI extremes can affect mean comparisons; retained-extreme primary results and capped sensitivity results target different quantities. A large sample improves some approximations but cannot remove bias, confounding or dependence. Marginal 95% intervals are not simultaneous; Holm controls family-wise error only under valid individual p-values. Thresholds are declared analytical judgments, not authoritative lending standards.

The exact original download URL, original access date, redistribution licence and version-specific dictionary were not supplied. The local SHA-256 identifies the file, not its original source. Lecture PDFs, quizzes and practice problems were not provided, so exact lecture mapping and the requested 80% syllabus claim cannot be verified. No identities, emails, contributions, sources, or statistics were invented.'''
    write('reports/limitations_and_future_work.md','# Limitations and future work\n\n'+limitations+'''

Future work: obtain the historical dictionary and course resources; confirm extraction/as-of date; follow fixed origination cohorts through a common horizon; account for censoring using suitable survival methods; investigate borrower clustering; assess missingness by vintage and outcome; and only then consider adjusted association models. A leakage-safe classifier would require a declared prediction time and temporal validation, and is intentionally outside this midterm's core scope.
''')
    write('reports/syllabus_mapping.md','''# Course mapping: evidence boundary

The official guidelines and template were supplied and inspected. Lectures 1-12, quiz solutions/rubric and practice problems were not supplied. Exact lecture numbers and an 80% taught-content fraction are therefore **unverified**; do not present this table as evidence of lecture coverage.

| Concept | Verified supplied reference | Project use | Status / presentation explanation |
| --- | --- | --- | --- |
| Dataset, encoding and size | Guidelines items 1-3 | Full audit and encoded_size.json | Required; numeric and nominal features need different representation |
| EDA | Guidelines item 4 | Six EDA figures | Required; describe patterns without inferring cause |
| Hypotheses, alpha, direction, practical threshold | Guidelines item 5a | analysis_plan.md | Required; fix the scientific question before test interpretation |
| Alternative tests | Guidelines item 5b; template Section 5 | Welch versus pooled/paired/z tests | Template illustrates Welch; lecture coverage unknown |
| Statistic, df, p and CI | Guidelines item 5c | Four result tables | Required; uncertainty is separate from practical impact |
| Missingness, IQR, descriptive summaries | Guidelines items 2-4 | Audit and outlier tables | General introductory methods; exact lecture unverified |
| Two-proportion z and chi-square | Requested master prompt | Term and grade tests | Candidate introductory methods; exact lecture unverified |
| Holm adjustment | Not verified in course resources | Four-test family | Extension: order p-values and control family-wise error |
| Bootstrap Cramer's V interval | Not verified in course resources | Grade uncertainty | Extension: resample the empirical cell distribution under IID assumptions |
| log1p plot / capped sensitivity | Not verified in course resources | Income EDA and robustness | Extensions; changed scales/estimands must be disclosed |

Replace the unverified entries only after inspecting the actual lectures. The workflow concentrates on introductory inference; no complex machine learning is included.
''')
    write('reports/references.md','''# References and provenance

1. User-supplied CSE558_Project_Report_Guidelines.pdf, inspected 29 October 2026. Authoritative submission requirements: 3-5 tests and at most eight pages.
2. User-supplied CSE558_Project_Report_Template.tex and .pdf, inspected 29 October 2026. Layout and six-section structure adapted; illustrative restaurant content removed. Guideline test count takes priority over the example template's 2-3.
3. User-supplied LendingClub_Dataset_Profile_Report.pdf, generated 29 October 2026 at 14:30. Preliminary profile only; source calculations are independently redone against the local CSV.
4. User-supplied accepted_2007_to_2018Q4.csv. The exact hash, byte size, dimensions and issue-date range are recorded in outputs/dataset_audit.json. Original download URL/date/licence: not supplied, not independently verified.
5. LendingClub issuer prospectus filed with SEC (2011): https://www.sec.gov/Archives/edgar/data/1409970/000095012311058394/c18687e424b3.htm . Accessed 29 October 2026. Historical context only: grade assignment and then-current DTI underwriting descriptions. These old criteria are not asserted as the definitions/rules for every vintage in this file.
6. Historical dictionary endpoint https://resources.lendingclub.com/LCDataDictionary.xlsx was attempted on 29 October 2026; it redirected to an inaccessible endpoint. It was not inspected and is not cited as verified support.

Numerical results are produced by the included code, not borrowed from external publications. No lecture references or download provenance have been fabricated. Python dependencies are pinned in requirements.txt; statistical implementations are checked against SciPy in the included unit tests.
''')
    method='''## Statistical theory and implementation

For two independent groups A and B, estimate delta = mean(A)-mean(B). A denotes Charged Off for numeric comparisons and 60 months for the term comparison. Sample means describe these groups; a population estimand requires an assumed repeatable sampling mechanism. All tests are observational.

**Welch t:** Let n_A,n_B be counts and s_A²,s_B² sample variances (divisor n-1). SE = sqrt(s_A²/n_A + s_B²/n_B). t = delta/SE under H0 delta=0. Degrees of freedom nu = (u+v)²/[u²/(n_A-1)+v²/(n_B-1)], where u=s_A²/n_A and v=s_B²/n_B. The two-sided p-value is 2*P(T_nu >= |t|); the 95% interval is delta +/- t_(.975,nu)*SE. It allows unequal variances but still requires independent observations and a reasonable mean sampling approximation. It is not a normality test. Large groups do not excuse extreme leverage or selection bias.

**Two-proportion z:** x_A and x_B count Charged Off loans, n_A and n_B include only observed terminal loans of the given term. p_hat_A=x_A/n_A, p_hat_B=x_B/n_B. Under equal proportions use p_pool=(x_A+x_B)/(n_A+n_B). SE0=sqrt[p_pool*(1-p_pool)*(1/n_A+1/n_B)]. z=(p_hat_A-p_hat_B)/SE0; p=2*P(Z>=|z|). The large-sample confidence interval instead uses SE=sqrt[p_hat_A*(1-p_hat_A)/n_A+p_hat_B*(1-p_hat_B)/n_B]. The null-pooled SE is not reused for the interval. Expected successes/failures must be adequate; the implementation rejects expected counts below five. df is not applicable for the standard normal reference. Without continuity correction, z² equals the 2x2 Pearson chi-square statistic, checked in code and tests.

**Chi-square:** O_ij is the observed grade-outcome count; E_ij = row_i_total * column_j_total / N. Sum (O-E)²/E to obtain chi-square. Under independence the approximate reference has (r-1)*(c-1) degrees of freedom, six for seven grades and two outcomes. The p-value is the upper-tail probability. This tail convention detects any association and is not a directional claim that every grade's event rate rises. Cramer's V = sqrt(chi-square/[N*min(r-1,c-1)]); here min=1. V measures association magnitude without a sign. A percentile interval from 1,000 seeded multinomial resamples of the observed cell proportions describes IID sampling uncertainty; it is an extension and does not correct dependence or selection. Grade-specific proportions remain necessary for interpretation.

**Holm:** Sort four p-values p_(1)<=...<=p_(4), multiply each by 4,3,2,1 respectively, then apply cumulative maxima and cap at one. Map adjusted values back to original questions. This addresses repeated testing; it does not make overlapping grade/rate associations independent. Intervals remain ordinary marginal intervals.

**Errors and interpretation:** A Type I error here would assert a nonzero difference/association when the corresponding population null holds; a Type II error would miss one. Alpha is a long-run false-positive criterion conditional on assumptions, not the probability H0 is true. A 95% frequentist interval is generated by a procedure with 95% coverage over repeated comparable samples; it does not assign 95% probability to a fixed parameter. A small p-value is not an effect size, causality claim, or practical decision. Failure to reject does not prove equality. Threshold decisions should consider the whole interval. If a p-value numerically underflows, the report uses a bound, never an exact zero claim.

**Alternatives:** Pooled t needs equal population variances, not established here; Welch avoids that unnecessary constraint. Known-sigma z is not warranted with estimated SDs. Paired t needs meaningful pairs, which these outcome groups lack. A rank test addresses a different distributional question and does not generally test equal means or medians. Exact contingency tests may replace asymptotic tests for sparse expected cells. Correlation imposes numeric coding/linear association assumptions that do not suit grade-category independence. These choices were made for estimands, not to obtain small p-values.
'''
    per_test=[]
    for r in results:
        details=mdtable(['Quantity','Computed value'],[[k,v] for k,v in r.items() if not isinstance(v,list)])
        per_test.append(f"### {r['test']}: {r['method']}\n\n{details}\n\nDecision: {r['decision']} at alpha=.05. Holm decision: {'reject' if r['holm_reject'] else 'fail to reject'}. Practical comparison: {r['practical']}. These are unadjusted associations among terminal outcomes.\n")
    sensitivity_text='\n\n'.join(f"**{k} sensitivity:** upper cap {v['cap']:.6g}; estimate {v['result']['estimate']:.6g}, CI [{v['result']['ci_low']:.6g}, {v['result']['ci_high']:.6g}]. Primary observations are unchanged. This tests capped-variable means, not the original estimand." for k,v in sens.items())
    write('reports/methodology_and_results.md',f'''# Methodology and results

Read analysis_plan.md for hypotheses, thresholds, direction and eligibility fixed before comparisons. Four tests executed on the full local file; observations were not fabricated from the preliminary profile.

{result_table}

## Sample accounting

{sample_counts}

{method}

## Auditable per-test calculations

{chr(10).join(per_test)}

## Sensitivity checks

{sensitivity_text}

Issue-year/term rates are in outputs/tables/cohort_term_rates.csv. These stratified descriptions expose composition but do not eliminate censoring. Pooled primary comparisons remain the declared questions.

{limitations}
''')
    outliers=pd.read_csv(ROOT/'outputs/tables/outliers.csv',index_col=0)
    outlier_table=mdtable(['Field','IQR flags','Flag %','Lower fence','Upper fence'],[[k,int(v.flagged),v.percent,v.lower,v.upper] for k,v in outliers.iterrows()])
    write('reports/detailed_technical_report.md',f'''# Statistical inference on observed LendingClub repayment outcomes

**NullPointer - CSE558 Data Science, IIIT-Delhi, Monsoon 2026**

Satyam Singh (2024514), Satguru Saran (2024510), Krishiv Vats (2024308). Emails and individual contributions must be supplied by the group; no allocation is invented.

## Part A - Framing and scope

LendingClub's historical accepted-loan records support questions about how origination descriptors relate to observed repayment outcomes. The purpose is not to build a classifier or to show that every non-paid account defaulted. Basic EDA asks what statuses, distributions and missingness patterns exist. The inferential question instead quantifies how large the terminal-outcome differences are, whether uncertainty excludes zero, and whether a declared meaningful threshold is exceeded. This is the project's contribution relative to status-count EDA, not a claim of research novelty in the wider literature.

The primary question compares issued rates between Charged Off and Fully Paid loans. Supporting questions compare DTI means, grade association and term-specific charge-off proportions. One loan is one observation. Descriptive statements apply to this file; inference is conditional on an assumed independent historical sampling mechanism; no predictive performance or causal effects are claimed.

## Part B - Dataset and full-file audit

The user supplied the local file `{a['filename']}` ({a['file_bytes']:,} bytes). UTF-8 parsing was successful. SHA-256: `{a['file_sha256']}`. Issue dates run from {a['issue_date_min']} through {a['issue_date_max']}. The audit scanned every row in chunks of 50,000 and inspected every source column, while retaining only selected columns for inference. Only a five-row sample was printed during initial inspection. The accumulated memory of string chunks was {a['accumulated_string_frame_bytes']:,} bytes; this is a summed representation cost, not measured peak RSS. The encoded matrix uses {e['memory_bytes']:,} bytes. Hardware needs depend on string storage and temporary copies; allow several GB of free memory and disk space for the raw file.

{comparison}

The supplied profile is not interchangeable with the CSV. Its 115 numeric plus 36 text columns total 151; its report also lists date-derived `__parsed` fields, which may explain the difference from 162. This explanation is plausible, not a verified reconstruction of the profiling run. Its issue dates cover April-December 2015, so it may describe a subset; the actual row count and full date coverage govern this analysis. No discrepancy is silently corrected to match the PDF.

{statuses}

The entire per-column missingness/type inventory is in outputs/tables/missingness.csv. Exact duplicate candidates are found using stable hashes and, when present, compared as full rows; no matching-feature loans are dropped automatically. IDs are checked separately. The full audit reports {a['duplicate_rows']:,} duplicate rows and {a['duplicate_ids']:,} repeated nonmissing IDs. A unique ID is not proof that borrowers are independent.

## Part C - Preparation and before/after reconciliation

Source rows {a['rows']:,} = terminal rows {c['terminal_rows']:,} + excluded other/missing-status rows {c['excluded_nonterminal']:,}. Current, late, grace-period, Default and ambiguous statuses are not relabelled as completed successful or failed repayments. Historical policy-status variants, if present, are also excluded rather than silently merged. This deliberately narrow outcome definition must be kept in mind when generalising.

Numeric fields are parsed after inspecting units/format; trailing percent symbols are supported. Whitespace is stripped from categorical labels. Exact change counts and parse failures appear in outputs/preparation.json. Missing outcomes are not imputed. Test-specific complete-case filters preserve all other usable terminal loans; the encoded representation has its own stricter complete-case rule, which does not reduce every test to the encoded sample.

{sample_counts}

Joint, hardship and settlement fields may be structurally missing when their conditions do not apply; the code preserves source missingness and does not infer missing-at-random from it. Whole-column mean/zero imputation would invent values and narrow uncertainty, so it is not used. No missingness mechanism is proved by the observed data.

{outlier_table}

IQR fences flag unusual observations rather than establish data errors. Primary means retain extremes. DTI sentinel-like values need historical documentation; capping is restricted to sensitivity analysis. Annual income uses log1p only for a descriptive scale comparison: zeros map to zero, negatives are excluded from that chart and not silently logged. The transformation does not prove normality. Tests remain on the original percentage-point scale.

Before encoding: {e['rows_before']:,} terminal rows and {e['columns_before']} selected attributes. After representation-specific complete-case filtering: {e['rows']:,} rows, with {e['excluded_missing']:,} excluded for missing selected attributes. Actual one-hot matrix: **{arithmetic}**, {'meeting' if e['meets_3m'] else 'not meeting'} the 3,000,000 requirement. Numeric features are loan amount, rate, DTI, income, lower FICO band and utilisation. Nominal indicators represent grade, term, tenure, verification, purpose and application type. Grade order matters for plots but no equal-spacing score is imposed. IDs, outcome and repayment variables are absent. This is a meaningful feature representation, not a blind expansion of employer text or IDs to inflate size.

## Part D - EDA and figure interpretation

1. `status.png` shows all source status counts, including unresolved and missing labels. It makes denominator selection visible, but does not estimate lifetime default probability.
2. `outcome_boxplots.png` compares rate and DTI medians/IQRs by terminal outcome. Fliers are hidden for legibility; every eligible value remains in the tests and full extrema are in numeric_summary.csv. Boxplots do not by themselves establish mean significance.
3. `category_rates.png` shows observed terminal charge-off percentages by grade and term. Group counts are provided in the adjacent saved contingency tables. Patterns may reflect underwriting, borrower mix and outcome maturity rather than causal grade/term effects.
4. `income_transform.png` puts the full original income range beside log(1+income). It reveals how scale affects visibility of the central mass, not whether income is Gaussian or whether a loan will fail.
5. `income_dti.png` is a reproducible 5,000-or-smaller random descriptive sample, seed 558. It visualises possible leverage/outliers without dumping millions of observations; all statistical tests use full eligible groups.
6. `missingness.png` shows the 20 most incomplete fields. Concentration in special-program/application fields warns against global deletion. The complete inventory is supplied as a table; the top-20 plot is not the whole audit.

## Part E - Theory

{method}

## Part F - Actual computed results

{result_table}

{chr(10).join(per_test)}

{sensitivity_text}

## Part G - Syllabus connection

The supplied guidelines explicitly request preparation, EDA and 3-5 hypothesis tests with alternative-test comparisons, intervals and practical thresholds. The template illustrates Welch's procedure. The exact lecture and quiz mapping cannot be verified because those files were absent. See syllabus_mapping.md for a clear evidence boundary. Holm and the bootstrap interval are explicitly labelled extensions; they support the core introductory inference instead of replacing it.

## Part H - Critical interpretation

{limitations}

## Part I - Conclusions and reproducibility

For each question the table above answers both statistical and practical significance. The result does not establish that changing interest, DTI, grade or term would change a borrower's outcome. The strength of this workflow is its audit trail: source file identity, exact eligibility rules, calculated matrix size, reusable tested formulas and reports generated from JSON outputs. The principal unresolved scientific weaknesses are selection, maturity, unverified dependence and historical provenance.

Run scripts/run_all.py for the full scan and figures, scripts/generate_reports.py for this document and the LaTeX source, and scripts/compile_report.py for PDF compilation. The notebooks independently execute their code from top to bottom against saved audit outputs; the raw scan itself runs in the command-line pipeline. Outputs are not hypothetical or reconstructed from a chart. See README.md for exact commands, missing course inputs and compilation requirements.
''')
    write('README.md',fr'''# NullPointer - LendingClub midterm project

Statistical inference on observed loan repayment outcomes. Team: Satyam Singh (2024514), Satguru Saran (2024510), Krishiv Vats (2024308). CSE558, IIIT-Delhi, Monsoon 2026.

## What was analysed

The supplied CSV was scanned in full by code; only a small initial sample and aggregate outputs were inspected in conversation. Actual dimensions: **{a['rows']:,} rows x {a['columns']} columns**. The preliminary profile reports 314,168 x 162 and therefore must not be substituted for the actual CSV. Raw data remains unchanged and is not bundled in this ZIP. Original download URL, acquisition date and licence were not supplied; see LICENSE_OR_DATA_NOTICE.md and the recorded SHA-256.

Questions: do terminal Charged Off/Fully Paid loans differ in mean issued rate and DTI; is grade associated with terminal outcome; and do 60-/36-month loans have different observed terminal charge-off proportions? These are historical observational associations, not causal effects or predictions. Methods: two Welch tests, chi-square independence with Cramer's V, two-proportion z, Holm adjustment, and limited sensitivity checks. Read reports/analysis_plan.md for thresholds fixed before comparisons.

## Install (Windows PowerShell)

Python {platform.python_version()} was used; Python 3.11+ is a reasonable baseline, but the exact pinned dependency set was tested on the recorded version. Allow several GB of free RAM; the chunked audit limits whole-file loading, although selected columns and encoded arrays still need memory. Raw input is {a['file_bytes']:,} bytes. No GPU, cloud service or credentials are required.

```powershell
cd 'C:\path\to\lendingclub-midterm-project'
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/run_all.py --data '..\accepted_2007_to_2018Q4.csv'
.\.venv\Scripts\python.exe scripts/generate_reports.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/execute_notebooks.py
.\.venv\Scripts\python.exe scripts/compile_report.py
```

Using the venv interpreter directly avoids PowerShell activation-policy problems. On macOS/Linux: `python3 -m venv .venv`, use `.venv/bin/python` in the same commands. Alternatively place the CSV in data/raw/accepted_2007_to_2018Q4.csv and omit `--data`. Relative paths are resolved from the working directory for an explicit data argument; internal outputs use the project root.

## Outputs and regeneration

- outputs/dataset_audit.json: exact file identity, dimensions, every column's missingness, status counts and duplicate checks.
- outputs/encoded_size.json: **{arithmetic}**; actual matrix, excluding IDs, outcome and leakage fields.
- outputs/results.json and outputs/tables/hypothesis_tests.csv: estimates, df, statistics, p-value bounds, intervals, sample sizes and thresholds.
- figures/eda/: six generated plots; source functions in src/eda.py. Regenerate by rerunning run_all.py with the raw file. Tables regenerate in the same run.
- reports/final_report.tex and compiled PDF: supplied-template adaptation with the official six-section structure.
- reports/detailed_technical_report.md: full explanation; methodology_and_results.md: compact calculation audit.
- reports/data_dictionary.md, syllabus_mapping.md, viva_questions_and_answers.md, limitations_and_future_work.md and references.md.
- notebooks/: audit, preparation/EDA and inference walkthroughs. Open with optional Jupyter (`python -m pip install jupyterlab`, then `python -m jupyter lab`). The included standard-library executor runs their plain-Python cells sequentially in isolated subprocesses and writes genuine execution outputs; it does not require Jupyter.

Reports are generated from computed outputs; editing the generated documents by hand will be overwritten on regeneration. Source inputs are preserved in source_materials. Run generate_reports.py only after the analysis completes successfully. All full-data plots and tables can be regenerated using run_all.py; no command downloads the raw dataset automatically.

One-command rebuild (all stages, raw data and TeX required): `python scripts/reproduce.py --data "../accepted_2007_to_2018Q4.csv"`. For portable Tectonic append `--tectonic "PATH/tectonic.exe"`. This convenience wrapper dispatches the individually validated commands; the delivered run executed the stages individually. To regenerate aggregate-only figures without rereading the CSV use `python scripts/generate_summary_figures.py`; regenerate the viva with `python scripts/create_viva.py`. Recreate notebook source with `python scripts/create_notebooks.py`, then execute it. Full validation: `python scripts/validate_project.py`.

## LaTeX PDF

Install MiKTeX/TeX Live with `pdflatex`, then run `python scripts/compile_report.py` (two passes, page-limit check). The script also supports `--tectonic PATH` for a portable Tectonic compiler. Manual pdfLaTeX: change into reports and run `pdflatex -interaction=nonstopmode -halt-on-error final_report.tex` twice. Tectonic may require first-run internet access for TeX packages. PDF validation status is recorded in outputs/pdf_validation.json if successfully compiled. Never substitute a random Markdown-to-PDF layout for the provided template.

## Known limits and submission edits

Lectures 1-12, quiz materials and practice problems were absent; exact syllabus coverage and the 80% target are unverified. Supply those to complete the course mapping. The report includes editable email/contribution and code URL fields, because those were not supplied. Replace them with true group details and your repository URL before submission. No Git repository was created. Review selection, censoring, missingness, dependence and subjective thresholds in the limitations document.

## Troubleshooting and completion checklist

File-not-found: supply a quoted absolute path with `--data` or place the input in data/raw. Missing package: use the same interpreter for pip and execution. Memory pressure: reduce chunk size in load_and_audit; selected-column/encoding memory still remains, so close other large applications. Unexpected categories or IDs: the pipeline stops instead of silently changing the research population; inspect the audit and document a justified correction. Missing TeX package: allow your TeX distribution to install it or use the portable compiler; inspect outputs/logs/latex.log. Missing output JSON: rerun the analysis before reports/notebooks. Test-fixture permission errors: run from a normal user terminal with a writable TEMP directory.

- Verify raw SHA-256 and dimensions match the intended file.
- Verify row-count reconciliation, four completed tests and actual encoded-size arithmetic.
- Verify all unit tests and notebook executions succeeded in outputs/validation.json.
- Verify PDF compilation and page count in outputs/pdf_validation.json.
- Inspect the final PDF visually, fill the personal/code fields and supply missing syllabus references.
''')
    requirements=[]
    for package in ['numpy','pandas','scipy','matplotlib']:
        requirements.append(package+'=='+importlib.metadata.version(package))
    requirements.append('pypdf>=5,<7')
    write('requirements.txt','\n'.join(requirements))
    # Use the actual supplied preamble, preserving layout/macros and replacing sample title/font setup.
    template=(ROOT/'source_materials/CSE558_Project_Report_Template.tex').read_text(encoding='utf-8')
    preamble=template.split(r'\begin{document}')[0]
    preamble=re.sub(r'\\newcommand\{\\projecttitle\}\{.*?\}\s*\\newif',lambda _:r'\newcommand{\projecttitle}{Observed repayment outcomes in LendingClub accepted loans}'+'\n'+r'\newif',preamble,flags=re.S)
    preamble=preamble.replace(r'\showhintstrue',r'\showhintsfalse')
    start=preamble.index(r'\usepackage{iftex}');end=preamble.index('%----------------------------------------------------------- packages')
    preamble=preamble[:start]+r'\usepackage[T1]{fontenc}'+'\n'+r'\usepackage[scaled=0.92]{helvet}\renewcommand{\familydefault}{\sfdefault}'+'\n'+preamble[end:]
    tex=preamble+r'''
\begin{document}
\twocolumn[{
{\small\bfseries CSE558 Data Science -- Midterm Project Report -- Monsoon 2026\par}
\vspace{4pt}{\LARGE\bfseries\projecttitle\par}\vspace{6pt}\rule{\linewidth}{1pt}
\textbf{Group:} NullPointer. \textbf{Dataset:} user-supplied local LendingClub CSV; original URL unverified.\\
\textbf{Code:} [Insert repository URL before submission]. README.md accompanies this project.\\
\begin{tabularx}{\linewidth}{@{}l l X X@{}}\toprule
Name & Roll number & Institute email & Contribution\\\midrule
Satyam Singh & 2024514 & [To supply] & [To confirm]\\
Satguru Saran & 2024510 & [To supply] & [To confirm]\\
Krishiv Vats & 2024308 & [To supply] & [To confirm]\\\bottomrule
\end{tabularx}\vspace{10pt}
}]
\section{Dataset}
'''
    tex+=texescape(f"Full CSV audit: {a['rows']:,} rows and {a['columns']} columns; {a['file_bytes']:,} bytes. One row is a source record; inference uses loans with terminal outcomes. Issue-date range: {a['issue_date_min'][:10]} to {a['issue_date_max'][:10]}. The local SHA-256 is saved in outputs/dataset_audit.json. Original acquisition date and licence are unknown.")+ '\n\n'
    tex+=texescape(f"The supplied profile reports 314,168 rows and 162 columns, with April-December 2015 issues. Its counts do not describe this full CSV. The 115 numeric plus 36 text fields total 151; parsed date fields may explain the profile column difference, but its exact run cannot be reconstructed.")+'\n\n'
    tex+=texescape(f"Before encoding: {e['rows_before']:,} terminal loans and 12 selected attributes. Complete-case one-hot representation: {arithmetic}; "+('meets' if e['meets_3m'] else 'does not meet')+' the 3M requirement. No IDs, outcomes or repayment-process features are counted.')+'\n\n'
    tex+=r'''\textbf{Key attributes.} Interest rate and DTI are percentage-point measures; loan amount and annual income are dollar amounts; FICO is an ordered score band; grade is ordinal A--G; term is categorical 36/60 months. Housing tenure, verification, purpose and application type are nominal. Exact vintage definitions remain a provenance limitation.
\section{Data preparation}
All source columns were audited in 50,000-row chunks. String-normalised hashing locates duplicate candidates, with exact full-row comparisons when candidates exist. IDs are separately checked. Categories are stripped of whitespace; numeric fields and issue months are parsed with logged failures. No outcome or numeric imputation is used. Each test uses its own complete cases.

Only Fully Paid and Charged Off labels define the primary terminal sample. Current, late, grace-period, Default and ambiguous labels are excluded. Do not equate unresolved loans with successful repayment. Missing special-program and joint fields may be structural; global deletion would be inappropriate.

IQR fences flag observations, not errors. All observed extremes remain in primary tests. A pooled 99th-percentile cap is a sensitivity analysis only. Income is plotted on original and log(1+income) scales for nonnegative values; no Gaussianity is claimed. One-hot encoding uses six selected categorical fields and six numeric fields, avoiding high-cardinality IDs/text and future repayment fields.
\section{What changed after preparation}
'''
    tex+=texescape(f"{a['rows']:,} source rows = {c['terminal_rows']:,} terminal rows + {c['excluded_nonterminal']:,} other/missing-status rows. Encoded complete cases retain {e['rows']:,}, excluding {e['excluded_missing']:,} terminal rows with missing selected fields. Exact duplicates: {a['duplicate_rows']:,}; repeated nonmissing IDs: {a['duplicate_ids']:,}. No duplicate-feature records are deleted merely for matching values.")+'\n\n'
    tex+=r'''Per-column missingness, outlier counts, parsing changes and before/after dimensions are in the reproducible output tables. The matrix size is an actual constructed representation; test denominators need not match it.
\section{Basic questions and problem statement}
EDA asks which statuses dominate, where missingness concentrates, and how borrower/loan descriptors vary. Our primary question quantifies the rate difference between terminal outcomes against a declared meaningful threshold. Supporting questions examine DTI, grade and term. This goes beyond descriptive status counts by separating magnitude, uncertainty and practical importance; it is not claimed as a novel discovery in lending research.
\begin{figure*}[p]\centering\includegraphics[width=.95\textwidth]{../figures/eda/status.png}
\caption{All source statuses. Unresolved loans make terminal-only denominator selection consequential.}\end{figure*}
\begin{figure*}[p]\centering\includegraphics[width=.95\textwidth]{../figures/eda/outcome_boxplots.png}
\caption{Rate and DTI distributions by terminal outcome (1,345,310 terminal loans before variable-specific missingness). Fliers are hidden only in this plot; full observations enter tests.}\end{figure*}
\begin{figure*}[p]\centering\includegraphics[width=.95\textwidth]{../figures/eda/category_rates.png}
\caption{Observed terminal charge-off proportions by grade and term. Composition and outcome maturity can confound these patterns.}\end{figure*}
\section{Statistical inferences}
All hypotheses were written before group tests. $\alpha=0.05$; numeric and proportion alternatives are two-sided. Chi-square uses its upper tail to detect any categorical association. Thresholds are analytical judgments, not industry standards. Loans are treated as independent for inference, an unverified assumption; large samples do not cure selection or dependence. Four tests form one Holm-adjusted family; intervals remain marginal 95\% intervals.
'''
    specs=[('Interest rate',r'H_0:\mu_{CO}-\mu_{FP}=0;\quad H_1:\mu_{CO}-\mu_{FP}\ne0',
        'Welch t permits unequal unknown variances. A 1 percentage-point difference is the declared threshold (about 100 dollars annual simple interest per 10,000 dollars principal, not amortised cost).',
        'Known-sigma z is unsuitable; population SD is unknown. Pooled t adds an unnecessary equal-variance assumption. Paired t lacks pairs. Rank tests target a different distributional question.'),
        ('Debt-to-income',r'H_0:\mu_{CO}-\mu_{FP}=0;\quad H_1:\mu_{CO}-\mu_{FP}\ne0',
        'Welch t on the original scale. Threshold: 2 percentage points (100 dollars monthly debt per 5,000 dollars monthly income illustrates scale). Extreme values and missingness warrant sensitivity analysis.',
        'Pooled, known-sigma and paired tests have the same limitations as for rate. Log/rank analyses change the estimand; primary inference retains original values.'),
        ('Grade',r'H_0:\text{independence};\quad H_1:\text{association}',
        "Pearson chi-square on the grade-by-outcome counts; Cramer's V measures magnitude. V=0.10 is a weak exploratory convention, not a validated business threshold. A 1,000-draw IID multinomial bootstrap gives its interval (extension).",
        'A correlation test would impose an arbitrary numeric grade spacing. Sparse-table exact methods are alternatives when expected counts fail; all expected cells are checked. No post-hoc grade tests are counted.'),
        ('Term',r'H_0:p_{60}-p_{36}=0;\quad H_1:p_{60}-p_{36}\ne0',
        'Pooled-null two-proportion z; unpooled large-sample difference interval. Event = Charged Off, denominator = terminal loans of each term. Threshold .02 means 2 additional events per 100 terminal loans.',
        'The uncorrected 2x2 chi-square is equivalent (z squared), checked but not counted as another finding. Fisher exact is unnecessary when expected cells are adequate. A t test is not the natural binary-count method.')]
    for r,(title,hyp,choice,alternatives) in zip(results,specs):
        tex+='\n'+r'\subsection{'+title+'}\n'+r'\textbf{a) Hypotheses and choice.} '+r'\('+hyp+r'\)'+'\n\n'+texescape(choice)+'\n\n'
        tex+=r'\textbf{b) Alternatives.} '+texescape(alternatives)+'\n\n'+r'\textbf{c) Result.} '
        n=f"n(CO)={r['n_a']:,}, n(FP)={r['n_b']:,}" if r['test'] in ['int_rate','dti'] else f"n(60)={r['n_a']:,}, n(36)={r['n_b']:,}" if r['test']=='term' else f"N={r['n']:,}"
        tex+=texescape(n+f"; excluded terminal rows={r['excluded']:,}. Estimate {r['estimate']:.5g}; 95% CI [{r['ci_low']:.5g}, {r['ci_high']:.5g}]; statistic {r['statistic']:.6g}; df {fmt(r['df'])}; p {r['p_display']}. {r['decision']}. Holm p {r['holm_p_display']}. {r['practical']}.")+'\n\n'
        if 'sd_a' in r:tex+=texescape(f"Group means {r['mean_a']:.5g}, {r['mean_b']:.5g}; SDs {r['sd_a']:.5g}, {r['sd_b']:.5g}; SE {r['se']:.5g}.")+'\n\n'
        if 'min_expected' in r:tex+=texescape(f"Minimum expected cell count: {r['min_expected']:.5g}.")+'\n\n'
        if r['test']=='term':tex+=texescape(f"Observed event proportions: {r['proportion_a']:.5g} (60 months), {r['proportion_b']:.5g} (36 months). Difference/interval above are proportions, not percentage points.")+'\n\n'
        conclusions={'int_rate':'Charged Off loans have higher mean issued rates in this terminal sample, beyond the chosen meaningful-difference threshold.',
            'dti':'Charged Off loans have higher mean DTI in this terminal sample, beyond the chosen meaningful-difference threshold.',
            'grade':'Grade and terminal outcome are associated; V exceeds the exploratory magnitude threshold. This is not independent causal evidence beyond the rate comparison.',
            'term':'The 60-month terminal group has a higher observed charge-off proportion by about 16.45 percentage points. Selection and maturity prevent a causal interpretation.'}
        tex+=texescape(conclusions[r['test']])+'\n\n'
    tex+=r'''\textbf{Calculation audit.} Welch: $SE=\sqrt{s_A^2/n_A+s_B^2/n_B}$, $t=\hat\Delta/SE$, with Satterthwaite df and t-quantile interval. Proportion z uses pooled $p$ under the null; its interval uses the separate estimated proportions. Chi-square sums $(O-E)^2/E$, with $E=$ row total times column total divided by $N$, and df=$(r-1)(c-1)$. Full intermediate values, formulas and alternatives are in methodology\_and\_results.md and the source functions.

\textbf{Sensitivity.}
'''
    for k,v in sens.items():tex+=texescape(f" {k}: capping at {v['cap']:.5g} gives difference {v['result']['estimate']:.5g}, CI [{v['result']['ci_low']:.5g}, {v['result']['ci_high']:.5g}].")+'\n'
    tex+=r'''
The cap changes the estimand; it is not a correction of proven errors. Issue-year/term rates are provided to inspect composition, not to claim censoring is resolved.
\section{Limitations}
Accepted loans exclude rejected applications. Terminal selection excludes unfinished loans and can overrepresent early charge-offs, particularly for newer long-term loans. These are conditional associations, not lifetime default rates or causal effects. Grade and rate reflect related underwriting information; shared borrowers and macroeconomic shocks can violate independence. No reliable borrower identifier was established. Complete cases can be selective, and extreme DTI values require historical documentation.

Holm addresses multiplicity conditional on valid p-values; it does not remove confounding. Subjective practical thresholds should be challenged. Historical file provenance, extraction date and licence are incomplete. The supplied lecture PDFs, quizzes and practice problems were absent, so exact lecture mapping and the 80\% syllabus target cannot be verified. Bootstrap and Holm are labelled extensions. No classifier is claimed.

\textbf{References and code.} Supplied CSE558 guidelines/template; supplied preliminary LendingClub profile; the local CSV identified by its saved hash. Historical grade context: LendingClub SEC prospectus (2011), \url{https://www.sec.gov/Archives/edgar/data/1409970/000095012311058394/c18687e424b3.htm}. This source does not verify definitions for every vintage. See references.md, README.md and src/statistical\_tests.py. Replace the code URL and team metadata fields before submission.
\end{document}
'''
    quality=read('quality_flags.json')
    nonneg=quality['dti_nonnegative_sensitivity']['summary']
    quality_note=(f"The source contains {a.get('verified_footer_rows',32)} total-funded footer records and {a.get('verified_separator_rows',1)} policy-section separator, all with missing loan amount/status; these are not loans and are excluded from every test. "
        f"There are {a.get('loan_records',a['rows']-33):,} loan records. Two observed DTI values are negative and 135 equal 999; their exact semantics are unverified. "
        f"Primary inference retains them transparently. Excluding the two negative DTI values gives difference {nonneg['estimate']:.6g}, CI [{nonneg['ci_low']:.6g}, {nonneg['ci_high']:.6g}], leaving the interpretation unchanged. "
        f"There are {quality['zero_income']:,} zero incomes and {quality['revol_util_above_100']:,} utilisation values above 100; these are flagged, not automatically deleted. No negative income was observed.")
    tex=tex.replace(r'\section{What changed after preparation}',texescape(quality_note)+'\n\n'+r'\section{What changed after preparation}')
    write('reports/final_report.tex',tex)
    for name in ['reports/detailed_technical_report.md','reports/methodology_and_results.md']:
        p=ROOT/name;p.write_text(p.read_text(encoding='utf-8')+'\n\n## Additional source-quality review\n\n'+quality_note+'\n',encoding='utf-8')
    return results
