#include <stdio.h>

int hanoi_moves(int n, char from, char to, char aux) {
    if (n == 1) return 1;
    int moves = hanoi_moves(n - 1, from, aux, to);
    moves += 1;
    moves += hanoi_moves(n - 1, aux, to, from);
    return moves;
}

int main(void) {
    int total = hanoi_moves(5, 'A', 'C', 'B');
    return total & 0x7F;
}
