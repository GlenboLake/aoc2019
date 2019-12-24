from functools import partial

with open('input/day22.txt') as f:
    shuffles = f.read().splitlines()


def part1():
    deck_size = 10007
    pos = 2019
    for shuffle in shuffles:
        if shuffle.startswith('cut'):
            pos -= int(shuffle.split()[-1])
            pos = pos % deck_size
        elif shuffle == 'deal into new stack':
            pos = deck_size - pos - 1
        else:
            inc = int(shuffle.split()[-1])
            pos = (inc * pos) % deck_size
    return pos


def part2():
    """Had to take this from /u/etotheipi1

    https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnifwk/
    """
    deck_size = 119315717514047

    def reverse_deal(i):
        return deck_size - 1 - i

    def reverse_cut(i, n):
        return (i + n + deck_size) % deck_size

    def modinv(a, m):
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, y, x = egcd(b % a, a)
                return g, x - (b // a) * y, y

        g, x, y = egcd(a, m)
        if g != 1:
            raise RuntimeError('No modular inverse')
        return x % m

    def reverse_inc(i, n):
        return modinv(n, deck_size) * i % deck_size

    commands = []
    for shuffle in shuffles:
        if shuffle.startswith('cut'):
            amount = int(shuffle.split()[-1])
            commands.insert(0, partial(reverse_cut, n=amount))
        elif shuffle == 'deal into new stack':
            commands.insert(0, reverse_deal)
        else:
            inc = int(shuffle.split()[-1])
            commands.insert(0, partial(reverse_inc, n=inc))

    def f(i):
        for func in commands:
            i = func(i)
        return i

    X = 2020
    Y = f(X)
    Z = f(Y)

    A = (Y - Z) * modinv(X - Y + deck_size, deck_size) % deck_size
    B = (Y - A * X) % deck_size
    n = 101741582076661
    return (pow(A, n, deck_size) * X + (pow(A, n, deck_size) - 1) * modinv(A - 1, deck_size) * B) % deck_size


if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())
