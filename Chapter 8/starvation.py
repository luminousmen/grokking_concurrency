#!/usr/bin/env python3
"""Three philosophers, thinking and eating sushi - but some has been starving"""

from threading import Thread, Lock

dumplings = 5000


class Philosopher(Thread):
    def __init__(self, name: str, left_chopstick: Lock, right_chopstick: Lock) -> None:
        super().__init__()
        self.name = name
        self.left_chopstick = left_chopstick
        self.right_chopstick = right_chopstick

    def run(self) -> None:
        # using globally shared variable
        global dumplings

        dumplings_eaten = 0
        while dumplings > 0:
            with self.left_chopstick:
                with self.right_chopstick:
                    if dumplings > 0:
                        dumplings -= 1
                        dumplings_eaten += 1
                        print(f"{self.name} eat a dumpling. Dumplings left: {dumplings}")

        print(f"{self.name} took {dumplings_eaten} pieces")


if __name__ == "__main__":
    chopstick_a = Lock()
    chopstick_b = Lock()

    for thread in range(50):
        Philosopher("Philosopher #1", chopstick_a, chopstick_b).start()
        Philosopher("Philosopher #2", chopstick_a, chopstick_b).start()
