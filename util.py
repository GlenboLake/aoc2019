from PIL import Image


def show_dict(d):
    """
    Create an image from a sparse dictionary

    :param dict d: A dictionary of 2-tuples to bits
    """
    left = min(k[0] for k in d)
    right = max(k[0] for k in d)
    width = right - left + 1

    top = max(k[1] for k in d)
    bottom = min(k[1] for k in d)
    height = top - bottom + 1

    normalized = {(k[0] - left, top - k[1]): v for k, v in d.items()}

    img = Image.new(mode='1', size=(2 * width, 2 * height))
    for row in range(height):
        for col in range(width):
            img.putpixel((2 * col, 2 * row), normalized.get((col, row), 0))
            img.putpixel((2 * col + 1, 2 * row), normalized.get((col, row), 0))
            img.putpixel((2 * col, 2 * row + 1), normalized.get((col, row), 0))
            img.putpixel((2 * col + 1, 2 * row + 1), normalized.get((col, row), 0))
    img.show()
