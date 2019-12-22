import string
from itertools import product

from intcode import load, run

program = load(21)

inputs = []
runner = run(program[:], inputs)

prompt = ''
v = None
while v != '\n':
    v = chr(next(runner))
    prompt += v
print(prompt)

springscript = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
'''
inputs.extend([ord(ch) for ch in springscript])

for val in runner:
    try:
        print(chr(val), end='')
    except ValueError:
        print()
        print(val)

def run_springscript(code):
    lines = code.splitlines()
    inputs = product([True, False], repeat=9)
    for seq in inputs:
        regs = {**dict(zip(string.ascii_uppercase, seq)), 'J': False, 'T': False}
        for line in lines:
            if line == 'WALK':
                break
            op, arg1, dst = line.split()
            if op == 'AND':
                regs[dst] = regs[arg1] and regs[dst]
            elif op == 'OR':
                regs[dst] = regs[arg1] or regs[dst]
            elif op == 'NOT':
                regs[dst] = not regs[arg1]
        print(''.join('#' if x else '.' for x in seq), regs['J'])


run_springscript('''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT E T
AND H T
AND T J
''')


springscript2 = '''\
NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J
NOT H T
NOT T T
OR E T
AND T J
RUN
'''

runner = run(program[:], [ord(ch) for ch in springscript2])

for val in runner:
    try:
        print(chr(val), end='')
    except ValueError:
        print(val)