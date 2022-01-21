#!/usr/bin/env python3
"""Implementing the game program using threads without multitasking using blocking thread"""
import time
import sys, select
from threading import Thread


class Task(Thread):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def run(self):
        while True:
            self.func()


def get_user_input():
    # getting the next user input
    i, o, e = select.select([sys.stdin], [], [], 1)
    if i:
        user_input = sys.stdin.readline().strip()
        print(f"user input: {user_input}\n")
        return user_input


def compute_game_world():
    # computing the internal game world
    print("computing")
    time.sleep(0.5)


def render_next_screen():
    # rendering the next screen of the program
    print("rendering\n")
    time.sleep(0.5)


if __name__ == "__main__":
    getUserInputTask = Task(get_user_input)
    computeGameWorldTask = Task(compute_game_world)
    renderNextScreenTask = Task(render_next_screen)

    getUserInputTask.run()
    computeGameWorldTask.run()
    renderNextScreenTask.run()
