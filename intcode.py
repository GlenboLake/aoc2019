from enum import IntEnum


class Op(IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    PRINT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    DONE = 99


writers = [
    Op.ADD,
    Op.MUL,
    Op.INPUT,
    Op.LESS_THAN,
    Op.EQUAL,
]


def run(program, input=None):
    ip = 0

    def get_args(nargs):
        nonlocal ip
        modes = program[ip] // 100
        args = []
        for i in range(1, nargs):
            arg = program[ip + i]
            if modes % 10 == 0:
                arg = program[arg]
            modes //= 10
            args.append(arg)
        arg = program[ip + nargs]
        if Op(program[ip] % 100) not in writers and modes % 10 == 0:
            arg = program[arg]
        args.append(arg)
        return args

    while True:
        opcode = Op(program[ip] % 100)

        if opcode == Op.DONE:
            break
        elif opcode == Op.ADD:
            a, b, dst = get_args(3)
            program[dst] = a + b
            ip += 4
        elif opcode == Op.MUL:
            a, b, dst = get_args(3)
            program[dst] = a * b
            ip += 4
        elif opcode == Op.INPUT:
            dst, = get_args(1)
            program[dst] = input
            ip += 2
        elif opcode == Op.PRINT:
            value, = get_args(1)
            if value != 0:
                print(value)
            ip += 2
        elif opcode == Op.JUMP_IF_TRUE:
            check, new_ip = get_args(2)
            if check:
                ip = new_ip
            else:
                ip += 3
        elif opcode == Op.JUMP_IF_FALSE:
            check, new_ip = get_args(2)
            if not check:
                ip = new_ip
            else:
                ip += 3
        elif opcode == Op.LESS_THAN:
            a, b, res = get_args(3)
            program[res] = int(a < b)
            ip += 4
        elif opcode == Op.EQUAL:
            a, b, res = get_args(3)
            program[res] = int(a == b)
            ip += 4
        else:
            raise NotImplementedError
