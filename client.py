import socket
import queue
import threading
from datetime import datetime


#http://pymotw.com/2/select/
#https://realpython.com/intro-to-python-threading/

messages = queue.Queue()

def add_input(s):
    while True:
        # get input from user to send to the server
        msg = input("")
        if msg == "::quit" or msg == "::q":
            s.close()
            exit(0)
        else:
            messages.put(msg)
        
        # if there is a message in the queue send the data and remove it from the queue
        if not messages.empty():
                msg = messages.get_nowait()
                #print("message: ", msg)

                # send message 
                s.sendall(msg.encode())


def client(uname, address, port):
    with socket.socket() as s:
        # connect and send username
        try:
            s.connect((address, port))
            s.sendall(uname.encode())
            print(s.recv(1024).decode())
        except:
            print("Error connecting socket.")
            exit(1)
        
        # start new thread
        inputs = threading.Thread(target=add_input, args=(s,))
        inputs.start()

        # Once connected, loop until user quits
        while True:
            # if there is data to be read, receive and print it
            # receive any messages from server
            data = s.recv(1024).decode()
            if data:
                print(data)

            if not data:
                print(f"Closing socket: {s.getsockname()}")
                s.close()
            

            """
            # if there is a message in the queue send the data and remove it from the queue
            if not messages.empty():
                msg = messages.get_nowait()
                print("message: ", msg)

                # send message 
                s.sendall(msg.encode())
            """
            
            """try:
                #print("queue: ", list(messages.queue))
                msg = messages.get_nowait()
                print("message: ", msg)

                # send message 
                s.sendall(msg.encode())
            except queue.Empty:
                continue"""



def main():
    # TODO: add command line args
    client("bob", '127.0.0.1', 1337)

if __name__ == '__main__':
    main()