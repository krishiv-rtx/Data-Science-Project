"""Chunked full-file audit; retain only analysis columns in memory."""
from collections import Counter
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from .config import SELECTED

def load_and_audit(path, chunk_size=50000):
    path = Path(path)
    before = path.stat()
    missing = Counter(); statuses = Counter(); types = {}; pieces = []; hashes = []
    rows = rows_missing = memory = 0
    # Consistent string representation makes duplicate hashes comparable across chunks.
    for i, chunk in enumerate(pd.read_csv(path, chunksize=chunk_size, dtype='string')):
        if i == 0:
            columns = list(chunk.columns)
            absent = set(SELECTED) - set(columns)
            if absent: raise ValueError(f'Missing required columns: {sorted(absent)}')
        rows += len(chunk)
        missing.update({c: int(v) for c, v in chunk.isna().sum().items()})
        rows_missing += int(chunk.isna().any(axis=1).sum())
        memory += int(chunk.memory_usage(deep=True).sum())
        statuses.update(chunk.loan_status.fillna('<missing>').value_counts().to_dict())
        for c in columns:
            observed = chunk[c].dropna()
            numeric = pd.to_numeric(observed, errors='coerce')
            kind = 'all_missing' if observed.empty else ('numeric' if numeric.notna().all() else 'text')
            types.setdefault(c, set()).add(kind)
        hashes.append(pd.util.hash_pandas_object(chunk, index=False).to_numpy())
        pieces.append(chunk[SELECTED].copy())
        print(f'Audited {rows:,} rows', flush=True)
    h = np.concatenate(hashes)
    duplicate_candidates = int(len(h) - len(np.unique(h)))
    # If hashes repeat, compare the complete source rows before calling them exact duplicates.
    exact_duplicates = 0
    if duplicate_candidates:
        counts = pd.Series(h).value_counts()
        repeated = set(counts[counts > 1].index)
        candidates = []
        for chunk in pd.read_csv(path, chunksize=chunk_size, dtype='string'):
            hh = pd.util.hash_pandas_object(chunk, index=False)
            candidates.append(chunk[hh.isin(repeated)])
        exact_duplicates = int(pd.concat(candidates, ignore_index=True).duplicated().sum())
    frame = pd.concat(pieces, ignore_index=True)
    valid_ids = frame.id.dropna()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError('Source metadata changed during analysis')
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8*1024*1024), b''): sha.update(block)
    audit = dict(rows=rows, columns=len(columns), column_names=columns,
        missing_counts=dict(missing), rows_with_missing=rows_missing,
        status_counts=dict(statuses), inferred_types={c: ('text' if 'text' in k else 'numeric' if 'numeric' in k else 'all_missing') for c,k in types.items()},
        duplicate_rows=exact_duplicates, duplicate_hash_candidates=duplicate_candidates,
        missing_ids=int(frame.id.isna().sum()), duplicate_ids=int(valid_ids.duplicated().sum()),
        unique_ids=int(valid_ids.nunique()), accumulated_string_frame_bytes=memory,
        file_bytes=before.st_size, file_sha256=sha.hexdigest(), filename=path.name,
        encoding='UTF-8 (pandas default; full parse succeeded)', raw_metadata_unchanged=True)
    return frame, audit
