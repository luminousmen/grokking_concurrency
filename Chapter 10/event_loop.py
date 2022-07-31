#!/usr/bin/env python3

"""Simple single threaded event loop implementation"""

import time
from collections import deque


class EventLoop:
    def __init__(self):
        # internal task queue
        self.events = deque()
        self.callbacks = {}

    def register_event(self, event, callback):
        self.callbacks[event] = callback

    def run_forever(self):
        # running the loop forever
        while True:
            # execute the ready tasks
            while self.events:
                event = self.events.popleft()
                callback = self.callbacks[event]
                callback(event)


def knock(event):
    print("Knock, knock.")
    time.sleep(1)
    # adding a next task into the event loop task queue
    event_loop.events.append("who")


def who(event):
    print("Who's there?")
    time.sleep(2)


if __name__ == "__main__":
    event_loop = EventLoop()
    event_loop.register_event("knock", knock)
    event_loop.register_event("who", who)
    # adding several events
    for _ in range(2):
        event_loop.events.append("knock")
    event_loop.run_forever()
