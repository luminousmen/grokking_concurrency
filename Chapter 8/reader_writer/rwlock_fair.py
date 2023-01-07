"""Reader-writer lock: fair lock"""

from threading import Lock
from rwlock import RWLock


class RWLockFair(RWLock):
    def __init__(self) -> None:
        super().__init__()
        # To achieve fairness and prevent starvation, we can use another mutex named that
        # will materialize the order of arrived events (read or write). This semaphore will be taken
        # by any entity that requests access to the resource, and released as soon as this entity
        # gains access to the resource
        self.order_lock = Lock()

    def acquire_read(self) -> None:
        with self.order_lock:
            super().acquire_read()

    def acquire_write(self) -> None:
        with self.order_lock:
            super().acquire_write()
