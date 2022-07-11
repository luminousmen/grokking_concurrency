#!/usr/bin/env python3

"""Simple TCP/IP socket server"""
import time
import socket

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)
FILENAME = "poem.txt"

if __name__ == "__main__":
    # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
    # here we create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f"Starting up on: {HOST}:{PORT}")
        # bind a socket to a specific network interface and port number
        server_socket.bind((HOST, PORT))
        print("Listen for incoming connections")
        # on server side let's start listening mode for this socket
        server_socket.listen()
        print("Waiting for a connection")
        # serving clients, sequentially
        while True:
            # accepting the incoming connection, blocking
            # conn = is a new socket object usable to send and receive data on the connection
            # addr = is the address bound to the socket on the other end of connection
            conn, (client_host, client_port) = server_socket.accept()
            address = f"{client_host}:{client_port}"
            print(f"Connected to {address}")
            try:
                while True:
                    server_socket.settimeout(5.0)
                    data = conn.recv(BUFFER_SIZE)
                    if not data:  # connection closed
                        print(f"Connection closed")
                        break
                    message = data.decode().upper()
                    print(f"Sending a line to {address}")
                    # send a response
                    conn.send(message.encode())
                    # Note: recommended way is to use .sendall(),
                    # but we will stick with send to keep reader's mental model
            finally:
                # server expects the client to close its side of the connection when it’s done.
                # In a real application, we should use timeout for clients if they don’t send
                # a request after a certain amount of time.
                conn.close()
    finally:
        server_socket.close()
        print("\nServer stopped.")
