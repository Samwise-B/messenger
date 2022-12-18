import socket
import select
import queue

clients = {}

def server(host, port):
    # create listening socket and bind to port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)

    print(f"Listening on {(host, port)}")

    # set socket blocking to false
    server.setblocking(False)

    # list of sockets ready for input & output
    inputs = [server]
    outputs = []

    # queue of messages for each socket
    message_queues = {}

    # main server loop
    try:
        while True:
            r, w, e = select.select(inputs, outputs, inputs)

            # handles reading of sockets with 3 cases
            for s in r:
                # if the socket is server, we accept any new connections
                if s is server:
                    conn, client_addr = s.accept()
                    print(f"New connection from {client_addr}")
                    conn.setblocking(False)

                    # we add the connection to the inputs list and create a message queue
                    inputs.append(conn)
                    message_queues[conn] = queue.Queue()
                else:
                    # try and receive data from the socket
                    data = s.recv(1024)
                    if data:
                        # if there is data add it to the sockets respective msg queue
                        print(f"received '{data}' from { s.getpeername() }")
                        message_queues[s].put(data)
                        # add the socket to the outputs stream
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        # otherwise, if there is no data the socket must be closed as the client has disconnected
                        print(f"Closing connection after reading no data: {client_addr}")
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
            # handles writing of sockets
            for s in w:
                try:
                    next_msg = message_queues[s].get_nowait()
                except queue.Empty:
                    print(f"output queue for {s.getpeername()} is empty")
                    outputs.remove(s)
                else:
                    print(f"sending '{next_msg}' to {s.getpeername()}")
                    s.send(next_msg)
            # handles errors in sockets
            for s in e:
                print(f"Handling exception for {s.getpeername()}")
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

                del message_queues[s]
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        server.close()


if __name__ == '__main__':
    server('127.0.0.1', 1337)