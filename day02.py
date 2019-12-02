with open('input/day02.txt') as f:
    ints = list(map(int, f.read().split(',')))


def run_prog(noun, verb):
    nums = ints.copy()
    nums[1] = noun
    nums[2] = verb
    pos = 0
    while True:
        op = nums[pos]
        if op == 99:
            break
        a, b, res = nums[pos + 1:pos + 4]
        if op == 1:
            result = nums[a] + nums[b]
        elif op == 2:
            result = nums[a] * nums[b]
        else:
            break
        nums[res] = result
        pos += 4
    return nums[0]


# part 1
print(run_prog(12, 2))

# part 2
for noun in range(100):
    for verb in range(100):
        if run_prog(noun, verb) == 19690720:
            print(100 * noun + verb)
