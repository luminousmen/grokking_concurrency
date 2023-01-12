"""Don"t mind it - just upgrading a mutex
     with additional attribute
     to make examples more explicit."""

from threading import Lock
from typing import Any, Tuple


class LockWithName:
    """ A standard python lock but with name attribute added. """

    def __init__(self, name: str):
        self.name = name
        self._lock = Lock()

    def acquire(self) -> None:
        self._lock.acquire()

    def release(self) -> None:
        self._lock.release()

    def locked(self) -> bool:
        return self._lock.locked()

    def __enter__(self) -> None:
        """ Allows this to be used with context management. """
        self.acquire()

    def __exit__(self, *args: Tuple[Any]) -> None:
        """ Allows this to be used with context management. """
        self.release()
