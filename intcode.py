import sys
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
    DONE = 99


# These are the ops for which the last parameter is always in position mode
writers = [
    Op.ADD,
    Op.MUL,
    Op.INPUT,
    Op.LESS_THAN,
    Op.EQUAL,
]


class ListPrinter(object):
    """
    Helper class to allow us to use `print` function for opcode 4 to write to a list

    This is mostly helpful because my input for Day 5, part 1 spit out a bunch of zeroes,
    so this is a way to suppress those and just look at the final thing printed.
    """

    def __init__(self, buf):
        """
        :param list buf: The object to add to
        """
        self.buf = buf

    def write(self, s):
        if s.strip():
            self.buf.append(s)


def run(program, input=None, buffer=sys.stdout):
    ip = 0
    if isinstance(buffer, list):
        buffer = ListPrinter(buffer)

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
            print(value, file=buffer)
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
