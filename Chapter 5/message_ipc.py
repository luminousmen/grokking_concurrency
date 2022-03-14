#!/usr/bin/env python3

"""Message passing IPC"""

import os
import time
import multiprocessing
from multiprocessing import Process


class ProcessOne(Process):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    def run(self) -> None:
        print(f"PID: {os.getpid()}")

        # open the channel for write
        file = os.fdopen(self.channel.fileno(), "w")

        for i in range(10):
            # attempt to write to shared channel until success
            while True:
                try:
                    print(f"Writing {int(i)}")
                    file.write(f"{i}\n")
                    file.flush()
                    if i % 6 == 0:
                        print("Intentionally sleeping for 5 seconds")
                        time.sleep(5)
                    break
                except:
                    pass

        # clean up channel
        self.channel.close()
        print("Process 1 finished")


class ProcessTwo(Process):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    def run(self) -> None:
        print(f"PID: {os.getpid()}")

        # open the file descriptor
        file = os.fdopen(self.channel.fileno(), "r")

        count = 0
        while count < 10:
            while True:
                try:
                    line = file.readline()
                    print(f"Read: {int(line)}")
                    count += 1
                    break
                except:
                    pass

        self.channel.close()
        print("Process 2 finished")


def main() -> None:
    print(f"PID: {os.getpid()}")

    # setup a channel
    read_channel, write_channel = multiprocessing.Pipe(False)

    # setup processes
    procs = [
        ProcessOne(write_channel),
        ProcessTwo(read_channel)
    ]

    # start processes
    for proc in procs:
        proc.start()

    # run to completion
    for proc in procs:
        proc.join()


if __name__ == "__main__":
    main()
