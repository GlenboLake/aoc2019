from intcode import run

with open('input/day05.txt') as f:
    ints = list(map(int, f.read().split(',')))

output = []
part_1 = run(ints[:], iter([1]))
print('part 1:', list(part_1)[-1])

output.clear()
part_2 = run(ints[:], iter([5]))
print('part 2:', list(part_2)[-1])
