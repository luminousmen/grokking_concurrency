#!/usr/bin/env python3

"""Three philosophers thinking and eating dumplings - avoiding deadlock
by introducing arbitrary"""

import time
from threading import Thread, Lock

dumplings = 100


class Waiter:
    def __init__(self):
        self.mutex = Lock()

    def ask_for_chopsticks(self, left_chopstick: Lock, right_chopstick: Lock) -> None:
        with self.mutex:
            left_chopstick.acquire()
            print(f"{id(left_chopstick)} chopstick grabbed")
            right_chopstick.acquire()
            print(f"{id(right_chopstick)} chopstick grabbed")

    def release_chopsticks(self, left_chopstick: Lock, right_chopstick: Lock) -> None:
        right_chopstick.release()
        print(f"{id(right_chopstick)} chopstick released")
        left_chopstick.release()
        print(f"{id(left_chopstick)} chopstick released")


class Philosopher(Thread):
    def __init__(self, name: str, waiter: Waiter, left_chopstick: Lock, right_chopstick: Lock) -> None:
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
            if dumplings > 0:
                dumplings -= 1
                print(f"{self.name} eat a dumpling. Dumplings left: {dumplings}")
            self.waiter.release_chopsticks(self.left_chopstick, self.right_chopstick)
            time.sleep(0.00001)


if __name__ == "__main__":
    chopstick_a = Lock()
    chopstick_b = Lock()

    waiter = Waiter()
    philosopher_1 = Philosopher("Philosopher #1", waiter, chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", waiter, chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
