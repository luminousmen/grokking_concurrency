""""""

import selectors
from collections import deque
from future import Future

BUFFER_SIZE = 1024


class EventLoop:
    def __init__(self):
        self.event_notifier = selectors.DefaultSelector()
        self.tasks = deque()
        self.handlers = {}

    def create_future(self):
        return Future(loop=self)

    def create_future_for_events(self, sock, events):
        future = self.create_future()

        def handler(sock, active_events):
            self.unregister_event(sock)
            future.set_result(active_events)

        self.register_event(sock, events, handler)
        return future

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
