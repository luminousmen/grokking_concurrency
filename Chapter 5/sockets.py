#!/usr/bin/env python3

""" Using sockets for IPC """

import socket
import os.path
from multiprocessing import Process

# in Unix everything is a file
SOCK_FILE = "./mailbox"


def send():
    # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
    # conn = is a new socket object usable to send and receive data on the connection
    # addr = is the address bound to the socket *on the other* end of connection
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCK_FILE)

    messages = [b"Hello", b" ", b"world!"]
    for msg in messages:
        print(f"Send: {msg}")
        client.send(msg)

    client.close()


def receive():
    # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
    # conn = is a new socket object usable to send and receive data on the connection
    # addr = is the address bound to the socket *on the other* end of connection
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # bind to the socket file
    server.bind(SOCK_FILE)
    server.listen()
    
    print("Listening of incoming messages...")
    # accept a connection
    conn, addr = server.accept()

    while True:
        # receive data from socket
        data = conn.recv(1024)
        if not data:
            break
        else:
            print(f"Received: {data}")
            if "end" == data:
                break
    
    server.close()


def main() -> None:
    # verify if exists the sock file
    if os.path.exists(SOCK_FILE):
        os.remove(SOCK_FILE)

    receiver = Process(target=receive)
    sender = Process(target=send)

    processes = [
        receiver,
        sender,
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    # cleaning up
    os.remove(SOCK_FILE)


if __name__ == "__main__":
    main()
