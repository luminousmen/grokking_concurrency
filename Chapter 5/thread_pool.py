#!/usr/bin/env python3.9

"""Simple thread pool implementation"""

import time
import queue
import typing as T
from threading import Thread, current_thread

Callback = T.Callable[..., None]
Task = T.Tuple[Callback, T.Any, T.Any]
TaskQueue = queue.Queue


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks: queue.Queue[Task]):
        super().__init__()
        self.tasks = tasks

    def run(self) -> None:
        # running the thread indefinitely
        while True:
            # getting the tasks from queue and execute
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads: int):
        # setting up the queue to put tasks
        self.tasks: TaskQueue = queue.Queue(num_threads)
        self.num_threads = num_threads

        # create long-running threads
        for _ in range(self.num_threads):
            worker = Worker(self.tasks)
            worker.setDaemon(True)
            worker.start()

    def submit(self, func: Callback, *args, **kargs) -> None:
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self) -> None:
        """Wait for completion of all the tasks in the queue"""
        # join method that blocks the main thread until the child
        # threads has finished
        self.tasks.join()


def cpu_waster(i: int) -> None:
    """Wasting the processor time, professionally"""
    name = current_thread().getName()
    print(f"{name} doing {i} work")
    time.sleep(3)


def main() -> None:
    pool = ThreadPool(num_threads=5)
    for i in range(20):
        pool.submit(cpu_waster, i)

    print("All work requests sent")
    pool.wait_completion()
    print("All work completed")


if __name__ == "__main__":
    main()
