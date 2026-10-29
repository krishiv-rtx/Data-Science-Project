"""Presentation-only refinements; empirical outputs and narrative are preserved."""
import re
from .config import ROOT

def refine():
    p=ROOT/'reports/final_report.tex'; text=p.read_text(encoding='utf-8')
    text=text.replace('[Insert repository URL before submission]',r'\url{https://github.com/krishiv-rtx/Data-Science-Project}')
    text=text.replace(r'{@{}l l X X@{}}',r'{@{}l l X@{}}')
    text=text.replace('Institute email & Contribution','Institute email')
    for name,email in [('Satyam Singh','satyam24514@iiitd.ac.in'),('Satguru Saran','satguru24510@iiitd.ac.in'),('Krishiv Vats','krishiv24308@iiitd.ac.in')]:
        text=re.sub(re.escape(name)+r'( & \d+ & )\[To supply\] & \[To confirm\]',lambda m:name+m[1]+email,text)
    text=text.replace('Replace the code URL and team metadata fields before submission.','Project code and README: '+r'\url{https://github.com/krishiv-rtx/Data-Science-Project}.')
    def table(rows):
        return r'\begin{tabularx}{\linewidth}{@{}>{\bfseries\raggedright\arraybackslash}p{.22\linewidth} X@{}}\toprule'+'\n'+('\\\\\midrule\n'.join(k+' & '+v.strip() for k,v in rows))+r'\\\bottomrule\end{tabularx}'+'\n\n'
    # Keep each original paragraph, reorganising the template's a/b/c fields as rows.
    pattern=r'(\\subsection\{(?:Interest rate|Debt-to-income|Grade|Term)\}\s*)(.*?)(?=\\subsection|\\textbf\{Calculation audit\.\})'
    def test_table(m):
        body=m[2]; parts=re.split(r'\\textbf\{([abc]\) [^}]+)\}',body)
        rows=[]
        for i in range(1,len(parts),2):
            label=parts[i]; content=parts[i+1].strip()
            for j,paragraph in enumerate(re.split(r'\n\s*\n',content)):
                if paragraph.strip():rows.append((label if j==0 else 'Detail',paragraph))
        return m[1]+table(rows)
    text=re.sub(pattern,test_table,text,flags=re.S)
    # Dataset and preparation use the same labelled table idiom as the supplied template.
    for section,labels in [('Dataset',['Source audit','Profile comparison','Encoded size','Attributes']),('Data preparation',['Audit and parsing','Eligibility','Outliers / encoding','Quality flags'])]:
        pattern=r'(\\section\{'+re.escape(section)+r'\}\s*)(.*?)(?=\\section)'
        def section_table(m):
            paragraphs=[v.strip() for v in re.split(r'\n\s*\n',m[2]) if v.strip()]
            # The quality paragraph follows the preceding preparation paragraph on one line.
            if section=='Data preparation' and len(paragraphs)==3:
                paragraphs=paragraphs[:2]+paragraphs[2].split('\nThe source contains')
                paragraphs[-1]='The source contains'+paragraphs[-1]
            return m[1]+table([(labels[min(i,len(labels)-1)],v) for i,v in enumerate(paragraphs)])
        text=re.sub(pattern,section_table,text,flags=re.S)
    extra=''
    for name,caption in [('missingness','Missingness in the 20 most incomplete fields. Conditional application and repayment-program fields require contextual handling.'),('income_transform','Annual income on original and log(1+income) scales. Changing scale reveals the central mass; it does not establish normality.'),('income_dti','Seeded descriptive income--DTI scatter. Extreme values and heterogeneous borrower characteristics limit simple interpretations.'),('../inference/effect_intervals','Computed estimates with marginal 95 percent confidence intervals and declared practical thresholds. Each panel retains its own units.')]:
        extra+=r'\begin{figure*}[p]\centering\includegraphics[width=.90\textwidth,height=.32\textheight,keepaspectratio]{../figures/eda/'+name+'.png}\n'+r'\caption{'+caption+r'}\end{figure*}'+'\n'
    text=text.replace(r'\section{Statistical inferences}',extra+r'\section{Statistical inferences}')
    p.write_text(text,encoding='utf-8')
    readme=ROOT/'README.md'; old=readme.read_text(encoding='utf-8')
    old=old.replace('The report includes editable email/contribution and code URL fields, because those were not supplied. Replace them with true group details and your repository URL before submission.','The report includes the supplied institute emails and project repository URL. The contribution column has been removed as requested.')
    tree=[]
    def walk(folder,prefix=''):
        items=sorted([p for p in folder.iterdir() if p.name not in {'__pycache__','tmp','.venv','.ipynb_checkpoints'} and p.suffix not in {'.pyc','.aux','.out','.log'}],key=lambda p:(not p.is_dir(),p.name))
        for i,item in enumerate(items):
            last=i==len(items)-1;tree.append(prefix+('â””â”€â”€ ' if last else 'â”œâ”€â”€ ')+item.name+('/' if item.is_dir() else ''))
            if item.is_dir():walk(item,prefix+('    ' if last else 'â”‚   '))
    walk(ROOT)
    intro='''# NullPointer | LendingClub repayment outcomes

**CSE558 Data Science Â· IIIT-Delhi Â· Monsoon 2026**

[Project repository](https://github.com/krishiv-rtx/Data-Science-Project) Â· [Final PDF report](reports/final_report.pdf) Â· [Statistical methodology](reports/methodology_and_results.md) Â· [Technical explanation](reports/detailed_technical_report.md)

## Project theme and features

A reproducible investigation of how issued loan characteristics relate to observed terminal repayment outcomes. The project connects full-file quality auditing, interpretable exploratory plots, four statistical tests, confidence intervals and practical significance. The visual theme uses teal for observed patterns and amber for comparison thresholds. Findings describe historical associations subject to selection, maturity and dependence limitations.

| Team member | Roll number | Institute email |
| --- | --- | --- |
| Satyam Singh | 2024514 | satyam24514@iiitd.ac.in |
| Satguru Saran | 2024510 | satguru24510@iiitd.ac.in |
| Krishiv Vats | 2024308 | krishiv24308@iiitd.ac.in |

| Feature | What the project provides |
| --- | --- |
| Full-file audit | 2,260,701 source records, 151 columns; source identity and quality checks |
| Explicit population | 1,345,310 Fully Paid / Charged Off loans; unresolved outcomes excluded |
| Statistical inference | Two Welch tests, grade chi-square and term proportion z-test |
| Practical interpretation | Original-scale estimates, 95% intervals, thresholds and sensitivity checks |
| Encoding audit | 1,344,080 Ã— 40 = 53,763,200 actual instance-attribute cells |
| Reproducibility | Modular scripts, executed notebooks, automated checks and generated reports |

## Plot gallery and reading guide

The figures below were generated from this project's actual CSV analysis. Full statistics and denominators are in `outputs/tables/`.

'''
    gallery=[('eda/status','All source loan statuses','Current loans remain unresolved. The distribution explains why all source records cannot be the denominator for terminal-outcome charge-off proportions.'),('eda/outcome_boxplots','Interest-rate and DTI distributions','Left: issued interest rates; right: debt-to-income ratios. The line is the median, the box spans Q1 to Q3, and whiskers extend to observations within 1.5 IQR. Fliers are hidden in the plot only. Welch tests quantify differences in means, rather than medians.'),('eda/category_rates','Grade and term charge-off proportions','These conditional terminal-outcome rates show category patterns; composition and maturity prevent causal interpretations.'),('eda/missingness','Missingness overview','The 20 most incomplete fields highlight why blanket deletion or imputation is inappropriate.'),('eda/income_transform','Income before and after transformation','Original and log1p scales show extreme skew and the central distribution. Log1p admits zero and does not guarantee normality.'),('eda/income_dti','Income and DTI relationship','A reproducible sample of at most 5,000 terminal loans illustrates borrower heterogeneity. Inferential tests use full eligible samples.'),('inference/effect_intervals','Effect estimates and confidence intervals','Compare the estimate and its marginal 95% interval with the declared practical threshold. Panels use different units; term differences are expressed in percentage points.')]
    for image,title,caption in gallery:intro+=f'### {title}\n\n![{title}](figures/{image}.png)\n\n{caption}\n\n'
    intro+='## Complete deliverable directory\n\nGenerated caches and temporary PDF-review files are omitted below. The raw CSV is external as documented in `data/raw/README.md`.\n\n```text\nlendingclub-midterm-project/\n'+'\n'.join(tree)+'\n```\n\n## Installation, execution and audit details\n\n'
    readme.write_text(intro+old[old.index('## What was analysed'):],encoding='utf-8')
