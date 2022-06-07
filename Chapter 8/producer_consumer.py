#!/usr/bin/env python3

"""Implementing parking garage using semaphore for control critical section"""

import time
from threading import Thread, Semaphore

CAPACITY = 5
# shared memory
BUFFER = ["" for i in range(CAPACITY)]

mutex = Semaphore()
empty = Semaphore(CAPACITY)
full = Semaphore(0)
producer_idx = 0


class Producer(Thread):
    def __init__(self, name: str, items_amount: int = 5):
        super().__init__()
        self.counter = 0
        self.name = name
        self.items_amount = items_amount

    def next_index(self, producer_idx) -> int:
        return (producer_idx + 1) % CAPACITY

    def run(self):
        global producer_idx
        while self.counter < self.items_amount:
            empty.acquire()
            mutex.acquire()

            self.counter += 1
            BUFFER[producer_idx] = f"{self.name}-{self.counter}"
            print(f"{self.name} produced: `{BUFFER[producer_idx]}`")
            producer_idx = self.next_index(producer_idx)

            mutex.release()
            full.release()
            time.sleep(1)


class Consumer(Thread):
    def __init__(self, name: str, items_amount: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.items_amount = items_amount

    def next_index(self):
        return (self.idx + 1) % CAPACITY

    def run(self):
        while self.counter < self.items_amount:
            full.acquire()
            mutex.acquire()

            item = BUFFER[self.idx]
            print(f"{self.name} consumed item: `{item}`")
            self.idx = self.next_index()
            self.counter += 1

            mutex.release()
            empty.release()
            time.sleep(2)


if __name__ == "__main__":
    threads = [
        Producer("John"),
        Producer("Sara"),
        Consumer("Bob")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
