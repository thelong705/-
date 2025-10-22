#!/bin/bash

# 编译优化级别
OPTIMIZATIONS=("O0" "O1" "O2" "O3" "Ofast")

echo "=== Sorting Algorithms Benchmark ==="
echo "Testing optimization levels: ${OPTIMIZATIONS[*]}"
echo ""

# 切换到src目录
cd ../src

# 清理之前的性能数据
rm -f ../results/performance_data.csv
rm -f ../data/test_data_*.txt

# 为每个优化级别编译和测试
for OPT in "${OPTIMIZATIONS[@]}"; do
    echo "=== Testing with -$OPT ==="
    
    # 编译
    echo "Compiling with -$OPT..."
    gcc -$OPT -fopenmp -o sort_test main.c quick_sort.c merge_sort.c utils.c
    
    if [ $? -ne 0 ]; then
        echo "Compilation failed for -$OPT"
        continue
    fi
    
    # 运行测试
    echo "Running tests..."
    ./sort_test $OPT
    
    echo "Completed -$OPT"
    echo ""
done

# 返回脚本目录
cd ../scripts

echo "=== All tests completed ==="
echo "Performance data saved to ../results/performance_data.csv"
