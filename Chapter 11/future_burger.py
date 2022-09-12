#!/usr/bin/env python3

from typing import Coroutine, Any
from random import randint


class Future:
    def __init__(self):
        self.done = False
        self.result = None
        self.coroutine = None

    def set_coroutine(self, coroutine) -> None:
        self.coroutine = coroutine

    def set_result(self, result: Any) -> None:
        self.done = True
        self.result = result

    def __await__(self):
        if not self.done:
            yield self
        return self.result


async def cook() -> Future:
    f = Future()

    def on_callback():
        burger = f"Burger #{randint(1, 10)}"
        print(f"{burger} is cooked!")
        f.set_result(burger)

    on_callback()
    c = await f
    return c


async def cashier(burger: Future) -> Future:
    f = Future()

    def on_callback():
        print("Burger is ready for pick up!")
        f.set_result(burger)

    on_callback()
    c = await f
    return c


async def order_burger() -> Future:
    burger = await cook()
    burger = await cashier(burger)
    return burger


def run_coroutine(coroutine: Coroutine) -> None:
    try:
        future = coroutine.send(None)
        future.set_coroutine(coroutine)
    except StopIteration as e:
        print(f"{e.value}? That's me! Mmmmmm!")


if __name__ == "__main__":
    run_coroutine(order_burger())
