#include <stdio.h>

int rle_encode(const char *src, int n, char *out) {
    if (n <= 0) return 0;
    int out_idx = 0;
    int i = 0;
    while (i < n) {
        int run = 1;
        while (i + 1 < n && src[i] == src[i + 1] && run < 255) {
            run++;
            i++;
        }
        out[out_idx++] = (char)run;
        out[out_idx++] = src[i];
        i++;
    }
    return out_idx;
}

int main(void) {
    const char raw[] = "AAABBBCCCCDD";
    char compressed[32];
    int len = rle_encode(raw, 12, compressed);
    return len;
}
