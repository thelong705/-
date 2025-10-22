#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// 简单的快速排序用于测试
void quick_sort(int arr[], int left, int right) {
    if (left >= right) return;
    
    int pivot = arr[right];
    int i = left - 1;
    
    for (int j = left; j < right; j++) {
        if (arr[j] <= pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    int temp = arr[i + 1];
    arr[i + 1] = arr[right];
    arr[right] = temp;
    
    int pi = i + 1;
    quick_sort(arr, left, pi - 1);
    quick_sort(arr, pi + 1, right);
}

// 生成测试数据
void generate_test_data(int count, const char* filename) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        printf("无法创建文件: %s\n", filename);
        return;
    }
    
    srand(time(NULL));
    fprintf(file, "%d\n", count);
    
    for (int i = 0; i < count; i++) {
        fprintf(file, "%d\n", rand() % 10000);
    }
    
    fclose(file);
    printf("生成测试数据: %s (%d条记录)\n", filename, count);
}

// 读取测试数据
int read_test_data(const char* filename, int arr[]) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("无法读取文件: %s\n", filename);
        return 0;
    }
    
    int count;
    fscanf(file, "%d", &count);
    
    for (int i = 0; i < count; i++) {
        fscanf(file, "%d", &arr[i]);
    }
    
    fclose(file);
    return count;
}

// 检查数组是否已排序
int is_sorted(int arr[], int size) {
    for (int i = 1; i < size; i++) {
        if (arr[i] < arr[i - 1]) return 0;
    }
    return 1;
}

int main() {
    printf("=== 简单排序测试程序 ===\n");
    
    // 确保目录存在
    system("mkdir -p ../data ../results");
    
    int sizes[] = {100, 1000, 10000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);
    
    // 创建CSV文件头
    FILE* csv = fopen("../results/performance_data.csv", "w");
    if (csv) {
        fprintf(csv, "Optimization,DataSize,Algorithm,Time,Comparisons,Swaps,MemoryUsage\n");
        fclose(csv);
        printf("创建CSV文件头\n");
    }
    
    for (int i = 0; i < num_sizes; i++) {
        int size = sizes[i];
        printf("\n测试数据规模: %d\n", size);
        
        // 生成测试数据
        char filename[100];
        sprintf(filename, "../data/test_data_%d.txt", size);
        generate_test_data(size, filename);
        
        // 读取数据
        int* arr = malloc(size * sizeof(int));
        int actual_size = read_test_data(filename, arr);
        
        if (actual_size != size) {
            printf("错误: 读取的数据量不匹配\n");
            free(arr);
            continue;
        }
        
        // 测试排序性能
        double start_time = omp_get_wtime();
        quick_sort(arr, 0, size - 1);
        double end_time = omp_get_wtime();
        double elapsed = end_time - start_time;
        
        // 验证排序结果
        int sorted = is_sorted(arr, size);
        
        printf("  排序时间: %.6f 秒\n", elapsed);
        printf("  排序正确: %s\n", sorted ? "是" : "否");
        
        // 保存结果到CSV
        csv = fopen("../results/performance_data.csv", "a");
        if (csv) {
            fprintf(csv, "O2,%d,QuickSort,%.6f,0,0,%lu\n", 
                   size, elapsed, size * sizeof(int));
            fclose(csv);
        }
        
        free(arr);
    }
    
    printf("\n=== 测试完成 ===\n");
    printf("数据文件位置: ../data/\n");
    printf("结果文件位置: ../results/performance_data.csv\n");
    
    // 显示生成的文件
    printf("\n生成的文件:\n");
    system("ls -la ../data/ ../results/ 2>/dev/null || echo '目录不存在'");
    
    return 0;
}
