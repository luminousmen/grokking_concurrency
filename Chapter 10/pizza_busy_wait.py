#!/usr/bin/env python3

"""Busy-waiting non-blocking server implementation"""

import typing as T
from socket import socket, create_server

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    clients: T.Set[socket] = set()

    def __init__(self) -> None:
        try:
            print(f"Starting up at: {ADDRESS}")
            self.server_socket = create_server(ADDRESS)
            # set socket to non-blocking mode
            self.server_socket.setblocking(False)
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def accept(self) -> None:
        try:
            # accepting the incoming connection
            # conn = is a new socket object usable to send and receive data on the
            # connection
            # addr = is the address bound to the socket on the other end of connection
            conn, address = self.server_socket.accept()
            print(f"Connected to {address}")
            # making this connection non-blocking
            conn.setblocking(False)
            self.clients.add(conn)
        except BlockingIOError:
            # [Errno 35] Resource temporarily unavailable
            # indicates that "accept" returned without results
            pass

    def serve(self, conn: socket) -> None:
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # send a response
                conn.send(response.encode())
        except BlockingIOError:
            # recv/send returns without data
            pass

    def start(self) -> None:
        try:
            print("Server listening for incoming connections")
            while True:
                self.accept()
                for conn in self.clients.copy():
                    self.serve(conn)
        finally:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    server = Server()
    server.start()
