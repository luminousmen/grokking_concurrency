#!/usr/bin/env python3.9

"""Philosophers thinking and eating dumplings - fighting deadlock
by setting priorities"""

from lock_with_name import LockWithName

from deadlock import Philosopher

if __name__ == "__main__":
    chopstick_a = LockWithName("chopstick_a")
    chopstick_b = LockWithName("chopstick_b")

    philosopher_1 = Philosopher("Philosopher #1", chopstick_a, chopstick_b)
    # changing the order a > b, so a should be acquired first
    philosopher_2 = Philosopher("Philosopher #2", chopstick_a, chopstick_b)

    philosopher_1.start()
    philosopher_2.start()
