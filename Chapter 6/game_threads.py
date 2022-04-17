#!/usr/bin/env python3

"""Implementing the game program using threads without multitasking using blocking thread"""
import sys
import time
import select
from threading import Thread


class Task(Thread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        while True:
            self.func()


def get_user_input() -> str:
    # getting the next user input
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        user_input = sys.stdin.readline().strip()
        print(f"user input: {user_input}\n")
        return user_input


def compute_game_world() -> None:
    # computing the internal game world
    print("computing")
    time.sleep(0.5)


def render_next_screen() -> None:
    # rendering the next screen of the program
    print("rendering\n")
    time.sleep(0.5)


def arcade_machine() -> None:
    get_user_input_task = Task(get_user_input)
    compute_game_world_task = Task(compute_game_world)
    render_next_screen_task = Task(render_next_screen)

    get_user_input_task.run()
    compute_game_world_task.run()
    render_next_screen_task.run()


if __name__ == "__main__":
    arcade_machine()
