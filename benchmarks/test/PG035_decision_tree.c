#include <stdio.h>

int classify_point(int x, int y, int z) {
    if (x > 10) {
        if (y < 20) {
            if (z >= 5) return 1;
            else return 2;
        } else {
            if (z % 2 == 0) return 3;
            else return 4;
        }
    } else {
        if (y >= 50) {
            if (z < 0) return 5;
            else return 6;
        } else {
            if (x == y) return 7;
            else return 8;
        }
    }
}

int main(void) {
    int c1 = classify_point(15, 10, 8);
    int c2 = classify_point(5, 50, -3);
    int c3 = classify_point(2, 2, 10);
    return c1 + c2 + c3;
}
