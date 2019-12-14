from itertools import permutations

from intcode import load, run

prog = load(7)


def part1(phases):
    value = 0
    for phase in phases:
        value = next(run(prog[:], (phase, value)))
    return value


print('Part 1:', max(part1(seq) for seq in permutations(range(5), 5)))


# Based heavily on the submission by dries007
# https://www.reddit.com/r/adventofcode/comments/e7a4nj/2019_day_7_solutions/f9y0yw6/
def part2(phases):
    feedback = None

    def amp_input(amp):
        yield phases[amp]

        if amp == 0:
            yield 0
            while True:
                yield feedback

        yield from run(prog[:], amp_input(amp - 1))

    amps = run(prog[:], amp_input(len(phases) - 1))
    for feedback in amps:
        pass
    return feedback


print('Part 2:', max(part2(seq) for seq in permutations(range(5, 10), 5)))
