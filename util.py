from PIL import Image


def normalize_dict(d):
    left = min(k[0] for k in d)
    top = max(k[1] for k in d)

    normalized = {(k[0] - left, top - k[1]): v for k, v in d.items()}
    return normalized


def show_dict(d):
    """
    Create an image from a sparse dictionary

    :param dict d: A dictionary of 2-tuples to bits
    """
    width = max(k[0] for k in d) + 1
    height = max(k[1] for k in d) + 1

    img = Image.new(mode='1', size=(2 * width, 2 * height))
    for row in range(height):
        for col in range(width):
            img.putpixel((2 * col, 2 * row), d.get((col, row), 0))
            img.putpixel((2 * col + 1, 2 * row), d.get((col, row), 0))
            img.putpixel((2 * col, 2 * row + 1), d.get((col, row), 0))
            img.putpixel((2 * col + 1, 2 * row + 1), d.get((col, row), 0))
    img.show()


def dict_str(d):
    width = max(k[0] for k in d) + 1
    height = max(k[1] for k in d) + 1

    s = ''
    for row in range(height):
        for col in range(width):
            s += '#' if d.get((col, row), 0) else ' '
        s += '\n'
    return s


_alphabet_text = '''\
 ##  ###   ##  #### ####  ##  #  # #  #
#  # #  # #  # #    #    #  # #  # # # 
#  # ###  #    ###  ###  #    #### ##  
#### #  # #    #    #    # ## #  # # # 
#  # #  # #  # #    #    #  # #  # # # 
#  # ###   ##  #### #     ### #  # #  #'''.splitlines()


def _extract_letter(i):
    return '\n'.join([line[5 * i:5 * (i + 1) - 1] for line in _alphabet_text])


_known = 'ABCEFGHK'
_alphabet = {_extract_letter(i): letter for i, letter in enumerate(_known)}


def ocr(d):
    s = dict_str(d).splitlines()
    width = len(s[0])
    offset = 0
    for offset in range(width):
        if not all(line[offset] == ' ' for line in s):
            break
    letters = ['\n'.join(line[i:i + 4] for line in s) for i in range(offset, width, 5)]
    while not letters[-1].strip():
        letters.pop(-1)
    result = ''
    for letter in letters:
        result += _alphabet.get(letter, '?')
        if result[-1] == '?':
            print('Unknown letter:')
            print(letter)

    return result
