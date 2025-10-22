import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

print("=== 手动图表生成 ===")

# 读取手动创建的数据
df = pd.read_csv('../results/manual_performance_data.csv')
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print("\n前5行数据:")
print(df.head())

# 创建多个图表
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 图表1: 执行时间比较 (O2优化)
ax1 = axes[0, 0]
o2_data = df[df['Optimization'] == 'O2']
algorithms = o2_data['Algorithm'].unique()

for algo in algorithms:
    algo_data = o2_data[o2_data['Algorithm'] == algo]
    ax1.plot(algo_data['DataSize'], algo_data['Time'], marker='o', label=algo, linewidth=2)

ax1.set_title('算法执行时间比较 (O2优化)', fontweight='bold')
ax1.set_xlabel('数据规模')
ax1.set_ylabel('时间 (秒)')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 图表2: 优化级别影响
ax2 = axes[0, 1]
size_10k = df[df['DataSize'] == 10000]

for algo in algorithms:
    algo_data = size_10k[size_10k['Algorithm'] == algo]
    times = [algo_data[algo_data['Optimization'] == opt]['Time'].values[0] for opt in ['O0', 'O2']]
    ax2.plot(['O0', 'O2'], times, marker='s', label=algo, linewidth=2)

ax2.set_title('优化级别影响 (10,000数据)', fontweight='bold')
ax2.set_xlabel('优化级别')
ax2.set_ylabel('时间 (秒)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 图表3: 比较次数
ax3 = axes[1, 0]
for algo in algorithms:
    algo_data = o2_data[o2_data['Algorithm'] == algo]
    ax3.plot(algo_data['DataSize'], algo_data['Comparisons'], marker='^', label=algo, linewidth=2)

ax3.set_title('比较次数 (O2优化)', fontweight='bold')
ax3.set_xlabel('数据规模')
ax3.set_ylabel('比较次数')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 图表4: 内存使用
ax4 = axes[1, 1]
for algo in algorithms:
    algo_data = o2_data[o2_data['Algorithm'] == algo]
    ax4.plot(algo_data['DataSize'], algo_data['MemoryUsage'], marker='d', label=algo, linewidth=2)

ax4.set_title('内存使用 (O2优化)', fontweight='bold')
ax4.set_xlabel('数据规模')
ax4.set_ylabel('内存 (字节)')
ax4.set_xscale('log')
ax4.set_yscale('log')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../results/manual_charts.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ 图表已保存为 '../results/manual_charts.png'")

# 生成报告
report = f"""
排序算法性能分析报告 (手动数据)
================================

数据概览:
--------
总记录数: {len(df)}
数据规模: {sorted(df['DataSize'].unique())}
算法: {list(df['Algorithm'].unique())}
优化级别: {list(df['Optimization'].unique())}

性能摘要 (O2优化):
----------------
"""
for size in sorted(df['DataSize'].unique()):
    report += f"\n数据规模 {size}:\n"
    size_data = df[(df['DataSize'] == size) & (df['Optimization'] == 'O2')]
    for algo in sorted(df['Algorithm'].unique()):
        algo_data = size_data[size_data['Algorithm'] == algo]
        if not algo_data.empty:
            time = algo_data['Time'].iloc[0]
            report += f"  {algo}: {time:.6f} 秒\n"

with open('../results/manual_report.txt', 'w') as f:
    f.write(report)

print("✅ 报告已保存为 '../results/manual_report.txt'")
print("\n🎉 手动数据分析和图表生成完成!")
