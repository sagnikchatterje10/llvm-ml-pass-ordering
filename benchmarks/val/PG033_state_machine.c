#include <stdio.h>

typedef enum { STATE_IDLE, STATE_ACTIVE, STATE_WAITING, STATE_DONE, STATE_ERROR } State;

State step_fsm(State s, int event) {
    switch (s) {
        case STATE_IDLE:
            return (event == 1) ? STATE_ACTIVE : STATE_IDLE;
        case STATE_ACTIVE:
            if (event == 0) return STATE_WAITING;
            if (event == 2) return STATE_DONE;
            if (event == 9) return STATE_ERROR;
            return STATE_ACTIVE;
        case STATE_WAITING:
            return (event == 1) ? STATE_ACTIVE : STATE_DONE;
        case STATE_DONE:
        case STATE_ERROR:
        default:
            return STATE_IDLE;
    }
}

int main(void) {
    State s = STATE_IDLE;
    int events[6] = {1, 0, 1, 2, 0, 1};
    for (int i = 0; i < 6; i++) {
        s = step_fsm(s, events[i]);
    }
    return (int)s;
}
