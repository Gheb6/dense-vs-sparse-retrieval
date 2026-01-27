# Dense vs Sparse Retrieval: BEIR Benchmark Replication

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pyserini](https://img.shields.io/badge/Pyserini-Lucene-orange)](https://github.com/castorini/pyserini)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green)](https://github.com/facebookresearch/faiss)
[![Paper](https://img.shields.io/badge/Paper-arXiv:2409.06464-red)](https://arxiv.org/abs/2409.06464)

This repository contains a complete replication of the experiments described in the paper **"Operational Advice for Dense and Sparse Retrievers: HNSW, Flat, or Inverted Indexes?"** (arXiv:2409.06464).

The project implements and compares three retrieval paradigms across BEIR datasets:
1.  **Sparse (Baseline):** BM25 (via Pyserini/Lucene)
2.  **Sparse (Learned):** SPLADE++ EnsembleDistil / SelfDistil
3.  **Dense:** BGE-base-en-v1.5 (via FAISS HNSW & Flat)

> **Key Contribution:** This implementation includes a custom **Matrix-based Sparse Retrieval Engine** (SciPy) for SPLADE that fixes quantization issues found in standard Pyserini implementations, restoring accuracy on datasets like NFCorpus (nDCG@10: 0.23 → 0.35).

---

## 📊 Reproduced Results (Example: NFCorpus)

This notebook successfully replicates **Table 1** (Effectiveness), **Table 3** (Indexing Time), and **Table 4** (Quantization Impact) from the paper.

| Method | Type | nDCG@10 | Recall@10 | QPS (Approx) |
| :--- | :--- | :--- | :--- | :--- |
| **BM25** | Sparse (Lexical) | 0.323 | 0.154 | ~46 |
| **SPLADE++ ED** | Sparse (Learned) | **0.357** | **0.169** | ~242 |
| **BGE-HNSW** | Dense (FP32) | 0.371 | 0.176 | ~1500 |
| **BGE-Flat** | Dense (FP32) | 0.369 | 0.176 | ~4800 |

*Note: Results obtained on a T4 GPU environment.*

---

## 🛠️ Methodology & Implementation Details

### 1. BM25 (Lucene)
- Uses **Pyserini** (Anserini bindings).
- Parameters matched to paper: `k1=0.9`, `b=0.4`.
- Multi-threaded indexing (16 threads).

### 2. SPLADE++ (The Matrix Fix) 🚀
Standard Lucene `Impact` indexing often degrades SPLADE performance on small datasets due to integer quantization artifacts (truncating float weights like `1.45` to integers).
- **My Solution:** I implemented a custom Python-based retrieval engine using **SciPy Sparse Matrices**.
- **Logic:** `Scores = Matrix_Docs (CSR) × Vector_Query (Transposed)`
- **Benefit:** Guarantees mathematical exactness (Exact Match) while maintaining high speed (~300 QPS) via vectorized operations.

### 3. Dense Retrieval (BGE)
- Model: `BAAI/bge-base-en-v1.5`
- Indexing: **FAISS** library.
- **HNSW:** `M=16`, `efConstruction=100`, `efSearch=1000`.
- **Quantization:** Includes comparison between FP32 and **INT8** indexes (Table 3 & 4 replication).

---

## 💻 Installation & Setup

This project requires **Java 21** (for Pyserini/Lucene) and specific Python libraries.

### 1. Prerequisites
The notebook handles the installation of Java 21 automatically on Colab/Kaggle environments.

### 2. Python Dependencies
```bash
pip install faiss-cpu
pip install huggingface-hub==0.23.0 transformers==4.36.2 sentence-transformers==2.2.2 pyserini beir pandas matplotlib seaborn scipy
```
## 🚀 Usage

1.  Open the Jupyter Notebook (`Dense_vs_Sparse_Replication_SPLADE_Fix.ipynb`).
2.  **Select Dataset:** Modify the `dataset_name` variable in Cell 3.
    ```python
    dataset_name = 'nfcorpus' # Options: 'scifact', 'trec-covid', 'fiqa', etc.
    ```
3.  **Run All Cells:** The notebook is linear and automated.
    * Downloads dataset
    * Builds indexes (BM25, FAISS, SPLADE Matrix)
    * Runs searches
    * Calculates metrics (nDCG@10, Recall@10)
    * Generates plots
4.  **Download Results:** The final cell creates a ZIP file containing all CSVs and Plots.

---

## 📂 Output Structure

The notebook generates a `FINAL_OUTPUT_{dataset_name}.zip` containing:

* `{dataset}_results.csv`: Main comparison table (Table 1 replication).
* `{dataset}_table3_indexing.csv`: Time analysis (FP32 vs INT8).
* `{dataset}_table4_int8.csv`: Quantization performance analysis.
* `{dataset}_speed_vs_quality.pdf`: Scatter plot visualization.
* `{dataset}_metrics_comparison.pdf`: Bar charts.

---

## 📚 References

* **Original Paper:** *Dense vs Sparse Retrieval: A Comprehensive Analysis on BEIR* ([arXiv:2409.06464](https://arxiv.org/abs/2409.06464))
* **BEIR Benchmark:** [https://github.com/beir-cellar/beir](https://github.com/beir-cellar/beir)
* **Pyserini:** [https://github.com/castorini/pyserini](https://github.com/castorini/pyserini)
* **SPLADE:** [https://github.com/naver/splade](https://github.com/naver/splade)

### 🎓 Project Information

* **Student:** Gabriele Righi
* **University:** University of Pisa
* **Course:** Information Retrieval 
* **Academic Year:** 2025/2026
* **Objective:** Reproduction of state-of-the-art retrieval models as part of the course evaluation

---

## 📝 How to Cite

If you use this code in your research, please cite this repository:

```bibtex
@misc{righi2025densesparse,
    title={Dense vs Sparse Retrieval: BEIR Benchmark Replication},
    author={Gabriele Righi},
    year={2026},
    howpublished={\url{https://github.com/Gheb6/dense-vs-sparse-retrieval}},
    institute={University of Pisa}
}
```
