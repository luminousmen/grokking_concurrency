#!/usr/bin/env python3.9

"""Using shared memory IPC between threads"""

import time
from threading import Thread, current_thread

SIZE = 5
# setup shared memory
shared_memory = [-1] * SIZE


class Producer(Thread):
    def run(self) -> None:
        self.name = "Producer"
        global shared_memory
        for i in range(SIZE):
            print(f"{current_thread().name}: Writing {int(i)}")
            shared_memory[i - 1] = i


class Consumer(Thread):
    def run(self) -> None:
        self.name = "Consumer"
        global shared_memory
        for i in range(SIZE):
            # try reading the data until succession
            while True:
                line = shared_memory[i]
                if line == -1:
                    # data hasn't change - waiting for a second
                    print(f"{current_thread().name}: Data not available\n"
                          f"Sleeping for 1 second before retrying")
                    time.sleep(1)
                    continue
                print(f"{current_thread().name}: Read: {int(line)}")
                break


def main() -> None:
    threads = [
        Consumer(),
        Producer(),
    ]

    # start threads
    for thread in threads:
        thread.start()

    # block the main thread until the child threads has finished
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
