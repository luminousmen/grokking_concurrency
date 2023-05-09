import os
import asyncio
import json
import typing as T

FileWithId = T.Tuple[str, str]
Occurrences = T.Dict[str, int]

PORT = 12345
HOST = "127.0.0.1"
TEMP_DIR = "temp"
END_MSG = b"EOF"


class Protocol(asyncio.Protocol):
    """The Protocol class is responsible for handling the low-level
    communication between the server and the workers. It sends and
    receives commands and data using the asyncio transport layer."""

    def __init__(self) -> None:
        super().__init__()
        self.buffer = b""

    def connection_made(self, transport: asyncio.Transport) -> None:
        """Callback for when a new worker connects."""
        self.transport = transport
        print("Connection made.")

    def data_received(self, data: bytes) -> None:
        self.buffer += data
        if END_MSG in self.buffer:
            if b":" not in data:
                # No data to be unpickled
                command, _ = self.buffer.split(END_MSG, 1)
                data = None
            else:
                # Deserialize the data and split it from the command
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(END_MSG, 1)
                data = json.loads(data.decode())
            self.process_command(command, data)

    def send_command(self, command, data: FileWithId = None) -> None:
        """Sends a command and data to the worker using the
        transport layer."""
        if data:
            pdata = json.dumps(data).encode()
            self.transport.write(command + b":" + pdata + END_MSG)
        else:
            self.transport.write(command + END_MSG)

    def get_temp_dir(self) -> str:
        """Returns the path to the temp directory."""
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def process_command(self, command: bytes, data):
        """Processes the received command and data."""
        raise NotImplementedError
