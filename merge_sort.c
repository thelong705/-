#include "sort_algorithms.h"

// 合并函数
void merge(int arr[], int left, int mid, int right, PerformanceStats *stats) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    
    if (stats) stats->memory_usage += (n1 + n2) * sizeof(int);
    
    // 创建临时数组
    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));
    
    // 拷贝数据到临时数组
    for (int i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];
    
    // 合并临时数组
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (stats) stats->comparisons++;
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        if (stats) stats->swaps++;
        k++;
    }
    
    // 拷贝剩余元素
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
        if (stats) stats->swaps++;
    }
    
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
        if (stats) stats->swaps++;
    }
    
    free(L);
    free(R);
}

// 顺序归并排序
void merge_sort_sequential(int arr[], int left, int right, PerformanceStats *stats) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        merge_sort_sequential(arr, left, mid, stats);
        merge_sort_sequential(arr, mid + 1, right, stats);
        
        merge(arr, left, mid, right, stats);
    }
}

// 并行归并排序
void merge_sort_parallel(int arr[], int left, int right, PerformanceStats *stats) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        
        // 设置并行化阈值，小数组使用顺序排序
        if (right - left > 1000) {
            #pragma omp parallel sections
            {
                #pragma omp section
                merge_sort_parallel(arr, left, mid, stats);
                
                #pragma omp section
                merge_sort_parallel(arr, mid + 1, right, stats);
            }
        } else {
            merge_sort_sequential(arr, left, mid, stats);
            merge_sort_sequential(arr, mid + 1, right, stats);
        }
        
        merge(arr, left, mid, right, stats);
    }
}
