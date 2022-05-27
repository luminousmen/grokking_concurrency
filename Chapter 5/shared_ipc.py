#!/usr/bin/env python3

""" Shared IPC """

import os
import time
from multiprocessing import Process, Array


def write(shared_memory: Array) -> None:
    for i in range(5):
        print(f"PID({os.getpid()}): Writing {int(i)}")
        shared_memory[i-1] = i


def read(shared_memory: Array) -> None:
    for i in range(5):
        # try reading the data until succession
        while True:
            line = shared_memory[i]
            if line == -1:
                # data hasn't change - waiting for a second
                print(f"PID({os.getpid()}): Data not available sleeping for 1 second before retrying")
                time.sleep(1)
                continue
            print(f"PID({os.getpid()}): Read: {int(line)}")
            break


def main() -> None:
    # setup shared memory using Array
    shared_memory = Array("i", [-1] * 5)

    # setup processes
    processes = [
        Process(target=read, args=(shared_memory,)),
        Process(target=write, args=(shared_memory,))
    ]

    # start processes
    for process in processes:
        process.start()

    # run to completion
    for process in processes:
        # join method that blocks the main process until the child processes has finished
        process.join()


if __name__ == "__main__":
    main()
