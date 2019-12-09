from collections import Iterator
from enum import IntEnum


class Op(IntEnum):
    """
    For readability's sake
    """
    ADD = 1
    MUL = 2
    INPUT = 3
    PRINT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUAL = 8
    BASE = 9
    DONE = 99


class Mode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


# These are the ops for which the last parameter is never in immediate mode (1)
writers = [
    Op.ADD,
    Op.MUL,
    Op.INPUT,
    Op.LESS_THAN,
    Op.EQUAL,
]


def run(program, inp):
    if not isinstance(inp, Iterator):
        inp = iter(inp)
    program.extend([0] * 10000)
    ip = 0
    base = 0

    def get_args(nargs):
        op = Op(program[ip] % 100)
        modes = program[ip] // 100
        args = []
        for i in range(1, nargs+1):
            arg = program[ip + i]
            mode = Mode(modes%10)
            modes //= 10
            if i < nargs or op not in writers:
                if mode == Mode.POSITION:
                    arg = program[arg]
                elif mode == Mode.RELATIVE:
                    arg = program[arg + base]
            elif mode == Mode.RELATIVE:
                arg += base
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
            program[dst] = next(inp)
            ip += 2
        elif opcode == Op.PRINT:
            value, = get_args(1)
            yield value
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
        elif opcode == Op.BASE:
            adj, = get_args(1)
            base += adj
            ip += 2
        else:
            raise NotImplementedError
