# Final validation summary

Project directory on creation host: `C:\Users\Gamerism\Downloads\stra dnsc [roject\lendingclub-midterm-project`.

Actual CSV: 2,260,701 parsed records x 151 columns, comprising 2,260,668 loan records and 33 non-loan metadata rows. The supplied profile differs; see the comparison table. Raw metadata stayed unchanged, and the raw file was not copied into this ZIP.

Actual encoded arithmetic: 1,344,080 x 40 = 53,763,200 cells, above 3,000,000. The full terminal sample is 1,345,310 loans.

## Test-specific samples

- int_rate: 268,559 + 1,076,751 loans.
- dti: 268,488 + 1,076,448 loans.
- grade: 1,345,310 loans.
- term: 324,567 + 1,020,743 loans.

## Executed checks

- Four empirical hypothesis tests completed, with estimates, intervals and practical thresholds.
- Full chunked audit/analysis executed; additional compact quality scan verified source metadata and DTI flags.
- Eleven automated unit tests passed; actual log is outputs/logs/unit_tests.log. Synthetic inputs were used only for software tests.
- All three notebooks executed from top to bottom in separate Python processes (12 code cells total); actual outputs are embedded. This is the included plain-Python executor, not a claim that a Jupyter kernel was installed or tested.
- Accounting and result-consistency assertions passed.
<<<<<<< HEAD
- The supplied-template adaptation compiled; PDF has 8 pages, below the eight-page cap. Manual visual review record matches this PDF: True. The delivered version was compiled with Tectonic, rendered and inspected; future regenerated PDFs must be checked again. Underfull line warnings were present in the delivered build; no overfull boxes were reported.
=======
- The supplied-template adaptation compiled; PDF has 4 pages, below the eight-page cap. Manual visual review record matches this PDF: True. The delivered version was compiled with Tectonic, rendered and inspected; future regenerated PDFs must be checked again. Underfull line warnings were present in the delivered build; no overfull boxes were reported.
>>>>>>> origin/main
- Generated report, figure, table and notebook scripts executed. An initial compiler wrapper validation failed because its Python interpreter lacked pypdf; the completed build used the bundled PDF runtime successfully. An initial sandbox test run could not write TEMP; the tests passed in the normal permission context.

## Remaining user inputs / scientific limitations

- Supply lecture, quiz and practice files for exact syllabus mapping; no invented lecture references.
- Confirm historical provenance/licence and source definitions.
<<<<<<< HEAD
- Supplied institute emails and repository URL are entered; the contribution column was removed as requested.
- Review selection, censoring, dependence, missingness and subjective practical thresholds before presenting the findings.

The full file list and SHA-256 of every packaged file are in FILE_MANIFEST.json. This is a local deliverable; no GitHub repository or commit was created.


Presentation update: replaced the three requested plots, added acronym and attribute references, independently cross-checked all four stored tests and report intervals, reran eleven unit checks and three notebooks successfully. Underlying empirical results remain unchanged.
=======
- Fill institute emails, actual contributions and repository URL. Team names and roll numbers are already entered.
- Review selection, censoring, dependence, missingness and subjective practical thresholds before presenting the findings.

The full file list and SHA-256 of every packaged file are in FILE_MANIFEST.json. This is a local deliverable; no GitHub repository or commit was created.
>>>>>>> origin/main
