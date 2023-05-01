import socket
import threading
import json
import sys

HOST = "localhost"
PORT = 65432

admin = "kepar"

def handle_client(client_socket, client_address, clients):
    """Handle a single client connection"""
    print(f"Accepted connection from {client_address}")
    try:
        # Get the client's username
        username = None
        while username is None:
            client_socket.sendall(b"Enter your username: ")
            username = client_socket.recv(1024).decode().strip()
            with open('creds.json') as f:
                data = json.load(f)
            if data.get(username) is None:
                client_socket.sendall(b"Invalid username. Try again.\n")
                username = None
        print(f"Client {client_address} connected as {username}")

        # Check the client's password
        while True:
            client_socket.sendall(b"Enter your password: ")
            password = client_socket.recv(1024).decode().strip()
            if check_credentials(username, password):
                break
            client_socket.sendall(b"Invalid password. Try again.\n")
        print(f"Client {client_address} logged in as {username}")

        # Add the client to the list of clients
        clients[client_socket] = username

        # Send a welcome message to the client
        welcome_message = f"Welcome to the chat room, {username}!"
        broadcast(welcome_message, clients)

        # Receive and broadcast messages from the client
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if data.decode().strip() == "/help":
                if username == admin:
                    message = b'Admin System: avaible commands: "/upload"'
                else:
                    message = b'System: avaible commands: "/upload"'
                client_socket.sendall(message)
                continue
            elif data.decode().strip() == "/upload":
                message = b'System: To upload stuff, use: https://1fichier.com/ or https://anonfiles.com/'
                client_socket.sendall(message)
                message = b'System: Tip: use a password to protect your file on 1fichier :)'
                client_socket.sendall(message)
                continue
            else:
                message = f"{username}: {data.decode().strip()}"
            broadcast(message, clients)
    except ConnectionResetError:
        pass
    finally:
        # Remove the client from the list of clients
        if client_socket in clients:
            username = clients[client_socket]
            del clients[client_socket]
            print(f"Client {client_address} disconnected")
            broadcast(f"{username} has left the chat", clients)
            client_socket.close()

def check_credentials(username, password):
    """Check if the given username and password are valid"""
    with open("creds.json") as f:
        creds = json.load(f)
    if username in creds and creds[username] == password:
        return True
    else:
        return False

def broadcast(message, clients):
    """Broadcast a message to all connected clients"""
    for sock in clients:
        sock.sendall(message.encode())

def run_server():
    """Start the chat server"""
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    sock.bind((HOST, PORT))

    # Listen for incoming connections
    sock.listen()

    print(f"Server listening on {HOST}:{PORT}")

    # Store a dictionary of connected clients
    clients = {}

    # Accept incoming connections and handle them in separate threads
    while True:
        client_socket, client_address = sock.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        thread.start()

if __name__ == "__main__":
    run_server()
