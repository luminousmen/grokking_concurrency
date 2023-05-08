#!/usr/bin/env python3.9
"""This module implements a simple burger ordering system using futures to
handle callbacks."""

# Allow forward references in type hints (Python>=3.7)
from __future__ import annotations

import typing as T
from collections import deque
from random import randint

Result = T.Any
Burger = Result
Coroutine = T.Callable[[], 'Future']


class Future:
    """A simple class representing a future result of an operation."""

    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None

    def set_coroutine(self, coroutine: Coroutine) -> None:
        self.coroutine = coroutine

    def set_result(self, result: Result) -> None:
        """Set the result of the operation."""
        self.done = True
        self.result = result

    def __iter__(self) -> Future:
        """Return self as an iterator."""
        return self

    def __next__(self) -> Result:
        if not self.done:
            raise StopIteration
        return self.result


class EventLoop:
    def __init__(self) -> None:
        self.tasks: T.Deque[Coroutine] = deque()

    def add_coroutine(self, coroutine: Coroutine) -> None:
        """ Add a task to the queue. """
        self.tasks.append(coroutine)

    def run_coroutine(self, task: T.Callable) -> None:
        future = task()
        future.set_coroutine(task)
        try:
            next(future)
            if not future.done:
                future.set_coroutine(task)
                self.add_coroutine(task)
        except StopIteration:
            return

    def run_forever(self) -> None:
        """ Run the loop until no more tasks exist in the queue. """
        while self.tasks:
            self.run_coroutine(self.tasks.popleft())


def cook(on_done: T.Callable[[Burger], None]) -> None:
    """Simulate cooking a burger."""
    burger: str = f"Burger #{randint(1, 10)}"
    print(f"{burger} is cooked!")
    on_done(burger)


def cashier(burger: Burger, on_done: T.Callable[[Burger], None]) -> None:
    """Simulate cashier"""
    print("Burger is ready for pick up!")
    on_done(burger)


def order_burger() -> Future:
    """Places an order for a burger."""
    order = Future()

    def on_cook_done(burger: Burger) -> None:
        cashier(burger, on_cashier_done)

    def on_cashier_done(burger: Burger) -> None:
        print(f"{burger}? That's me! Mmmmmm!")
        order.set_result(burger)

    cook(on_cook_done)
    return order


if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.add_coroutine(order_burger)
    event_loop.run_forever()
