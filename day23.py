from collections import deque

from intcode import load, run

program = load(23)

class Queue:
    def __init__(self, *init):
        self.buffer = deque(init)

    def send(self, *values):
        self.buffer.extend(values)

    def __next__(self):
        if self.buffer:
            return self.buffer.popleft()
        else:
            return -1

buffers = [Queue(i) for i in range(50)]
vms = [run(program[:], buffer) for buffer in buffers]

while True:
    for vm, buffer in zip(vms, buffers):
        if not buffer.buffer:
            continue
        dest = next(vm)
        x = next(vm)
        y = next(vm)
        print(f'{x},{y} for {dest}')
        if dest == 255:
            print('Part 1:', y)
            break
        buffers[dest].send(x, y)
