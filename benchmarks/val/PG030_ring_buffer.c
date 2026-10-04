#include <stdio.h>

#define CAP 8

struct RingBuffer {
    int buffer[CAP];
    int head;
    int tail;
    int count;
};

void rb_init(struct RingBuffer *rb) {
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

int rb_push(struct RingBuffer *rb, int val) {
    if (rb->count == CAP) return 0;
    rb->buffer[rb->tail] = val;
    rb->tail = (rb->tail + 1) % CAP;
    rb->count++;
    return 1;
}

int rb_pop(struct RingBuffer *rb, int *val) {
    if (rb->count == 0) return 0;
    *val = rb->buffer[rb->head];
    rb->head = (rb->head + 1) % CAP;
    rb->count--;
    return 1;
}

int main(void) {
    struct RingBuffer rb;
    rb_init(&rb);
    for (int i = 0; i < 6; i++) rb_push(&rb, i * 10);
    int v1, v2;
    rb_pop(&rb, &v1);
    rb_pop(&rb, &v2);
    return (v1 + v2 + rb.count) & 0xFF;
}
