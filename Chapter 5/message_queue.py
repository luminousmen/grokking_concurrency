import os
import time
from multiprocessing import Process, Queue


def process_queue(queue: Queue) -> None:
    while not queue.empty():
        # getting new data for processing from the queue
        item = queue.get()
        print("{} removed {} from the queue".format(os.getpid(), item))
        time.sleep(2)


if __name__ == "__main__":
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
        thread.join()
