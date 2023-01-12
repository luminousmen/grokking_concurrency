#!/usr/bin/env python3

"""Implementation of event-based concurrency using Reactor pattern"""

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from socket import socket, create_server
import typing as T

Data = bytes
Action = T.Union[T.Callable[[socket], None],
               T.Tuple[T.Callable[[socket, Data], None], str]]

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine


class EventLoop:
    def __init__(self) -> None:
        # Python library offers us two modules that support synchronous
        # I/O multiplexing: select and selectors.
        # select is more low level and exposes you to the specific select-family
        # syscalls, selectors is a higher level module that choose the best
        # implementation on your system,
        # roughly epoll|kqueue|devpoll > poll > select
        self.event_notifier = DefaultSelector()

    def register_event(self, source: socket, event: int, action: Action) -> None:
        try:
            self.event_notifier.register(source, event, action)
        except KeyError:  # already exists so modify
            self.event_notifier.modify(source, event, action)

    def run_forever(self) -> T.NoReturn:
        while True:
            # .select() blocks until there are sockets ready for I/O.
            events = self.event_notifier.select()
            for (source, _, _, action), event in events:
                if event & EVENT_READ:
                    action(source)
                elif event & EVENT_WRITE:
                    action, msg = action   # separate callable and data
                    action(source, msg)
                else:
                    raise RuntimeError


class Server:
    def __init__(self, event_loop: EventLoop) -> None:
        self.event_loop = event_loop
        try:
            print(f"Starting up at: {ADDRESS}")
            # On POSIX platforms the SO_REUSEADDR socket option is set
            self.server_socket = create_server(ADDRESS)
            print("Listen for incoming connections")
            # Let's start listening mode for this socket
            self.server_socket.listen()
            print("Waiting for a connection")
            self.server_socket.setblocking(False)
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def _on_accept(self, conn: socket) -> None:
        # accepting the incoming connection, non-blocking
        # conn = is a new socket object usable to send and receive data on
        # the connection on the other end of connection
        conn, client_address = self.server_socket.accept()
        conn.setblocking(False)
        print(f"Connected to {client_address}")
        # future calls to the self.event_notifier.select() will be notified
        # whether this socket connection has any pending I/O events
        self.event_loop.register_event(conn, EVENT_READ, self._on_read)

    def _on_read(self, conn: socket) -> None:
        print(f"Message received from {conn.getpeername()}")
        data = conn.recv(BUFFER_SIZE)
        if data:
            message = data.decode()
            self.event_loop.register_event(
                conn, EVENT_WRITE, (self._on_write, message))
        else:
            self.event_loop.event_notifier.unregister(conn)
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()

    def _on_write(self, conn: socket, message: bytes) -> None:
        print(f"Sending a message to {conn.getpeername()}")
        try:
            order = int(message)
            response = f"Thank you for ordering {order} pizzas!\n"
        except ValueError:
            response = "Wrong number of pizzas, please try again\n"
        print(f"Sending message to {conn.getpeername()}")
        # send a response
        conn.send(response.encode())
        self.event_loop.register_event(conn, EVENT_READ, self._on_read)

    def start(self) -> None:
        # registering the server socket for the OS to monitor
        # Once register is done future calls to the self.event_notifier.select()
        # will be notified whether server socket has any pending accept events
        # from the clients
        self.event_loop.register_event(
            self.server_socket, EVENT_READ, self._on_accept)


if __name__ == "__main__":
    loop = EventLoop()
    Server(loop).start()
    loop.run_forever()
