#!/usr/bin/env python3.9

"""Process lifecycle example"""

import time
from multiprocessing import Process


class Worker(Process):
    def run(self) -> None:
        print("Worker started...")
        time.sleep(3)
        print("Worker is done.")


def main() -> None:
    print("Boss requesting Worker's help.")
    worker = Worker()
    print(f"\tWorker alive?: {worker.is_alive()}")

    print("Boss tells Worker to start.")
    worker.start()
    print(f"\tWorker alive?: {worker.is_alive()}")

    print("Boss goes for coffee.")
    time.sleep(0.5)
    print(f"\tWorker alive?: {worker.is_alive()}")

    print("Boss patiently waits for Worker to finish and join...")
    worker.join()
    print(f"\tWorker alive?: {worker.is_alive()}")

    print("Boss and Worker are both done!")


if __name__ == "__main__":
    main()
