#!/usr/bin/env python3.9

"""Threaded echo server implementation"""

from socket import socket, create_server
from threading import Thread

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Handler(Thread):
    def __init__(self, conn: socket):
        super().__init__()
        self.conn = conn

    def run(self) -> None:
        """Serve the incoming connection in a thread by sending and
        receiving data."""
        print(f"Connected to {self.conn.getpeername()}")
        try:
            while True:
                data = self.conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {self.conn.getpeername()}")
                # send a response
                self.conn.send(response.encode())
        finally:
            # server expects the client to close its side of the connection
            # when it’s done. In a real application, we should use timeout for
            # clients if they don’t send a request after a certain amount of time.
            # a request after a certain amount of time.
            print(f"Connection with {self.conn.getpeername()} "
                  f"has been closed")
            self.conn.close()


class Server:
    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket = create_server(ADDRESS)
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def start(self) -> None:
        """Start the server by continuously accepting and serving incoming
        connections."""
        print("Server listening for incoming connections")
        try:
            while True:
                conn, address = self.server_socket.accept()
                print(f"Client connection request from {address}")
                thread = Handler(conn)
                thread.start()
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
