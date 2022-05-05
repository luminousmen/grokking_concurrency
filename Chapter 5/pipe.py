#!/usr/bin/env python3

""" Using pipes for IPC """

import os
from multiprocessing import Process


def write(conn: int) -> None:
    # opening stream for writing
    w = os.fdopen(conn, "w")
    print(f"PID({os.getpid()}): Sending rubber duck...")
    w.write("Rubber duck")
    # close the writer file descriptor
    w.close()


def read(conn: int) -> None:
    # opening stream for reading
    r = os.fdopen(conn)
    print(f"PID({os.getpid()}): Reading...")
    # reading 11 bytes ~ 11 char symbols - just enough to get a "rubber duck"
    msg = r.read(11)
    print(f"PID({os.getpid()}): Received: {msg}")


def main() -> None:
    # file descriptors for reading and writing
    reader_conn, writer_conn = os.pipe()
    reader = Process(target=read, args=(reader_conn,))
    writer = Process(target=write, args=(writer_conn,))

    processes = [
        writer,
        reader
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
