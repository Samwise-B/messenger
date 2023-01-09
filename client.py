import socket
import queue
import threading
import sys


#http://pymotw.com/2/select/
#https://realpython.com/intro-to-python-threading/

messages = queue.Queue()
quit_flag = False

def close_sock(s):
    quit_flag = True
    s.close()

def add_input(s):
    while True:
        # get input from user to send to the server
        msg = input("")
        if msg == "::quit" or msg == "::q":
            close_sock(s)
            break
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
            if quit_flag:
                print("Goodbye")
                s.close()
                return 0

            # if there is data to be read, receive and print it
            # receive any messages from server
            try:
                data = s.recv(1024).decode()
            except ConnectionAbortedError:
                print("Goodbye")
                return 0

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
    argc = len(sys.argv)
    if (argc == 4):
        uname = sys.argv[1]
        hostname = sys.argv[2]
        port = int(sys.argv[3])
    else:
        print("Usage: python client.py [username] [hostname] [port]")
        return 1    
    
    client(uname, hostname, port)

if __name__ == '__main__':
    main()