"""Add technical notation to the report without changing empirical results."""
import re
from .config import ROOT

def annotate():
    p=ROOT/'reports/final_report.tex';text=p.read_text()
    def section(m):
        heading,body=m[1],m[2]
        if 'Interest rate' in heading or 'Debt-to-income' in heading:
            h0=r'\(H_0:\Delta_\mu=\mu_{\mathrm{CO}}-\mu_{\mathrm{FP}}=0\). '
            h1=r'\(H_1:\Delta_\mu\ne0\). '
            statistic='t';definition=r'\(\mu_{\mathrm{CO}},\mu_{\mathrm{FP}}\): population means for CO (Charged Off) and FP (Fully Paid); \(\widehat\Delta_\mu=\bar x_{\mathrm{CO}}-\bar x_{\mathrm{FP}}\).'
        elif 'Grade' in heading:
            h0=r'\(H_0:G\perp Y\). ';h1=r'\(H_1:G\not\perp Y\). '
            statistic=r'\chi^2';definition=r'\(G\): recorded grade; \(Y\): terminal outcome; \(\perp\) means statistical independence. \(V=\sqrt{\chi^2/N}\) is Cramer\textquotesingle s association measure for this two-outcome table.'
        else:
            h0=r'\(H_0:\Delta_p=p_{60}-p_{36}=0\). ';h1=r'\(H_1:\Delta_p\ne0\). '
            statistic='z';definition=r'\(p_{60},p_{36}\): population charge-off proportions among terminal loans of each term; \(\widehat\Delta_p=\widehat p_{60}-\widehat p_{36}\).'
        body=body.replace('Null hypothesis (H0) & ',r'Null hypothesis \(H_0\) & '+h0)
        body=body.replace('Alternative (H1) & ',r'Alternative \(H_1\) & '+h1)
        body=body.replace('Significance level & 0.05;',r'Significance level & \(\alpha=0.05\);')
        body=re.sub(r'(Test statistic & )([0-9.]+)',lambda v:v[1]+r'\('+statistic+'='+v[2]+r'\)',body)
        body=body.replace('degrees of freedom:',r'df (degrees of freedom):')
        body=body.replace('95\\% confidence interval & ',r'95\% CI (confidence interval) & ')
        body=body.replace('Probability / decision & < ',r'Probability / decision & \(p<')
        body=body.replace('2.23e-308 (floating-point underflow)',r'2.23\times10^{-308}\) (floating-point underflow)')
        body=body.replace(r'\toprule',r'\toprule'+'\n'+r'Notation & '+definition+r'\\\midrule',1)
        return heading+body
    text=re.sub(r'(\\subsection\{(?:Interest rate|Debt-to-income|Grade|Term)\}\s*)(.*?)(?=\\subsection|\\textbf\{Calculation audit\.\})',section,text,flags=re.S)
    for short,full in [('DTI','debt-to-income ratio'),('IQR','interquartile range'),('IID','independent and identically distributed'),('FICO','Fair Isaac Corporation credit score')]:
        text=text.replace(full+' ('+short+')',short+' ('+full+')')
    text=text.replace('Full CSV audit:', 'Full CSV (comma-separated values) audit:',1)
    text=text.replace('population SD is unknown','population SD (standard deviation) is unknown',1)
    text=text.replace('The local SHA-256 is saved','The local SHA-256 (Secure Hash Algorithm, 256-bit) fingerprint is saved',1)
    text=text.replace('Course PDFs','Course PDFs (Portable Document Format files)',1)
    text=text.replace('lecture PDFs,','lecture PDFs (Portable Document Format files),',1)
    text=text.replace(r'\textbf{Acronyms and statistical shorthand.}',r'\textbf{Acronym directory and statistical shorthand.}')
    symbols=r'''
\medskip\textbf{Mathematical notation.} \(\mu\): population mean; \(\bar x\): sample mean; \(p\): population proportion (or a p-value when explicitly labelled); \(\widehat p\): sample proportion; \(\Delta\): difference; \(s\): SD (standard deviation); \(\mathrm{SE}\): standard error; \(\nu\): degrees of freedom; \(n,N\): sample counts; \(\alpha\): significance level; \(t,z,\chi^2\): test statistics. \(H_0\) is the null hypothesis; \(H_1\) is the alternative hypothesis. Welch, Holm and Cramer are names, not acronyms.
'''
    text=text.replace(r'\end{document}',symbols+r'\end{document}')
    p.write_text(text)
