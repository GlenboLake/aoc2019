from intcode import load, run

program = load(9)

print('Part 1:', next(run(program, [1])))
print('Part 2:', next(run(program, [2])))
