def part1(mass):
    return mass // 3 - 2


assert part1(12) == 2
assert part1(14) == 2
assert part1(1969) == 654
assert part1(100756) == 33583

with open('input/day01.txt') as f:
    masses = list(map(int, f))
print(sum(map(part1, masses)))


def part2(mass):
    total = 0
    fuel = part1(mass)
    while fuel > 0:
        total += fuel
        fuel = part1(fuel)
    return total


assert part2(14) == 2
assert part2(1969) == 966
assert part2(100756) == 50346

print(sum(map(part2, masses)))
