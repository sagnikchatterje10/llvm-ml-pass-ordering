#include <stdio.h>

#define OP_NOP 0
#define OP_ADD 1
#define OP_SUB 2
#define OP_MUL 3
#define OP_HALT 4

int run_vm(const int *ops, int len) {
    int acc = 0;
    for (int pc = 0; pc < len; pc += 2) {
        int opcode = ops[pc];
        int operand = ops[pc + 1];
        switch (opcode) {
            case OP_NOP:
                break;
            case OP_ADD:
                acc += operand;
                break;
            case OP_SUB:
                acc -= operand;
                break;
            case OP_MUL:
                acc *= operand;
                break;
            case OP_HALT:
                return acc;
            default:
                acc = -1;
                return acc;
        }
    }
    return acc;
}

int main(void) {
    int program[10] = {OP_ADD, 15, OP_MUL, 3, OP_SUB, 5, OP_HALT, 0, OP_ADD, 99};
    int res = run_vm(program, 10);
    return res & 0xFF;
}
