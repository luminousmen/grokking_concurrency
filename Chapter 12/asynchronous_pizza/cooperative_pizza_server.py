#!/usr/bin/env python3

"""Cooperative pizza server"""

import socket
from typing import NoReturn

from async_socket import AsyncSocket
from event_loop import EventLoop

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    def __init__(self, loop) -> None:
        self.loop = loop
        self.server_socket = AsyncSocket(
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM), loop=loop)
        # allows multiple sockets to be bound to an identical socket address
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            print(f"Starting up on: {ADDRESS}")
            # bind a socket to a specific network interface and port number
            self.server_socket.bind(ADDRESS)
            print("Listen for incoming connections")
            # on server side let"s start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
            self.server_socket.setblocking(False)
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")
        self.loop.add_coroutine(self.serve_forever())

    async def serve_forever(self) -> NoReturn:
        try:
            while True:
                conn, address = await self.server_socket.accept()
                print(f"Connected to {address}")
                self.loop.add_coroutine(self.serve(conn))
        finally:
            self.server_socket.close()
            print("\nServer stopped.")

    async def serve(self, conn) -> None:
        try:
            while True:
                data = await conn.recv(BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!\n"
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # send a response
                await conn.send(response.encode())
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    loop = EventLoop()
    server = Server(loop=loop)
    loop.run_forever()
