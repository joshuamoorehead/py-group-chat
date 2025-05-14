# Python Group Chat Server

This project is a TCP-based group chat system written in Python. It demonstrates non-blocking socket programming and real-time message broadcasting using `select()`. Multiple clients can connect to a central server, send messages, and receive updates in real-time from other participants.

Developed by Joshua Moorehead.

---

## Features

- Supports multiple concurrent clients
- Real-time broadcast of client messages
- Server-side tracking of connected users
- Graceful handling of disconnects
- Uses Python's `socket` and `select` libraries

---

## File Overview

- `server.py`: Runs the chat server and manages client connections
- `client.py`: Connects to the server and allows interactive messaging

---

## How to Run

### 1. Start the Server
```bash
python server.py 50000
```

### 2. Connect Clients
In separate terminal windows:
```bash
python client.py localhost 50000 Alice
python client.py localhost 50000 Bob
python client.py localhost 50000 Charlie
```

Each client can type messages that will be broadcast to all others.

### 3. Exit
- Clients: Press `Ctrl+D` (EOF)
- Server: Press `Ctrl+D` to shut down the server and disconnect all clients

---

## Requirements

- Python 3.x
- No external libraries needed

---

## License

This code is provided for educational and personal use. Developed independently and not derived from course-distributed templates.