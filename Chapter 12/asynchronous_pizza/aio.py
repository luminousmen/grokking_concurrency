#!/usr/bin/env python3

"""Non-blocking single threaded echo server implementation using asyncio
library"""

import asyncio
import socket

from asynchronous_pizza_joint import Kitchen

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class Server:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        # AF_UNIX and SOCK_STREAM are constants represent the protocol and
        # socket type respectively here we create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # set socket to non-blocking mode
            self.server_socket.setblocking(False)
            print(f"Starting up on: {ADDRESS}")
            # bind a socket to a specific network interface and port number
            self.server_socket.bind(ADDRESS)
            print("Listen for incoming connections")
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    async def start(self) -> None:
        try:
            while True:
                conn, addr = await self.loop.sock_accept(self.server_socket)
                self.loop.create_task(self.serve(conn))
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    async def serve(self, conn) -> None:
        try:
            while True:
                data = await self.loop.sock_recv(conn, BUFFER_SIZE)
                if not data:
                    break
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas!"
                    print(f"Sending message to {conn.getpeername()}")
                    await self.loop.sock_sendall(conn, f"{response}".encode())
                    await self.loop.run_in_executor(None, Kitchen.cook_pizza, order)
                    print(f"Sending message to {conn.getpeername()}")
                    await self.loop.sock_sendall(
                        conn,
                        f"You order on {order} pizzas is ready!".encode())
                except ValueError:
                    response = "Wrong number of pizzas, please try again\n"
                    print(f"Sending message to {conn.getpeername()}")
                    await conn.send(response.encode())
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
        except Exception:
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
            self.server_socket.close()
            print("\nServer stopped.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = Server(loop)
    loop.create_task(server.start())
    loop.run_forever()
    loop.close()
