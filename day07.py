from itertools import permutations

from intcode import run

with open('input/day07.txt') as f:
    prog = list(map(int, f.read().strip().split(',')))

inputs = list(permutations(range(5), 5))

demo = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
best = 0

for seq in inputs:
    value = 0
    for amp in seq:
        value = next(run(prog, iter((amp, value))))
    best = max(best, value)
print('Part 1:', best)
