with open('input/day16.txt') as f:
    digits = list(map(int, f.read().strip()))


def iter_pattern(repeats):
    while True:
        for p in [1, 0, -1, 0]:
            for _ in range(repeats):
                yield p


def iterate(seq):
    new_seq = []
    for i in range(len(seq)):
        pat = iter_pattern(i + 1)
        total = 0
        for digit in seq[i:]:
            v = next(pat)
            total += digit * v
        new_seq.append(abs(total) % 10)
    return new_seq


seq = digits
for _ in range(100):
    seq = iterate(seq)
print('Part 1:', ''.join(map(str, seq[:8])))

# part 2
offset = int(''.join(map(str, digits[:7])))
"""Because the offset is in the second half of the sequence, everything is
just cumulative sums. In the example, the second half of the first phase's output is:
1*0 + 2*0 + 3*0 + 4*0 + 5*1 + 6*1 + 7*1 + 8*1  = 6
1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*1 + 7*1 + 8*1  = 1
1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*0 + 7*1 + 8*1  = 5
1*0 + 2*0 + 3*0 + 4*0 + 5*0 + 6*0 + 7*0 + 8*1  = 8

This can be condensed to
5 + 6 + 7 + 8 = 6
    6 + 7 + 8 = 1
        7 + 8 = 5
            8 = 8

Thus the nth-from-last digit is the sum of the last n digits, mod 10. Because we don't
deal with any of the -1s from the pattern, we can skip abs too.
"""

seq = digits * 10_000
seq = seq[offset:]
for _ in range(100):
    new_seq = []
    cum_sum = 0
    for digit in seq[::-1]:
        cum_sum += digit
        new_seq.append(cum_sum % 10)
    seq = new_seq[::-1]
print('Part 2:', ''.join(map(str, seq[:8])))
