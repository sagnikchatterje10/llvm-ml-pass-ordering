#include <stdio.h>

#define N 8

void matmul(const int a[N][N], const int b[N][N], int c[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            int acc = 0;
            for (int k = 0; k < N; k++) {
                acc += a[i][k] * b[k][j];
            }
            c[i][j] = acc;
        }
    }
}

int main(void) {
    int a[N][N], b[N][N], c[N][N];
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            a[i][j] = (i + j) & 7;
            b[i][j] = (i * j + 1) & 7;
            c[i][j] = 0;
        }
    }
    matmul(a, b, c);
    return c[0][0] + c[N-1][N-1];
}
