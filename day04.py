from collections import Counter

min_, max_ = 387638, 919123


def valid1(num):
    return list(num) == sorted(num) and max(Counter(num).values()) >= 2


def valid2(num):
    return list(num) == sorted(num) and 2 in Counter(num).values()


part1 = part2 = 0
for i in range(min_, max_ + 1):
    if valid1(str(i)):
        part1 += 1
    if valid2(str(i)):
        part2 += 1

print(part1)
print(part2)
