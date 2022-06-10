"""Don"t mind it - just upgrading a mutex with additional attribute to make examples more explicit"""

from threading import Lock


class LockWithName:
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.lock = Lock()
