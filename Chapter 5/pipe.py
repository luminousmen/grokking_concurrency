from multiprocessing import Process, Pipe


def send_hello(conn):
    conn.send("Hello!")
    conn.close()


def get_hello(conn):
    msg = conn.recv()
    print(msg)


if __name__ == '__main__':
    receiver_conn, sender_conn = Pipe()
    sender = Process(target=send_hello, args=(sender_conn,))
    receiver = Process(target=get_hello, args=(receiver_conn,))

    processes = [
        sender,
        receiver
    ]
    for process in processes:
        process.start()

    for process in processes:
        process.join()
