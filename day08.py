from util import ocr

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

d = {}

for layer in reversed(layers):
    d.update({(i % width, i // width): v for i, v in enumerate(layer) if v != 2})

for row in range(height):
    for col in range(width):
        pixels = [layer.pop(0) for layer in layers]
        for x in pixels:
            if x != 2:
                d[col, row] = x
                break

print(ocr(d))
