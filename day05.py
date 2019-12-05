from intcode import run

with open('input/day05.txt') as f:
    ints = list(map(int, f.read().split(',')))

print('part 1: ', end='')
run(ints.copy(), 1)
print('part 2: ', end='')
run(ints.copy(), 5)
