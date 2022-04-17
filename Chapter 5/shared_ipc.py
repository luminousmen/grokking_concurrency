#!/usr/bin/env python3

""" Shared IPC """

import os
import time
from multiprocessing import Process, Array


def send(shared_memory: Array) -> None:
    print(f"PID: {os.getpid()}")

    for i in range(10):
        # attempt to write to our shared memory until succession
        while True:
            try:
                print(f"Writing {int(i)}")
                shared_memory[i-1] = i
                if i % 6 == 0:
                    print("Sleeping for 5 seconds")
                    time.sleep(5)
                break
            except:
                pass

    print("Process 1 finished")


def receive(shared_memory: Array) -> None:
    print(f"PID: {os.getpid()}")

    for i in range(10):
        while True:
            try:
                line = shared_memory[i]
                if line == -1:
                    print("Data not available sleeping for 1 second before retrying")
                    time.sleep(1)
                    raise
                print(f"Read: {int(line)}")
                break
            except:
                pass

    print("Process 2 finished")


def main() -> None:
    print(f"PID: {os.getpid()}")

    # setup shared memory using Array
    shared_memory = Array("i", [-1] * 10)

    # setup processes
    processes = [
        Process(target=receive, args=(shared_memory,)),
        Process(target=send, args=(shared_memory,))
    ]

    # start processes
    for process in processes:
        process.start()

    # run to completion
    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
