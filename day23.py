import threading
import time
from queue import Queue

from intcode import load, run

program = load(23)

NAT = 255


class IterableQueue(Queue):
    def __init__(self, *values):
        super().__init__()
        self.done = threading.Event()
        for v in values:
            self.put(v)

    def __iter__(self):
        return self

    def __next__(self):
        if self.done.is_set():
            raise KeyboardInterrupt()
        if self.qsize():
            return self.get()
        return -1

    def abort(self):
        # print('Aborting')
        self.done.set()


def nat_func(buffers):
    def idle_check():
        # print('idle check!', flush=True)
        for _ in range(20):
            if any(b.qsize() for b in buffers.values()):
                return False
            time.sleep(0.05)
        return True

    queue = buffers[NAT]
    last_x, last_y = None, None
    last_sent = None
    while True:
        if queue.qsize():
            x = queue.get()
            y = queue.get()
            # print(f'\nNAT received packet: {x},{y}')
            if last_y is None:
                print('\nPart 1:', y)
            last_x, last_y = x, y
        if idle_check():
            # print(f'IDLE, sending {last_x},{last_y} to 0')
            buffers[0].put(last_x)
            buffers[0].put(last_y)
            if last_y == last_sent:
                print('Part 2:', last_y)
                for buf in buffers.values():
                    buf.abort()
                break
            last_sent = last_y
    # print('NAT exiting')


def run_vm(buffers, addr):
    vm = run(program[:], buffers[addr])
    try:
        while True:
            dest = next(vm)
            x = next(vm)
            y = next(vm)
            # if dest == NAT:
            #     print(f'Thread {addr}: {x},{y} for {dest}')
            # else:
            #     print(threading.current_thread().name)
            buffers[dest].put(x)
            buffers[dest].put(y)
    except KeyboardInterrupt:
        pass
    # print(threading.current_thread().name, 'exiting')


buffer_list = {i: IterableQueue(i) for i in range(50)}
buffer_list[NAT] = IterableQueue()
threads = [threading.Thread(target=run_vm, args=(buffer_list, i), name=str(i)) for i in range(50)]
nat_thread = threading.Thread(target=nat_func, args=(buffer_list,))

nat_thread.start()
for t in threads:
    t.start()
try:
    nat_thread.join()
    for t in threads:
        t.join()
except KeyboardInterrupt:
    for i in range(50):
        buffer_list[i].abort()
        while not buffer_list[i].empty():
            buffer_list[i].get_nowait()