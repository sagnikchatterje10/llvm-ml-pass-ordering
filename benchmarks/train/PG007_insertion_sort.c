#include <stdio.h>

void insertion_sort(int *arr, int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

int main(void) {
    int nums[10] = {12, 11, 13, 5, 6, 7, 2, 45, 9, 1};
    insertion_sort(nums, 10);
    return nums[0] + nums[5];
}
