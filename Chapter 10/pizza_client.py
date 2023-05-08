#!/usr/bin/env python3.9

"""Simple Pizza Client"""

from socket import create_connection

BUFFER_SIZE = 1024
ADDRESS = ("127.0.0.1", 12345)   # address and port of the host machine

with create_connection(ADDRESS) as conn:
    while order := input("How many pizzas do you want? "):
        conn.send(order.encode())
        response = conn.recv(BUFFER_SIZE)
        print(f"Server replied '{response.decode().rstrip()}'")
    print("Client closing")
