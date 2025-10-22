#include "sort_algorithms.h"

// 初始化性能统计
void init_performance_stats(PerformanceStats *stats) {
    stats->time = 0.0;
    stats->comparisons = 0;
    stats->swaps = 0;
    stats->memory_usage = 0;
}

// 打印性能统计
void print_performance_stats(const PerformanceStats *stats, const char *algorithm_name) {
    printf("=== %s Performance ===\n", algorithm_name);
    printf("Time: %.6f seconds\n", stats->time);
    printf("Comparisons: %lld\n", stats->comparisons);
    printf("Swaps: %lld\n", stats->swaps);
    printf("Memory Usage: %lld bytes\n", stats->memory_usage);
    printf("\n");
}

// 生成测试数据
void generate_test_data(const char *filename, int count, int data_type) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        printf("Error opening file for writing!\n");
        return;
    }
    
    srand(time(NULL));
    
    // 写入数据数量
    fprintf(file, "%d\n", count);
    
    // 生成随机数据
    for (int i = 0; i < count; i++) {
        if (data_type == 0) { // 整数
            int value = rand() % (count * 10); // 范围根据数据量调整
            fprintf(file, "%d\n", value);
        } else { // 浮点数
            double value = (double)rand() / RAND_MAX * count * 10.0;
            fprintf(file, "%.2f\n", value);
        }
    }
    
    fclose(file);
    printf("Generated %d test data points in %s\n", count, filename);
}

// 读取测试数据
void read_test_data(const char *filename, int arr[], int *count) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file for reading!\n");
        *count = 0;
        return;
    }
    
    fscanf(file, "%d", count);
    
    for (int i = 0; i < *count; i++) {
        fscanf(file, "%d", &arr[i]);
    }
    
    fclose(file);
}

// 打印数组
void print_array(int arr[], int size) {
    printf("[");
    for (int i = 0; i < size && i < 20; i++) { // 只打印前20个元素
        printf("%d", arr[i]);
        if (i < size - 1 && i < 19) printf(", ");
    }
    if (size > 20) printf(", ...");
    printf("]\n");
}

// 检查数组是否已排序
int is_sorted(int arr[], int size) {
    for (int i = 1; i < size; i++) {
        if (arr[i] < arr[i - 1]) {
            return 0;
        }
    }
    return 1;
}

// 复制数组
void copy_array(int dest[], int src[], int size) {
    for (int i = 0; i < size; i++) {
        dest[i] = src[i];
    }
}
