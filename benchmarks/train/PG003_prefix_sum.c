#include <stdio.h>

void prefix_sum(int *arr, int *out, int n) {
    if (n <= 0) return;
    out[0] = arr[0];
    for (int i = 1; i < n; i++) {
        out[i] = out[i - 1] + arr[i];
    }
}

int main(void) {
    int data[20];
    int result[20];
    for (int i = 0; i < 20; i++) data[i] = i * 2 + 1;
    prefix_sum(data, result, 20);
    return result[19] & 0x7F;
}
