#!/usr/bin/env python3
"""
排序算法性能分析与可视化
支持多优化级别测试、时间复杂度分析和矢量图生成
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.optimize import curve_fit
import os
from datetime import datetime

# 设置图表风格
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class SortingPerformanceAnalyzer:
    def __init__(self):
        self.df = None
        self.theoretical_complexity = {
            'QuickSort_Recursive': 'O(n log n)',
            'QuickSort_NonRecursive': 'O(n log n)',
            'MergeSort_Sequential': 'O(n log n)',
            'MergeSort_Parallel': 'O(n log n)'
        }
        
    def load_data(self, filename='../results/performance_data.csv'):
        """加载性能数据"""
        try:
            self.df = pd.read_csv(filename)
            print("✅ 数据加载成功!")
            print(f"数据规模: {len(self.df)} 条记录")
            print(f"优化级别: {self.df['Optimization'].unique()}")
            print(f"算法: {self.df['Algorithm'].unique()}")
            print(f"数据规模范围: {self.df['DataSize'].min()} - {self.df['DataSize'].max()}")
            return True
        except FileNotFoundError:
            print("❌ 性能数据文件未找到，请先运行测试程序")
            return False
    
    def preprocess_data(self):
        """数据预处理"""
        if self.df is None:
            return
        
        # 计算性能指标
        self.df['TimePerElement'] = self.df['Time'] / self.df['DataSize']
        self.df['ComparisonsPerElement'] = self.df['Comparisons'] / self.df['DataSize']
        self.df['SwapsPerElement'] = self.df['Swaps'] / self.df['DataSize']
        self.df['MemoryPerElement'] = self.df['MemoryUsage'] / self.df['DataSize']
        
        # 添加算法类型分类
        self.df['AlgorithmType'] = self.df['Algorithm'].apply(
            lambda x: '快速排序' if 'Quick' in x else '归并排序'
        )
        
        print("✅ 数据预处理完成!")
    
    def generate_summary_report(self):
        """生成摘要报告"""
        if self.df is None:
            return
        
        print("\n" + "="*80)
        print("                    排序算法性能分析报告")
        print("="*80)
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"数据记录总数: {len(self.df)}")
        
        # 最佳性能分析
        best_performance = self.df.loc[self.df.groupby(['DataSize', 'Algorithm'])['Time'].idxmin()]
        
        print("\n🏆 各算法最佳优化级别:")
        summary_table = best_performance[['DataSize', 'Algorithm', 'Optimization', 'Time', 'Comparisons', 'MemoryUsage']].copy()
        summary_table['Time'] = summary_table['Time'].round(6)
        summary_table['MemoryUsage_MB'] = (summary_table['MemoryUsage'] / 1024 / 1024).round(2)
        print(summary_table.to_string(index=False))
        
        # 性能提升分析
        print("\n📈 优化级别性能提升分析 (相对于-O0):")
        optimization_levels = ['O1', 'O2', 'O3', 'Ofast']
        
        for size in sorted(self.df['DataSize'].unique()):
            print(f"\n数据规模 {size:,}:")
            size_data = self.df[self.df['DataSize'] == size]
            o0_data = size_data[size_data['Optimization'] == 'O0']
            
            for algo in self.df['Algorithm'].unique():
                o0_time = o0_data[o0_data['Algorithm'] == algo]['Time'].mean()
                if not np.isnan(o0_time):
                    improvements = []
                    for opt in optimization_levels:
                        opt_time = size_data[
                            (size_data['Algorithm'] == algo) & 
                            (size_data['Optimization'] == opt)
                        ]['Time'].mean()
                        if not np.isnan(opt_time):
                            improvement = ((o0_time - opt_time) / o0_time) * 100
                            improvements.append(f"{opt}: {improvement:+.1f}%")
                    
                    if improvements:
                        print(f"  {algo:<25} {', '.join(improvements)}")
    
    def plot_optimization_impact(self):
        """绘制优化级别影响分析"""
        if self.df is None:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('编译优化级别对排序算法性能的影响分析', fontsize=14, fontweight='bold')
        
        algorithms = self.df['Algorithm'].unique()
        optimizations = self.df['Optimization'].unique()
        
        # 1. 执行时间对比
        for i, algo in enumerate(algorithms):
            ax = axes[i//2, i%2]
            algo_data = self.df[self.df['Algorithm'] == algo]
            
            for opt in optimizations:
                opt_data = algo_data[algo_data['Optimization'] == opt]
                if not opt_data.empty:
                    grouped = opt_data.groupby('DataSize')['Time'].mean()
                    ax.plot(grouped.index, grouped.values, 
                           marker='o', linewidth=2, label=opt, markersize=4)
            
            ax.set_title(f'{algo}', fontweight='bold')
            ax.set_xlabel('数据规模')
            ax.set_ylabel('执行时间 (秒)')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(title='优化级别', fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/optimization_impact.pdf', bbox_inches='tight', dpi=300)
        plt.savefig('../results/optimization_impact.png', bbox_inches='tight', dpi=300)
        plt.show()
    
    def plot_algorithm_comparison(self):
        """绘制算法性能对比"""
        if self.df is None:
            return
        
        # 使用O2优化级别的数据进行比较
        o2_data = self.df[self.df['Optimization'] == 'O2']
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('排序算法性能对比分析 (O2优化级别)', fontsize=14, fontweight='bold')
        
        metrics = ['Time', 'Comparisons', 'Swaps', 'MemoryUsage']
        metric_names = ['执行时间 (秒)', '比较次数', '交换次数', '内存使用 (字节)']
        scales = ['log', 'log', 'log', 'log']
        
        for idx, (metric, name, scale) in enumerate(zip(metrics, metric_names, scales)):
            ax = axes[idx//2, idx%2]
            
            for algo in o2_data['Algorithm'].unique():
                algo_metric_data = o2_data[o2_data['Algorithm'] == algo]
                if not algo_metric_data.empty:
                    grouped = algo_metric_data.groupby('DataSize')[metric].mean()
                    ax.plot(grouped.index, grouped.values, 
                           marker='s', linewidth=2, label=algo, markersize=4)
            
            ax.set_title(name)
            ax.set_xlabel('数据规模')
            ax.set_ylabel(name)
            ax.set_xscale('log')
            if scale == 'log':
                ax.set_yscale('log')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/algorithm_comparison.pdf', bbox_inches='tight', dpi=300)
        plt.savefig('../results/algorithm_comparison.png', bbox_inches='tight', dpi=300)
        plt.show()
    
    def theoretical_complexity_analysis(self):
        """理论时间复杂度分析"""
        if self.df is None:
            return
        
        # 理论复杂度函数
        def n_log_n(x, a, b):
            return a * x * np.log(x) + b
        
        def n_squared(x, a, b):
            return a * x * x + b
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('排序算法时间复杂度验证分析', fontsize=14, fontweight='bold')
        
        algorithms = self.df['Algorithm'].unique()
        o2_data = self.df[self.df['Optimization'] == 'O2']
        
        for i, algo in enumerate(algorithms):
            ax = axes[i//2, i%2]
            algo_data = o2_data[o2_data['Algorithm'] == algo]
            
            if len(algo_data) < 3:
                continue
            
            # 实际测量数据
            sizes = algo_data['DataSize'].unique()
            times = []
            
            for size in sizes:
                time_val = algo_data[algo_data['DataSize'] == size]['Time'].mean()
                times.append(time_val)
            
            sizes = np.array(sizes)
            times = np.array(times)
            
            # 绘制实际数据点
            ax.scatter(sizes, times, color='red', s=50, zorder=5, 
                      label='实测数据', alpha=0.7)
            
            # 尝试不同复杂度模型的拟合
            try:
                # n log n 拟合
                popt_log, pcov_log = curve_fit(n_log_n, sizes, times, 
                                             p0=[1e-7, 0], maxfev=5000)
                sizes_fit = np.linspace(min(sizes), max(sizes), 100)
                times_fit_log = n_log_n(sizes_fit, *popt_log)
                
                # 计算R²
                residuals_log = times - n_log_n(sizes, *popt_log)
                ss_res_log = np.sum(residuals_log**2)
                ss_tot_log = np.sum((times - np.mean(times))**2)
                r_squared_log = 1 - (ss_res_log / ss_tot_log)
                
                ax.plot(sizes_fit, times_fit_log, 'b-', linewidth=2,
                       label=f'n log n 拟合 (R² = {r_squared_log:.4f})')
                
                # 尝试n²拟合对比
                try:
                    popt_sq, pcov_sq = curve_fit(n_squared, sizes, times, 
                                               p0=[1e-9, 0], maxfev=5000)
                    times_fit_sq = n_squared(sizes_fit, *popt_sq)
                    
                    residuals_sq = times - n_squared(sizes, *popt_sq)
                    ss_res_sq = np.sum(residuals_sq**2)
                    r_squared_sq = 1 - (ss_res_sq / ss_tot_log)
                    
                    ax.plot(sizes_fit, times_fit_sq, 'g--', linewidth=1,
                           label=f'n² 拟合 (R² = {r_squared_sq:.4f})', alpha=0.7)
                except:
                    pass
                
            except Exception as e:
                print(f"拟合失败 {algo}: {e}")
                # 直接绘制连线
                ax.plot(sizes, times, 'b-', linewidth=1, label='实测趋势')
            
            ax.set_title(f'{algo}\n理论复杂度: {self.theoretical_complexity[algo]}', 
                        fontweight='bold')
            ax.set_xlabel('数据规模 n')
            ax.set_ylabel('执行时间 (秒)')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/complexity_analysis.pdf', bbox_inches='tight', dpi=300)
        plt.savefig('../results/complexity_analysis.png', bbox_inches='tight', dpi=300)
        plt.show()
    
    def plot_parallel_efficiency(self):
        """并行效率分析"""
        if self.df is None:
            return
        
        # 分析并行归并排序的效率
        parallel_data = self.df[self.df['Algorithm'] == 'MergeSort_Parallel']
        sequential_data = self.df[self.df['Algorithm'] == 'MergeSort_Sequential']
        
        if parallel_data.empty or sequential_data.empty:
            print("缺少并行/顺序归并排序数据")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('并行归并排序效率分析', fontsize=14, fontweight='bold')
        
        # 计算加速比
        speedup_data = []
        for size in sequential_data['DataSize'].unique():
            seq_time = sequential_data[
                (sequential_data['DataSize'] == size) & 
                (sequential_data['Optimization'] == 'O2')
            ]['Time'].mean()
            
            par_time = parallel_data[
                (parallel_data['DataSize'] == size) & 
                (parallel_data['Optimization'] == 'O2')
            ]['Time'].mean()
            
            if not np.isnan(seq_time) and not np.isnan(par_time) and par_time > 0:
                speedup = seq_time / par_time
                speedup_data.append((size, speedup))
        
        if speedup_data:
            sizes, speedups = zip(*speedup_data)
            
            # 加速比
            axes[0].plot(sizes, speedups, 'bo-', linewidth=2, markersize=6)
            axes[0].axhline(y=1, color='r', linestyle='--', alpha=0.7, label='基线')
            axes[0].set_xlabel('数据规模')
            axes[0].set_ylabel('加速比 (顺序时间/并行时间)')
            axes[0].set_xscale('log')
            axes[0].set_title('并行加速比分析')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # 效率分析
            # 假设使用4个线程（根据OpenMP默认设置）
            theoretical_threads = 4
            efficiencies = [s / theoretical_threads for s in speedups]
            axes[1].plot(sizes, efficiencies, 'go-', linewidth=2, markersize=6)
            axes[1].axhline(y=1, color='r', linestyle='--', alpha=0.7, label='理想效率')
            axes[1].set_xlabel('数据规模')
            axes[1].set_ylabel('并行效率')
            axes[1].set_xscale('log')
            axes[1].set_title('并行效率分析')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../results/parallel_efficiency.pdf', bbox_inches='tight', dpi=300)
        plt.savefig('../results/parallel_efficiency.png', bbox_inches='tight', dpi=300)
        plt.show()
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        if self.df is None:
            return
        
        # 保存详细数据到Excel
        with pd.ExcelWriter('../results/sorting_performance_analysis.xlsx') as writer:
            # 原始数据
            self.df.to_excel(writer, sheet_name='原始数据', index=False)
            
            # 汇总统计
            summary = self.df.groupby(['Algorithm', 'Optimization', 'DataSize']).agg({
                'Time': ['mean', 'std', 'min', 'max'],
                'Comparisons': 'mean',
                'Swaps': 'mean',
                'MemoryUsage': 'mean'
            }).round(6)
            summary.to_excel(writer, sheet_name='汇总统计')
            
            # 最佳性能
            best_performance = self.df.loc[self.df.groupby(['DataSize', 'Algorithm'])['Time'].idxmin()]
            best_performance.to_excel(writer, sheet_name='最佳性能', index=False)
        
        print("✅ 详细分析报告已保存为 '../results/sorting_performance_analysis.xlsx'")
    
    def run_complete_analysis(self):
        """运行完整分析流程"""
        if not self.load_data():
            return
        
        self.preprocess_data()
        self.generate_summary_report()
        self.plot_optimization_impact()
        self.plot_algorithm_comparison()
        self.theoretical_complexity_analysis()
        self.plot_parallel_efficiency()
        self.generate_comprehensive_report()
        
        print("\n🎉 分析完成! 生成的文件:")
        print("📊 图表文件:")
        print("   - optimization_impact.pdf/png (优化级别影响)")
        print("   - algorithm_comparison.pdf/png (算法对比)")
        print("   - complexity_analysis.pdf/png (复杂度分析)")
        print("   - parallel_efficiency.pdf/png (并行效率)")
        print("📈 数据文件:")
        print("   - sorting_performance_analysis.xlsx (完整数据分析)")
        print("   - performance_data.csv (原始数据)")

def main():
    """主函数"""
    print("="*60)
    print("       排序算法性能数据分析与可视化系统")
    print("="*60)
    
    analyzer = SortingPerformanceAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
