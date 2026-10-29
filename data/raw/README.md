# Raw data location

Place your existing `accepted_2007_to_2018Q4.csv` here, or use `--data` with its path. The delivered archive deliberately omits the 1.675 GB raw CSV. The original remains in the parent directory on the task computer. No copy is necessary: from this project root use `python scripts/run_all.py --data "../accepted_2007_to_2018Q4.csv"`.

The pipeline opens the source read-only and records SHA-256, size, and unchanged metadata. It never overwrites the CSV. Do not assume a similarly named internet download has the same rows or schema; compare its hash with outputs/dataset_audit.json.
