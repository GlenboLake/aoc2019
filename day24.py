from copy import deepcopy

with open('input/day24.txt') as f:
    bugs = [[int(ch == '#') for ch in line] for line in f.read().splitlines()]


def print_grid(grid):
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            print('?' if (i, j) == (2, 2) else '#' if ch else '.', end='')
        print('')


def part1():
    grid = deepcopy(bugs)

    def tick():
        new_grid = [[0 for _ in range(5)] for _ in range(5)]

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

    def biodiversity():
        flat = [val for row in grid for val in row]
        return sum(2 ** i * v for i, v in enumerate(flat))

    seen = []
    while grid not in seen:
        seen.append(grid)
        grid = tick()
    return biodiversity()


sample = [[int(ch == '#') for ch in line] for line in '''....#\n#..#.\n#.?##\n..#..\n#....'''.splitlines()]

EMPTY_GRID = [[0] * 5 for _ in range(5)]


def part2():
    planet = {0: bugs}

    def tick_level(level):
        nonlocal planet
        new_grid = [[0 for _ in range(5)] for _ in range(5)]

        def count_adjacent(x, y):
            total = 0
            here, above, below = [], [], []
            if x == 0:
                if level - 1 in planet:
                    total += planet[level - 1][1][2]
                above.append((1, 2))
            else:
                total += planet[level][x - 1][y]
                here.append((x - 1, y))
            if x == 4:
                if level - 1 in planet:
                    total += planet[level - 1][3][2]
                above.append((3, 2))
            else:
                total += planet[level][x + 1][y]
                here.append((x + 1, y))
            if y == 0:
                if level - 1 in planet:
                    total += planet[level - 1][2][1]
                above.append((2, 1))
            else:
                total += planet[level][x][y - 1]
                here.append((x, y - 1))
            if y == 4:
                if level - 1 in planet:
                    total += planet[level - 1][2][3]
                above.append((2, 3))
            else:
                total += planet[level][x][y + 1]
                here.append((x, y + 1))

            if level + 1 in planet:
                if (x, y) == (1, 2):
                    total += sum(planet[level + 1][0][i] for i in range(5))
                    below.extend([(0, i) for i in range(5)])
                elif (x, y) == (3, 2):
                    total += sum(planet[level + 1][4][i] for i in range(5))
                    below.extend([(4, i) for i in range(5)])
                elif (x, y) == (2, 1):
                    total += sum(planet[level + 1][i][0] for i in range(5))
                    below.extend([(0, i) for i in range(5)])
                elif (x, y) == (2, 3):
                    total += sum(planet[level + 1][i][4] for i in range(5))
                    below.extend([(i, 4) for i in range(5)])

            return total

        for row in range(5):
            for col in range(5):
                if row == col == 2:
                    new_grid[row][col] = 0
                    continue
                adj = count_adjacent(row, col)
                if planet[level][row][col] == 1 and adj != 1:
                    new_grid[row][col] = 0
                elif planet[level][row][col] == 0 and adj in (1, 2):
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = planet[level][row][col]
        return new_grid

    def tick():
        nonlocal planet
        min_level = min(planet) - 1
        max_level = max(planet) + 1
        planet[min_level] = [[0] * 5 for _ in range(5)]
        planet[max_level] = [[0] * 5 for _ in range(5)]
        new_planet = {lev: tick_level(lev) for lev in range(min_level, max_level + 1)}
        return new_planet

    for _ in range(200):
        planet = tick()
    return sum(cell for layer in planet.values() for row in layer for cell in row)


print('Part 1:', part1())
print('Part 2:', part2())
