#include <stdio.h>

#define W 10
#define H 10

void conv2d(const int in[H][W], int out[H][W], const int kernel[3][3]) {
    for (int y = 1; y < H - 1; y++) {
        for (int x = 1; x < W - 1; x++) {
            int acc = 0;
            for (int ky = -1; ky <= 1; ky++) {
                for (int kx = -1; kx <= 1; kx++) {
                    acc += in[y + ky][x + kx] * kernel[ky + 1][kx + 1];
                }
            }
            out[y][x] = acc / 9;
        }
    }
}

int main(void) {
    int in[H][W], out[H][W] = {0};
    int k[3][3] = {{1, 1, 1}, {1, 2, 1}, {1, 1, 1}};
    for (int i = 0; i < H; i++)
        for (int j = 0; j < W; j++)
            in[i][j] = (i * 3 + j) % 256;
    conv2d(in, out, k);
    return out[5][5] & 0xFF;
}
