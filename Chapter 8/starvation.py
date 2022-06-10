#!/usr/bin/env python3
"""Three philosophers, thinking and eating sushi - but some has been starving"""
import time
from threading import Thread

from deadlock.lock_with_name import LockWithName

dumplings = 1000
THREAD_DELAY = 1e-16


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: LockWithName, right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        dumplings_eaten = 0
        while dumplings > 0:
            self.left_chopstick.lock.acquire()
            self.right_chopstick.lock.acquire()
            if dumplings > 0:
                dumplings -= 1
                dumplings_eaten += 1
                time.sleep(THREAD_DELAY)
            self.right_chopstick.lock.release()
            self.left_chopstick.lock.release()
        print(f"{self.name} took {dumplings_eaten} pieces")


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    threads = []
    for i in range(10):
        threads.append(Philosopher(f"Philosopher #{i}", chopstick_a, chopstick_b))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
