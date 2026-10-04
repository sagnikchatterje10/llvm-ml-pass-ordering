#include <stdio.h>

void bubble_sort(int *arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
                swapped = 1;
            }
        }
        if (!swapped) break;
    }
}

int main(void) {
    int nums[10] = {64, 34, 25, 12, 22, 11, 90, 88, 76, 45};
    bubble_sort(nums, 10);
    return nums[0] + nums[9];
}
