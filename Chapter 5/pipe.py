#!/usr/bin/env python3

""" Using pipes for IPC """

import os
from multiprocessing import Process


def send(conn):
    # opening stream for writing
    w = os.fdopen(conn, "w")
    print("Sending rubber duck...")
    w.write("Rubber duck")
    # close the writer file descriptor
    w.close()


def receive(conn):
    # opening stream for reading
    r = os.fdopen(conn)
    print("Reading...")
    # reading 11 bytes ~ 11 char symbols - just enough to get a "rubber duck"
    msg = r.read(11)
    print(f"Received: {msg}")


def main() -> None:
    # file descriptors for reading and writing
    receiver_conn, sender_conn = os.pipe()
    receiver = Process(target=receive, args=(receiver_conn,))
    sender = Process(target=send, args=(sender_conn,))

    processes = [
        sender,
        receiver
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()