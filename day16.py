with open('input/day16.txt') as f:
    digits = list(map(int, f.read().strip()))


def iter_pattern(pattern, repeats):
    while True:
        for p in pattern:
            for _ in range(repeats):
                yield p


def iterate(seq, pattern):
    new_seq = []
    for i in range(len(seq)):
        pat = iter_pattern(pattern, i + 1)
        next(pat)
        total = 0
        for digit in seq:
            v = next(pat)
            # print(f'{digit}*{v} ', end='')
            total += digit * v
        # print(f'= {total} -> {abs(total) % 10}')
        new_seq.append(abs(total) % 10)
    return new_seq


seq = digits
for _ in range(100):
    seq = iterate(seq, [0, 1, 0, -1])
print('Part 1:', ''.join(map(str, seq[:8])))
