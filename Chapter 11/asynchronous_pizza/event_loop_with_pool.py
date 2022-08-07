""""""

import selectors
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import socket
from future import Future

BUFFER_SIZE = 1024


class Executor:
    def __init__(self):
        self.pool = ThreadPoolExecutor()

    def execute(self, func, *args):
        future_notify, future_event = socket.socketpair()
        future_event.setblocking(False)

        def _execute():
            result = func(*args)
            future_notify.send(result.encode())
        self.pool.submit(_execute)
        return future_event


class EventLoop:
    def __init__(self):
        self.event_notifier = selectors.DefaultSelector()
        self.tasks = deque()
        self.handlers = {}
        self.executor = Executor()

    def create_future(self):
        return Future(loop=self)

    def create_future_for_events(self, sock, events):
        future = self.create_future()

        def handler(sock, active_events):
            self.unregister_event(sock)
            future.set_result(active_events)

        self.register_event(sock, events, handler)
        return future

    async def run_in_executor(self, func, *args):
        future_event = self.executor.execute(func, *args)
        while True:
            try:
                return future_event.recv(BUFFER_SIZE)
            except BlockingIOError:
                future = self.create_future_for_events(future_event, selectors.EVENT_READ)
                await future

    def register_event(self, sock, events, handler):
        self.handlers[sock] = handler
        self.event_notifier.register(sock, events, handler)

    def unregister_event(self, sock):
        self.event_notifier.unregister(sock)
        self.handlers.pop(sock)

    def add_coroutine(self, co):
        self.tasks.append(co)

    def run_coroutine(self, co):
        try:
            future = co.send(None)
            future.set_coroutine(co)
        except StopIteration as e:
            pass

    def run_forever(self):
        while True:
            while not self.tasks:
                events = self.event_notifier.select()
                for key, mask in events:
                    handler = self.handlers.get(key.fileobj)
                    if handler:
                        handler(key.fileobj, events)

            while self.tasks:
                self.run_coroutine(co=self.tasks.popleft())
