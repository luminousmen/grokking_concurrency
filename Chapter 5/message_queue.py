#!/usr/bin/env python3

""" Using message queues for IPC """

import os
import time
from multiprocessing import Process, Queue


def process_queue(queue: Queue) -> None:
    while not queue.empty():
        # getting new data for processing from the queue
        item = queue.get()
        print(f"PID({os.getpid()}): processing {item} from the queue")
        time.sleep(2)


def main() -> None:
    # creating a queue and putting integer number into it to process
    q = Queue()
    for i in range(10):
        q.put(i)

    processes = []
    # running 4 processes to process data from the queue
    for _ in range(4):
        process = Process(target=process_queue, args=(q,))
        process.start()
        processes.append(process)

    for thread in processes:
        # join method that blocks the main thread until the child threads has finished
        thread.join()


if __name__ == "__main__":
    main()
