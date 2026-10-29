"""Clear tables, acronym reference and a comprehensive project entry point."""
import json,re
import pandas as pd
from .config import ROOT

GLOSSARY=[('DTI','Debt-to-income ratio','How much income is committed to debt obligations; expressed as a percentage. Exact historical debt definitions require source documentation.'),('FICO','Fair Isaac Corporation credit score','A credit-history score; a higher score generally indicates stronger recorded credit history, not certainty of repayment.'),('CI','Confidence interval','A range from a procedure with stated long-run coverage, conditional on sampling assumptions.'),('SD','Standard deviation','How spread out individual observations are.'),('SE','Standard error','How uncertain an estimated mean or difference is.'),('df','Degrees of freedom','The reference distribution parameter used by a statistical test.'),('IQR','Interquartile range','Third quartile minus first quartile: the spread of the middle half of values.'),('CO','Charged Off','Recorded terminal charge-off outcome; not a synonym for every unresolved or late loan.'),('FP','Fully Paid','Recorded terminal full-repayment outcome.'),('EDA','Exploratory data analysis','Plots and summaries used to understand the observations.'),('H0','Null hypothesis','The equality or independence statement tested.'),('H1','Alternative hypothesis','The difference or association statement investigated.'),('IID','Independent and identically distributed','A working sampling assumption used by the bootstrap; not verified for loans.'),('USD','United States dollars','Currency used for recorded income and principal amounts.'),('CSV','Comma-separated values','The source table file format.'),('SHA-256','Secure Hash Algorithm, 256-bit','A file fingerprint used to identify the exact input.'),('Holm','Holm multiple-testing adjustment','An adjustment addressing the four-test family; a name, not an acronym.'),('p-value','Null-tail probability','Probability of a statistic at least as extreme under the null and working assumptions; not the probability the null is true.'),('alpha','Significance level','The chosen false-positive criterion, 0.05 for these tests.'),('percentage point','Absolute difference between percentages','For example, 20% minus 18% is 2 percentage points, not a 2% relative increase.')]
ATTR=[('id','Loan identifier','Tracks a loan; has no numerical risk interpretation.'),('loan_status','Recorded loan outcome','Defines Fully Paid and Charged Off groups; Current is unresolved.'),('issue_d','Loan issue month','Shows loan vintage and helps explain maturity differences.'),('loan_amnt','Requested loan amount, in dollars','Shows the size of the loan, not the amount repaid.'),('int_rate','Issued annual interest rate, in percent','The price charged for borrowing; tested between outcome groups.'),('dti','Debt-to-income ratio, in percent','A debt-burden measure; higher means more debt relative to income.'),('annual_inc','Reported annual income, dollars per year','Borrower income scale; zero/extreme values need context.'),('fico_range_low','Lower end of the origination credit-score band','An approximate credit-score range endpoint, not the exact score.'),('revol_util','Revolving credit utilisation, in percent','How much of available revolving credit is used; unusually large values need review.'),('grade','Recorded loan grade, A through G','An ordered underwriting label, not an equally spaced number.'),('term','Scheduled loan duration, in months','The comparison uses 36-month and 60-month loans.'),('home_ownership','Reported housing situation','For example, rent, mortgage or own; a category, not wealth itself.'),('verification_status','Recorded income-verification category','Describes verification status; does not guarantee truthful income.'),('purpose','Stated reason for borrowing','For example, debt consolidation; self-reported category.'),('application_type','Individual or joint application','Helps interpret why joint-applicant fields may be missing.'),('charged_off','Derived 1 for Charged Off, 0 for Fully Paid','Defined only in the selected terminal-outcome sample.')]
def mdtable(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)+'\n'
def esc(s):return str(s).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
def apply():
    r=json.loads((ROOT/'outputs/results.json').read_text());p=ROOT/'reports/final_report.tex';tex=p.read_text()
    replacements={'missingness.png':'loan_purposes.png','income_transform.png':'income_and_loan_amount.png','../inference/effect_intervals.png':'../inference/group_mean_comparison.png'}
    for old,new in replacements.items():tex=tex.replace(old,new)
    tex=tex.replace('Missingness in the 20 most incomplete fields. Conditional application and repayment-program fields require contextual handling.','Stated borrowing purposes. The count bars show which reasons for borrowing are most common among loan records.')
    tex=tex.replace('Annual income on original and log(1+income) scales. Changing scale reveals the central mass; it does not establish normality.','Left: annual income on the natural log(1+income) scale. Right: requested loan amounts in dollars. The latter shows the size and common values of requested loans; logging income does not retain its original dollar-scale interpretation.')
    tex=tex.replace('Computed estimates with marginal 95 percent confidence intervals and declared practical thresholds. Each panel retains its own units.','Average interest rate and debt-to-income ratio for Fully Paid and Charged Off loans. Both axes begin at zero. Charged Off loans have higher group averages; test tables quantify uncertainty and do not establish causation.')
    pattern=r'(\\subsection\{(Interest rate|Debt-to-income|Grade|Term)\}\s*)(.*?)(?=\\subsection|\\textbf\{Calculation audit\.\})'
    titles=['Interest rate','Debt-to-income','Grade','Term']
    def tab(m):
        v=r[titles.index(m[2])];old=m[3]
        # Preserve rationale, alternatives and interpretation from the existing table as a note.
        content=old.split('\\toprule',1)[-1].rsplit('\\bottomrule',1)[0]
        oldrows=re.split(r'\\\\\\midrule\s*',content)
        retained=[]
        for row in oldrows:
            if ' & ' not in row:continue
            label,value=row.split(' & ',1);value=value.rstrip().removesuffix('\\\\').strip()
            if label.startswith('b)'):retained.append(('Why not alternatives?',value))
            elif label=='Detail' and not value.startswith(('Group means','Minimum expected','Observed event')):retained.append(('Interpretation' if len(value)>40 and not value.startswith(('Welch','Pearson','Pooled-null')) else 'Why this test?',value))
        numeric=v['test'] in ['int_rate','dti'];term=v['test']=='term'
        hypothesis='The two population means are equal.' if numeric else 'Grade and terminal outcome are independent.' if not term else 'The two population charge-off proportions are equal.'
        alt='The two means differ.' if numeric else 'Grade and terminal outcome are associated.' if not term else 'The two charge-off proportions differ.'
        factor=100 if term else 1;units='percentage points' if numeric or term else "Cramer's V (association magnitude)"
        sample=f"Charged Off: {v['n_a']:,}; Fully Paid: {v['n_b']:,}." if numeric else f"60 months: {v['n_a']:,}; 36 months: {v['n_b']:,}." if term else f"{v['n']:,} loans, seven grades, two outcomes."
        rows=[('Null hypothesis (H0)',hypothesis),('Alternative (H1)',alt),('Test / direction',v['method']+'; '+('upper-tail independence test' if v['test']=='grade' else 'two-sided')),('Significance level','0.05; Holm adjustment across four tests.'),('Eligible sample',sample+f" Excluded terminal rows: {v['excluded']:,}."),('Practical threshold',f"{v['threshold']*factor:.3g} {units}; analyst judgement, not an industry standard."),('Estimated difference' if v['test']!='grade' else 'Association size',f"{v['estimate']*factor:.5g} {units}."),('95% confidence interval',f"[{v['ci_low']*factor:.5g}, {v['ci_high']*factor:.5g}] {units}; marginal interval."),('Test statistic',f"{v['statistic']:.6g}; degrees of freedom: "+(f"{v['df']:.6g}." if v['df'] is not None else 'not applicable.')),('Probability / decision',v['p_display']+'; reject the null hypothesis. Holm-adjusted decision also rejects.')]
        if numeric:rows.append(('Group averages',f"Charged Off {v['mean_a']:.5g}%; Fully Paid {v['mean_b']:.5g}%. Standard error of difference {v['se']:.5g} percentage points."))
        elif term:rows.append(('Group event rates',f"60 months {100*v['proportion_a']:.3f}%; 36 months {100*v['proportion_b']:.3f}%."))
        if 'min_expected' in v:rows.append(('Approximation check',f"Smallest expected count {v['min_expected']:.5g}; above five."))
        rows=[(k,esc(val)) for k,val in rows]+retained
        return m[1]+r'\begin{tabularx}{\linewidth}{@{}>{\bfseries\raggedright\arraybackslash}p{.28\linewidth} X@{}}\toprule'+'\n'+(r'\\\midrule'+'\n').join(esc(k)+' & '+value for k,value in rows)+r'\\\bottomrule\end{tabularx}'+'\n\n'
    tex=re.sub(pattern,tab,tex,flags=re.S)
    # Define abbreviations at first narrative occurrence, retaining familiar dataset field names.
    for token,expansion in [('DTI','debt-to-income ratio (DTI)'),('IQR','interquartile range (IQR)'),('IID','independent and identically distributed (IID)'),('FICO','Fair Isaac Corporation credit score (FICO)')]:
        tex=re.sub(r'\b'+token+r'\b',lambda _:expansion,tex,count=1)
    glossary=r'\clearpage\onecolumn\section{Plain-language reference}\small'+'\n'
    glossary+=r'\textbf{Selected source and derived attributes.} The complete source inventory is in attributes\_plain\_language.md. Historical definitions remain subject to the provenance caveat.'+'\n'
    glossary+=r'\begin{tabularx}{\linewidth}{@{}l X X@{}}\toprule Attribute & Plain meaning & What it tells us\\\midrule'+'\n'
    glossary+=(r'\\'+'\n').join(' & '.join(esc(x) for x in row) for row in ATTR)+r'\\\bottomrule\end{tabularx}'+'\n'+r'\medskip'+'\n'
    glossary+=r'\textbf{Acronyms and statistical shorthand.}\par\begin{tabularx}{\linewidth}{@{}l X@{}}\toprule Short form & Expanded meaning\\\midrule'+'\n'
    glossary+=(r'\\'+'\n').join(esc(row[0])+' & '+esc(row[1]) for row in GLOSSARY[:16])+r'\\\bottomrule\end{tabularx}'+'\n'
    tex=tex.replace(r'\end{document}',glossary+r'\end{document}');p.write_text(tex)
    (ROOT/'reports/acronym_directory.md').write_text('# Acronym directory and statistical reading guide\n\n'+mdtable(['Short form','Expanded meaning','In simple language'],GLOSSARY),encoding='utf-8')
    attrtext='# Attribute guide in everyday language\n\n## Attributes used in this project\n\n'+mdtable(['Attribute','Plain meaning','What it signifies'],ATTR)
    attrtext+='\n## Complete source inventory\n\nAll source fields are listed below with their observed missing counts and analytical decision. For unused fields without a verified historical definition, the expanded name is a reading aid only; it must not be presented as a certified definition. See the detailed selected-attribute table above for the variables actually used.\n\n'
    mapping={x[0]:x[1]+'; '+x[2] for x in ATTR}; expansions={'amnt':'amount','inc':'income','int':'interest','inv':'investor','acc':'account','accts':'accounts','num':'number','mths':'months','mo':'months','yrs':'years','revol':'revolving credit','util':'utilisation','bal':'balance','bc':'bankcard','il':'installment loan','tl':'trade line (credit account)','tot':'total','cur':'current','pymnt':'payment','rec':'received','prncp':'principal','inq':'credit inquiries','sec':'secondary','app':'applicant','fico':'credit score','delinq':'delinquency','dlq':'delinquency','dpd':'days past due','pct':'percentage','hi':'high','lim':'limit','coll':'collection','amt':'amount','rcnt':'recent','op':'opened','derog':'derogatory credit event','emp':'employment','d':'date'}
    rows=[]
    for _,row in pd.read_csv(ROOT/'outputs/tables/feature_audit.csv').iterrows():
        name=row['feature']; meaning=mapping.get(name,' '.join(expansions.get(t,t) for t in name.split('_'))+' (name-based reading aid; exact vintage definition unverified)')
        rows.append([name,meaning,int(row['missing_count']),row['decision']])
    attrtext+=mdtable(['Source field','Meaning / reading aid','Missing source records','Use and caution'],rows)
    (ROOT/'reports/attributes_plain_language.md').write_text(attrtext,encoding='utf-8')
    readme=ROOT/'README.md';old=readme.read_text(encoding='utf-8')
    old=old.replace('figures/eda/missingness.png','figures/eda/loan_purposes.png').replace('figures/eda/income_transform.png','figures/eda/income_and_loan_amount.png').replace('figures/inference/effect_intervals.png','figures/inference/group_mean_comparison.png')
    start=old.index('## Plot gallery and reading guide');end=old.index('## Complete deliverable directory')
    gallery='## Plot gallery and reading guide\n\n'
    for path,title,explanation in [('eda/status','1. Recorded loan statuses','Current loans are unresolved, which determines the eligible denominator.'),('eda/outcome_boxplots','2. Interest-rate and debt-to-income distributions','The centre line is the median; the box is the middle half of values. Hidden fliers remain in tests.'),('eda/category_rates','3. Charge-off proportions by grade and term','Category differences describe terminal loans and are affected by maturity and borrower mix.'),('eda/loan_purposes','4. Why borrowers requested loans','A familiar count bar chart makes common borrowing reasons easy to compare.'),('eda/income_and_loan_amount','5. Income and requested loan sizes','Left: natural log(1 + annual income). Right: a conventional dollar-scale loan-amount histogram. The logarithm changes interpretation and does not retain all original-scale information.'),('eda/income_dti','6. Income and debt-to-income scatter','Each point is one sampled terminal loan. Outlying points warn against treating averages as the whole story.'),('inference/group_mean_comparison','7. Two easy-to-read group-average comparisons','Zero-based bars compare the average issued interest rate and debt-to-income ratio for Fully Paid and Charged Off loans. Test tables provide confidence intervals.')]:
        gallery+=f'### {title}\n\n![{title}](figures/{path}.png)\n\n{explanation}\n\n'
    old=old[:start]+gallery+old[end:]
    contents='''## Start here: understand the project in one pass

1. **Question:** How do issued loan characteristics differ between loans recorded as Fully Paid and Charged Off?
2. **Population:** The source contains 2,260,701 records, including 33 metadata records. Tests use 1,345,310 terminal-outcome loans; unresolved outcomes are excluded.
3. **Preparation:** Audit every column, check identifiers and duplicates, strip category whitespace, parse measurements, and use test-specific observed values. Preserve unusual measurements in primary tests and disclose sensitivities.
4. **Evidence:** Compare the group means for interest rate and debt burden, then grade association and term-specific charge-off proportions. Report magnitude, uncertainty and practical thresholds.
5. **Interpretation:** These are conditional historical associations. Borrower mix, incomplete follow-up and dependence prevent causal claims.
6. **Reproduce:** Follow the installation and one-command rebuild instructions below. The raw source file is external; generated figures and reports are already included.

## Navigation

| Need | Open |
| --- | --- |
| Submission report, including plain-language reference | [Final PDF](reports/final_report.pdf) |
| Every acronym and statistical symbol explained | [Acronym directory](reports/acronym_directory.md) |
| Selected attributes and all 151 source fields | [Plain-language attribute guide](reports/attributes_plain_language.md) |
| Exact units, derived variables and temporal caveats | [Data dictionary](reports/data_dictionary.md) |
| Test formulas, hypotheses, alternatives and actual results | [Methodology](reports/methodology_and_results.md) |
| Full explanation and limitations | [Technical report](reports/detailed_technical_report.md) |
| Presentation preparation | [Viva questions](reports/viva_questions_and_answers.md) |
| Machine-readable findings | [Result records](outputs/results.json) |

## What the four tests say

'''
    summaries=[]
    for v in r:
        scale=100 if v['test']=='term' else 1
        summaries.append([v['test'],v['method'],f"{scale*v['estimate']:.4f}",f"{scale*v['ci_low']:.4f} to {scale*v['ci_high']:.4f}",'percentage points' if v['test']!='grade' else "Cramer's association measure",'Above the declared threshold; association only'])
    contents+=mdtable(['Question / variable','Test','Estimate','95% confidence interval','Units','Interpretation'],summaries)+'\nThe numeric contrasts are Charged Off minus Fully Paid; the term contrast is 60 months minus 36 months. All four null hypotheses are rejected under the working assumptions, including Holm adjustment. Statistical evidence is not proof of causation.\n\n'
    old=old.replace('## Project theme and features',contents+'## Project theme and features',1)
    old+='\n## Acronyms and selected attributes at a glance\n\n'+mdtable(['Short form','Expansion','Meaning'],GLOSSARY)+'\n'+mdtable(['Attribute','Plain meaning','What it signifies'],ATTR)
    old+='\n## Rebuilding the replacement plots\n\nRun `python scripts/generate_explainer_figures.py --data "../accepted_2007_to_2018Q4.csv"` once to create the aggregate histogram and purpose counts. Later runs can omit `--data` to use `outputs/tables/explainer_plot_counts.json`. This cache stores bin counts and category totals, not borrower rows. Then regenerate reports with `python scripts/generate_reports.py` and compile the PDF.\n'
    readme.write_text(old,encoding='utf-8')
    # Keep companion explanations aligned with the revised gallery.
    for filename in ['detailed_technical_report.md','methodology_and_results.md','data_dictionary.md','viva_questions_and_answers.md','limitations_and_future_work.md','analysis_plan.md','syllabus_mapping.md']:
        path=ROOT/'reports'/filename
        content=path.read_text(encoding='utf-8')
        if '## Reading help' not in content:
            content+='\n\n## Reading help\n\n[Acronym directory](acronym_directory.md) expands statistical shorthand. [Plain-language attribute guide](attributes_plain_language.md) explains the selected variables and inventories all source fields.\n'
        for token,expansion in [('DTI','debt-to-income ratio (DTI)'),('IQR','interquartile range (IQR)'),('IID','independent and identically distributed (IID)'),('SE','standard error (SE)'),('SD','standard deviation (SD)'),('EDA','exploratory data analysis (EDA)'),('CI','confidence interval (CI)')]:
            phrase=expansion.rsplit(' (',1)[0]
            content=re.sub(r'(?:'+re.escape(phrase)+r' \(){2,}'+token+r'\){2,}',lambda _:expansion,content)
            if expansion not in content:content=re.sub(r'\b'+token+r'\b',lambda _:expansion,content,count=1)
        content=content.replace('`income_transform.png` puts the full original income range beside log(1+income). It reveals how scale affects visibility of the central mass, not whether income is Gaussian or whether a loan will fail.','`income_and_loan_amount.png` pairs log(1+income) with the requested-loan-amount histogram. It shows income on a compressed scale and the sizes of requested loans; no Gaussianity is claimed.')
        content=content.replace('`missingness.png` shows the 20 most incomplete fields. Concentration in special-program/application fields warns against global deletion. The complete inventory is supplied as a table; the top-20 plot is not the whole audit.','`loan_purposes.png` shows how many loans were requested for each stated purpose. `group_mean_comparison.png` contrasts the two outcome groups on original-scale average rate and debt burden. Missingness remains fully audited in the tables.')
        path.write_text(content,encoding='utf-8')
