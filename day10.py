from collections import defaultdict
from itertools import combinations

import math

with open('input/day10.txt') as f:
    field = f.read().splitlines()

asteroids = [(x, y) for y, line in enumerate(field) for x, ch in enumerate(line) if ch == '#']

visibility = defaultdict(int)


def line_of_sight(ast1, ast2):
    dx, dy = ast2[0] - ast1[0], ast2[1] - ast1[1]
    factor = math.gcd(dx, dy)
    if factor > 1:
        dx //= factor
        dy //= factor
        x, y = ast1[0] + dx, ast1[1] + dy
        while (x, y) != ast2:
            if (x, y) in asteroids:
                return False
            x += dx
            y += dy
    return True


for a, b in combinations(asteroids, 2):
    if line_of_sight(a, b):
        visibility[a] += 1
        visibility[b] += 1
best = max(visibility, key=lambda item: visibility[item])
print('Part 1:', visibility[best])


def angle(ast):
    rise = ast[1] - best[1]
    run = ast[0] - best[0]
    base_angle = math.acos(run / math.sqrt(rise ** 2 + run ** 2)) * 180 / math.pi
    base_angle = round(base_angle, 5)
    return base_angle if rise <= 0 else 360 - base_angle


asteroids.remove(best)

angles = {asteroid: angle(asteroid)
          for asteroid in asteroids}


def zap(angle):
    return min([ast for ast, ang in angles.items() if ang == angle],
               key=lambda ast: abs(ast[0] - best[0]) + abs(ast[1] - best[1]))


def next_angle(angle):
    candidates = [ang for ang in angles.values() if ang < angle]
    if candidates:
        return max(candidates)
    else:
        return max(angles.values())


angle = 90
zapped = 0, 0
for i in range(200):
    zapped = zap(angle)
    del angles[zapped]
    angle = next_angle(angle)
print('Part 2:', zapped[0] * 100 + zapped[1])
