# NullPointer - LendingClub midterm project

Statistical inference on observed loan repayment outcomes. Team: Satyam Singh (2024514), Satguru Saran (2024510), Krishiv Vats (2024308). CSE558, IIIT-Delhi, Monsoon 2026.

## What was analysed

The supplied CSV was scanned in full by code; only a small initial sample and aggregate outputs were inspected in conversation. Actual dimensions: **2,260,701 rows x 151 columns**. The preliminary profile reports 314,168 x 162 and therefore must not be substituted for the actual CSV. Raw data remains unchanged and is not bundled in this ZIP. Original download URL, acquisition date and licence were not supplied; see LICENSE_OR_DATA_NOTICE.md and the recorded SHA-256.

Questions: do terminal Charged Off/Fully Paid loans differ in mean issued rate and DTI; is grade associated with terminal outcome; and do 60-/36-month loans have different observed terminal charge-off proportions? These are historical observational associations, not causal effects or predictions. Methods: two Welch tests, chi-square independence with Cramer's V, two-proportion z, Holm adjustment, and limited sensitivity checks. Read reports/analysis_plan.md for thresholds fixed before comparisons.

## Install (Windows PowerShell)

Python 3.14.3 was used; Python 3.11+ is a reasonable baseline, but the exact pinned dependency set was tested on the recorded version. Allow several GB of free RAM; the chunked audit limits whole-file loading, although selected columns and encoded arrays still need memory. Raw input is 1,675,133,810 bytes. No GPU, cloud service or credentials are required.

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
- outputs/encoded_size.json: **1,344,080 x 40 = 53,763,200 instance-attribute cells**; actual matrix, excluding IDs, outcome and leakage fields.
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
