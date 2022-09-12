#!/usr/bin/env python3

"""Coroutine implementation and usage"""

from typing import Coroutine
import asyncio
from collections import deque


class EventLoop:
    def __init__(self):
        self.tasks = deque()

    def add_coroutine(self, co: Coroutine) -> None:
        self.tasks.append(co)

    def run_coroutine(self, co: Coroutine) -> None:
        try:
            co.send(None)
            self.add_coroutine(co)
        except StopIteration as e:
            pass

    def run_forever(self) -> None:
        while self.tasks:
            print("Event loop cycle.")
            self.run_coroutine(co=self.tasks.popleft())


async def fibonacci(n: int):
    """Generating fibonacci sequence using native coroutines"""
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        print(f"Fibonacci({i}): {a}")
        # returns control to the event loop
        await asyncio.sleep(0)


if __name__ == "__main__":
    el = EventLoop()
    el.add_coroutine(fibonacci(5))
    el.run_forever()
