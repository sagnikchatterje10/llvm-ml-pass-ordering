#include <stdio.h>

struct TreeNode {
    int val;
    int left_idx;
    int right_idx;
};

int tree_sum(const struct TreeNode *nodes, int idx) {
    if (idx < 0) return 0;
    int s = nodes[idx].val;
    s += tree_sum(nodes, nodes[idx].left_idx);
    s += tree_sum(nodes, nodes[idx].right_idx);
    return s;
}

int main(void) {
    struct TreeNode nodes[5] = {
        {10, 1, 2},
        {5, 3, 4},
        {15, -1, -1},
        {2, -1, -1},
        {7, -1, -1}
    };
    int total = tree_sum(nodes, 0);
    return total & 0xFF;
}
