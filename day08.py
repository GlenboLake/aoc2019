from PIL import Image

width, height = 25, 6

with open('input/day08.txt') as f:
    data = list(map(int, f.read().strip()))

layers = []
while data:
    layer = []
    for _ in range(width):
        for _ in range(height):
            layer.append(data.pop(0))
    layers.append(layer)

zeros_layer = min(layers, key=lambda lay: lay.count(0))

print(zeros_layer.count(1) * zeros_layer.count(2))

img = Image.new(mode='1', size=(width, height))

for row in range(height):
    for col in range(width):
        pixels = [layer.pop(0) for layer in layers]
        for x in pixels:
            if x == 0:
                img.putpixel((col, row), 0)
                break
            elif x == 1:
                img.putpixel((col, row), 1)
                break
img.show()
