#include <stdio.h>

double horner(const double *coeffs, int degree, double x) {
    double res = coeffs[0];
    for (int i = 1; i <= degree; i++) {
        res = res * x + coeffs[i];
    }
    return res;
}

int main(void) {
    double poly[5] = {3.0, -2.0, 5.0, -1.0, 7.0};
    double r = horner(poly, 4, 2.5);
    return (int)r & 0xFF;
}
