#include <stdio.h>

long long mod_pow(long long base, long long exp, long long mod) {
    long long res = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) res = (res * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return res;
}

int main(void) {
    long long r = mod_pow(7, 25, 1000000007);
    return (int)(r & 0xFF);
}
