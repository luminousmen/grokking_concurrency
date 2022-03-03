#!/usr/bin/env python3
"""Forking child processes in Python"""
import os


def child():
    print(f"Hello from child PID: {os.getpid()}")
    os._exit(0)


def parent(num_children: int):
    for i in range(num_children):
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print(f"Hello from parent PID: {os.getpid()}, {newpid}")


if __name__ == "__main__":
    num_children = 5
    parent(num_children)
