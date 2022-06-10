#!/usr/bin/env python3

"""Three philosophers thinking and eating dumplings - avoiding deadlock
by introducing arbitrary"""

import time
from threading import Thread, Lock

from lock_with_name import LockWithName

THREAD_DELAY = 0.1
dumplings = 100


class Waiter:
    def __init__(self):
        self.mutex = Lock()

    def ask_for_chopsticks(self, left_chopstick: LockWithName, right_chopstick: LockWithName):
        with self.mutex:
            left_chopstick.lock.acquire()
            print(f"{left_chopstick.name} chopstick grabbed")
            right_chopstick.lock.acquire()
            print(f"{right_chopstick.name} chopstick grabbed")

    def release_chopsticks(self, left_chopstick: LockWithName,
                           right_chopstick: LockWithName) -> None:
        right_chopstick.lock.release()
        print(f"{right_chopstick.name} chopstick released")
        left_chopstick.lock.release()
        print(f"{left_chopstick.name} chopstick released")


class Philosopher(Thread):
    def __init__(self, name: str, waiter: Waiter, left_chopstick: LockWithName,
                 right_chopstick: LockWithName):
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick
        self.waiter = waiter

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            self.waiter.ask_for_chopsticks(self.left_chopstick, self.right_chopstick)

            dumplings -= 1
            print(f"{self.name} eat a dumpling. Dumplings left: {dumplings}")

            self.waiter.release_chopsticks(self.left_chopstick, self.right_chopstick)
            time.sleep(THREAD_DELAY)


if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    waiter = Waiter()
    philosopher_1 = Philosopher("Philosopher #1", waiter, chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", waiter, chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
