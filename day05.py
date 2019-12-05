with open('input/day05.txt') as f:
    ints = list(map(int, f.read().split(',')))


def run_prog(input):
    nums = ints.copy()
    pos = 0
    while True:
        op = nums[pos]
        opcode = op % 100
        param_1 = op // 100 % 10
        param_2 = op // 1000 % 10
        param_3 = op // 10000
        if opcode == 99:
            break
        a, b, res = nums[pos + 1:pos + 4]
        if opcode == 1:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            nums[res] = a + b
            pos += 4
        elif opcode == 2:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            nums[res] = a * b
            pos += 4
        elif opcode == 3:
            nums[a] = input
            pos += 2
        elif opcode == 4:
            print(nums[a])
            pos += 2
        elif opcode == 5:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            if a:
                pos = b
            else:
                pos += 3
        elif opcode == 6:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            if not a:
                pos = b
            else:
                pos += 3
        elif opcode == 7:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            nums[res] = 1 if a < b else 0
            pos += 4
        elif opcode == 8:
            if not param_1:
                a = nums[a]
            if not param_2:
                b = nums[b]
            nums[res] = 1 if a == b else 0
            pos += 4
        else:
            break
    return nums[0]


print('part 1: ', end='')
run_prog(1)
print('part 2: ', end='')
run_prog(5)

ints = list(map(int, '3,9,8,9,10,9,4,9,99,-1,8'.split(',')))
for i in range(7, 10):
    print(i)
    run_prog(5)
