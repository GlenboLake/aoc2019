from copy import deepcopy
from pprint import pprint

with open('input/day24.txt') as f:
    bugs = [[int(ch == '#') for ch in line] for line in f.read().splitlines()]

pprint(bugs)


def tick(grid):
    new_grid = [[None for _ in range(5)] for _ in range(5)]

    def count_adjacent(x, y):
        total = 0
        if x > 0:
            total += grid[x - 1][y]
        if x < 4:
            total += grid[x + 1][y]
        if y > 0:
            total += grid[x][y - 1]
        if y < 4:
            total += grid[x][y + 1]
        return total

    for i in range(5):
        for j in range(5):
            adj = count_adjacent(i, j)
            if grid[i][j] == 1 and adj != 1:
                new_grid[i][j] = 0
            elif grid[i][j] == 0 and adj in (1, 2):
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = grid[i][j]
    return new_grid


def biodiversity(grid):
    flat = [val for row in grid for val in row]
    return sum(2 ** i * v for i, v in enumerate(flat))


def print_grid(grid):
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            print('?' if (i, j) == (2, 2) else '#' if ch else '.', end='')
        print('')


def part1():
    grid = deepcopy(bugs)
    seen = []
    while grid not in seen:
        seen.append(grid)
        grid = tick(grid)
    return biodiversity(grid)


sample = [[int(ch == '#') for ch in line] for line in '''....#\n#..#.\n#.?##\n..#..\n#....'''.splitlines()]

EMPTY_GRID = [[0] * 5 for _ in range(5)]


def part2():
    planet = {0: sample}

    def tick_level(level):
        nonlocal planet
        new_grid = [[None for _ in range(5)] for _ in range(5)]

        def count_adjacent(x, y):
            total = 0
            if x in (0, 4) or y in (0, 4):
                # Adjacent to next level up
                if x == 0:
                    if level - 1 in planet:
                        total += planet[level - 1][1][2]
                    total += planet[level][x + 1][y]
                elif x == 4:
                    if level - 1 in planet:
                        total += planet[level - 1][3][2]
                    total += planet[level][x - 1][y]
                if y == 0:
                    if level - 1 in planet:
                        total += planet[level - 1][2][1]
                    total += planet[level][x][y + 1]
                if y == 4:
                    if level - 1 in planet:
                        total += planet[level - 1][2][3]
                    total += planet[level][x][y - 1]
            elif x in (1, 3) and y in (1, 3):
                # Normal, not adjacent to any other levels
                return (planet[level][x - 1][y] + planet[level][x + 1][y] +
                        planet[level][x][y - 1] + planet[level][x][y + 1])
            else:
                # Adjacent to next level down
                total = (planet[level][x - 1][y] + planet[level][x + 1][y] +
                         planet[level][x][y - 1] + planet[level][x][y + 1] -
                         planet[level][2][2])
                if level + 1 in planet:
                    if x == 1:
                        total += sum(planet[level + 1][0][i] for i in range(5))
                    elif x == 3:
                        total += sum(planet[level + 1][4][i] for i in range(5))
                    elif y == 1:
                        total += sum(planet[level + 1][i][0] for i in range(5))
                    else:
                        total += sum(planet[level + 1][i][4] for i in range(5))
            return total

        for i in range(5):
            for j in range(5):
                if i == j == 2:
                    continue
                adj = count_adjacent(i, j)
                if planet[level][i][j] == 1 and adj != 1:
                    new_grid[i][j] = 0
                elif planet[level][i][j] == 0 and adj in (1, 2):
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = planet[level][i][j]
        return new_grid

    def tick():
        nonlocal planet
        min_level = min(planet) - 1
        max_level = max(planet) + 1
        planet[min_level] = [[0] * 5 for _ in range(5)]
        planet[max_level] = [[0] * 5 for _ in range(5)]
        new_planet = {lev: tick_level(lev) for lev in range(min_level, max_level + 1)}
        return {k: v for k, v in new_planet.items() if v != EMPTY_GRID}

    def print_planet():
        nonlocal planet
        min_level = min(planet)
        max_level = max(planet)
        for level in range(min_level, max_level + 1):
            print(f'Depth {level}')
            print_grid(planet[level])

    # for _ in range(10):
    planet = tick()
    print_planet()


print(part1())
print(part2())
