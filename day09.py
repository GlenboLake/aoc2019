from intcode import run

with open('input/day09.txt') as f:
    program = list(map(int, f.read().strip().split(',')))

print('Part 1:', next(run(program, [1])))
print('Part 2:', next(run(program, [2])))
