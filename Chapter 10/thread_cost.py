#!/usr/bin/env python3.9

"""Creating do-nothing threads, professionally"""

import os
from time import sleep
from threading import Thread
# IMPORTANT! Do `pip install psutil` if it is not installed yet
import psutil

GB = 1024 ** 3
MB = 1024 ** 2
# WARNING!
# This can end up in `RuntimeError: can't start new thread`
# Increase this number at your own risk
NUM_THREADS = 1000


if __name__ == "__main__":
    threads = []
    for _ in range(NUM_THREADS):
        threads.append(Thread(target=lambda: sleep(30)))

    for thread in threads:
        thread.start()

    # vms - total program size
    # rss - resident set size
    total_memory = psutil.Process().memory_info().vms
    ram_memory = psutil.Process().memory_info().rss
    print(f"Process with PID={os.getpid()} takes total of {total_memory / GB:.1f}GB memory used")
    print(f"Process with PID={os.getpid()} takes {ram_memory / MB:.1f}MB of RAM memory used")
    print(f"Each thread takes about {total_memory / NUM_THREADS / MB:.1f}MB memory")

    for thread in threads:
        thread.join()
