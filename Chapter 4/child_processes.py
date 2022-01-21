#!/usr/bin/env python3
"""Forking child processes in Python"""
import os


def child():
    print("Hello from child",  os.getpid())
    os._exit(0)


def parent():
    for i in range(5):
        newpid = os.fork()
        if newpid == 0:
            child()
        else:
            print("Hello from parent", os.getpid(), newpid)


if __name__ == "__main__":
    parent()
