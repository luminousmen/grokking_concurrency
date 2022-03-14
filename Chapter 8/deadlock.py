#!/usr/bin/env python3

"""Three philosophers thinking and eating dumplings - deadlock happens"""

import time
from threading import Thread, Lock

dumplings = 20


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: Lock, right_chopstick: Lock) -> None:
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        while dumplings > 0:
            self.left_chopstick.acquire()
            print(f"{id(self.left_chopstick)} chopstick grabbed by {self.name}")
            self.right_chopstick.acquire()
            print(f"{id(self.right_chopstick)} chopstick grabbed by {self.name}")

            if dumplings > 0:
                dumplings -= 1
                print(f"{self.name} eat a dumpling. Dumplings left: {dumplings}")

            self.right_chopstick.release()
            print(f"{id(self.right_chopstick)} chopstick released by {self.name}")
            self.left_chopstick.release()
            print(f"{id(self.left_chopstick)} chopstick released by {self.name}")
            time.sleep(0.00001)


if __name__ == "__main__":
    chopstick_a = Lock()
    chopstick_b = Lock()

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    philosopher_2 = Philosopher("Philosopher #2", chopstick_b, chopstick_a)

    philosopher_1.start()
    philosopher_2.start()
