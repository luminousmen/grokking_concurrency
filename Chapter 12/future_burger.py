#!/usr/bin/env python3
# Allow forward references in type hints (Python>=3.7)
from __future__ import annotations

from random import randint
from collections.abc import Coroutine
import typing as T


Result = T.Any
Burger = Result  # our Burger is a string!


class Future:
    def __init__(self) -> None:
        self.done = False
        self.coroutine = None
        self.result = None

    def set_coroutine(self, coroutine: Coroutine[T.Any, T.Any, Result]) -> None:
        self.coroutine = coroutine

    def set_result(self, result: Result) -> None:
        self.done = True
        self.result = result

    def __await__(self) -> T.Generator[Future, None, Result]:
        if not self.done:
            yield self
        return self.result


async def cook() -> Burger:
    order = Future()

    def on_callback() -> None:   # Locally defined function
        burger: str = f"Burger #{randint(1, 10)}"
        print(f"{burger} is cooked!")
        order.set_result(burger)

    on_callback()
    cooked_burger = await order
    return cooked_burger


async def cashier(burger: Burger) -> Burger:
    ready = Future()

    def on_callback() -> None:
        print("Burger is ready for pick up!")
        ready.set_result(burger)

    on_callback()
    ordered_burger = await ready
    return ordered_burger


async def order_burger() -> Burger:
    burger = await cook()
    burger = await cashier(burger)
    return burger


def run_coroutine(coroutine: Coroutine[T.Any, T.Any, Result]) -> None:
    try:
        future = coroutine.send(None)
        future.set_coroutine(coroutine)
    except StopIteration as exc:
        print(f"{exc.value}? That's me! Mmmmmm!")


if __name__ == "__main__":
    run_coroutine(order_burger())
