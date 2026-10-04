#include <stdio.h>

int gcd(int a, int b) {
    while (b != 0) {
        int t = b;
        b = a % b;
        a = t;
    }
    return a;
}

long long lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    return ((long long)a / gcd(a, b)) * b;
}

int main(void) {
    int g = gcd(48, 180);
    long long l = lcm(48, 180);
    return (int)((g + l) & 0xFF);
}
