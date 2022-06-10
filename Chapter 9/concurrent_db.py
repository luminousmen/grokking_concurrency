import json
import os
from threading import Lock


class FileDB(object):
    def __init__(self, location):
        self.read_lock = Lock()
        self.location = os.path.expanduser(location)

    def get(self, key: str):
        # reader lock
        pass

    def insert(self, key: str, data: dict):
        # writer lock
        pass

    def delete(self, key: str):
        # writer lock
        pass

    def search(self, query: str):
        # concurrent search
        pass

    def start(self):
        # interface in a separate thread
        pass


if __name__ == "__main__":
    db = FileDB()
    db.start()
