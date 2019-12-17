from intcode import load, run

program = load(17)

runner = run(program[:], [])

overview = ''.join(chr(x) for x in runner).strip().splitlines()
print('\n'.join(overview))

# View the map
width = len(overview[0])
height = len(overview)

intersections = set()
for y in range(1, height - 1):
    for x in range(1, width - 1):
        try:
            if (overview[y][x] == '#' and
                    overview[y][x - 1] == '#' and
                    overview[y][x + 1] == '#' and
                    overview[y - 1][x] == '#' and
                    overview[y + 1][x] == '#'):
                intersections.add((x, y))
        except IndexError:
            print(x, y)
            raise
print('Part 1:', sum(x * y for x, y in intersections))

# Mapped these out manually just by looking for patterns
main = [ord(ch) for ch in 'B,C,B,A,C,A,B,C,B,A\n']
A = [ord(ch) for ch in 'L,6,R,12,R,12,R,10\n']
B = [ord(ch) for ch in 'R,10,L,8,R,10,R,4\n']
C = [ord(ch) for ch in 'L,6,L,6,R,10\n']
inputs = main + A + B + C + [ord('n'), ord('\n')]
runner2 = run([2] + program[1:], inputs)

ch = None
for ch in runner2:
    pass
print('Part 2:', ch)
