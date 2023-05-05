#!/usr/bin/env python3

"""Implementation of event-based concurrency using Reactor pattern"""

import typing as T
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
from socket import socket, create_server

Data = bytes
Action = T.Union[T.Callable[[socket], None], T.Tuple[
    T.Callable[[socket, Data], None], str]]

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)  # address and port of the host machine


class EventLoop:
    def __init__(self) -> None:
        # Python library offers us two modules that support synchronous
        # I/O multiplexing: select and selectors.
        # select is more low level and exposes you to the specific select-family
        # syscalls, selectors is a higher level module that choose the best
        # implementation on your system,
        # roughly epoll|kqueue|devpoll > poll > select
        self.event_notifier = DefaultSelector()

    def register_event(self, source: socket, event: int,
                       action: Action) -> None:
        """Registers an event to the event notifier with the given source,
        event, and action. If the event already exists, modifies the action
        of the event."""
        try:
            self.event_notifier.register(source, event, action)
        except KeyError:  # already exists so modify
            self.event_notifier.modify(source, event, action)

    def unregister_event(self, source: socket) -> None:
        """Unregisters the event with the given source from the event
        notifier."""
        self.event_notifier.unregister(source)

    def run_forever(self) -> None:
        """Runs the event loop indefinitely, waiting for registered events
        and executing their associated actions when they occur"""
        while True:
            # select() blocks until there are sockets ready for I/O.
            events = self.event_notifier.select()
            for (source, _, _, action), event in events:
                if event & EVENT_READ:
                    action(source)
                elif event & EVENT_WRITE:
                    action, msg = action  # separate callable and data
                    action(source, msg)
                else:
                    raise RuntimeError("No such event")


class Server:
    """A simple TCP server that uses event-based concurrency with the
    reactor pattern."""

    def __init__(self, event_loop: EventLoop) -> None:
        self.event_loop = event_loop
        try:
            print(f"Starting up at: {ADDRESS}")
            # On POSIX platforms the SO_REUSEADDR socket option is set
            self.server_socket = create_server(ADDRESS)
            # set socket to non-blocking mode
            self.server_socket.setblocking(False)
            # on server side let's start listening mode for this socket
            self.server_socket.listen()
        except OSError:
            self.server_socket.close()
            print("\nServer stopped.")

    def _on_accept(self, _: socket) -> None:
        """Callback that is called when a new incoming client connection
        is accepted by the server socket. It registers the connected socket
        for read events."""
        try:
            conn, client_address = self.server_socket.accept()
        except BlockingIOError:
            return
        conn.setblocking(False)
        print(f"Connected to {client_address}")
        # future calls to the self.event_notifier.select() will be notified
        # whether this socket connection has any pending I/O events
        self.event_loop.register_event(conn, EVENT_READ, self._on_read)

    def _on_read(self, conn: socket) -> None:
        """Callback that is called when the connected socket has incoming
        data to be read. It reads data from the socket, handles the
        received message and registers the socket for write events if
        required."""
        try:
            data = conn.recv(BUFFER_SIZE)
        except BlockingIOError:
            return
        if not data:
            self.event_loop.unregister_event(conn)
            print(f"Connection with {conn.getpeername()} has been closed")
            conn.close()
            return
        message = data.decode().strip()
        self.event_loop.register_event(conn, EVENT_WRITE,
                                       (self._on_write, message))

    def _on_write(self, conn: socket, message: bytes) -> None:
        """Callback that is called when the connected socket is ready to
        write data. It writes the message to the socket and registers the
        socket for read events."""
        try:
            order = int(message)
            response = f"Thank you for ordering {order} pizzas!\n"
        except ValueError:
            response = "Wrong number of pizzas, please try again\n"
        print(f"Sending message to {conn.getpeername()}")
        try:
            conn.send(response.encode())
        except BlockingIOError:
            return
        self.event_loop.register_event(conn, EVENT_READ, self._on_read)

    def start(self) -> None:
        # registering the server socket for the OS to monitor
        # Once register is done future calls to the self.event_notifier.select()
        # will be notified whether server socket has any pending accept events
        # from the clients
        print("Server listening for incoming connections")
        self.event_loop.register_event(
            self.server_socket, EVENT_READ, self._on_accept)


if __name__ == "__main__":
    loop = EventLoop()
    Server(loop).start()
    loop.run_forever()
