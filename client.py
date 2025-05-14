# client.py
# Author: Joshua Moorehead
# Description: A TCP chat client that connects to a central server and sends/receives messages using select.


from socket import *
from select import select
from sys import *

# Client needs server's contact information and client name
if len(argv) != 4:
    print("usage:", argv[0], "<server name> <server port> <client name>")
    exit()

# Get server's whereabouts and client name
serverName = argv[1]
serverPort = int(argv[2])
clientName = argv[3]

# Create a socket
sock = socket(AF_INET, SOCK_STREAM)

# Connect to the server
sock.connect((serverName, serverPort))
print(f"Connected to server at ('{serverName}', '{serverPort}')")

# Send client name to server
sock.send(clientName.encode())

# Make a file stream out of socket
sockFile = sock.makefile(mode='r')

# Make a list of inputs to watch for
inputSet = [stdin, sockFile]

# Keep sending and receiving messages from the server
while True:
    # Wait for a message from keyboard or socket
    readableSet, _, _ = select(inputSet, [], [])

    # Check if there is a message from the keyboard
    if stdin in readableSet:
        # Read a line form the keyboard
        line = stdin.readline()

        # If EOF ==> client wants to close connection
        if not line:
            print('*** Client closing connection')
            break

        # Send the line to server
        sock.send(line.encode())

    # Check if there is a message from the socket
    if sockFile in readableSet:
        # Read a message from the server
        line = sockFile.readline()

        # If EOF ==> server closed the connection
        if not line:
            print('*** Server closed connection')
            break
            
        # Display the line
        print('Server:',line, end='')

# Close the connection
sockFile.close()
sock.close()