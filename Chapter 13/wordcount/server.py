#!/usr/bin/env python3.9

import os
import glob
import asyncio

from scheduler import Scheduler
from protocol import Protocol, HOST, PORT, FileWithId


class Server(Protocol):
    def __init__(self, scheduler: Scheduler) -> None:
        super().__init__()
        self.scheduler = scheduler

    def connection_made(self, transport) -> None:
        peername = transport.get_extra_info("peername")
        print(f"New worker connection from {peername}")
        self.transport = transport
        self.start_new_task()

    def start_new_task(self) -> None:
        command, data = self.scheduler.next_task()
        if command is None:
            return
        self.send_command(command=command, data=data)

    def process_command(
            self, command: bytes, data: FileWithId = None) -> None:
        commands = {
            b"mapdone": self.map_done,
            b"reducedone": self.reduce_done,
        }
        if command in commands:
            commands[command](data)

    def map_done(self, data: FileWithId) -> None:
        self.scheduler.map_done(data)
        self.start_new_task()

    def reduce_done(self, data: FileWithId) -> None:
        self.scheduler.reduce_done(data)
        self.start_new_task()


def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_event_loop()
    data = list(
        glob.glob(f"{os.path.abspath(os.getcwd())}/input_files/*.txt"))
    scheduler = Scheduler(data)
    coro = loop.create_server(lambda: Server(scheduler), HOST, PORT)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print(f"Serving on {server.sockets[0].getsockname()}")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()


if __name__ == "__main__":
    main()
