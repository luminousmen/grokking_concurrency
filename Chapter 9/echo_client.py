#!/usr/bin/env python3

"""
"""
import socket

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        ping = b"Ping!"
        while True:
            s.sendall(ping)
            data = s.recv(1024)
            # deserialize message from byte stream
            message = data.decode()
            print(f"Received `{message}`")
