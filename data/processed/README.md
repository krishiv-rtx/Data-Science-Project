# Processed data policy

Selected numeric/category values and terminal subsets are constructed in memory by src/preprocessing.py. No row-level borrower data is written into this deliverable. Re-run the pipeline against the original CSV to reconstruct them. Aggregate processed tables are in outputs/tables, including contingency tables, group summaries and before/after counts. This keeps the ZIP compact and avoids unnecessary duplication of the source.
