#!/usr/bin/env python3

"""Implementing the game program using threads utilizing multitasking with time sharing"""

import itertools
import collections
import typing as T
from threading import Thread, Event

from stopwatch import Stopwatch
from pacman import get_user_input, compute_game_world, render_next_screen

TIME_SLICE = 5  # seconds


class Task(Thread):
    def __init__(self, func: T.Callable[[], None]) -> None:
        super().__init__()
        self.paused = True  # Start out paused.
        self.func = func
        self._event = Event()

    def run(self) -> None:
        # emulate OS blocking behaviour using events
        self.resume()
        while True:
            self._event.wait()
            self.func()

    def pause(self) -> None:
        self._event.clear()

    def resume(self) -> None:
        self._event.set()


def arcade_machine() -> None:
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)
    tasks = [get_user_input_task, compute_game_world_task, render_next_screen_task]
    stopwatch = Stopwatch()

    count = itertools.count()
    queue = collections.deque()
    for task in tasks:
        queue.append((next(count), task))

    while True:
        # get next task from queue
        _, task = queue.popleft()
        stopwatch.start()
        print(f"Running {task} for {TIME_SLICE} seconds...")
        if not task.is_alive():
            task.start()

        while stopwatch.elapsed_time < TIME_SLICE:
            task.resume()

        task.pause()
        queue.append((next(count), task))


if __name__ == "__main__":
    arcade_machine()
