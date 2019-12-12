import re
from itertools import combinations

from util import lcm

with open('input/day12.txt') as f:
    data = f.read().splitlines()


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = self.dy = self.dz = 0

    @classmethod
    def from_str(cls, s):
        result = re.fullmatch(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', s)
        return cls(*map(int, result.groups()))

    def pull(self, other):
        if self.x < other.x:
            self.dx += 1
        elif self.x > other.x:
            self.dx -= 1
        if self.y < other.y:
            self.dy += 1
        elif self.y > other.y:
            self.dy -= 1
        if self.z < other.z:
            self.dz += 1
        elif self.z > other.z:
            self.dz -= 1

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    @property
    def energy(self):
        potential = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic = abs(self.dx) + abs(self.dy) + abs(self.dz)
        return potential * kinetic


moons = [Moon.from_str(line) for line in data]
periods = [None, None, None]


def move_moons():
    for a, b in combinations(moons, 2):
        a.pull(b)
        b.pull(a)
    for m in moons:
        m.move()


def axis_state(axis):
    axis = 'xyz'[axis]
    positions = [getattr(m, axis) for m in moons]
    velocities = [getattr(m, 'd' + axis) for m in moons]
    return tuple([*positions, *velocities])


initial_states = [axis_state(0), axis_state(1), axis_state(2)]
it = 0
while not all(periods):
    move_moons()
    it += 1
    if it == 1000:
        print('Part 1:', sum(m.energy for m in moons))
    for ax in range(3):
        if periods[ax] is not None:
            continue
        if axis_state(ax) == initial_states[ax]:
            periods[ax] = it

print('Part 2:', lcm(*periods))
