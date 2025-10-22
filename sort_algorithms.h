#ifndef SORT_ALGORITHMS_H
#define SORT_ALGORITHMS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <omp.h>

// 栈结构用于非递归快速排序
typedef struct {
    int left;
    int right;
} StackItem;

typedef struct {
    StackItem *items;
    int top;
    int capacity;
} Stack;

// 性能统计结构
typedef struct {
    double time;
    long long comparisons;
    long long swaps;
    long long memory_usage;
} PerformanceStats;

// 函数声明
// 快速排序
void quick_sort_recursive(int arr[], int low, int high, PerformanceStats *stats);
void quick_sort_non_recursive(int arr[], int low, int high, PerformanceStats *stats);
int partition(int arr[], int low, int high, PerformanceStats *stats);
int median_of_three(int arr[], int low, int high);

// 归并排序
void merge_sort_sequential(int arr[], int left, int right, PerformanceStats *stats);
void merge_sort_parallel(int arr[], int left, int right, PerformanceStats *stats);
void merge(int arr[], int left, int mid, int right, PerformanceStats *stats);

// 栈操作
Stack* create_stack(int capacity);
void push(Stack *stack, int left, int right);
StackItem pop(Stack *stack);
int is_empty(Stack *stack);
void free_stack(Stack *stack);

// 工具函数
void generate_test_data(const char *filename, int count, int data_type);
void read_test_data(const char *filename, int arr[], int *count);
void print_array(int arr[], int size);
int is_sorted(int arr[], int size);
void copy_array(int dest[], int src[], int size);
void init_performance_stats(PerformanceStats *stats);
void print_performance_stats(const PerformanceStats *stats, const char *algorithm_name);

#endif
