#include <stdio.h>

int collatz_length(long long n) {
    int steps = 0;
    while (n > 1) {
        if (n & 1) {
            n = 3 * n + 1;
        } else {
            n = n / 2;
        }
        steps++;
    }
    return steps;
}

int main(void) {
    int s1 = collatz_length(27);
    int s2 = collatz_length(19);
    return (s1 + s2) & 0xFF;
}
