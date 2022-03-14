#!/usr/bin/env python3

#
""""""

import time
import random
import threading

TOTAL_SPOTS = 3


class Garage:
    def __init__(self):
        self.semaphore = threading.Semaphore(TOTAL_SPOTS)
        self.cars_lock = threading.Lock()
        self.cars = []

    def count_parked_cars(self):
        return len(self.cars)

    def enter(self, car: str) -> None:
        """entrances call this function when a car wants to enter"""
        self.semaphore.acquire()
        self.cars_lock.acquire()
        self.cars.append(car)
        self.cars_lock.release()

    def exit(self, car: str) -> None:
        """ entrances call this function when a car exits"""
        self.cars_lock.acquire()
        self.cars.remove(car)
        self.semaphore.release()
        self.cars_lock.release()


def park(garage: Garage, car_name: str) -> None:
    garage.enter(car_name)
    print(f"{car_name} car parked")
    time.sleep(random.uniform(1, 2))
    print(f"{car_name} leaving")
    garage.exit(car_name)


if __name__ == "__main__":
    garage = Garage()

    threads = []
    # test garage for 10 busy hours straight
    for car_num in range(10):
        t = threading.Thread(target=park, args=(garage, f"car-{car_num}"))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    print("Number of parked car after a busy day:")
    print(f"{garage.count_parked_cars()}. Expected: 0")
