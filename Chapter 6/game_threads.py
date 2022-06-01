#!/usr/bin/env python3

"""Implementing the game program using threads without multitasking using blocking thread"""
from threading import Thread
import typing as T

from pacman import get_user_input, compute_game_world, render_next_screen


class Task(Thread):
    def __init__(self, func: T.Callable[[], None]):
        super().__init__()
        self.func = func

    def run(self) -> None:
        while True:
            self.func()


def arcade_machine() -> None:
    """The main function that implements arcade machine functionality"""
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)

    get_user_input_task.run()
    compute_game_world_task.run()
    render_next_screen_task.run()


if __name__ == "__main__":
    arcade_machine()
