from intcode import run

with open('input/day05.txt') as f:
    ints = list(map(int, f.read().split(',')))

output = []
run(ints.copy(), 1, buffer=output)
print('part 1:', output[-1])

output.clear()
run(ints.copy(), 5, buffer=output)
print('part 2:', output[-1])
