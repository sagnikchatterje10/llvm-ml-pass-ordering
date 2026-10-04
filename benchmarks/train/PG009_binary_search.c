#include <stdio.h>

int binary_search(const int *arr, int n, int target) {
    int low = 0;
    int high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int main(void) {
    int sorted[16] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 100, 120, 135, 140, 150, 160};
    int r1 = binary_search(sorted, 16, 23);
    int r2 = binary_search(sorted, 16, 999);
    return r1 + (r2 == -1 ? 1 : 0);
}
