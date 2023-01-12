#!/usr/bin/env python3
"""Two polite philosophers, thinking and eating sushi - but some has been starving"""

import time
from threading import Thread

from deadlock.lock_with_name import LockWithName

THREAD_DELAY = 1
dumplings = 20


class Philosopher(Thread):
    def __init__(
            self, name: str,
            left_chopstick: LockWithName,
            right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()
            print(f"{self.left_chopstick.name} chopstick grabbed by {self.name}")
            if self.right_chopstick.locked():
                print(f"{self.name} cannot get the {self.right_chopstick.name} chopstick, politely concedes...")
            else:
                self.right_chopstick.acquire()
                print(f"{self.right_chopstick.name} chopstick grabbed by {self.name}")
                dumplings -= 1
                print(f"{self.name} eat a dumpling. Dumplings left: {dumplings}")
                time.sleep(THREAD_DELAY)
                self.right_chopstick.release()
            self.left_chopstick.release()


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
