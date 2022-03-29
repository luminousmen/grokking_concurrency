#!/usr/bin/env python3

""" Using pipes for IPC """

import os
from multiprocessing import Process


def send_hello(conn):
    # opening stream for writing
    w = os.fdopen(conn, 'w')
    print("Sending hello...")
    w.write("Hello!")
    # close the writer file descriptor
    w.close()
    print("Child closing")


def get_hello(conn):
    # opening stream for reading
    r = os.fdopen(conn)
    print("Reading hello...")
    # reading 6 bytes ~ 6 char symbols - just enough to get hello
    msg = r.read(6)
    print(f"We got: {msg}")


if __name__ == '__main__':
    # file descriptors for reading and writing
    reader_conn, writer_conn = os.pipe()
    reader = Process(target=send_hello, args=(writer_conn,))
    writer = Process(target=get_hello, args=(reader_conn,))

    processes = [
        writer,
        reader
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()
