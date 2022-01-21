#!/usr/bin/env python3
"""Two processes lifecycle example"""

import time
from multiprocessing import Process


class Worker(Process):
    def run(self):
        print("Worker started...")
        time.sleep(3)
        print("Worker is done.")


if __name__ == "__main__":
    print("Boss requesting Worker's help.")
    worker = Worker()
    print("  Worker alive?:", worker.is_alive())

    print("Boss tells Worker to start.")
    worker.start()
    print("  Worker alive?:", worker.is_alive())

    print("Boss goes for coffee.")
    time.sleep(0.5)
    print("  Worker alive?:", worker.is_alive())

    print("Boss patiently waits for Worker to finish and join...")
    worker.join()
    print("  Worker alive?:", worker.is_alive())

    print("Boss and Worker are both done!")
