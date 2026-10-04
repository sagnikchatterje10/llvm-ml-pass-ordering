#include <stdio.h>

unsigned int popcount(unsigned int v) {
    v = v - ((v >> 1) & 0x55555555);
    v = (v & 0x33333333) + ((v >> 2) & 0x33333333);
    return (((v + (v >> 4)) & 0xF0F0F0F) * 0x1010101) >> 24;
}

int main(void) {
    unsigned int test_vals[8] = {0, 1, 0xFF, 0x12345678, 0xAAAAAAAA, 0x55555555, 0xFFFFFFFF, 42};
    unsigned int acc = 0;
    for (int i = 0; i < 8; i++) acc += popcount(test_vals[i]);
    return (int)(acc & 0xFF);
}
