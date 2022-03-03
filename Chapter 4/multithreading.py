#!/usr/bin/env python3

"""Threads that waste CPU cycles"""

import os
import time
import threading


def cpu_waster(i: int) -> None:
    """Wasting the processor time, professionally"""
    name = threading.current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)


def display_threads() -> None:
    """Display information about current process"""
    print(f"PID: {os.getpid()}")
    print(f"Thread Count: {threading.active_count()}")
    print("Active threads:")
    for thread in threading.enumerate():
        print(thread)


def main(num_threads: int) -> None:
    display_threads()

    print(f"Starting {num_threads} CPU wasters...")
    for i in range(num_threads):
        threading.Thread(target=cpu_waster, args=(i,)).start()

    display_threads()


if __name__ == "__main__":
    num_threads = 10
    main(num_threads)
