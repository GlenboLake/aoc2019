from queue import Queue

from intcode import load, run

program = load(15)
inputs = []

runner = run(program[:], inputs)

# Directions to move
NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

# Possible return values
WALL = 0
MOVED = 1
DONE = 2


def dirname(d):
    """For putting directions into print statements"""
    return {
        1: 'north',
        2: 'south',
        3: 'west',
        4: 'east',
    }[d]


right = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH
}
left = {v: k for k, v in right.items()}


class Point(tuple):
    def __new__(cls, x, y):
        return super().__new__(Point, [x, y])

    def __add__(self, other):
        return Point(self[0] + other[0], self[1] + other[1])


changes = {
    NORTH: Point(0, 1),
    SOUTH: Point(0, -1),
    WEST: Point(-1, 0),
    EAST: Point(1, 0)
}


def print_map():
    """Just a little debugging function"""
    xmin = min([x for x, y in ship_map])
    xmax = max([x for x, y in ship_map])
    ymin = min([y for x, y in ship_map])
    ymax = max([y for x, y in ship_map])

    for y in range(ymax, ymin - 1, -1):
        for x in range(xmin, xmax + 1):
            if (x, y) == droid:
                print('D', end='')
            elif (x, y) not in ship_map:
                print(' ', end='')
            elif ship_map[x, y] == WALL:
                print('#', end='')
            elif ship_map[x, y] == MOVED:
                print('.', end='')
            elif ship_map[x, y] == DONE:
                print('O', end='')
        print()


d = NORTH
droid = Point(0, 0)
ship_map = {droid: MOVED}
value = None
travel_distance = {(0, 0): 0}


def move():
    global droid, d, value
    # Try moving to the right first to make sure we're following the wall
    moving = right[d]
    inputs.append(moving)
    value = next(runner)

    if value == WALL:
        # Wall to the right, mark it as such and continue moving in the same direction
        ship_map[droid + changes[moving]] = WALL
    else:
        # The wall ended; mark that the droid traveled that way and set
        # it as the droid's new travel direction
        if droid + changes[moving] not in travel_distance:
            travel_distance[droid + changes[moving]] = travel_distance[droid] + 1
        droid += changes[moving]
        ship_map[droid] = value
        d = moving
        return

    # If there's still a wall to the right, continue forward
    inputs.append(d)
    value = next(runner)

    if value == WALL:
        # This means there's a wall both to the right and in front of us, so turn left.
        # If we reach a dead end, we'll end up at this point twice in a row
        ship_map[droid + changes[d]] = WALL
        d = left[d]
    else:
        if droid + changes[d] not in travel_distance:
            travel_distance[droid + changes[d]] = travel_distance[droid] + 1
        droid += changes[d]
        ship_map[droid] = value


while value != DONE:
    move()

print('Part 1:', travel_distance[droid])

oxygen_system = droid

# Continue mapping all the way back to the origin
while droid != (0, 0):
    move()

o2_time = {oxygen_system: 0}
fill = Queue()
fill.put(oxygen_system)

while fill.qsize():
    point = fill.get()
    adjacent = list(filter(lambda p: p not in o2_time and ship_map[p] != WALL,
                           {point + diff for diff in changes.values()}))
    for p in adjacent:
        o2_time[p] = o2_time[point] + 1
        fill.put(p)
print('Part 2:', max(o2_time.values()))
