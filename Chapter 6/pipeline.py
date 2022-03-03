#!/usr/bin/env python3

#
"""Task parallelism using Pipeline processing pattern"""
import time
from multiprocessing import Queue
from threading import Thread


class ProduceThread(Thread):
    def __init__(self, out_queue: Queue) -> None:
        super().__init__()
        self.out_queue = out_queue

    def run(self) -> None:
        for msg in range(100):
            print(f"GENERATING: {msg}")
            time.sleep(1)
            msg = msg
            # send the message to the next stage
            self.out_queue.put(msg)


class ProcessThread(Thread):
    def __init__(self, in_queue: Queue, out_queue: Queue) -> None:
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def process(self, msg) -> None:
        print(f"PROCESSING: {msg}")
        time.sleep(2)
        msg = msg * 2
        return msg

    def run(self) -> None:
        while True:
            # get the message from the previous stage.
            msg = self.in_queue.get()
            # process the message
            out = self.process(msg)
            # send message to next stage
            self.out_queue.put(out)


class ConsumeThread(Thread):
    def __init__(self, in_queue: Queue) -> None:
        super().__init__()
        self.in_queue = in_queue

    def consume(self, msg: str) -> None:
        time.sleep(1)
        print(f"RECEIVED: {msg}")

    def run(self) -> None:
        while True:
            # get the message from the previous stage
            msg = self.in_queue.get()
            # consume the message
            self.consume(msg)


class Pipeline:
    def run_parallel(self) -> None:
        queues = [Queue() for _ in range(2)]
        threads = [
            ProduceThread(queues[0]),
            ProcessThread(queues[0], queues[1]),
            ConsumeThread(queues[1])
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run_parallel()
