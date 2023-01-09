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
                        # check if it is a new client sending username
                        if s not in clients.keys():
                            clients[s] = data.decode()
                            print(f"New connection from {s.getpeername()}.")
                            #s.send(f"Welcome to the server {clients[s]}.".encode())
                            message_queues[s].put(f"Welcome to the server {clients[s]}.".encode())
                            msg = f"{clients[s]} has joined".encode()
                            #message_queues[s].put(f"{clients[s]} has joined".encode())
                        else:
                            # append username to message
                            msg = f"{clients[s]}: ".encode() + data
                        # if there is data add it to all the sockets' msg queues
                        print(f"received '{data}' from { s.getpeername() }")
                        for sock in message_queues.keys():
                            if sock != s:
                                message_queues[sock].put(msg)
                        # add the socket to the outputs stream
                            if sock not in outputs:
                                outputs.append(sock)
                    else:
                        # otherwise, if there is no data the socket must be closed as the client has disconnected
                        print(f"Closing connection after reading no data: {client_addr}")
                        if s in outputs:
                            outputs.remove(s)
                        clients.pop(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
            # handles writing of sockets, for each socket that is writable (w)
            for s in w:
                # get the next message from s's queue
                try:
                    # append username to front of message
                    next_msg = message_queues[s].get_nowait()
                except queue.Empty:
                    #continue
                    print(f"output queue for {s.getpeername()} is empty")
                    outputs.remove(s)
                else:
                    print(w)
                    s.send(next_msg)
                    """
                    for sock in w:
                        print(f"sending '{next_msg}' to {sock.getpeername()}")
                        sock.send(next_msg)
                    """
            # handles errors in sockets
            for s in e:
                print(f"Handling exception for {s.getpeername()}")
                clients.pop(s)
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