#include <stdio.h>

static double f(double t, double y) {
    return t * y - 0.5 * y * y;
}

double rk2_integrate(double t0, double y0, double h, int steps) {
    double t = t0;
    double y = y0;
    for (int i = 0; i < steps; i++) {
        double k1 = h * f(t, y);
        double k2 = h * f(t + h, y + k1);
        y += 0.5 * (k1 + k2);
        t += h;
    }
    return y;
}

int main(void) {
    double res = rk2_integrate(0.0, 1.0, 0.05, 20);
    return (int)(res * 10.0) & 0xFF;
}
