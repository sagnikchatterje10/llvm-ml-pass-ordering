#include <stdio.h>

unsigned int crc32_simple(const unsigned char *data, int len) {
    unsigned int crc = 0xFFFFFFFF;
    for (int i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
            else
                crc >>= 1;
        }
    }
    return ~crc;
}

int main(void) {
    unsigned char msg[] = "Compiler Optimization ML 2026";
    unsigned int c = crc32_simple(msg, sizeof(msg) - 1);
    return (int)(c & 0x7F);
}
