"""Event loop implementation with futures, coroutines and ThreadPool"""

import socket
from collections import deque
from multiprocessing.pool import ThreadPool
import typing as T
import select

from future import Future

Data = bytes
Action = T.Callable[[socket, T.Any], None]
Mask = int  # selectors constants EVENT_READ & EVENT_WRITE

BUFFER_SIZE = 1024


class Executor:
    def __init__(self):
        self.pool = ThreadPool()

    def execute(self, func, *args):
        future_notify, future_event = socket.socketpair()
        future_event.setblocking(False)

        def _execute():
            result = func(*args)
            future_notify.send(result.encode())

        self.pool.apply_async(_execute)
        return future_event


class EventLoop:
    def __init__(self):
        self._numtasks = 0
        self._ready = deque()
        self._read_waiting = {}
        self._write_waiting = {}
        self.executor = Executor()

    def register_event(self, source: socket.socket, event: Mask, future,
                       task: Action) -> None:
        key = source.fileno()
        if event & select.POLLIN:
            self._read_waiting[key] = (future, task)
        elif event & select.POLLOUT:
            self._write_waiting[key] = (future, task)

    def add_coroutine(self, task: T.Generator) -> None:
        self._ready.append((task, None))
        self._numtasks += 1

    def add_ready(self, task: T.Generator, msg=None):
        self._ready.append((task, msg))

    def run_coroutine(self, task: T.Generator, msg) -> None:
        try:
            # run the coroutine to the next yield
            future = task.send(msg)
            future.coroutine(self, task)
        except StopIteration:
            self._numtasks -= 1

    def run_in_executor(self, func, *args) -> Future:
        future_event = self.executor.execute(func, *args)
        future = Future()

        def handle_yield(loop, task):
            try:
                data = future_event.recv(BUFFER_SIZE)
                loop.add_ready(task, data)
            except BlockingIOError:
                loop.register_event(
                    future_event, select.POLLIN, future, task)

        future.set_coroutine(handle_yield)
        return future

    def run_forever(self) -> None:
        while self._numtasks:
            if not self._ready:
                readers, writers, _ = select.select(
                    self._read_waiting, self._write_waiting, [])
                for reader in readers:
                    future, task = self._read_waiting.pop(reader)
                    future.coroutine(self, task)

                for writer in writers:
                    future, task = self._write_waiting.pop(writer)
                    future.coroutine(self, task)

            task, msg = self._ready.popleft()
            self.run_coroutine(task, msg)
