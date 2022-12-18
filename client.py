import socket
from datetime import datetime

def client(uname, address, port):
    with socket.socket() as s:
        # connect and send username
        try:
            s.connect((address, port))
            s.sendall(uname.encode())
            print(s.recv(1024).decode())
        except:
            print("Error connecting socket.")
        # Once connected, loop until user quits
        while True:
            # get input from user to send to the server
            msg = input(">> ")
            if msg == "::quit" or msg == "::q":
                s.close()
                return 0
            
            # send message 
            s.sendall(msg.encode())

            # receive any messages from server
            data = s.recv(1024).decode()
            print(data)

            if not data:
                print(f"Closing socket: {s.getsockname()}")
                s.close()

def main():
    client("bob", '127.0.0.1', 1337)

if __name__ == '__main__':
    main()