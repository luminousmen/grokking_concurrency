#!/usr/bin/env python3

""" Using pipes for IPC """

import os
from threading import Thread, current_thread


class Writer(Thread):
    """Writer thread will write messages into the pipe"""
    def __init__(self, conn: int):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        # opening stream for writing
        pipe = os.fdopen(self.conn, "w")
        print(f"Thread({current_thread().ident}): Sending rubber duck...")
        pipe.write("Rubber duck")
        # close the writer file descriptor
        pipe.close()


class Reader(Thread):
    """Writer thread will write messages into the pipe"""
    def __init__(self, conn: int):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        # opening stream for reading
        pipe = os.fdopen(self.conn)
        print(f"Thread({current_thread().ident}): Reading...")
        # reading 11 bytes ~ 11 char symbols - just enough to get a "rubber duck"
        msg = pipe.readline()
        print(f"Thread({current_thread().ident}): Received: {msg}")


def main() -> None:
    # file descriptors for reading and writing
    reader_conn, writer_conn = os.pipe()
    reader = Reader(reader_conn)
    writer = Writer(writer_conn)

    threads = [
        writer,
        reader
    ]
    # start threads
    for thread in threads:
        thread.start()

    # block the main thread until the child threads has finished
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
