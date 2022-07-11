import socket

# the maximum amount of data to be received at once
BUFFER_SIZE = 1024
HOST = "127.0.0.1"  # address of the host machine
PORT = 12345  # port to listen on (non-privileged ports are > 1023)
FILENAME = "poem.txt"
sockets = set()
remove_pending = set()

if __name__ == "__main__":
    # AF_UNIX and SOCK_STREAM are constants represent the protocol and socket type respectively
    # here we create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set Non-Blocking socket
    server_socket.setblocking(False)
    print(f"Starting up on: {HOST}:{PORT}")
    # bind a socket to a specific network interface and port number
    server_socket.bind((HOST, PORT))
    print("Listen for incoming connections")
    # on server side let's start listening mode for this socket
    server_socket.listen()
    print("Waiting for a connection")

    while True:
        try:
            conn, (client_host, client_port) = server_socket.accept()
            conn.setblocking(False)
            sockets.add(conn)
        except BlockingIOError:  # [Errno 35] Resource temporarily unavailable - indicates that "accept" returned without results
            pass

        remove_pending.clear()
        for conn in sockets:
            try:
                data = conn.recv(1024)
                if not data:  # connection closed
                    remove_pending.add(conn)
                else:
                    print(data)
                    conn.sendall(data)
            except BlockingIOError:  # recv/send return without data.
                pass

        # remove closed connections
        for conn in remove_pending:
            sockets.remove(conn)
