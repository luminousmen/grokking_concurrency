"""Reader-writer lock: fair lock"""

from threading import Lock


class RWLockFair:
    def __init__(self):
        self.readers = 0
        # To achieve fairness and prevent starvation, we can use another mutex named that
        # will materialize the order of arrived events (read or write). This semaphore will be taken
        # by any entity that requests access to the resource, and released as soon as this entity
        # gains access to the resource
        self.order_lock = Lock()
        self.read_lock = Lock()
        self.write_lock = Lock()

    def acquire_read(self):
        self.order_lock.acquire()
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1:
            self.write_lock.acquire()
        self.order_lock.release()
        self.read_lock.release()

    def release_read(self):
        assert self.readers >= 1
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.write_lock.release()
        self.read_lock.release()

    def acquire_write(self):
        self.order_lock.acquire()
        self.write_lock.acquire()
        self.order_lock.release()

    def release_write(self):
        self.write_lock.release()

