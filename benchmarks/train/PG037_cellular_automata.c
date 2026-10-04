#include <stdio.h>

#define CELLS 32

void evolve_rule30(unsigned char *state, int steps) {
    unsigned char next[CELLS];
    for (int s = 0; s < steps; s++) {
        for (int i = 0; i < CELLS; i++) {
            unsigned char left = (i > 0) ? state[i - 1] : state[CELLS - 1];
            unsigned char center = state[i];
            unsigned char right = (i < CELLS - 1) ? state[i + 1] : state[0];
            int pat = (left << 2) | (center << 1) | right;
            next[i] = (30 >> pat) & 1;
        }
        for (int i = 0; i < CELLS; i++) state[i] = next[i];
    }
}

int main(void) {
    unsigned char state[CELLS] = {0};
    state[CELLS / 2] = 1;
    evolve_rule30(state, 10);
    int count = 0;
    for (int i = 0; i < CELLS; i++) count += state[i];
    return count;
}
