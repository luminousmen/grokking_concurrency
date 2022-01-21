#!/usr/bin/env python3
""" Threads that waste CPU cycles """

import os
import time
import threading


def cpu_waster():
    while True:
        print(f"Hello from {threading.current_thread().name}")
        time.sleep(5)


def display_threads():
    # display information about this process
    print("Process ID: ", os.getpid())
    print("Thread Count: ", threading.active_count())
    for thread in threading.enumerate():
        print(thread)


if __name__ == "__main__":
    num_threads = 10
    display_threads()

    print(f"Starting {num_threads} CPU wasters...")
    for i in range(num_threads):
        threading.Thread(target=cpu_waster).start()

    display_threads()
