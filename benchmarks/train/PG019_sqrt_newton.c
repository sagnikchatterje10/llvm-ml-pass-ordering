#include <stdio.h>

double sqrt_newton(double n) {
    if (n < 0) return -1.0;
    if (n == 0) return 0.0;
    double x = n;
    for (int i = 0; i < 20; i++) {
        double root = 0.5 * (x + (n / x));
        double diff = root - x;
        if (diff < 0) diff = -diff;
        if (diff < 1e-6) return root;
        x = root;
    }
    return x;
}

int main(void) {
    double s = sqrt_newton(256.0);
    return (int)s;
}
