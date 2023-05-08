#!/usr/bin/env python3.9

"""Coroutine implementation and usage"""

from collections import deque
import typing as T

# there is a similar type in collections.abc
Coroutine = T.Generator[None, None, int]


class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()

    def add_coroutine(self, task: Coroutine) -> None:
        """ Add a task to the queue. """
        self.tasks.append(task)

    def run_coroutine(self, task: Coroutine) -> None:
        try:
            task.send(None)
            self.add_coroutine(task)
        except StopIteration:
            print("Task completed")

    def run_forever(self) -> None:
        """ Run the loop until no more tasks exist in the queue. """
        while self.tasks:
            print("Event loop cycle.")
            self.run_coroutine(self.tasks.popleft())


def fibonacci(n: int) -> Coroutine:
    """ Generating fibonacci sequence as a non-recursive
    awaitable task (coroutine) """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        # yield control back to the event loop
        yield
    return a


if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(fibonacci(5))
    event_loop.run_forever()
