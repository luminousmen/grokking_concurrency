#!/usr/bin/env python3

"""Cooperative pizza server"""

import socket

from async_socket import AsyncSocket
from event_loop import EventLoop

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    def __init__(self, event_loop: EventLoop):
        self.event_loop = event_loop
        print(f"Starting up on: {ADDRESS}")
        self.server_socket = AsyncSocket(socket.create_server(ADDRESS))
        self.event_loop.add_coroutine(self.serve_forever())

    def serve_forever(self):
        print("Server listening for incoming connections")
        try:
            while True:
                conn, address = yield self.server_socket.accept()
                print(f"Connected to {address}")
                self.event_loop.add_coroutine(self.serve(AsyncSocket(conn)))
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    def serve(self, conn: AsyncSocket):
        while True:
            data = yield conn.recv(BUFFER_SIZE)
            if not data:
                break

            try:
                order = int(data.decode())
                response = f"Thank you for ordering {order} pizzas!\n"
            except ValueError:
                response = "Wrong number of pizzas, please try again\n"

            print(f"Sending message to {conn.getpeername()}")
            # yield loop.run_in_executor(Kitchen.cook_pizza, 20)
            yield conn.send(response.encode())
        print(f"Connection with {conn.getpeername()} has been closed")
        conn.close()


if __name__ == "__main__":
    loop = EventLoop()
    server = Server(event_loop=loop)
    loop.run_forever()
