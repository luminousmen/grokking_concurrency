#!/usr/bin/env python3

"""Forking child processes in Python"""

import os


def run_child() -> None:
    """Running some logic inside child process"""
    print("Child: I am the child process")
    print(f"Child: Child’s PID: {os.getpid()}")
    print(f"Child: Parent’s PID: {os.getppid()}")
    # stopping the child process to not waste resources
    os._exit(0)


def start_parent(num_children: int) -> None:
    """Forking the current process"""
    for i in range(num_children):
        newpid = os.fork()
        if newpid == 0:
            run_child()
        else:
            # PID of the parent process should remain the same
            print("Parent : I am the parent process")
            print(f"Parent : Parent’s PID: {os.getpid()}")
            print(f"Parent : Child’s PID: {newpid}")


if __name__ == "__main__":
    num_children = 3
    start_parent(num_children)
