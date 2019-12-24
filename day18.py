from collections import defaultdict, deque
from string import ascii_lowercase as key_chars, ascii_uppercase as door_chars
from time import time
from typing import Dict

WALL = '#'

with open('input/day18.txt') as f:
    caves = f.read().splitlines()


def method2(cave_map):
    key_count = len(set(''.join(cave_map)) & set(key_chars))
    x, y = [(row, col) for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch == '@'][0]
    initial_state = x, y, frozenset()
    states = {
        initial_state: 0
    }
    paths = deque()
    paths.append(initial_state)
    while paths:
        x, y, keys_collected = state = paths.popleft()
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


def method3(cave_map):
    keys = {(row, col): ch for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch in key_chars}
    start = [(row, col) for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch == '@'][0]

    # Find requirements
    requirements = {}
    states = {start: (0, frozenset())}
    diffs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    to_check = deque([start])
    while to_check:
        x, y = state = to_check.popleft()
        dist, needed_keys = states[state]
        for dx, dy in diffs:
            x2, y2 = x + dx, y + dy
            if (x2, y2) in states:
                continue
            value = cave_map[x2][y2]
            if value == WALL:
                continue
            elif value in door_chars:
                needed_keys |= {value.lower()}
            elif value in key_chars:
                requirements[x2, y2] = needed_keys
                needed_keys |= {value}
            new_state = dist + 1, needed_keys
            states[x2, y2] = new_state
            to_check.append((x2, y2))

    distances = {'@': {keys[k]: states[k][0] for k in requirements}}
    requirements = {keys[k]: v for k, v in requirements.items()}

    to_visit = deque()
    for pos, key in keys.items():
        distances[key] = {}
        states = {pos: 0}
        to_visit.append(pos)
        while to_visit:
            x, y = state = to_visit.popleft()
            dist = states[state]
            for dx, dy in diffs:
                x2, y2 = x + dx, y + dy
                if (x2, y2) in states:
                    continue
                value = cave_map[x2][y2]
                if value == WALL:
                    continue
                states[x2, y2] = dist + 1
                to_visit.append((x2, y2))
                if value in key_chars:
                    distances[key][value] = dist + 1

    # Now basic pathfinding between nodes
    init_state = '@', frozenset()
    states = {init_state: 0}
    to_visit.append(init_state)
    while to_visit:
        node, keys_collected = state = to_visit.popleft()
        dist = states[state]
        options = [n for n in distances[node] if requirements[n] <= keys_collected]
        for option in options:
            new_state = option, keys_collected | {option}
            new_dist = dist + distances[node][option]
            if new_state not in states or states[new_state] > new_dist:
                states[new_state] = new_dist
                to_visit.append(new_state)
    return min([v for k, v in states.items() if len(k[1]) == len(keys)])


def part2(cave_map):
    key_names = {(row, col): ch for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch in key_chars}
    x, y = [(row, col) for row, line in enumerate(cave_map) for col, ch in enumerate(line) if ch == '@'][0]
    cave_map[x - 1] = cave_map[x - 1][:y - 1] + '@#@' + cave_map[x - 1][y + 2:]
    cave_map[x] = cave_map[x][:y - 1] + '###' + cave_map[x][y + 2:]
    cave_map[x + 1] = cave_map[x + 1][:y - 1] + '@#@' + cave_map[x + 1][y + 2:]
    bots = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
    bots = {f'bot{i}': xy for i, xy in enumerate(bots)}

    requirements = {}

    # Get distances to each key for each bot
    def scan(bot):
        nonlocal key_names, requirements
        start = bot, frozenset({})
        states = {start: 0}
        to_visit = deque([start])
        result = {}
        while to_visit:
            bot, keys_needed = state = to_visit.popleft()
            botx, boty = bot
            for xa, ya in [(botx, boty + 1), (botx, boty - 1), (botx + 1, boty), (botx - 1, boty)]:
                value = cave_map[xa][ya]
                if value == WALL:
                    continue
                if value in door_chars + key_chars:
                    new_keys_needed = keys_needed | {value.lower()}
                else:
                    new_keys_needed = keys_needed
                new_state = (xa, ya), new_keys_needed
                if new_state not in states:
                    states[new_state] = states[state] + 1
                    if (xa, ya) in key_names:
                        key_name = key_names[xa, ya]
                        if key_name not in result:
                            requirements[key_name] = new_keys_needed - {key_name}
                            result[key_name] = states[new_state]
                    to_visit.append(new_state)
        return result

    distances: Dict[str, Dict[int]] = defaultdict(dict, {name: scan(pos) for name, pos in bots.items()})

    # Get key-to-key distances
    diffs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for key_pos, key_name in key_names.items():
        states = {key_pos: 0}
        to_visit = deque([key_pos])
        while to_visit:
            x, y = state = to_visit.popleft()
            dist = states[state]
            for dx, dy in diffs:
                x2, y2 = x + dx, y + dy
                if (x2, y2) in states:
                    continue
                value = cave_map[x2][y2]
                if value == WALL:
                    continue
                states[x2, y2] = dist + 1
                to_visit.append((x2, y2))
                if value in key_chars:
                    distances[key_name][value] = dist + 1

    initial_state = frozenset(bots.keys()), frozenset()
    states = {initial_state: 0}
    to_visit = deque([initial_state])
    while to_visit:
        bot_locs, keys_collected = state = to_visit.popleft()
        distance_so_far = states[state]
        options = [loc for loc, prereq in requirements.items() if keys_collected >= prereq and loc not in bot_locs]
        for opt in options:
            bot = [b for b in bot_locs if opt in distances[b]][0]
            new_bot_locs = bot_locs - {bot} | {opt}
            new_keys = keys_collected | {opt}
            new_state = new_bot_locs, new_keys
            new_dist = distance_so_far + distances[bot][opt]
            if new_state not in states or states[new_state] > new_dist:
                states[new_state] = new_dist
                to_visit.append(new_state)
    return min(v for k, v in states.items() if len(k[1]) == len(key_names))


start_time = time()
print('Part 1:', method2(caves), end=', ')
print(time() - start_time)
start_time = time()
print('Part 1:', method3(caves), end=', ')
print(time() - start_time)
start_time = time()
print('Part 2:', part2(caves), end=', ')
print(time() - start_time)
