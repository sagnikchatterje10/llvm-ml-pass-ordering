#include <stdio.h>

struct Node {
    int data;
    int next_idx;
};

int filter_sum(const struct Node *pool, int head, int threshold) {
    int sum = 0;
    int curr = head;
    while (curr >= 0) {
        if (pool[curr].data > threshold) {
            sum += pool[curr].data;
        }
        curr = pool[curr].next_idx;
    }
    return sum;
}

int main(void) {
    struct Node pool[6] = {
        {10, 1}, {25, 2}, {5, 3}, {40, 4}, {15, 5}, {30, -1}
    };
    int s = filter_sum(pool, 0, 15);
    return s & 0xFF;
}
