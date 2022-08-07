"""Asynchronous socket implementation - same functionality but with asynchronous flavour!"""

import selectors


class AsyncSocket:
    def __init__(self, sock, loop):
        sock.setblocking(False)
        self.sock = sock
        self.loop = loop

    async def accept(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                return AsyncSocket(sock=sock, loop=self.loop), addr
            except BlockingIOError:
                future = self.loop.create_future_for_events(self.sock, selectors.EVENT_READ)
                await future

    async def recv(self, bufsize):
        while True:
            try:
                return self.sock.recv(bufsize)
            except BlockingIOError:
                future = self.loop.create_future_for_events(self.sock, selectors.EVENT_READ)
                await future

    async def send(self, data):
        while True:
            try:
                return self.sock.send(data)
            except BlockingIOError:
                future = self.loop.create_future_for_events(self.sock, selectors.EVENT_WRITE)
                await future

    def __getattr__(self, name):
        return getattr(self.sock, name)
