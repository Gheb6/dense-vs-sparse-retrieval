# Implementation Notes: Dense vs Sparse Retrieval on BEIR

## Overview
This document describes the technical challenges and implementation decisions encountered while replicating the paper's results on dense vs sparse retrieval methods on BEIR datasets using Pyserini.

## Problem 1: Dense Vector Indexing - Lucene HNSW vs FAISS

### The Issue
The paper states: "All experiments were conducted using the Anserini open-source IR toolkit, based on Lucene 9.9.1... We used bindings for Lucene HNSW indexes recently introduced in Ma et al. CIKM 2023."

Our initial assumption was that Pyserini (the Python bindings for Anserini) would provide a direct way to build Lucene HNSW indexes programmatically.

### Investigation Results

**Finding: NO Python API for Lucene HNSW indexing exists in Pyserini**

After investigation, we discovered:

1. **FAISS is the Standard for Dense Indexing in Pyserini**
   - Official Pyserini documentation shows all dense vector indexing (HNSW, Flat, PQ, HNSWPQ) uses FAISS library
   - Command: `python -m pyserini.index.faiss --hnsw` (not Lucene)
   - No equivalent `python -m pyserini.index.lucene` command for vector indexing

2. **Command-Line Tool Limitations**
   - `pyserini.index.lucene` command-line tool does not support vector/HNSW parameters
   - Attempted flags that don't exist: `--hnsw`, `--hnswM`, `--hnswefC`, `--vector-indexing-approach`
   - Tool only supports traditional text-based inverted indexing

3. **Paper vs Implementation Gap**
   - The paper used **Anserini (Java)** which has native Lucene HNSW support
   - Pyserini (Python) wraps Anserini but doesn't expose the Lucene dense indexing API
   - "Bindings for Lucene HNSW indexes" mentioned in the paper likely refers to **search** capability only, not **indexing**

### Why This Matters

The paper's justification for using Lucene was to provide a "fair comparison" between dense and sparse methods in the same library:

> "However, we selected Lucene because it provides implementations of both dense and sparse retrieval, making comparisons reasonably fair. For example, comparing Faiss HNSW indexes (implemented in C++) with Lucene inverted indexes (implemented in Java) or even Numpy would be conflating too many non-relevant factors (e.g., language choice)."

By using FAISS for dense indexing, we are partially violating this principle.

### Our Solution: Use FAISS with Paper Parameters

**Decision**: Use FAISS library for both HNSW and Flat indexes with **identical parameters** from the paper:
- M = 16 (connections per node)
- efConstruction = 100 (construction parameter)
- efSearch = 1000 (search parameter)

**Justification**:
1. Both FAISS HNSW and Lucene HNSW implement the same algorithm with the same parameters
2. Quality metrics (nDCG@10, Recall@10) should be similar despite implementation differences
3. QPS differences are expected due to language choice (C++ vs Java) and hardware
4. Learning Java/Anserini would require weeks of additional work

**Implementation**:
```python
import faiss

# Create HNSW index with paper parameters
hnsw_index = faiss.IndexHNSWFlat(dimension, M, faiss.METRIC_INNER_PRODUCT)
hnsw_index.hnsw.efConstruction = ef_construction
hnsw_index.hnsw.efSearch = ef_search
hnsw_index.add(doc_embeddings)
```

### Results Comparison

| Method | Your nDCG@10 | Paper nDCG@10 | Difference |
|--------|--------------|---------------|------------|
| BM25 | 0.679 | 0.679 | ✅ Perfect match |
| SPLADE++ ED | 0.549 | 0.704 | ⚠️ -0.155 (22% gap) |
| **BGE Dense** | **0.738** | **0.741** | ✅ **-0.003 (0.4% gap)** |

**Conclusion**: The FAISS HNSW implementation produces nearly identical quality results to the paper (0.4% difference), validating our choice.

---

## Problem 2: SPLADE++ EnsembleDistil Query Encoding

### The Issue
SPLADE query encoding returned incorrect format, causing `AttributeError: 'numpy.ndarray' object has no attribute 'items'`

### Root Cause
Initial attempt used `AutoQueryEncoder` which returned dense numpy arrays instead of sparse token dictionaries that `LuceneImpactSearcher` expects:

```python
# ❌ WRONG - Returns numpy array
splade_query_encoder = AutoQueryEncoder('naver/splade-cocondenser-ensembledistil')
# Result: numpy.ndarray, not dict of {token: weight}
```

### Solution
Pass model name as string directly to `LuceneImpactSearcher` with `encoder_type='pytorch'`:

```python
# ✅ CORRECT - Searcher handles encoding internally
splade_searcher = LuceneImpactSearcher(
    splade_index_dir,
    'naver/splade-cocondenser-ensembledistil',  # Model name as string
    encoder_type='pytorch',  # Use PyTorch encoder
)
```

### Status
✅ **Fixed** - but quality still differs from paper (0.549 vs 0.704)

### Remaining Investigation Needed
The 22% quality gap suggests potential issues with:
- Document encoding batch size or format
- SPLADE index building (impact scoring)
- GPU memory causing silent encoding failures
- Difference in SPLADE model version or configuration

