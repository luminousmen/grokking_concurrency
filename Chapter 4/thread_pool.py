#!/usr/bin/env python3
"""Simple thread pool implementation"""
import time
import queue
from threading import Thread, current_thread


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = queue.Queue(num_threads)
        self.num_threads = num_threads
        for _ in range(self.num_threads): 
            worker = Worker(self.tasks)
            worker.setDaemon(True)
            worker.start()

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


def cpu_waister(i):
    name = current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)


if __name__ == "__main__":
    pool = ThreadPool(5)
    for vegetable in range(20):
        pool.add_task(cpu_waister, vegetable)
    print("All work requests sent")
    pool.wait_completion()
    print("All work completed")


