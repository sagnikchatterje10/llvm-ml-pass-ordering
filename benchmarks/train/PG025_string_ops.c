#include <stdio.h>

int str_len(const char *s) {
    const char *p = s;
    while (*p) p++;
    return (int)(p - s);
}

void str_cpy(char *dest, const char *src) {
    while ((*dest++ = *src++));
}

int main(void) {
    const char *msg = "Optimizing LLVM IR";
    char buf[32];
    str_cpy(buf, msg);
    return str_len(buf);
}
