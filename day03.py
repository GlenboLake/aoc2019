with open('input/day03.txt') as f:
    wire1 = f.readline().split(',')
    wire2 = f.readline().split(',')


def manhattan(point):
    return sum(map(abs, point))


def path(steps):
    x, y = 0, 0
    wire = {}
    i = 0
    for s in steps:
        d = s[0]
        count = int(s[1:])
        for _ in range(count):
            i += 1
            if d == 'R':
                x += 1
            elif d == 'L':
                x -= 1
            elif d == 'D':
                y += 1
            elif d == 'U':
                y -= 1
            wire[x, y] = i
    return wire


wire1_path = path(wire1)
wire2_path = path(wire2)

intersections = set(wire1_path) & set(wire2_path)

distances = {
    manhattan(point): wire1_path[point] + wire2_path[point]
    for point in intersections
}

print(min(distances.keys()))
print(min(distances.values()))
