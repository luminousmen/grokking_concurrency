#!/usr/bin/env python3

"""Simple single threaded event loop implementation"""

# Allow forward references in type hints (Python>=3.7)
from __future__ import annotations

from collections import deque
from time import sleep
import typing as T


class Event:
    def __init__(self, name: str, action: T.Callable[..., None],
                 next_event: T.Optional[Event] = None) -> None:
        self.name = name
        self._action = action
        self._next_event = next_event

    def execute_action(self) -> None:
        self._action(self)
        if self._next_event:
            event_loop.register_event(self._next_event)


class EventLoop:
    """ Maintains a deque of Events and executes them. """

    def __init__(self) -> None:
        # internal event queue
        self._events: deque[Event] = deque()

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def run_forever(self) -> T.NoReturn:
        print(f"Queue running with {len(self._events)} events")
        while True:   # busy-waiting
            # execute the action of the next event
            try:
                event = self._events.popleft()
            except IndexError:
                continue
            event.execute_action()


def knock(event: Event) -> None:
    print(event.name)
    sleep(1)


def who(event: Event) -> None:
    print(event.name)
    sleep(1)


if __name__ == "__main__":
    event_loop = EventLoop()
    # A callback which simply does an action.
    replying = Event("Who's there?", who)
    # A callback which does an action and adds another Event to the deque.
    knocking = Event("Knock-knock", knock, replying)
    # adding several _events
    for _ in range(2):
        event_loop.register_event(knocking)
    event_loop.run_forever()
