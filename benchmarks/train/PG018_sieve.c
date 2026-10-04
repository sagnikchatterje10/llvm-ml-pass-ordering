#include <stdio.h>

int count_primes(int limit) {
    char is_prime[100];
    for (int i = 0; i < limit; i++) is_prime[i] = 1;
    is_prime[0] = is_prime[1] = 0;
    for (int p = 2; p * p < limit; p++) {
        if (is_prime[p]) {
            for (int i = p * p; i < limit; i += p) {
                is_prime[i] = 0;
            }
        }
    }
    int count = 0;
    for (int i = 2; i < limit; i++) {
        if (is_prime[i]) count++;
    }
    return count;
}

int main(void) {
    return count_primes(100);
}
