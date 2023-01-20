import os
import asyncio
import pickle
import typing as T

FileWithId = T.Tuple[int, str]
Occurrence = T.Tuple[str, int]
Occurrences = T.Dict[str, int]

PORT = 8888
HOST = "localhost"
TEMP_DIR = "temp"
END_MSG = b"EOF"
RESULT_FILENAME = "result.json"


class Protocol(asyncio.Protocol):
    def __init__(self) -> None:
        super().__init__()
        self.buffer = b""

    def connection_made(self, transport) -> None:
        self.transport = transport
        print("Connection made.")

    def data_received(self, data: bytes) -> None:
        self.buffer = self.buffer + data
        if END_MSG in self.buffer:
            if b":" not in data:
                command, _ = self.buffer.split(END_MSG, 1)
                data = None
            else:
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(END_MSG, 1)
                data = pickle.loads(data)
            self.process_command(command, data)

    def send_command(self, command, data: FileWithId = None) -> None:
        if data:
            pdata = pickle.dumps(data)
            self.transport.write(command + b":" + pdata + END_MSG)
        else:
            self.transport.write(command + END_MSG)

    def get_temp_dir(self) -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def get_result_filename(self) -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, RESULT_FILENAME)
