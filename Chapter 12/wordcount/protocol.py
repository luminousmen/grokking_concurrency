import os
import asyncio
import pickle
import shutil

PORT = 8888
HOST = "localhost"
TEMP_DIR = "temp"
END_MSG = b"EOF"
RESULT_FILENAME = "result.json"


class Protocol(asyncio.Protocol):
    def __init__(self):
        super().__init__()
        self.buffer = b""

    def connection_made(self, transport):
        self.transport = transport
        print("Connection made.")

    def data_received(self, data):
        self.buffer = self.buffer + data
        print(self.buffer)
        if END_MSG in self.buffer:
            if b':' not in data:
                command, _ = self.buffer.split(END_MSG, 1)
                data = None
            else:
                command, data = self.buffer.split(b":", 1)
                data, self.buffer = data.split(END_MSG, 1)
                data = pickle.loads(data)
            self.process_command(command, data)

    def send_command(self, command, data=None):
        if data:
            pdata = pickle.dumps(data)
            print(command, data, pdata)
            self.transport.write(command + b":" + pdata + END_MSG)
        else:
            self.transport.write(command + END_MSG)

    def get_temp_dir(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def get_result_filename(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, RESULT_FILENAME)

    def recreate_temp_dir(self, dirname):
        shutil.rmtree(dirname, ignore_errors=True)
        os.makedirs(dirname)
