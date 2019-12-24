import sys
from collections import deque
from typing import Tuple

with open('input/day20.txt') as f:
    data = f.read()

sample = '''\
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''


def parse_maze(maze_data):
    maze_data = maze_data.splitlines()
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
    labels.update({(len(maze_data) - 3, i): label for i, label in enumerate(right_labels) if label.strip()})

    # Inner labels
    top_labels = [a + b for a, b in zip(maze_data[ir][ir:-ir], maze_data[ir + 1][ir:-ir])]
    labels.update({(i, ir - 1): label for i, label in enumerate(top_labels, start=ir) if len(label.strip()) == 2})
    bottom_labels = [a + b for a, b in zip(maze_data[-ir - 2][ir:-ir], maze_data[-ir - 1][ir:-ir])]
    labels.update(
        {(i, len(maze_data) - ir): label for i, label in enumerate(bottom_labels, start=ir) if len(label.strip()) == 2})
    left_labels = [line[ir:ir + 2] for line in maze_data[ir:-ir]]
    labels.update({(ir - 1, i): label for i, label in enumerate(left_labels, start=ir) if len(label.strip()) == 2})
    right_labels = [line[-ir - 2:-ir] for line in maze_data[ir:-ir]]
    labels.update({(len(maze_data) - ir + 2, i): label for i, label in enumerate(right_labels, start=ir) if
                   len(label.strip()) == 2})

    start = [k for k, v in labels.items() if v == 'AA'][0]
    goal = [k for k, v in labels.items() if v == 'ZZ'][0]
    # print(start)
    # print(goal)
    portals = {}
    for label in set(labels.values()) - {'AA', 'ZZ'}:
        # print(label)
        a, b = [k for k, v in labels.items() if v == label]
        portals[a] = b
        portals[b] = a
    # print(labels)
    # print(portals)

    distances = {start: 0}
    to_visit = deque([start])
    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while to_visit:
        x, y = to_visit.popleft()
        dist = distances[x, y]
        # print(f'Traveling from {x},{y} ({dist})')
        for dx, dy in diffs:
            x2 = x + dx
            y2 = y + dy
            if maze_data[y2][x2] != '.':
                continue
            elif distances.get((x2, y2), sys.maxsize) > dist + 1:
                # print(f'({x},{y}) -> ({x2},{y2}) = {dist + 1}')
                to_visit.append((x2, y2))
                distances[x2, y2] = dist + 1
        if (x,y) in portals:
            # print(f'Following portal {labels[x,y]} to {portals[x,y]}')
            dest = portals[x, y]
            if distances.get(dest, sys.maxsize) > dist + 1:
                to_visit.append(dest)
                distances[dest] = dist + 1
    return distances[goal]


# print(parse_maze(sample))
print(parse_maze(data))
