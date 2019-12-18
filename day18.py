from collections import defaultdict
from itertools import combinations
from queue import Queue
from string import ascii_lowercase as key_chars, ascii_uppercase as door_chars
from typing import List, Tuple

WALL = '#'

with open('input/day18.txt') as f:
    caves = f.read().splitlines()

keys = {}
doors = {}
me = None
for i, line in enumerate(caves):
    for j, ch in enumerate(line):
        if ch in key_chars:
            keys[ch] = i, j
        if ch in door_chars:
            doors[ch.lower()] = i, j
        if ch == '@':
            me = i, j


def measure(start, end):
    distances = {start: 0}
    blocking_doors = defaultdict(set)
    q = Queue()
    q.put(start)
    while end not in distances:
        x, y = q.get()
        doors_on_path = blocking_doors[x, y]
        adjacent: List[Tuple[int, int]] = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        adjacent = [point for point in adjacent if caves[x][y] != WALL and point not in distances]
        for xa, ya in adjacent:
            distances[xa, ya] = distances[x, y] + 1
            blocking_doors[xa, ya].update(doors_on_path)
            here = caves[xa][ya]
            if here in door_chars + key_chars and (xa, ya) != end:
                blocking_doors[xa, ya].add(caves[xa][ya].lower())
            q.put((xa, ya))
    return distances[end], blocking_doors[end]


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


def valid_next(order):
    return [k for k in keys if not (key_blocks[k] - set(order)) and k not in order]


starts = valid_next([])
order_distances = {tuple(k): v for k, v in distances['@'].items() if k in starts}


def condense(mapping):
    unique_keys = {(frozenset(key[:-1]), key[-1]) for key in mapping}
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
print('Part 1:', min(v for k, v in order_distances.items() if len(k) == len(keys)))
