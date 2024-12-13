#!/usr/bin/env python3.9

"""Implementing the game program using threads without multitasking using
blocking threads """

import typing as T
from threading import Thread, Event

from pacman import get_user_input, compute_game_world, render_next_screen

processor_free = Event()
processor_free.set()

class Task(Thread):
    def __init__(self, func: T.Callable[..., None]):
        super().__init__()
        self.func = func

    def run(self) -> None:
        while True:
            processor_free.wait()  # block until signalled
            processor_free.clear()  # don't let other tasks resume
            self.func()
            processor_free.set()


def arcade_machine() -> None:
    """The main function that implements arcade machine functionality"""
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)

    get_user_input_task.start()
    compute_game_world_task.start()
    render_next_screen_task.start()


if __name__ == "__main__":
    arcade_machine()
