from collections import namedtuple, defaultdict

import math

Ingredient = namedtuple('Ingredient', ['element', 'count'])


def parse_reaction(line):
    before, after = line.split('=>')
    before = [Ingredient(r.strip().split()[1], int(r.strip().split()[0])) for r in before.split(',')]
    after = Ingredient(after.strip().split()[1], int(after.strip().split()[0]))
    return after.element, (before, after.count)


with open('input/day14.txt') as f:
    formulae = dict(parse_reaction(line) for line in f)


def needs(element, factor):
    if element == 'ORE':
        return {'ORE': 0}
    ingredients, count = formulae[element]
    factor = math.ceil(factor / count)
    basic_costs = dict(ingredients)

    return {k: v * factor for k, v in basic_costs.items()}


def count_ore(fuel_count):
    inventory = defaultdict(int, FUEL=fuel_count)
    while True:
        options = [k for k, v in inventory.items() if v > 0 and k != 'ORE']
        if not options:
            break
        # print(f'{len(options)}/{len(inventory)} seen elements complete: {",".join(sorted(options))}')
        element = options[0]
        ingredients, count = formulae[element]
        factor = math.ceil(inventory[element] / count)
        for chemical, chem_count in ingredients:
            inventory[chemical] += chem_count * factor
        inventory[element] -= count * factor
    return inventory['ORE']


print('Part 1:', count_ore(1))

goal = 1_000_000_000_000
min_, max_ = 1, goal
while max_ - min_ > 1:
    check = (min_ + max_) // 2
    ore = count_ore(check)
    if ore < goal:  # Possible, with ore to spare. So we can make more than this
        min_ = check
    else:
        max_ = check
print('Part 2:', min_)
