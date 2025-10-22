#!/usr/bin/env python3
"""
最小化分析脚本 - 仅使用基本功能生成图表
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def check_and_fix_data():
    """检查和修复数据文件"""
    csv_file = '../results/performance_data.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ 数据文件不存在: {csv_file}")
        return None
    
    print(f"✅ 找到数据文件: {csv_file}")
    
    try:
        # 读取数据
        df = pd.read_csv(csv_file)
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        if df.empty:
            print("❌ 数据文件为空")
            return None
            
        # 显示前几行数据
        print("\n前5行数据:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"❌ 读取数据时出错: {e}")
        return None

def create_simple_charts(df):
    """创建简单图表"""
    try:
        print("\n开始创建图表...")
        
        # 图表1: 不同数据规模的执行时间
        plt.figure(figsize=(10, 6))
        
        # 按算法分组
        algorithms = df['Algorithm'].unique()
        colors = ['blue', 'red', 'green', 'orange']
        
        for i, algo in enumerate(algorithms):
            algo_data = df[df['Algorithm'] == algo]
            plt.plot(algo_data['DataSize'], algo_data['Time'], 
                    marker='o', label=algo, color=colors[i % len(colors)], 
                    linewidth=2, markersize=6)
        
        plt.title('排序算法执行时间比较', fontsize=14, fontweight='bold')
        plt.xlabel('数据规模')
        plt.ylabel('执行时间 (秒)')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('../results/chart1_time_comparison.png', dpi=150, bbox_inches='tight')
        print("✅ 图表1保存: ../results/chart1_time_comparison.png")
        
        # 图表2: 优化级别影响 (如果有多个优化级别)
        if 'Optimization' in df.columns and len(df['Optimization'].unique()) > 1:
            plt.figure(figsize=(10, 6))
            
            optimizations = df['Optimization'].unique()
            for opt in optimizations:
                opt_data = df[df['Optimization'] == opt]
                # 使用第一个算法为例
                algo = df['Algorithm'].iloc[0]
                algo_opt_data = opt_data[opt_data['Algorithm'] == algo]
                if not algo_opt_data.empty:
                    plt.plot(algo_opt_data['DataSize'], algo_opt_data['Time'], 
                            marker='s', label=f'{algo} ({opt})', linewidth=2)
            
            plt.title('编译优化级别对性能的影响', fontsize=14, fontweight='bold')
            plt.xlabel('数据规模')
            plt.ylabel('执行时间 (秒)')
            plt.xscale('log')
            plt.yscale('log')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('../results/chart2_optimization_impact.png', dpi=150, bbox_inches='tight')
            print("✅ 图表2保存: ../results/chart2_optimization_impact.png")
        else:
            print("ℹ️  只有一个优化级别，跳过优化级别比较图表")
        
        # 显示图表
        plt.show()
        
    except Exception as e:
        print(f"❌ 创建图表时出错: {e}")
        import traceback
        traceback.print_exc()

def generate_basic_report(df):
    """生成基础报告"""
    print("\n" + "="*50)
    print("          性能分析报告")
    print("="*50)
    
    print(f"总数据记录: {len(df)}")
    print(f"数据规模: {sorted(df['DataSize'].unique())}")
    print(f"算法: {list(df['Algorithm'].unique())}")
    
    if 'Optimization' in df.columns:
        print(f"优化级别: {list(df['Optimization'].unique())}")
    
    # 性能摘要
    print("\n性能摘要:")
    for size in sorted(df['DataSize'].unique()):
        print(f"\n数据规模 {size}:")
        size_data = df[df['DataSize'] == size]
        for algo in sorted(df['Algorithm'].unique()):
            algo_data = size_data[size_data['Algorithm'] == algo]
            if not algo_data.empty:
                time = algo_data['Time'].iloc[0]
                print(f"  {algo}: {time:.6f} 秒")

def main():
    """主函数"""
    print("=== 最小化性能分析 ===")
    
    # 检查并加载数据
    df = check_and_fix_data()
    if df is None:
        print("\n无法继续分析，请先运行C测试程序生成数据")
        return
    
    # 生成报告
    generate_basic_report(df)
    
    # 创建图表
    create_simple_charts(df)
    
    print("\n🎉 分析完成!")
    print("生成的图表保存在 ../results/ 目录中")

if __name__ == "__main__":
    main()
