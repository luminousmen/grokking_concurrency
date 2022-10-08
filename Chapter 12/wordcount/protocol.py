import asyncio
import pickle
import os
import shutil

PORT = 11235
HOST = "localhost"
TEMP_DIR = "temp"


class Protocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self.buffer = b''

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made.")

    def data_received(self, data):
        self.buffer = self.buffer + data
        if b'\n' in data:
            if b':' not in data:
                command, _ = self.buffer.split(b"\n", 1)
                data = None
            else:
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(b"\n", 1)
                data = pickle.loads(data)
            self.process_command(command, data)

    async def get_command(self, client_reader):
        # give client a chance to respond, timeout after 10 seconds
        self.buffer = await asyncio.wait_for(client_reader.readline(1024 * 128), timeout=10.0)
        command, data = self.buffer.split(b":", 1)
        data, self.buffer = data.split(b"\n", 1)
        data = pickle.loads(data)
        return command, data

    def send_command(self, command, data=None):
        if data:
            pdata = pickle.dumps(data)
            self.transport.write(command + b":" + pdata + b"\n")
        else:
            self.transport.write(command + b"\n")

    def get_temp_dir(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def get_result_filename(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, "result.json")

    def recreate_temp_dir(self, dirname):
        shutil.rmtree(dirname, ignore_errors=True)
        os.makedirs(dirname)
