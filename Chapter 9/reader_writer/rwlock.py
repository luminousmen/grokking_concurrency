"""Reader-writer lock: readers have priority"""

from threading import Lock


class RWLock:
    """    A read-write lock that allows multiple readers or one
    writer at a time."""
    def __init__(self) -> None:
        self.readers = 0
        self.read_lock = Lock()
        self.write_lock = Lock()

    def acquire_read(self) -> None:
        """Acquires the read lock for the current thread.
        If there is a writer waiting for the lock, the method blocks until
        the writer releases the lock."""
        self.read_lock.acquire()
        self.readers += 1
        if self.readers == 1:
            self.write_lock.acquire()
        self.read_lock.release()

    def release_read(self) -> None:
        """Releases the read lock held by the current thread.
        If there are no more readers holding the lock, the method releases
        the write lock."""
        assert self.readers >= 1
        self.read_lock.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.write_lock.release()
        self.read_lock.release()

    def acquire_write(self) -> None:
        """Acquires the write lock for the current thread.
        If there is a reader or a writer holding the lock, the method
        blocks until the lock is released."""
        self.write_lock.acquire()

    def release_write(self) -> None:
        """Releases the write lock held by the current thread."""
        self.write_lock.release()
