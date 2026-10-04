#include <stdio.h>

unsigned int reverse_bits(unsigned int n) {
    n = ((n >> 1) & 0x55555555) | ((n & 0x55555555) << 1);
    n = ((n >> 2) & 0x33333333) | ((n & 0x33333333) << 2);
    n = ((n >> 4) & 0x0F0F0F0F) | ((n & 0x0F0F0F0F) << 4);
    n = ((n >> 8) & 0x00FF00FF) | ((n & 0x00FF00FF) << 8);
    return (n >> 16) | (n << 16);
}

int main(void) {
    unsigned int r = reverse_bits(0x12345678);
    return (int)(r & 0xFF);
}
