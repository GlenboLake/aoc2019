from pprint import pprint

width, height = 25, 6

with open('input/day08.txt') as f:
    data = list(map(int, f.read().strip()))

size = width*height

layers = []
while data:
    layer = []
    for w in range(width):
        for h in range(height):
            layer.append(data.pop(0))
    layers.append(layer)

zeros_layer = min(layers, key=lambda lay: lay.count(0))

print(zeros_layer.count(1) * zeros_layer.count(2))

BLACK = chr(9608)
WHITE = chr(9617)

for row in range(height):
    for col in range(width):
        pixels = [layer.pop(0) for layer in layers]
        for x in pixels:
            if x == 0:
                print(BLACK, end='')
                break
            elif x == 1:
                print(WHITE, end='')
                break
    print()