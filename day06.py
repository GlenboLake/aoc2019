from collections import defaultdict, deque

orbits = defaultdict(list)
links = defaultdict(list)

with open('input/day06.txt') as f:
    for row in f:
        a, b = row.strip().split(')')
        orbits[a].append(b)
        links[a].append(b)
        links[b].append(a)


def count_children(obj):
    if obj not in orbits:
        return 0
    children = orbits[obj]
    return len(children) + sum([count_children(ch) for ch in children])


print('Part 1:', sum([count_children(o) for o in orbits.keys()]))


def path(start, end):
    dists = {start: 0}
    objects = deque([start])
    seen = {start}
    while end not in dists:
        thing = objects.pop()
        dist = dists[thing]
        for neighbor in links[thing]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            objects.appendleft(neighbor)
            dists[neighbor] = dist + 1
    return dists[end]


you_parent = [k for k, v in orbits.items() if 'YOU' in v].pop()
san_parent = [k for k, v in orbits.items() if 'SAN' in v].pop()
print('Part 2:', path(you_parent, san_parent))
