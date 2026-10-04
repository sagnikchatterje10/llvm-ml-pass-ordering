#include <stdio.h>

#define TABLE_SIZE 16

struct HashEntry {
    int key;
    int value;
    int occupied;
};

void ht_init(struct HashEntry *table) {
    for (int i = 0; i < TABLE_SIZE; i++) table[i].occupied = 0;
}

void ht_insert(struct HashEntry *table, int key, int val) {
    int idx = (key >= 0 ? key : -key) % TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        if (!table[pos].occupied || table[pos].key == key) {
            table[pos].key = key;
            table[pos].value = val;
            table[pos].occupied = 1;
            return;
        }
    }
}

int ht_lookup(const struct HashEntry *table, int key) {
    int idx = (key >= 0 ? key : -key) % TABLE_SIZE;
    for (int i = 0; i < TABLE_SIZE; i++) {
        int pos = (idx + i) % TABLE_SIZE;
        if (!table[pos].occupied) return -1;
        if (table[pos].key == key) return table[pos].value;
    }
    return -1;
}

int main(void) {
    struct HashEntry ht[TABLE_SIZE];
    ht_init(ht);
    ht_insert(ht, 101, 500);
    ht_insert(ht, 117, 600); // hash collision (101%16 == 117%16 == 5)
    ht_insert(ht, 202, 700);
    int v1 = ht_lookup(ht, 101);
    int v2 = ht_lookup(ht, 117);
    return (v1 + v2) & 0xFF;
}
