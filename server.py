# server.py
# Author: Joshua Moorehead
# Description: A Python-based TCP group chat server using socket and select.


from socket import *
from select import select
from sys import *

# Server needs the port number to listen on
if len(argv) != 2:
    print('usage:', argv[0], '<port>')
    exit()

# Get the port on which server should listen
serverPort = int(argv[1])

# Create the server socket
serverSock = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the given port
serverSock.bind(('', serverPort))

# Set the server for listening
serverSock.listen(5)

print('Server is ready to receive')

# List to keep track of connected clients
clients = []
client_names = {}

# Make a list of inputs to watch for
inputs = [serverSock, stdin]

# Keep accepting new clients and receiving messages
while True:
    # Wait for a message from keyboard or any of the sockets
    readables, _, _ = select(inputs, [], [])

    for readable in readables:
        if readable == serverSock:
            # New client connection
            clientSock, clientAddr = serverSock.accept()
            print('New client connected from', clientAddr)
            inputs.append(clientSock)
            clients.append(clientSock)

            # Receive client name
            name = clientSock.recv(1024).decode().strip()
            client_names[clientSock] = name
            print(f'Client {name} joined the chat')

            # Broadcast join message
            for client in clients:
                if client != clientSock:
                    client.send(f'*** {name} joined the chat ***\n'.encode())

        elif readable == stdin:
            # Server wants to close
            message = stdin.readline()
            if not message:
                print('*** Server closing ***')
                for client in clients:
                    client.close()
                serverSock.close()
                exit()

        else:
            # Message from a client
            try:
                message = readable.recv(1024).decode()
                if message:
                    sender_name = client_names[readable]
                    print(f'{sender_name}: {message}', end='')
                    for client in clients:
                        if client != readable:
                            client.send(f'{sender_name}: {message}'.encode())
                else:
                    # Client disconnected
                    name = client_names[readable]
                    print(f'*** {name} left the chat ***')
                    clients.remove(readable)
                    inputs.remove(readable)
                    del client_names[readable]
                    readable.close()
                    for client in clients:
                        client.send(f'*** {name} left the chat ***\n'.encode())
            except:
                # Client disconnected unexpectedly
                name = client_names[readable]
                print(f'*** {name} left the chat unexpectedly ***')
                clients.remove(readable)
                inputs.remove(readable)
                del client_names[readable]
                readable.close()
                for client in clients:
                    client.send(f'*** {name} left the chat unexpectedly ***\n'.encode())