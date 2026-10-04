#include <stdio.h>

#define MAX(a, b) ((a) > (b) ? (a) : (b))

int knapsack(int W, const int *wt, const int *val, int n) {
    int dp[16][32] = {0};
    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= W; w++) {
            if (wt[i - 1] <= w) {
                dp[i][w] = MAX(val[i - 1] + dp[i - 1][w - wt[i - 1]], dp[i - 1][w]);
            } else {
                dp[i][w] = dp[i - 1][w];
            }
        }
    }
    return dp[n][W];
}

int main(void) {
    int val[4] = {60, 100, 120, 80};
    int wt[4] = {10, 20, 30, 15};
    int W = 30;
    int res = knapsack(W, wt, val, 4);
    return res & 0xFF;
}
