#!/usr/bin/env python3

"""Implementing the game program using threads utilizing multitasking with
time sharing """

import typing as T
from threading import Thread, Timer, Event
from sys import setswitchinterval

from pacman import get_user_input, compute_game_world, render_next_screen

GLOBAL_FLAG = Event()
GLOBAL_FLAG.set()

TIME_SLICE = 5  # seconds


class Task(Thread):
    """ A Thread running a given pacman function repeatedly
        while blocking to await a global flag.
    """
    def __init__(self, func: T.Callable[..., None]):
        super().__init__(daemon=True)   # so that it is closed at end
        self.func = func

    def run(self) -> None:
        # emulate OS blocking behaviour using GLOBAL_FLAGs
        while True:
            print(f"{self.name} waiting to run `{self.func.__name__}`")
            GLOBAL_FLAG.wait()   # block until signalled
            # due to GIL only one task will see the flag has been set
            GLOBAL_FLAG.clear()  # don't let other tasks resume
            print(f"Running `{self.func.__name__}`")
            self.func()


class RepeatTimer(Timer):
    """ Calls the given function repeatedly at specified intervals."""
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def clock_tick():
    """ Sets the Global Flag to allow a waiting Task to run. """
    print("------Tick------")
    GLOBAL_FLAG.set()  # on tick signal waiting Tasks


def arcade_machine() -> None:
    """The main function that implements arcade machine functionality"""
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)
    tasks = [get_user_input_task,
             compute_game_world_task, render_next_screen_task]
    RepeatTimer(TIME_SLICE, clock_tick).start()
    for task in tasks:
        task.start()


if __name__ == "__main__":
    setswitchinterval(100)   # turn off python's own thread time sharing
    arcade_machine()
