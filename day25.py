import re

from intcode import load, run

program = load(25)

inputs = []
runner = run(program[:], inputs)


def enter_command(cmd):
    global runner, inputs
    ascii_command = [ord(ch) for ch in cmd]
    inputs.extend(ascii_command)
    if not cmd.endswith('\n'):
        inputs.append(ord('\n'))
    return get_text()


def get_text():
    text = ''
    while not text.endswith('Command?\n'):
        try:
            text += chr(next(runner))
        except StopIteration:
            break
    return text


if __name__ == '__main__':
    commands = [
        'south',
        'take fuel cell',
        'north',
        'west',
        'take mutex',
        'south',
        'south',
        'take coin',
        'north',
        'east',
        'take cake',
        'north',
        'west',
        'south',
        'west'
    ]
    response = None
    get_text()
    for command in commands:
        response = enter_command(command)
    password = re.search(r'\d+', response)
    print(password[0])
