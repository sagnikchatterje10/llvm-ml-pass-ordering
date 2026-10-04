#include <stdio.h>

long long vec_dot(const int *a, const int *b, int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += (long long)a[i] * b[i];
    }
    return sum;
}

int main(void) {
    int a[16] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
    int b[16] = {16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    long long res = vec_dot(a, b, 16);
    return (int)(res & 0xFF);
}
