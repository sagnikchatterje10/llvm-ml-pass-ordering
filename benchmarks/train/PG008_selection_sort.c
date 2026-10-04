#include <stdio.h>

void selection_sort(int *arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        if (min_idx != i) {
            int tmp = arr[i];
            arr[i] = arr[min_idx];
            arr[min_idx] = tmp;
        }
    }
}

int main(void) {
    int a[8] = {29, 10, 14, 37, 13, 5, 2, 99};
    selection_sort(a, 8);
    return a[0] + a[7];
}
