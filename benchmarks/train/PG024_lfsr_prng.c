#include <stdio.h>

unsigned int lfsr_step(unsigned int *lfsr) {
    unsigned int bit = ((*lfsr >> 0) ^ (*lfsr >> 2) ^ (*lfsr >> 3) ^ (*lfsr >> 5)) & 1;
    *lfsr = (*lfsr >> 1) | (bit << 15);
    return *lfsr;
}

int main(void) {
    unsigned int state = 0xACE1;
    unsigned int sum = 0;
    for (int i = 0; i < 50; i++) {
        sum += lfsr_step(&state);
    }
    return (int)(sum & 0xFF);
}
