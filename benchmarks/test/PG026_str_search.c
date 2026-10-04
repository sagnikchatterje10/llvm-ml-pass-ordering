#include <stdio.h>

int str_find(const char *haystack, const char *needle) {
    if (!*needle) return 0;
    for (int i = 0; haystack[i] != '\0'; i++) {
        int match = 1;
        for (int j = 0; needle[j] != '\0'; j++) {
            if (haystack[i + j] == '\0' || haystack[i + j] != needle[j]) {
                match = 0;
                break;
            }
        }
        if (match) return i;
    }
    return -1;
}

int main(void) {
    const char *h = "the quick brown fox jumps over the lazy dog";
    const char *n = "fox";
    return str_find(h, n);
}
