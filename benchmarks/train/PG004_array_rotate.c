#include <stdio.h>

static void reverse_range(int *arr, int start, int end) {
    while (start < end) {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}

void rotate_left(int *arr, int n, int k) {
    if (n <= 0) return;
    k = k % n;
    if (k < 0) k += n;
    reverse_range(arr, 0, k - 1);
    reverse_range(arr, k, n - 1);
    reverse_range(arr, 0, n - 1);
}

int main(void) {
    int arr[12] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
    rotate_left(arr, 12, 5);
    return arr[0] + arr[11];
}
