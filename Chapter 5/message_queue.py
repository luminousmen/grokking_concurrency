#!/usr/bin/env python3.9

"""Using message queues for IPC between threads"""

import time
from queue import Queue
from threading import Thread, current_thread


class Worker(Thread):
    def __init__(self, queue: Queue, id: int):
        super().__init__(name=str(id))
        self.queue = queue

    def run(self) -> None:
        while not self.queue.empty():
            # getting new data for processing from the queue
            item = self.queue.get()
            print(f"Thread {current_thread().name}: "
                  f"processing item {item} from the queue")
            time.sleep(2)


def main(thread_num: int) -> None:
    # creating a queue and putting integer number into it to process
    q = Queue()
    for i in range(10):
        q.put(i)

    threads = []
    # running threads to process data from the queue
    for i in range(thread_num):
        thread = Worker(q, i + 1)
        thread.start()
        threads.append(thread)

    # block the main thread until the child threads has finished
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    thread_num = 4
    main(thread_num)
