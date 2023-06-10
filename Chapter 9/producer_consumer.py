#!/usr/bin/env python3.9

"""Implementing parking garage using semaphore for control critical section"""

import time
from threading import Thread, Semaphore, Lock

SIZE = 5
# shared memory
BUFFER = ["" for i in range(SIZE)]
producer_idx: int = 0

mutex = Lock()
empty = Semaphore(SIZE)
full = Semaphore(0)


class Producer(Thread):
    """Producer thread will produce an item and put it into the buffer"""

    def __init__(self, name: str, maximum_items: int = 5):
        super().__init__()
        self.counter = 0
        self.name = name
        self.maximum_items = maximum_items

    def next_index(self, index: int) -> int:
        """Get the next empty buffer index"""
        return (index + 1) % SIZE

    def run(self) -> None:
        global producer_idx
        while self.counter < self.maximum_items:
            # wait untill the buffer have some empty slots
            empty.acquire()
            # critical section for changing the buffer
            mutex.acquire()
            self.counter += 1
            BUFFER[producer_idx] = f"{self.name}-{self.counter}"
            print(f"{self.name} produced: "
                  f"'{BUFFER[producer_idx]}' into slot {producer_idx}")
            producer_idx = self.next_index(producer_idx)
            # leaving critical section
            mutex.release()
            # buffer have one more item to consume
            full.release()
            # simulating some real action here
            time.sleep(1)


class Consumer(Thread):
    """Consumer thread will consume items from the buffer"""

    def __init__(self, name: str, maximum_items: int = 10):
        super().__init__()
        self.name = name
        self.idx = 0
        self.counter = 0
        self.maximum_items = maximum_items

    def next_index(self) -> int:
        """Get the next buffer index to consume"""
        return (self.idx + 1) % SIZE

    def run(self) -> None:
        while self.counter < self.maximum_items:
            # wait untill the buffer has some new items to consume
            full.acquire()
            # critical section for changing the buffer
            mutex.acquire()
            item = BUFFER[self.idx]
            print(f"{self.name} consumed item: "
                  f"'{item}' from slot {self.idx}")
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
        Producer("SpongeBob"),
        Producer("Patrick"),
        Consumer("Squidward")
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
