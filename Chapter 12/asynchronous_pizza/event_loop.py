"""Event loop implementation with futures and coroutines"""

from selectors import DefaultSelector
from collections import deque
import typing as T
from socket import socket

from future import Future

Data = bytes
Action = T.Callable[[socket, T.Any], None]
Mask = int  # selectors constants EVENT_READ & EVENT_WRITE

BUFFER_SIZE = 1024


class EventLoop:
    def __init__(self) -> None:
        self.event_notifier = DefaultSelector()
        self.tasks: T.Deque[T.Coroutine[T.Any, T.Any, T.Any]] = deque()

    def register_event(self, source: socket, event: int, action: Action) -> None:
        try:
            self.event_notifier.register(source, event, action)
        except KeyError:  # already exists so modify
            self.event_notifier.modify(source, event, action)

    def unregister_event(self, source: socket) -> None:
        self.event_notifier.unregister(source)

    def create_future_for_events(self, sock: socket, events: Mask) -> Future:
        future = Future(loop=self)

        def handler(sock: socket, result: T.Any) -> None:
            self.unregister_event(sock)
            future.set_result(result)

        self.register_event(sock, events, handler)
        return future

    def add_coroutine(self, co: T.Coroutine[T.Any, T.Any, T.Any]) -> None:
        self.tasks.append(co)

    def run_coroutine(self, co: T.Coroutine[T.Any, T.Any, T.Any]) -> None:
        try:
            future = co.send(None)
            future.set_coroutine(co)
        except StopIteration:
            pass

    def run_forever(self) -> T.NoReturn:
        while True:
            while not self.tasks:
                try:
                    events = self.event_notifier.select()
                    for (source, _, _, action), _ in events:
                        action(source, events)
                except OSError:
                    pass

            while self.tasks:
                self.run_coroutine(co=self.tasks.popleft())
