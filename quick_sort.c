#include "sort_algorithms.h"

// 三数取中法选择pivot
int median_of_three(int arr[], int low, int high) {
    int mid = low + (high - low) / 2;
    
    // 对三个数进行排序
    if (arr[low] > arr[mid]) {
        if (arr[mid] > arr[high]) return mid;
        else return (arr[low] > arr[high]) ? high : low;
    } else {
        if (arr[low] > arr[high]) return low;
        else return (arr[mid] > arr[high]) ? high : mid;
    }
}

// 分区函数
int partition(int arr[], int low, int high, PerformanceStats *stats) {
    // 使用三数取中法选择pivot
    int pivot_index = median_of_three(arr, low, high);
    int pivot = arr[pivot_index];
    
    // 将pivot移到末尾
    int temp = arr[pivot_index];
    arr[pivot_index] = arr[high];
    arr[high] = temp;
    if (stats) stats->swaps++;
    
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (stats) stats->comparisons++;
        if (arr[j] <= pivot) {
            i++;
            // 交换arr[i]和arr[j]
            temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            if (stats) stats->swaps++;
        }
    }
    
    // 将pivot放到正确位置
    temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    if (stats) stats->swaps++;
    
    return i + 1;
}

// 递归快速排序
void quick_sort_recursive(int arr[], int low, int high, PerformanceStats *stats) {
    if (low < high) {
        int pi = partition(arr, low, high, stats);
        quick_sort_recursive(arr, low, pi - 1, stats);
        quick_sort_recursive(arr, pi + 1, high, stats);
    }
}

// 栈操作函数
Stack* create_stack(int capacity) {
    Stack *stack = (Stack*)malloc(sizeof(Stack));
    stack->items = (StackItem*)malloc(capacity * sizeof(StackItem));
    stack->top = -1;
    stack->capacity = capacity;
    return stack;
}

void push(Stack *stack, int left, int right) {
    if (stack->top < stack->capacity - 1) {
        stack->top++;
        stack->items[stack->top].left = left;
        stack->items[stack->top].right = right;
    }
}

StackItem pop(Stack *stack) {
    StackItem item = {-1, -1};
    if (stack->top >= 0) {
        item = stack->items[stack->top];
        stack->top--;
    }
    return item;
}

int is_empty(Stack *stack) {
    return stack->top == -1;
}

void free_stack(Stack *stack) {
    free(stack->items);
    free(stack);
}

// 非递归快速排序
void quick_sort_non_recursive(int arr[], int low, int high, PerformanceStats *stats) {
    if (high - low <= 0) return;
    
    Stack *stack = create_stack(high - low + 1);
    push(stack, low, high);
    
    while (!is_empty(stack)) {
        StackItem item = pop(stack);
        int l = item.left;
        int r = item.right;
        
        if (l < r) {
            int pi = partition(arr, l, r, stats);
            
            // 先压入较大的分区，减少栈深度
            if (pi - l > r - pi) {
                push(stack, l, pi - 1);
                push(stack, pi + 1, r);
            } else {
                push(stack, pi + 1, r);
                push(stack, l, pi - 1);
            }
        }
    }
    
    free_stack(stack);
}
