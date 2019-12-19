import time
from collections import defaultdict, deque
from itertools import combinations
from string import ascii_lowercase as key_chars, ascii_uppercase as door_chars
from typing import List, Tuple

WALL = '#'

with open('input/day18.txt') as f:
    caves = f.read().splitlines()


def method1(cave_map):
    keys = {}
    doors = {}
    me = None
    for i, line in enumerate(cave_map):
        for j, ch in enumerate(line):
            if ch in key_chars:
                keys[ch] = i, j
            if ch in door_chars:
                doors[ch.lower()] = i, j
            if ch == '@':
                me = i, j

    def measure(start, end):
        dists = {start: 0}
        blocking_doors = defaultdict(set)
        q = deque()
        q.append(start)
        while end not in dists:
            x, y = q.popleft()
            doors_on_path = blocking_doors[x, y]
            adjacent: List[Tuple[int, int]] = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
            adjacent = [point for point in adjacent if cave_map[x][y] != WALL and point not in dists]
            for xa, ya in adjacent:
                dists[xa, ya] = dists[x, y] + 1
                blocking_doors[xa, ya].update(doors_on_path)
                here = cave_map[xa][ya]
                if here in door_chars + key_chars and (xa, ya) != end:
                    blocking_doors[xa, ya].add(cave_map[xa][ya].lower())
                q.append((xa, ya))
        return dists[end], blocking_doors[end]

    distances = defaultdict(dict)
    key_blocks = defaultdict(set)
    for k1, k2 in combinations(keys, 2):
        distance, _ = measure(keys[k1], keys[k2])
        distances[k1][k2] = distances[k2][k1] = distance

    for key, loc in keys.items():
        distance, block = measure(me, loc)
        distances['@'][key] = distance
        if block:
            key_blocks[key].update(block)

    def valid_next(seq):
        return [k for k in keys if not (key_blocks[k] - set(seq)) and k not in seq]

    starts = valid_next([])
    order_distances = {tuple(k): v for k, v in distances['@'].items() if k in starts}

    def condense(mapping):
        unique_keys = {(frozenset(k[:-1]), k[-1]) for k in mapping}
        condensed = {}
        for prefix, final in unique_keys:
            subdict = {k: v for k, v in mapping.items() if set(k[:-1]) == prefix and k[-1] == final}
            best_seq = min(subdict, key=lambda k: subdict[k])
            condensed[best_seq] = subdict[best_seq]
        return condensed

    for i in range(1, len(keys)):
        order_distances = condense(order_distances)
        new_order_distances = {}
        for order, distance in order_distances.items():
            for n in valid_next(order):
                new_order_distances[order + (n,)] = distance + distances[order[-1]][n]
        order_distances = new_order_distances
    return min(v for k, v in order_distances.items() if len(k) == len(keys))


start = time.time()
print('Part 1:', method1(caves))
print(time.time() - start)


def method2(cave_map):
    key_count = len(set(''.join(cave_map)) & set(key_chars))
    x, y = [(row, col) for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch == '@'][0]
    initial_state = x, y, frozenset()
    states = {
        initial_state: 0
    }
    paths = deque()
    paths.append(initial_state)
    path_lengths = []
    while paths:
        x, y, keys_collected = state = paths.popleft()
        path_lengths.append(states[state])
        for xa, ya in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
            value = cave_map[xa][ya]
            if value == WALL or value in door_chars and value.lower() not in keys_collected:
                continue
            if value in key_chars:
                new_keys_collected = keys_collected | {value}
                if len(new_keys_collected) == key_count:
                    return states[state] + 1
            else:
                new_keys_collected = keys_collected
            new_state = (xa, ya, new_keys_collected)
            if new_state not in states:
                states[new_state] = states[state] + 1
                paths.append(new_state)
    return min([v for k, v in states.items() if len(k[-1]) == key_count])


sample1 = '''#########
#b.A.@.a#
#########'''.splitlines()
sample2 = '''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''.splitlines()
sample3 = '''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''.splitlines()

start = time.time()
print('Part 1:', method2(caves))
print(time.time() - start)