---

## Problem 3: HNSW Index Building with Lucene (Command-Line)

### The Issue
Attempted to build Lucene HNSW index via command-line with flags:
```bash
python -m pyserini.index.lucene \
  --dim 768 \
  --hnswM 16 \
  --hnswefC 100 \
  --hnswefS 1000
```

**Error**: `"-hnswM is not a valid option"`

### Investigation
Checked available options:
```bash
python -m pyserini.index.lucene -options
```

Result: Only traditional Lucene inverted index options (no vector support)

### Solution
Switched to FAISS for all dense indexing (Problem 1 above)

---

## Problem 4: Directory Creation for Visualizations

### The Issue
Visualization cell (cell 26) tried to save plots to a directory that didn't exist yet:
```
FileNotFoundError: [Errno 2] No such file or directory: 'results_scifact/speed_vs_quality.pdf'
```

### Root Cause
Execution order: Visualization cell (26) ran before Save Results cell (27) which created the directory

### Solution
Added `os.makedirs()` at the start of visualization cell:
```python
output_dir = f'results_{dataset_name}'
os.makedirs(output_dir, exist_ok=True)  # Create before saving
```

### Status
✅ **Fixed**

---

## Problem 5: SPLADE Memory Issues on Google Colab

### The Issue
Initial SPLADE document encoding with `--device cpu` was killed with SIGKILL (out of memory)

### Root Cause
- CPU encoding is slow and memory-intensive
- Large batch size (32) with full corpus exceeded available memory

### Solution
- Switch to GPU: `--device cuda`
- Batch size remains 32 (acceptable for T4 GPU)

### Status
✅ **Fixed**

---

## Current Status

### ✅ Working Correctly
- **BM25**: nDCG@10 matches paper exactly (0.679)
- **BGE Dense (HNSW)**: nDCG@10 nearly matches paper (0.738 vs 0.741, 0.4% difference)
- **BGE Dense (Flat)**: nDCG@10 matches HNSW (brute-force baseline works)
- **BM25 QPS**: 17.4 queries/sec
- **BGE QPS**: 507 (HNSW), 924 (Flat) - both excellent

### ⚠️ Needs Investigation
- **SPLADE++ ED**: nDCG@10 significantly lower than paper (0.549 vs 0.704, 22% gap)
  - Document encoding may have issues
  - Index building may not be creating proper sparse representations
  - Query encoding may be incorrect despite format fix

---

## Architecture: Hybrid Lucene + FAISS

```
Retrieval Methods:
├── BM25 (Sparse)
│   └── Lucene inverted index (JSON Collection)
│       └── DefaultLuceneDocumentGenerator
│
├── SPLADE++ ED (Sparse)
│   └── Lucene impact index (JsonVectorCollection)
│       └── DefaultLuceneDocumentGenerator + --impact flag
│
├── BGE-HNSW (Dense)
│   └── FAISS HNSW index
│       └── Parameters: M=16, efC=100, efSearch=1000
│
└── BGE-Flat (Dense)
    └── FAISS Flat index (brute-force)
        └── Baseline for comparing HNSW speedup
```

**Justification**: 
- Sparse retrieval (BM25, SPLADE) ✓ Lucene (matches paper)
- Dense retrieval (BGE) ✓ FAISS (only option in Pyserini Python API)

---

## Lessons Learned

1. **API Documentation is Key**: Pyserini documentation explicitly states dense indexing uses FAISS, but we initially missed this
2. **Paper vs Implementation Gap**: Academic papers use one toolkit (Anserini Java), but Python users get different defaults
3. **Quality Over Speed**: For academic reproducibility, matching quality metrics is more important than QPS (which depends on hardware anyway)
4. **Parameters Are Portable**: HNSW parameters (M, efC, efSearch) are algorithm-independent and transfer between implementations

---

## Recommendations for Future Work

1. **Debug SPLADE**: Investigate the 22% quality gap before making other changes
   - Verify GPU encoding is actually happening
   - Check SPLADE sparse token format
   - Compare with paper's SPLADE configuration

2. **Document Limitations**: In thesis/paper, explicitly state:
   - "Dense indexing uses FAISS instead of Lucene due to Pyserini API limitations"
   - "Identical HNSW parameters (M=16, efC=100, efSearch=1000) were used"
   - "Quality metrics closely match the paper (BGE: 0.4% difference)"

3. **QPS Caveats**: When reporting QPS values, note:
   - Different hardware (Colab T4 vs Mac Studio M1 Ultra)
   - Different implementation language (Python/C++ vs Java)
   - Single-threaded measurement (paper used 16 threads)

4. **Validation**: Compare results on multiple BEIR datasets to ensure consistency

---

## References

- Paper: Dense vs Sparse Retrieval on BEIR Benchmark
- Anserini: http://anserini.io/
- Pyserini: https://github.com/castorini/pyserini
- FAISS: https://github.com/facebookresearch/faiss
- BEIR: https://github.com/beir-cellar/beir
