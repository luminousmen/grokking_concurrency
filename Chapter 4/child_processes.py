#!/usr/bin/env python3.9

"""Forking child processes in Python"""

import os
from multiprocessing import Process


def run_child() -> None:
    """Running some logic inside child process"""
    print("Child: I am the child process")
    print(f"Child: Child’s PID: {os.getpid()}")
    print(f"Child: Parent’s PID: {os.getppid()}")


def start_parent(num_children: int) -> None:
    print("Parent : I am the parent process")
    print(f"Parent : Parent’s PID: {os.getpid()}")
    # spawning/forking new processes
    for i in range(num_children):
        print(f"Starting Process {i}")
        Process(target=run_child).start()


if __name__ == "__main__":
    num_children = 3
    start_parent(num_children)
