import sys
from collections import deque
from typing import Tuple

with open('input/day20.txt') as f:
    data = f.read()


def parse_maze(maze_data) -> Tuple[Tuple[int, int], Tuple[int, int], dict]:
    ir = 0  # Inner Radius
    for ir in range(2, len(maze_data[0])):
        if maze_data[ir][ir] not in '.#':
            break

    labels = {}
    # Outer labels
    top_labels = [a + b for a, b in zip(*maze_data[:2])]
    labels.update({(i, 2): label for i, label in enumerate(top_labels) if label.strip()})
    bottom_labels = [a + b for a, b in zip(*maze_data[-2:])]
    labels.update({(i, len(maze_data) - 3): label for i, label in enumerate(bottom_labels) if label.strip()})
    left_labels = [line[:2] for line in maze_data]
    labels.update({(2, i): label for i, label in enumerate(left_labels) if label.strip()})
    right_labels = [line[-2:] for line in maze_data]
    labels.update({(len(maze_data[0]) - 3, i): label for i, label in enumerate(right_labels) if label.strip()})

    # Inner labels
    top_labels = [a + b for a, b in zip(maze_data[ir][ir:-ir], maze_data[ir + 1][ir:-ir])]
    labels.update({(i, ir - 1): label for i, label in enumerate(top_labels, start=ir) if len(label.strip()) == 2})
    bottom_labels = [a + b for a, b in zip(maze_data[-ir - 2][ir:-ir], maze_data[-ir - 1][ir:-ir])]
    labels.update(
        {(i, len(maze_data) - ir): label for i, label in enumerate(bottom_labels, start=ir) if len(label.strip()) == 2})
    left_labels = [line[ir:ir + 2] for line in maze_data[ir:-ir]]
    labels.update({(ir - 1, i): label for i, label in enumerate(left_labels, start=ir) if len(label.strip()) == 2})
    right_labels = [line[-ir - 2:-ir] for line in maze_data[ir:-ir]]
    labels.update({(len(maze_data[0]) - ir, i): label for i, label in enumerate(right_labels, start=ir) if
                   len(label.strip()) == 2})

    start = [k for k, v in labels.items() if v == 'AA'][0]
    goal = [k for k, v in labels.items() if v == 'ZZ'][0]
    portals = {}
    for label in set(labels.values()) - {'AA', 'ZZ'}:
        a, b = [k for k, v in labels.items() if v == label]
        portals[a] = b
        portals[b] = a

    return start, goal, portals


def part1(maze_data):
    maze_data = maze_data.splitlines()
    start, goal, portals = parse_maze(maze_data)
    distances = {start: 0}
    to_visit = deque([start])
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while to_visit:
        x, y = to_visit.popleft()
        dist = distances[x, y]
        for dx, dy in diffs:
            x2 = x + dx
            y2 = y + dy
            if maze_data[y2][x2] != '.':
                continue
            elif distances.get((x2, y2), sys.maxsize) > dist + 1:
                to_visit.append((x2, y2))
                distances[x2, y2] = dist + 1
        if (x, y) in portals:
            dest = portals[x, y]
            if distances.get(dest, sys.maxsize) > dist + 1:
                to_visit.append(dest)
                distances[dest] = dist + 1
    return distances[goal]


def part2(maze_data):
    maze_data = maze_data.splitlines()
    start, goal, portals = parse_maze(maze_data)
    portal_x_range = min(p[0] for p in portals), max(p[0] for p in portals)
    portal_y_range = min(p[1] for p in portals), max(p[1] for p in portals)

    def is_outer(portal):
        x, y = portal
        return x in portal_x_range or y in portal_y_range

    start = (start[0], start[1], 0)
    goal = (goal[0], goal[1], 0)
    states = {start: 0}
    to_visit = deque([start])
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while to_visit:
        x, y, depth = state = to_visit.popleft()
        if state == goal:
            break
        dist = states[x, y, depth]
        for dx, dy in diffs:
            x2 = x + dx
            y2 = y + dy
            if maze_data[y2][x2] != '.':
                continue
            elif states.get((x2, y2, depth), sys.maxsize) > dist + 1:
                to_visit.append((x2, y2, depth))
                states[x2, y2, depth] = dist + 1
        if (x, y) in portals:
            new_depth = depth - 1 if is_outer((x, y)) else depth + 1
            if new_depth >= 0:
                dest = portals[x, y] + (new_depth,)
                if states.get(dest, sys.maxsize) > dist + 1:
                    to_visit.append(dest)
                    states[dest] = dist + 1
    return states[goal]


print('Part 1:', part1(data))
print('Part 2:', part2(data))
