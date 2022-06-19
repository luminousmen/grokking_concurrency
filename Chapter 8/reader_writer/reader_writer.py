#!/usr/bin/env python3

"""Readers-writers problem using mutex: readers have priority"""

import time
import random
from threading import Thread

from rwlock import RWLock

# shared memory
counter = 0
lock = RWLock()


class User(Thread):
    """User of the library catalog. Reader implementation"""
    def __init__(self, idx: int):
        super().__init__()
        self.idx = idx

    def run(self) -> None:
        while True:
            lock.acquire_read()
            print(f"User {self.idx} reading: {counter}")
            time.sleep(random.randrange(1, 3))
            lock.release_read()
            # simulating some real action here
            time.sleep(0.5)


class Librarian(Thread):
    """Writer of the library catalog. Writer implementation"""
    def run(self) -> None:
        global counter
        while True:
            lock.acquire_write()
            print(f"Librarian writing...")
            counter += 1
            print(f"New value: {counter}")
            # simulating some real action here
            time.sleep(random.randrange(1, 3))
            lock.release_write()


if __name__ == "__main__":
    threads = [
        User(0),
        User(1),
        Librarian()
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
