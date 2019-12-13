from enum import IntEnum

from intcode import run

with open('input/day13.txt') as f:
    program = list(map(int, f.read().split(',')))

runner = run(program[:], [])

board = {}

for x in runner:
    y = next(runner)
    id_ = next(runner)
    board[x, y] = id_

print('Part 1:', list(board.values()).count(2))

board_size = len(board)

TILESET = {
    0: ' ',
    1: '#',
    2: 'X',
    3: '-',
    4: 'o'
}


class TileSet(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __str__(self):
        return TILESET[self.value]


def draw():
    global board
    width = max(k[0] for k in board) + 1
    height = max(k[1] for k in board) + 1

    s = ''
    for row in range(height):
        for col in range(width):
            s += str(board[col, row])
        s += '\n'
    print(s)


def point_joystick():
    global board
    ball = [k for k, v in board.items() if v == 4][0][0]
    paddle = [k for k, v in board.items() if v == 3][0][0]
    if paddle < ball:
        return 1
    elif paddle > ball:
        return -1
    return 0


inputs = []
runner = run([2] + program[1:], inputs)


def init_board():
    global board, score
    for _ in range(board_size + 1):
        x = next(runner)
        y = next(runner)
        value = next(runner)
        if (x, y) == (-1, 0):
            score = value
        else:
            board[x, y] = TileSet(value)


def update():
    global score
    value = None
    # When the game updates, it sets destroyed blocks to empty
    # and updates the ball/paddle position, except on the last
    # frame, when the ball is not made to move. The ball update
    # is the last one on most frames, but is omitted after all
    # blocks have been destroyed, so we have to catch
    # StopIteration and break
    while value != TileSet.BALL.value:
        try:
            x = next(runner)
        except StopIteration:
            break
        y = next(runner)
        value = next(runner)
        if (x, y) == (-1, 0):
            score = value
        else:
            board[x, y] = TileSet(value)


init_board()
while True:
    if list(board.values()).count(2) == 0:
        break
    inputs.append(point_joystick())
    update()

print('Part 2:', score)
