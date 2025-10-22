#include "sort_algorithms.h"

#define MAX_SIZE 1000000

void test_sort_algorithm(const char *name, 
                        void (*sort_func)(int[], int, int, PerformanceStats*), 
                        int arr[], 
                        int size, 
                        int original[],
                        PerformanceStats *stats) {
    
    printf("Testing %s...\n", name);
    
    // 复制原始数组
    int *test_arr = (int*)malloc(size * sizeof(int));
    copy_array(test_arr, original, size);
    
    // 初始化性能统计
    init_performance_stats(stats);
    
    double start_time = omp_get_wtime();
    
    // 执行排序
    sort_func(test_arr, 0, size - 1, stats);
    
    double end_time = omp_get_wtime();
    stats->time = end_time - start_time;
    
    // 验证排序结果
    int sorted = is_sorted(test_arr, size);
    
    printf("  Time: %.6f seconds\n", stats->time);
    printf("  Sorted: %s\n", sorted ? "Yes" : "No");
    
    if (size <= 20) {
        printf("  Original: ");
        print_array(original, size);
        printf("  Sorted:   ");
        print_array(test_arr, size);
    }
    
    free(test_arr);
    printf("\n");
}

void save_performance_data(const char *filename, 
                          const char *optimization, 
                          int size, 
                          const char *algorithm,
                          const PerformanceStats *stats) {
    FILE *file = fopen(filename, "a");
    if (file == NULL) {
        file = fopen(filename, "w");
        fprintf(file, "Optimization,DataSize,Algorithm,Time,Comparisons,Swaps,MemoryUsage\n");
    }
    
    fprintf(file, "%s,%d,%s,%.6f,%lld,%lld,%lld\n", 
            optimization, size, algorithm, stats->time, 
            stats->comparisons, stats->swaps, stats->memory_usage);
    
    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <optimization_level>\n", argv[0]);
        printf("Optimization levels: O0, O1, O2, O3, Ofast\n");
        return 1;
    }
    
    char *optimization = argv[1];
    int sizes[] = {100, 1000, 10000, 100000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    
    printf("=== Sorting Algorithms Performance Test ===\n");
    printf("Optimization Level: %s\n\n", optimization);
    
    PerformanceStats stats;
    
    for (int i = 0; i < num_sizes; i++) {
        int size = sizes[i];
        printf("Testing with %d elements:\n", size);
        printf("========================\n");
        
        // 生成测试数据文件
        char filename[50];
        sprintf(filename, "../data/test_data_%d.txt", size);
        generate_test_data(filename, size, 0); // 0表示生成整数
        
        // 读取测试数据
        int *original_arr = (int*)malloc(size * sizeof(int));
        int actual_size;
        read_test_data(filename, original_arr, &actual_size);
        
        if (actual_size != size) {
            printf("Error: Expected %d elements, got %d\n", size, actual_size);
            free(original_arr);
            continue;
        }
        
        // 测试各种排序算法
        test_sort_algorithm("Quick Sort (Recursive)", 
                           quick_sort_recursive, 
                           original_arr, size, original_arr, &stats);
        save_performance_data("../results/performance_data.csv", optimization, size, 
                             "QuickSort_Recursive", &stats);
        
        test_sort_algorithm("Quick Sort (Non-Recursive)", 
                           quick_sort_non_recursive, 
                           original_arr, size, original_arr, &stats);
        save_performance_data("../results/performance_data.csv", optimization, size, 
                             "QuickSort_NonRecursive", &stats);
        
        test_sort_algorithm("Merge Sort (Sequential)", 
                           merge_sort_sequential, 
                           original_arr, size, original_arr, &stats);
        save_performance_data("../results/performance_data.csv", optimization, size, 
                             "MergeSort_Sequential", &stats);
        
        test_sort_algorithm("Merge Sort (Parallel)", 
                           merge_sort_parallel, 
                           original_arr, size, original_arr, &stats);
        save_performance_data("../results/performance_data.csv", optimization, size, 
                             "MergeSort_Parallel", &stats);
        
        free(original_arr);
        printf("\n");
    }
    
    printf("Performance data saved to ../results/performance_data.csv\n");
    return 0;
}
