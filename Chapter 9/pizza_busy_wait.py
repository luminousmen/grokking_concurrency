#!/usr/bin/env python3

"""Non-blocking single threaded pizza server implementation using busy-wait"""

import socket

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)


class Server:
    clients = set()

    def __init__(self):
        # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
        # here we create a TCP/IP socket
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

    def accept(self) -> None:
        try:
            # accepting the incoming connection
            # conn = is a new socket object usable to send and receive data on the
            # connection
            # addr = is the address bound to the socket on the other end of connection
            conn, address = self.server_socket.accept()
            # making this connection non-blocking
            conn.setblocking(False)
            self.clients.add(conn)
            print(f"Connected to {address}")
        except BlockingIOError:
            # [Errno 35] Resource temporarily unavailable
            # indicates that "accept" returned without results
            pass

    def serve(self, conn: socket) -> None:
        try:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                self.clients.remove(conn)
                print(f"Connection with {conn.getpeername()} has been closed")
                conn.close()
            else:
                try:
                    order = int(data.decode())
                    response = f"Thank you for ordering {order} pizzas\n"
                except ValueError:
                    response = "Wrong number of orders, please try again\n"
                print(f"Sending message to {conn.getpeername()}")
                # send a response
                conn.send(response.encode())
                # Note: recommended way is to use .sendall(),
                # but we will stick with send to keep reader's mental model
        except BlockingIOError:
            # recv/send returns without data
            pass

    def start(self):
        try:
            # infinite polling cycle
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
