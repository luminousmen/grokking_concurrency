#!/usr/bin/env python3

"""Non-blocking single threaded echo server implementation using asyncio
library"""

import asyncio
import socket

from asynchronous_pizza_joint import Kitchen

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)


class Server:
    def __init__(self, loop):
        self.loop = loop
        # AF_UNIX and SOCK_STREAM are constants represent the protocol and
        # socket type respectively here we create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # set socket to non-blocking mode
            self.server_socket.setblocking(False)
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

    async def start(self):
        try:
            while True:
                conn, addr = await self.loop.sock_accept(self.server_socket)
                self.loop.create_task(self.serve(conn))
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    async def serve(self, conn):
        try:
            while True:
                data = await self.loop.sock_recv(conn, BUFFER_SIZE)
                if not data:
                    break
                result = await self.loop.run_in_executor(None, Kitchen.cook_pizza, (int(data)))
                await self.loop.sock_send(conn, f"{result}\n".encode())
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
