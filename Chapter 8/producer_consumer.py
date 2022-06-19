#!/usr/bin/env python3

"""Implementing parking garage using semaphore for control critical section"""

import time
from threading import Thread, Semaphore

SIZE = 5
# shared memory
BUFFER = ["" for i in range(SIZE)]

mutex = Semaphore()
empty = Semaphore(SIZE)
full = Semaphore(0)
producer_idx = 0


class Producer(Thread):
    """Producer thread will produce an item and put it into the buffer"""
    def __init__(self, name: str, items_amount: int = 5):
        super().__init__()
        self.counter = 0
        self.name = name
        self.items_amount = items_amount

    def next_index(self, producer_idx) -> int:
        """Get the next empty buffer index"""
        return (producer_idx + 1) % SIZE

    def run(self):
        global producer_idx
        while self.counter < self.items_amount:
            # wait till the buffer have some empty slots
            empty.acquire()
            # critical section for changing the buffer
            mutex.acquire()

            self.counter += 1
            BUFFER[producer_idx] = f"{self.name}-{self.counter}"
            print(f"{self.name} produced: `{BUFFER[producer_idx]}`")
            producer_idx = self.next_index(producer_idx)
            # leaving critical section
            mutex.release()
            # buffer have one more item to consume
            full.release()
            # simulating some real action here
            time.sleep(1)


class Consumer(Thread):
    """Consumer thread will consume items from the buffer"""
    def __init__(self, name: str, items_amount: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.items_amount = items_amount

    def next_index(self):
        """Get the next buffer index to consume"""
        return (self.idx + 1) % SIZE

    def run(self):
        while self.counter < self.items_amount:
            # wait till the buffer have some new items to consume
            full.acquire()
            # critical section for changing the buffer
            mutex.acquire()

            item = BUFFER[self.idx]
            print(f"{self.name} consumed item: `{item}`")
            self.idx = self.next_index()
            self.counter += 1

            # leaving critical section
            mutex.release()
            # one more empty slot is available in buffer
            empty.release()
            # simulating some real action here
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
