#!/usr/bin/env python3

"""Shared IPC"""

import os
import time
from multiprocessing import Process, Array


class ProcessOne(Process):
    def __init__(self, shared: Array) -> None:
        super().__init__()
        self.shared = shared

    def run(self) -> None:
        print(f"PID: {os.getpid()}")

        for i in range(10):
            # attempt to write to our shared memory until succession
            while True:
                try:
                    print(f"Writing {int(i)}")
                    self.shared[i-1] = i
                    if i % 6 == 0:
                        print("Sleeping for 5 seconds")
                        time.sleep(5)
                    break
                except:
                    pass

        print("Process 1 finished")


class ProcessTwo(Process):
    def __init__(self, shared: Array) -> None:
        super().__init__()
        self.shared = shared

    def run(self) -> None:
        print(f"PID: {os.getpid()}")

        for i in range(10):
            while True:
                try:
                    line = self.shared[i]
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
    arr = Array("i", [-1] * 10)

    # setup processes
    procs = [
        ProcessOne(arr),
        ProcessTwo(arr)
    ]

    # start processes
    for proc in procs:
        proc.start()

    # run to completion
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    main()
