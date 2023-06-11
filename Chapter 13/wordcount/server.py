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

    def connection_made(self, transport: asyncio.Transport) -> None:
        """Callback for when a new worker connects."""
        peername = transport.get_extra_info("peername")
        print(f"New worker connection from {peername}")
        self.transport = transport
        self.start_new_task()

    def start_new_task(self) -> None:
        """Sends the next task to the worker."""
        command, data = self.scheduler.get_next_task()
        self.send_command(command=command, data=data)

    def process_command(self, command: bytes,
                        data: FileWithId = None) -> None:
        """Processes the response from the worker, updating the state
        of the scheduler and sending the next task if necessary."""
        if command == b"mapdone":
            self.scheduler.map_done(data)
            self.start_new_task()
        elif command == b"reducedone":
            self.scheduler.reduce_done()
            self.start_new_task()
        else:
            print(f"Unknown command received: {command}")


def main():
    event_loop = asyncio.get_event_loop()
    current_path = os.path.abspath(os.getcwd())
    file_locations = list(
        glob.glob(f"{current_path}/input_files/*.txt"))
    scheduler = Scheduler(file_locations)
    server = event_loop.create_server(
        lambda: Server(scheduler), HOST, PORT)
    # ensure that the server is fully set up and running
    server = event_loop.run_until_complete(server)
    print(f"Serving on {server.sockets[0].getsockname()}")
    try:
        event_loop.run_forever()
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()


if __name__ == "__main__":
    main()
