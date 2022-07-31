#!/usr/bin/env python3

"""Implementation of event-based concurrency using Reactor pattern"""

import selectors
import socket

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)


class EventLoop:
    def __init__(self):
        # Python library offers us two modules that support synchronous I/O multiplexing:
        # select and selectors. select is more low level and expose you to the specific
        # select-family syscalls, selectors is a higher level module that choose the best
        # implementation on your system, roughly epoll|kqueue|devpoll > poll > select
        self.event_notifier = selectors.DefaultSelector()

    def register_event(self, socket, event, callback):
        try:
            self.event_notifier.get_key(socket)
        except KeyError:
            self.event_notifier.register(socket, event, callback)
        else:
            self.event_notifier.modify(socket, event | event, callback)

    def run_forever(self):
        while True:
            # .select() blocks until there are sockets ready for I/O.
            events = self.event_notifier.select()
            for key, mask in events:
                # key.fileobj is a socket object, and the mask is the event mask of the operations
                # that are ready
                if mask == selectors.EVENT_READ:
                    # on_read or accept calls
                    callback = key.data
                    callback(key.fileobj)
                elif mask == selectors.EVENT_WRITE:
                    callback, msg = key.data
                    callback(key.fileobj, msg)
                else:
                    raise RuntimeError


class Server:
    def __init__(self, event_loop):
        self.event_loop = event_loop
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
            self.server_socket.setblocking(False)
        except Exception:
            self.server_socket.close()
            print("\nServer stopped.")

    def _on_accept(self, sock):
        # accepting the incoming connection, blocking
        # conn = is a new socket object usable to send and receive data on the connection
        # client_host, client_port = is the address bound to the socket
        # on the other end of connection
        conn, address = self.server_socket.accept()
        conn.setblocking(False)
        print(f"Connected to {address}")
        # future calls to the self.event_notifier.select() will be notified whether this socket
        # connection has any pending I/O events
        self.event_loop.register_event(conn, selectors.EVENT_READ, self._on_read)

    def _on_read(self, conn):
        data = conn.recv(BUFFER_SIZE)
        if data:
            message = data.decode()
            self.event_loop.register_event(conn, selectors.EVENT_WRITE, (self._on_write, message))
        else:
            self.event_loop.event_notifier.unregister(conn)
            conn.close()
            print(f"Connection with {conn.getpeername()} has been closed")

    def _on_write(self, conn, message):
        print(f"Sending a message to {conn.getpeername()}")
        # send a response
        conn.send(message.upper().encode())
        self.event_loop.register_event(conn, selectors.EVENT_READ, self._on_read)

    def start(self):
        # future calls to the self.event_notifier.select() will be notified whether this socket
        # has any pending accept events from the clients
        self.event_loop.register_event(self.server_socket, selectors.EVENT_READ, self._on_accept)


if __name__ == "__main__":
    event_loop = EventLoop()
    Server(event_loop).start()
    event_loop.run_forever()
