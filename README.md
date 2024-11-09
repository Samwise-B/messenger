# Peer-to-Peer Messenger Application

This project implements a simple P2P messenger application using the python socket library. Each user acts as both a client and a server, able to receive and send requests to other users.

# Peer-to-Peer Instant Messenger
This project is a simple peer-to-peer (P2P) instant messenger application implemented in Python 3.10 using the socket library for direct network communication. The application is designed to simulate a lightweight chat server with multiple clients, each capable of sending and receiving messages in real time.

The server manages multiple client connections, and clients can join, send messages to all connected users, and disconnect without interrupting server functionality. This project emphasizes foundational network programming skills and showcases the ability to build reliable, interactive client-server systems.

# Features
## Server
- Real-time Message Broadcasting: The server receives messages from connected clients and broadcasts them to all users.
- Client Connection Management: Tracks when clients join and leave, maintaining seamless chat continuity.
- Logging: Automatically generates a server.log file, recording each client's connection, disconnection, and chat activity. This log ensures a complete record of interactions.
- Error Handling: Supports multiple clients while remaining robust even when clients disconnect unexpectedly.
## Client
- User-Friendly Chat Interface: Each client receives a simple text interface, allowing users to send and receive messages.
- Username Display: Each client’s username is used to identify their messages, with notifications when users join or leave.
- Persistent Messaging: Messages sent by one client are immediately visible to all other connected clients.
# Setup and Usage
## Prerequisites
- Python 3.10 (or higher)
- Windows OS
# Running the Application
Start the Server: Run the following command to start the server on a specified port:

`python server.py [port]`

Start the Client: Each client can connect to the server using a unique username and the server's hostname (or IP) and port:

`python client.py [username] [hostname] [port]`

# Sample Interaction
- When a client connects, they receive a welcome message from the server.
- A connected client can send messages, which are instantly broadcast to all active clients.
- When a client disconnects, a message alerts remaining users that they have left.
# File Structure
- `server.py`: Handles incoming client connections, broadcasts messages, manages client disconnections, and writes logs.
- `client.py`: Establishes a connection with the server, facilitates message sending, and displays messages from other clients.

# Technical Overview
This instant messenger application was developed using low-level socket programming to ensure efficient and direct network communication. The server operates on TCP to maintain stable connections, and all messages and events are logged in real-time to server.log.

## Key Libraries
`socket`: For direct network communication.
`threading`: To support concurrent client connections and ensure the server remains responsive.
# Logging
The server logs each client’s activity in server.log, including:
- Client connection details (IP address and port).
- Messages exchanged.
- Client disconnection events.
## Example Log
Below is an example of entries in server.log when two clients connect, chat, and disconnect:
`less
[2023-11-09 12:34:56] Client John connected from 127.0.0.1:12000
[2023-11-09 12:35:01] [John]: Hello everyone!
[2023-11-09 12:36:00] Client Jane connected from 127.0.0.1:12001
[2023-11-09 12:36:05] [Jane]: Hi John!
[2023-11-09 12:37:00] [John] has left
[2023-11-09 12:37:02] Client John disconnected
`
# Future Improvements
- Private Messaging: Extend the application to allow private, direct messages between clients.
- Message Persistence: Enable message storage, allowing clients to retrieve chat history upon reconnection.
- Encryption: Add secure communication features using SSL/TLS for encrypted data transfer.
