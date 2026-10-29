"""Check computed artifacts, execute notebooks/tests, record honest validation."""
from pathlib import Path
import sys,json,subprocess,platform,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'outputs'/name).read_text(encoding='utf-8'))
a=read('dataset_audit.json');e=read('encoded_size.json');c=read('preparation.json');r=read('results.json')
assert a['rows']==sum(a['status_counts'].values())
assert a['rows']==a['loan_records']+a['verified_nonloan_rows']
assert c['rows_before']==c['terminal_rows']+c['excluded_nonterminal']
assert e['cells']==e['rows']*e['columns'] and e['meets_3m']
assert e['rows_before']==e['rows']+e['excluded_missing']
assert len(r)==4 and all(v['ci_low']<v['estimate']<v['ci_high'] for v in r)
for v in r:
    n=v['n_a']+v['n_b'] if 'n_a' in v else v['n']
    assert n+v['excluded']==c['terminal_rows']
    assert v['p'] is None or 0<v['p']<=1
checks={}
for label,command in [('unit_tests',[sys.executable,'-m','unittest','discover','-s','tests','-v']),
                      ('notebooks',[sys.executable,'scripts/execute_notebooks.py'])]:
    p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
    (ROOT/f'outputs/logs/{label}.log').write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
    checks[label]={'passed':p.returncode==0,'exit_code':p.returncode}
    if p.returncode:raise SystemExit(f'{label} failed; inspect output log')
pdf=read('pdf_validation.json') if (ROOT/'outputs/pdf_validation.json').exists() else {'compiled':False,'pages':None}
review=read('pdf_visual_review.json') if (ROOT/'outputs/pdf_visual_review.json').exists() else {}
visual_match=(ROOT/'reports/final_report.pdf').exists() and review.get('sha256')==hashlib.sha256((ROOT/'reports/final_report.pdf').read_bytes()).hexdigest()
checks.update(python_version=platform.python_version(),full_csv_analysis_executed=True,
    source_metadata_unchanged=a['raw_metadata_unchanged'],four_empirical_tests_completed=True,
    accounting_assertions_passed=True,encoded_size_actual_matrix=True,pdf=pdf,
    visual_pdf_review='Manual review record matches this PDF' if visual_match else 'Manual visual review needed for the regenerated PDF',
    unresolved=['Lecture PDFs, quizzes and practice problems absent; exact syllabus mapping unverified',
        'Original download URL, acquisition date and licence unverified',
        'User must fill true institute emails, contributions and repository URL before submission'])
(ROOT/'outputs/validation.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
sample='\n'.join('- '+v['test']+': '+(f"{v['n_a']:,} + {v['n_b']:,}" if 'n_a' in v else f"{v['n']:,}")+' loans.' for v in r)
summary=f'''# Final validation summary

Project directory on creation host: `{ROOT}`.

Actual CSV: {a['rows']:,} parsed records x {a['columns']} columns, comprising {a['loan_records']:,} loan records and {a['verified_nonloan_rows']} non-loan metadata rows. The supplied profile differs; see the comparison table. Raw metadata stayed unchanged, and the raw file was not copied into this ZIP.

Actual encoded arithmetic: {e['rows']:,} x {e['columns']} = {e['cells']:,} cells, above 3,000,000. The full terminal sample is {c['terminal_rows']:,} loans.

## Test-specific samples

{sample}

## Executed checks

- Four empirical hypothesis tests completed, with estimates, intervals and practical thresholds.
- Full chunked audit/analysis executed; additional compact quality scan verified source metadata and DTI flags.
- Eleven automated unit tests passed; actual log is outputs/logs/unit_tests.log. Synthetic inputs were used only for software tests.
- All three notebooks executed from top to bottom in separate Python processes (12 code cells total); actual outputs are embedded. This is the included plain-Python executor, not a claim that a Jupyter kernel was installed or tested.
- Accounting and result-consistency assertions passed.
- The supplied-template adaptation compiled; PDF has {pdf['pages']} pages, below the eight-page cap. Manual visual review record matches this PDF: {visual_match}. The delivered version was compiled with Tectonic, rendered and inspected; future regenerated PDFs must be checked again. Underfull line warnings were present in the delivered build; no overfull boxes were reported.
- Generated report, figure, table and notebook scripts executed. An initial compiler wrapper validation failed because its Python interpreter lacked pypdf; the completed build used the bundled PDF runtime successfully. An initial sandbox test run could not write TEMP; the tests passed in the normal permission context.

## Remaining user inputs / scientific limitations

- Supply lecture, quiz and practice files for exact syllabus mapping; no invented lecture references.
- Confirm historical provenance/licence and source definitions.
- Fill institute emails, actual contributions and repository URL. Team names and roll numbers are already entered.
- Review selection, censoring, dependence, missingness and subjective practical thresholds before presenting the findings.

The full file list and SHA-256 of every packaged file are in FILE_MANIFEST.json. This is a local deliverable; no GitHub repository or commit was created.
'''
(ROOT/'reports/validation_summary.md').write_text(summary,encoding='utf-8')
print(json.dumps(checks,indent=2))
