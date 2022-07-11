#!/usr/bin/env python3

"""
"""
import socket
import time
from threading import Thread

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)
FILENAME = "poem.txt"


class Handler(Thread):
    def __init__(self, conn, client_host, client_port):
        super().__init__()
        self.conn = conn
        self.address = f"{client_host}:{client_port}"

    def run(self) -> None:
        print(f"Connected to {self.address}")
        try:
            with open(FILENAME, "r") as f:
                for line in f:
                    print(f"Sending a line to {self.address}")
                    # send a response
                    self.conn.send(line.encode())
                    # Note: recommended way is to use .sendall(),
                    # but we will stick with send to keep reader's mental model
                    time.sleep(1)
        finally:
            # server expects the client to close its side of the connection when it’s done.
            # In a real application, we should use timeout for clients if they don’t send
            # a request after a certain amount of time.
            self.conn.close()
            print(f"Connection with {self.address} has been closed.")


if __name__ == "__main__":
    # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
    # here we create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allows multiple sockets to be bound to an identical socket address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        print(f"Starting up on: {HOST}:{PORT}")
        # bind a socket to a specific network interface and port number
        server_socket.bind((HOST, PORT))
        print("Listen for incoming connections")
        # on server side let's start listening mode for this socket
        server_socket.listen()
        print("Server started...")
        while True:
            # accepting the incoming connection, blocking
            # conn = is a new socket object usable to send and receive data on the connection
            # addr = is the address bound to the socket on the other end of connection
            conn, (client_host, client_port) = server_socket.accept()
            thread = Handler(conn=conn, client_host=client_host, client_port=client_port)
            thread.start()
    finally:
        server_socket.close()
        print("\nServer stopped.")
