from itertools import combinations
from pprint import pformat

from intcode import load, run

program = load(25)

inputs = []
runner = run(program[:], inputs)

collection = '''south
take fuel cell
south
take manifold
north
north
west
take mutex
south
south
take coin
west
take dehydrated water
south
take prime number
north
east
north
east
take cake
north
west
south
drop cake
drop coin
drop dehydrated water
drop fuel cell
drop manifold
drop mutex
drop prime number
nonsense
'''

items = [
    'cake',
    'coin',
    'dehydrated water',
    'fuel cell',
    'manifold',
    'mutex',
    'prime number'
]


def get_text():
    text = ''
    while not text.endswith('Command?\n'):
        try:
            text += chr(next(runner))
        except StopIteration:
            break
    return text


def command():
    global runner
    cmd = input()
    if cmd == 'restart':
        inputs.clear()
        runner = run(program[:], inputs)
        return
    inputs.extend([ord(ch) for ch in cmd])
    inputs.append(10)


text = ''
inputs.extend([ord(ch) for ch in collection])
while 'Unrecognized' not in text:
    text = get_text()
inputs.extend([ord(ch) for ch in 'west\n'])
print(get_text(), end='')

lighter = []
heavier = []
for triplet in combinations(items, 4):
    print('...trying', triplet)
    for thing in triplet:
        inputs.extend([ord(ch) for ch in f'take {thing}\n'])
        get_text()
    inputs.extend([ord(ch) for ch in 'west\n'])
    response = get_text()
    if 'lighter' in response:
        lighter.append(triplet)
    elif 'heavier' in response:
        heavier.append(triplet)
    else:
        print(response)
        break
    for thing in triplet:
        inputs.extend([ord(ch) for ch in f'drop {thing}\n'])
        get_text()
else:
    print('Too light:', len(heavier), heavier)
    print('Too heavy:', len(lighter), pformat(lighter))

inputs.extend([ord(ch) for ch in 'inv\n'])
print(get_text())