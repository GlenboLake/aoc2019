from intcode import load, run

DEBUG = False

program = load(19)

inputs = []
runner = run(program[:], inputs)


def check(x, y):
    return next(run(program[:], [x, y]))


def part1():
    hits = 0
    for x in range(50):
        print(f'{x: 3} ', end='')
        for y in range(50):
            result = check(x, y)
            if result == 0:
                print('.', end='')
            elif result == 1:
                print('#', end='')
                hits += 1
            else:
                print('?', end='')
        print()
    return hits


def part1_no_draw():
    return sum(check(x, y) for x in range(50) for y in range(50))


print('Part 1:', part1_no_draw())


def part2():
    size = 100
    ranges = {}
    x = 40
    affected = [y for y in range(50) if check(x, y)]
    left, right = min(affected), max(affected)
    ranges[x] = left, right
    while True:
        left, right = ranges[x]
        x += 1
        while check(x, left) == 0:
            left += 1
        while check(x, right) == 1:
            right += 1
        right -= 1
        ranges[x] = left, right

        # print(f'{x: 5}, {left: 5}, {right: 5}')

        if (x - size + 1 in ranges) and (ranges[x - size + 1][1] >= left + size - 1):
            return (x - size + 1) * 10000 + left


print('Part 2:', part2())
