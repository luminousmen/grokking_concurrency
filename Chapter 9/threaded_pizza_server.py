#!/usr/bin/env python3

"""Multithreaded echo server implementation"""

import socket
from threading import Thread

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)


class Handler(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        print(f"Connected to {self.conn.getpeername()}")
        try:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                except ValueError:
                    response = "Wrong number of orders, please try again\n"
                print(f"Sending message to {self.conn.getpeername()}")
                # send a response
                self.conn.send(response.encode())
                # Note: recommended way is to use .sendall(),
                # but we will stick with send to keep reader's mental model
        finally:
            # server expects the client to close its side of the connection when it’s done.
            # In a real application, we should use timeout for clients if they don’t send
            # a request after a certain amount of time.
            print(f"Connection with {self.conn.getpeername()} has been closed")
            self.conn.close()


class Server:
    def __init__(self):
        # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
        # here we create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # allows multiple sockets to be bound to an identical socket address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print(f"Starting up on: {HOST}:{PORT}")
            # bind a socket to a specific network interface and port number
            self.server_socket.bind((HOST, PORT))
            print("Listen for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self):
        # accepting the incoming connection, blocking
        # conn = is a new socket object usable to send and receive data on the connection
        # addr = is the address bound to the socket on the other end of connection
        conn, address = self.server_socket.accept()
        return conn

    def start(self):
        try:
            while True:
                conn = self.accept()
                thread = Handler(conn=conn)
                thread.start()
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
