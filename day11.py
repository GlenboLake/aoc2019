from collections import defaultdict

from intcode import run
from util import show_dict

with open('input/day11.txt') as f:
    data = list(map(int, f.read().split(',')))

BLACK = 0
WHITE = 1


def solve(part):
    inputs = [BLACK if part == 1 else WHITE]
    panels = {}
    if part == 2:
        panels[0, 0] = WHITE
    robot_runner = run(data[:], iter(inputs))
    x, y = 0, 0

    d = 0
    directions = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0)
    }

    for color in robot_runner:
        panels[x, y] = color
        turn = next(robot_runner)
        if turn == 0:
            d -= 1
        else:
            d += 1
        d %= 4
        x += directions[d][0]
        y += directions[d][1]
        inputs.append(panels.get((x, y), BLACK))
    return panels


print('part 1:', len(solve(1)))

show_dict(solve(2))
