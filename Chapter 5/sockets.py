#!/usr/bin/env python3.9

""" Using sockets for IPC """

import socket
import os.path
import time
from threading import Thread, current_thread

# in Unix everything is a file
SOCK_FILE = "./mailbox"
BUFFER_SIZE = 1024


class Sender(Thread):
    def run(self) -> None:
        self.name = "Sender"
        # AF_UNIX (Unix domain socket) and SOCK_STREAM are constants
        # that represent the socket family and socket type respectively
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCK_FILE)

        messages = ["Hello", " ", "world!"]
        for msg in messages:
            print(f"{current_thread().name}: Send: '{msg}'")
            client.sendall(str.encode(msg))

        client.close()


class Receiver(Thread):
    def run(self) -> None:
        self.name = "Receiver"
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # bind socket to the file
        server.bind(SOCK_FILE)
        # let's start listening mode for this socket
        server.listen()

        print(f"{current_thread().name}: Listening for incoming messages...")
        # accept a connection
        conn, addr = server.accept()

        while True:
            # receive data from socket
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            message = data.decode()
            print(f"{current_thread().name}: Received: '{message}'")

        server.close()


def main() -> None:
    # verify if exists the sock file
    if os.path.exists(SOCK_FILE):
        os.remove(SOCK_FILE)

    # receiver will create a socket and socket file
    receiver = Receiver()
    receiver.start()
    # waiting untill the socket has been created
    time.sleep(1)
    sender = Sender()
    sender.start()

    # block the main thread until the child threads has finished
    for thread in [receiver, sender]:
        thread.join()

    # cleaning up
    os.remove(SOCK_FILE)


if __name__ == "__main__":
    main()
