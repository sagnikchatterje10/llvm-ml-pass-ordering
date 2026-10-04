#include <stdio.h>

int is_palindrome(const char *s, int len) {
    const char *left = s;
    const char *right = s + len - 1;
    while (left < right) {
        if (*left != *right) return 0;
        left++;
        right--;
    }
    return 1;
}

int main(void) {
    const char w1[] = "racecar";
    const char w2[] = "compiler";
    int r1 = is_palindrome(w1, 7);
    int r2 = is_palindrome(w2, 8);
    return r1 + (r2 ? 0 : 2);
}
