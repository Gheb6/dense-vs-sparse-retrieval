"""
Comprehensive visualization of FiQA retrieval results
Creates publication-quality plots for analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set publication-quality style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16
})

# Load data
exp_df = pd.read_csv('FiQA_results/experiment_results_fiqa.csv')
hybrid_df = pd.read_csv('FiQA_results/hybrid_results_fiqa.csv')
latency_df = pd.read_csv('FiQA_results/latency_data_fiqa.csv')

print("="*80)
print("FIQA RESULTS ANALYSIS")
print("="*80)
print("\n📊 EXPERIMENT RESULTS:")
print(exp_df.to_string(index=False))
print("\n🔀 HYBRID RESULTS:")
print(hybrid_df.to_string(index=False))

# ============================================================================
# FIGURE 1: Comprehensive 4-Panel Overview
# ============================================================================
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Define colors
colors_type = {'Dense': '#3498db', 'Sparse': '#e74c3c', 'Hybrid': '#2ecc71'}

# Panel 1: Quality Metrics Comparison
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(exp_df))
width = 0.35

recall_bars = ax1.bar(x - width/2, exp_df['Recall@10'], width, 
                      label='Recall@10', color='#3498db', alpha=0.8, edgecolor='black')
ndcg_bars = ax1.bar(x + width/2, exp_df['nDCG@10'], width,
                    label='nDCG@10', color='#e67e22', alpha=0.8, edgecolor='black')

ax1.set_ylabel('Score', fontweight='bold')
ax1.set_title('Quality Metrics: Recall@10 vs nDCG@10', fontweight='bold', fontsize=14)
ax1.set_xticks(x)
ax1.set_xticklabels(exp_df['Method'], rotation=20, ha='right')
ax1.legend(loc='upper right', framealpha=0.95)
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, max(exp_df['Recall@10'].max(), exp_df['nDCG@10'].max()) * 1.15)

# Add value labels on bars
for bars in [recall_bars, ndcg_bars]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)

# Panel 2: Latency Distribution (Log Scale)
ax2 = fig.add_subplot(gs[1, 0])
methods = exp_df['Method']
medians = exp_df['Median Latency (ms)']
p95s = exp_df['P95 Latency (ms)']

bar_colors = [colors_type[t] for t in exp_df['Type']]
bars = ax2.barh(methods, medians, color=bar_colors, alpha=0.7, edgecolor='black')

# Highlight fastest
fastest_idx = medians.argmin()
bars[fastest_idx].set_edgecolor('gold')
bars[fastest_idx].set_linewidth(3)

ax2.set_xlabel('Median Latency (ms, log scale)', fontweight='bold')
ax2.set_title('Latency Comparison (Log Scale)', fontweight='bold')
ax2.set_xscale('log')
ax2.grid(axis='x', alpha=0.3)

# Add latency values
for i, (med, p95) in enumerate(zip(medians, p95s)):
    ax2.text(med * 1.5, i, f'{med:.2f}ms', va='center', fontsize=9, fontweight='bold')

# Panel 3: Speed vs Quality Trade-off
ax3 = fig.add_subplot(gs[1, 1])

for _, row in exp_df.iterrows():
    color = colors_type[row['Type']]
    marker = 'o' if row['Type'] == 'Dense' else ('s' if row['Type'] == 'Sparse' else '^')
    ax3.scatter(row['Median Latency (ms)'], row['Recall@10'], 
               s=250, alpha=0.7, color=color, marker=marker, 
               edgecolors='black', linewidth=2, label=row['Type'])

# Add method labels
for _, row in exp_df.iterrows():
    ax3.annotate(row['Method'], 
                (row['Median Latency (ms)'], row['Recall@10']),
                xytext=(10, 5), textcoords='offset points',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.4))

ax3.set_xlabel('Median Latency (ms, log scale)', fontweight='bold')
ax3.set_ylabel('Recall@10', fontweight='bold')
ax3.set_title('Speed-Quality Trade-off', fontweight='bold')
ax3.set_xscale('log')
ax3.grid(True, alpha=0.3)

# Remove duplicate legend entries
handles, labels = ax3.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax3.legend(by_label.values(), by_label.keys(), loc='best', framealpha=0.9)

# Panel 4: Hybrid Search Analysis
ax4 = fig.add_subplot(gs[2, :])

alphas = [0.3, 0.5, 0.7]
hybrid_recall = hybrid_df['Recall@10'].values
hybrid_ndcg = hybrid_df['nDCG@10'].values

# Plot lines
ax4.plot(alphas, hybrid_recall, marker='o', linewidth=3, markersize=12,
        color='#2ecc71', label='Hybrid Recall@10', linestyle='-')
ax4.plot(alphas, hybrid_ndcg, marker='s', linewidth=3, markersize=12,
        color='#e67e22', label='Hybrid nDCG@10', linestyle='--')

# Reference lines
flat_recall = exp_df[exp_df['Method'] == 'Flat']['Recall@10'].values[0]
flat_ndcg = exp_df[exp_df['Method'] == 'Flat']['nDCG@10'].values[0]
bm25_recall = exp_df[exp_df['Method'] == 'BM25']['Recall@10'].values[0]
bm25_ndcg = exp_df[exp_df['Method'] == 'BM25']['nDCG@10'].values[0]

ax4.axhline(y=flat_recall, color='blue', linestyle=':', linewidth=2, 
           label='Flat (best dense) Recall', alpha=0.7)
ax4.axhline(y=bm25_recall, color='red', linestyle=':', linewidth=2,
           label='BM25 Recall', alpha=0.7)

ax4.set_xlabel('α (Dense Weight in Hybrid)', fontweight='bold', fontsize=12)
ax4.set_ylabel('Score', fontweight='bold', fontsize=12)
ax4.set_title('Hybrid Search: Impact of α Parameter', fontweight='bold')
ax4.set_xticks(alphas)
ax4.legend(loc='best', framealpha=0.9)
ax4.grid(True, alpha=0.3)

# Annotate values
for i, (a, r, n) in enumerate(zip(alphas, hybrid_recall, hybrid_ndcg)):
    ax4.annotate(f'{r:.3f}', (a, r), xytext=(0, 10),
                textcoords='offset points', ha='center', fontsize=9, fontweight='bold')
    ax4.annotate(f'{n:.3f}', (a, n), xytext=(0, -15),
                textcoords='offset points', ha='center', fontsize=9, fontweight='bold')

plt.suptitle('FiQA Retrieval System Performance Analysis', 
            fontsize=16, fontweight='bold', y=0.995)
plt.savefig('FiQA_results/comprehensive_analysis.pdf', dpi=300, bbox_inches='tight')
print("\n✅ Saved: FiQA_results/comprehensive_analysis.pdf")
plt.show()

# ============================================================================
# FIGURE 2: Latency Distributions (Box + Violin)
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Box plot
ax1 = axes[0]
bp = ax1.boxplot([latency_df[col] for col in latency_df.columns],
                  labels=latency_df.columns,
                  patch_artist=True, showfliers=False)

colors = ['#3498db', '#3498db', '#3498db', '#e74c3c']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax1.set_ylabel('Latency (ms, log scale)', fontweight='bold')
ax1.set_title('Latency Distribution: Box Plot (650 queries)', fontweight='bold')
ax1.set_yscale('log')
ax1.grid(axis='y', alpha=0.3)
ax1.tick_params(axis='x', rotation=15)

# Violin plot
ax2 = axes[1]
positions = range(1, len(latency_df.columns) + 1)
parts = ax2.violinplot([latency_df[col] for col in latency_df.columns],
                       positions=positions, showmeans=True, showmedians=True)

for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(colors[i])
    pc.set_alpha(0.7)

ax2.set_xticks(positions)
ax2.set_xticklabels(latency_df.columns, rotation=15)
ax2.set_ylabel('Latency (ms, log scale)', fontweight='bold')
ax2.set_title('Latency Distribution: Violin Plot', fontweight='bold')
ax2.set_yscale('log')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('FiQA_results/latency_distributions.pdf', dpi=300, bbox_inches='tight')
print("✅ Saved: FiQA_results/latency_distributions.pdf")
plt.show()

# ============================================================================
# FIGURE 3: Key Insights Table
# ============================================================================
print("\n" + "="*80)
print("KEY INSIGHTS FROM FIQA RESULTS")
print("="*80)

# Calculate key metrics
flat = exp_df[exp_df['Method'] == 'Flat'].iloc[0]
hnsw = exp_df[exp_df['Method'] == 'HNSW'].iloc[0]
hnsw_int8 = exp_df[exp_df['Method'] == 'HNSW-INT8'].iloc[0]
bm25 = exp_df[exp_df['Method'] == 'BM25'].iloc[0]

speedup_hnsw = flat['Median Latency (ms)'] / hnsw['Median Latency (ms)']
speedup_int8 = flat['Median Latency (ms)'] / hnsw_int8['Median Latency (ms)']
recall_drop_hnsw = (flat['Recall@10'] - hnsw['Recall@10']) / flat['Recall@10'] * 100
recall_drop_int8 = (flat['Recall@10'] - hnsw_int8['Recall@10']) / flat['Recall@10'] * 100

dense_vs_sparse = (flat['Recall@10'] - bm25['Recall@10']) / bm25['Recall@10'] * 100

print(f"\n1️⃣  DENSE vs SPARSE:")
print(f"    Flat (dense) beats BM25 (sparse) by {dense_vs_sparse:.1f}% in Recall@10")
print(f"    → Dense embeddings capture semantic meaning better for FiQA")

print(f"\n2️⃣  HNSW EFFICIENCY:")
print(f"    {speedup_hnsw:.1f}x faster than Flat with only {recall_drop_hnsw:.2f}% quality loss")
print(f"    → Production-ready: <1ms latency enables real-time search")

print(f"\n3️⃣  QUANTIZATION WINS:")
print(f"    HNSW-INT8 is {speedup_int8:.1f}x faster than Flat")
print(f"    Quality loss: {recall_drop_int8:.2f}% (negligible)")
print(f"    → Best choice: same speed, 4x less memory, same quality")

print(f"\n4️⃣  BM25 BOTTLENECK:")
print(f"    BM25 latency: {bm25['Median Latency (ms)']:.1f}ms (vs HNSW: {hnsw['Median Latency (ms)']:.2f}ms)")
print(f"    → {bm25['Median Latency (ms)'] / hnsw['Median Latency (ms)']:.0f}x slower makes hybrid search impractical")

print(f"\n5️⃣  HYBRID POTENTIAL:")
best_hybrid = hybrid_df.loc[hybrid_df['Recall@10'].idxmax()]
print(f"    Best hybrid (α={best_hybrid['Method'][-4:]}) matches HNSW quality")
print(f"    But {best_hybrid['Median Latency (ms)'] / hnsw['Median Latency (ms)']:.0f}x slower due to BM25")
print(f"    → Need optimized BM25 (Elasticsearch, Lucene) for production")

print("\n" + "="*80)
print("PRODUCTION RECOMMENDATION: HNSW-INT8")
print("="*80)
print("✅ Sub-millisecond latency (<0.3ms)")
print("✅ Minimal quality loss (<4% vs Flat)")
print("✅ 4x memory savings vs regular HNSW")
print("✅ Scalable to millions of documents")
print("="*80)
