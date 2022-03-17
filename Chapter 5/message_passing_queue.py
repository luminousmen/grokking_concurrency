import os
import time
import queue
from multiprocessing import Process


def process_queue(queue: queue.Queue) -> None:
    while not queue.empty():
        # getting new data for processing from the queue
        item = queue.get()
        print("{} removed {} from the queue".format(os.getpid(), item))
        queue.task_done()
        time.sleep(2)


if __name__ == "__main__":
    # creating a queue and putting integer number into it to process
    q = queue.Queue()
    for i in range(5):
        q.put(i)

    processes = []
    # running 4 processes to process data from the queue
    for _ in range(4):
        process = Process(target=process_queue, args=(q,))
        process.start()
        processes.append(process)

    for thread in processes:
        thread.join()
