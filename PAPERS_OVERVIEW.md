# Information Retrieval Project - Paper Selection Guide

## Project Requirements

The project is based on a scientific paper and can be approached at different levels:

### Level 0-4 Grading Scale:
- **Basic Level (0-1)**: Read and understand the techniques presented in the article
- **Intermediate Level (2)**: Conduct experiments to verify assumptions, main properties, or conclusions
- **Advanced Level (3)**: Replicate the results from the article
- **Expert Level (4)**: Re-implement the proposed solution, potentially improving it with alternative strategies

---

## Available Papers by Category

### Classic IR (4 papers)

#### 1. The WebGraph Framework I: Compression Techniques
- **Authors**: Paolo Boldi, Sebastiano Vigna (2024)
- **Conference**: The WebConf
- **Links**: [Paper](https://vigna.di.unimi.it/ftp/papers/WebGraphI.pdf) | [Code](https://github.com/vigna/webgraph-rs)
- **Focus**: Graph compression techniques for web graphs
- **Difficulty**: Intermediate to Advanced
- **Notes**: Recent paper (2024) with available Rust implementation

# 2. Better Bitmap Performance with Roaring Bitmaps
- **Authors**: Samy Chambi, Daniel Lemire, Owen Kaser, Robert Godin (2016)
- **Journal**: Software: Practice and Experience
- **Links**: [Paper](http://arxiv.org/abs/1402.6407) | [Code](https://roaringbitmap.org/)
- **Focus**: Efficient bitmap compression and operations
- **Difficulty**: Intermediate
- **Notes**: Widely used in practice, multiple implementations available

### 3. FSST: Fast Static Symbol Table Compression
- **Authors**: Peter Boncz, Thomas Neumann, Viktor Leis (2020)
- **Conference**: VLDB
- **Links**: [Paper](https://www.vldb.org/pvldb/vol13/p2649-boncz.pdf) | [Code](https://github.com/cwida/fsst)
- **Focus**: String compression technique
- **Difficulty**: Intermediate to Advanced
- **Notes**: Novel compression approach for strings in databases

#### 4. Finding the Best of Both Worlds: Faster and More Robust Top-k Document Retrieval
- **Authors**: Omar Khattab, Mohammad Hammoud, Tamer Elsayed (2020)
- **Conference**: SIGIR
- **Links**: [Paper](https://web2.qatar.cmu.edu/~mhhammou/SIGIR_20_LazyBM.pdf)
- **Focus**: Efficient top-k document retrieval algorithms
- **Difficulty**: Intermediate to Advanced
- **Notes**: Combines different retrieval strategies

---

### Learning to Rank (4 papers)

#### 5. Quality versus Efficiency in Document Scoring with Learning-to-Rank Models
- **Authors**: Gabriele Capannini, Claudio Lucchese, Franco Maria Nardini, Salvatore Orlando, Raffaele Perego, Nicola Tonellotto (2016)
- **Journal**: Information Processing and Management
- **Links**: PDF on Teams
- **Focus**: Trade-offs in learning-to-rank systems
- **Difficulty**: Intermediate
- **Notes**: Practical considerations for LTR deployment

#### 6. The Istella22 Dataset: Bridging Traditional and Neural Learning to Rank Evaluation
- **Authors**: Domenico Dato, Sean MacAvaney, Franco Maria Nardini, Raffaele Perego, Nicola Tonellotto (2022)
- **Conference**: SIGIR
- **Links**: [Paper](https://dl.acm.org/doi/10.1145/3477495.3531740) | [Code](https://github.com/hpclab/istella22-experiments)
- **Focus**: New benchmark dataset for LTR evaluation
- **Difficulty**: Basic to Intermediate
- **Notes**: Good for experimental validation, dataset available

#### 7. LightGBM: A Highly Efficient Gradient Boosting Decision Tree
- **Authors**: Guolin Ke, Qi Meng, Thomas Finley, et al. (2017)
- **Conference**: NeurIPS
- **Links**: [Paper](https://proceedings.neurips.cc/paper_files/paper/2017/file/6449f44a102fde848669bdd9eb6b76fa-Paper.pdf) | [Code](https://github.com/microsoft/LightGBM)
- **Focus**: Efficient gradient boosting implementation
- **Difficulty**: Intermediate to Advanced
- **Notes**: Widely used ML library, good for comparisons

#### 8. XGBoost: A Scalable Tree Boosting System
- **Authors**: Tianqi Chen, Carlos Guestrin (2016)
- **Conference**: KDD
- **Links**: [Paper](https://www.kdd.org/kdd2016/papers/files/rfp0697-chenAemb.pdf) | [Code](https://github.com/dmlc/xgboost)
- **Focus**: Scalable gradient boosting framework
- **Difficulty**: Intermediate to Advanced
- **Notes**: Industry-standard tool, extensive documentation

---

### Neural IR (12 papers)

#### 9. Efficient Inverted Indexes for Approximate Retrieval over Learned Sparse Representations
- **Authors**: Sebastian Bruch, Franco Maria Nardini, Cosimo Rulli, Rossano Venturini (2024)
- **Conference**: SIGIR
- **Links**: [Paper](https://arxiv.org/abs/2404.18812) | [Code](https://github.com/TusKANNy/seismic)
- **Focus**: Indexing for neural sparse retrieval
- **Difficulty**: Advanced
- **Notes**: Recent (2024), combines neural IR with traditional indexing

#### 10. From Distillation to Hard Negative Sampling: Making Sparse Neural IR Models More Effective
- **Authors**: Thibault Formal, Carlos Lassance, Benjamin Piwowarski, Stéphane Clinchant (2022)
- **Conference**: SIGIR
- **Links**: [Paper](https://arxiv.org/abs/2205.04733) | [Code](https://github.com/naver/splade)
- **Focus**: SPLADE model training techniques
- **Difficulty**: Advanced
- **Notes**: Neural sparse retrieval, active research area

## 11. Operational Advice for Dense and Sparse Retrievers: HNSW, Flat, or Inverted Indexes?
- **Authors**: Jimmy Lin (2024)
- **Venue**: ArXiv
- **Links**: [Paper](https://arxiv.org/abs/2409.06464)
- **Focus**: Practical comparison of retrieval index structures
- **Difficulty**: Intermediate
- **Notes**: Very recent, practical focus

#### 12. Optimizing Dense Retrieval Model Training with Hard Negatives
- **Authors**: Jingtao Zhan, Jiaxin Mao, Yiqun Liu, Jiafeng Guo, Min Zhang, Shaoping Ma (2022)
- **Links**: [Paper](https://jiafengguo.github.io/2021/021-Optimizing%20Dense%20Retrieval%20Model%20Training%20with%20Hard%20Negatives.pdf) | [Code](https://github.com/jingtaozhan/DRhard)
- **Focus**: Training strategies for dense retrieval
- **Difficulty**: Advanced
- **Notes**: Important technique in neural IR

#### 13. How to Train Your DRAGON: Diverse Augmentation Towards Generalizable Dense Retrieval
- **Authors**: Sheng-Chieh Lin, Akari Asai, Minghan Li, et al. (2023)
- **Conference**: EMNLP
- **Links**: [Paper](https://aclanthology.org/2023.findings-emnlp.423.pdf) | [Code](https://github.com/facebookresearch/dpr-scale)
- **Focus**: Data augmentation for dense retrieval
- **Difficulty**: Advanced
- **Notes**: Meta/Facebook research, focuses on generalization

#### 14. A Reproducibility Study of PLAID
- **Authors**: Sean MacAvaney, Nicola Tonellotto (2024)
- **Conference**: SIGIR
- **Links**: [Paper](https://arxiv.org/abs/2404.14989) | [Code](https://github.com/seanmacavaney/plaidrepro)
- **Focus**: Reproducibility in neural IR
- **Difficulty**: Advanced
- **Notes**: Great for understanding reproducibility challenges

#### 15. Billion-scale Similarity Search with GPUs
- **Authors**: Jeff Johnson, Matthijs Douze, Hervé Jégou (2017)
- **Venue**: ArXiv
- **Links**: [Paper & Code](https://github.com/facebookresearch/faiss)
- **Focus**: FAISS - efficient similarity search library
- **Difficulty**: Advanced
- **Notes**: Industry-standard tool, GPU optimization

#### 16. Product Quantization for Nearest Neighbor Search
- **Authors**: Hervé Jégou, Matthijs Douze, Cordelia Schmid (2011)
- **Journal**: TPAMI
- **Links**: PDF on Teams
- **Focus**: Compression for vector search
- **Difficulty**: Intermediate to Advanced
- **Notes**: Foundational work in ANN search

#### 17. DARTH: Declarative Recall Through Early Termination for Approximate Nearest Neighbor Search
- **Authors**: Manos Chatzakis, Yannis Papakonstantinou, Themis Palpanas (2025)
- **Conference**: SIGMOD
- **Links**: [Paper](https://arxiv.org/pdf/2505.19001)
- **Focus**: Early termination strategies for ANN
- **Difficulty**: Advanced
- **Notes**: Very recent (2025), cutting-edge research

#### 18. Similarity Search in a Blink of an Eye
- **Authors**: Cecilia Aguerrebere, Ishwar Singh Bhati, Mark Hildebrand, Mariano Tepper, Theodore Willke (2023)
- **Conference**: VLDB
- **Links**: [Paper](https://arxiv.org/pdf/2304.04759)
- **Focus**: Ultra-fast similarity search
- **Difficulty**: Advanced
- **Notes**: Performance-focused approach

#### 19. ACORN: Performant and Predicate-Agnostic Search Over Vector Embeddings and Structured Data
- **Authors**: Liana Patel, Peter Kraft, Carlos Guestrin, Matei Zaharia (2024)
- **Links**: [Paper](https://arxiv.org/pdf/2403.04871)
- **Focus**: Hybrid search (vectors + structured data)
- **Difficulty**: Advanced
- **Notes**: Combines multiple data types

#### 20. Filtered Approximate Nearest Neighbor Search: A Unified Benchmark and Systematic Experimental Study
- **Authors**: Jiayang Shi, Yuzheng Cai, Weiguo Zheng (2025)
- **Links**: [Paper](https://arxiv.org/pdf/2509.07789)
- **Focus**: Benchmark and evaluation of filtered ANN
- **Difficulty**: Intermediate to Advanced
- **Notes**: Very recent (2025), survey/benchmark paper

---

## Selection Criteria and Recommendations

### For Basic Level (Understanding):
- **Best choices**: Papers #6, #11, #20
- These papers provide good surveys or benchmark studies that are easier to understand

### For Intermediate Level (Experiments):
- **Best choices**: Papers #2, #3, #6, #11, #16
- These have clear experimental setups and available datasets/code

### For Advanced Level (Replication):
- **Best choices**: Papers #1, #7, #8, #10, #14
- These have code available and well-documented experiments

### For Expert Level (Implementation/Improvement):
- **Best choices**: Papers #1, #9, #10, #12, #13, #15
- These offer opportunities for novel improvements and have active research communities

### By Interest Area:

#### Compression & Efficiency:
- Papers #1, #2, #3, #16

#### Learning to Rank:
- Papers #5, #6, #7, #8

#### Neural Retrieval:
- Papers #9, #10, #12, #13, #14

#### Vector Search & ANN:
- Papers #11, #15, #16, #17, #18, #19, #20

#### Reproducibility:
- Paper #14 (explicit focus on reproducibility)

---

## Next Steps

1. **Read abstracts and introductions** of 3-5 papers that interest you
2. **Check code availability** - papers with code are easier to work with
3. **Assess dataset availability** - crucial for experiments and replication
4. **Consider your background** - ML-heavy papers require strong ML knowledge
5. **Check recency** - very recent papers (2024-2025) might have fewer resources but are more novel

## Notes
- Papers marked "PDF on Teams" are not freely available online
- Most papers have code repositories for reference
- Consider the computational resources needed (especially for neural IR papers)

---

**Contact your instructor** if you need clarification on any paper or have questions about scope.
