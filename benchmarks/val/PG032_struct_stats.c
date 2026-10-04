#include <stdio.h>

struct Item {
    int id;
    int weight;
    int value;
};

void compute_stats(const struct Item *items, int n, int *total_weight, int *max_value) {
    *total_weight = 0;
    *max_value = -1;
    for (int i = 0; i < n; i++) {
        *total_weight += items[i].weight;
        if (items[i].value > *max_value) {
            *max_value = items[i].value;
        }
    }
}

int main(void) {
    struct Item list[5] = {
        {1, 10, 60},
        {2, 20, 100},
        {3, 30, 120},
        {4, 15, 75},
        {5, 25, 95}
    };
    int tw, mv;
    compute_stats(list, 5, &tw, &mv);
    return (tw + mv) & 0xFF;
}
