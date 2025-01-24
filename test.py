import socket
import os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

port = int(os.environ.get("PORT", 1234))  # Default to 1234 if PORT is not set
server_socket.bind(("0.0.0.0", port))
print(f"Server is running on port {port}")

server_socket.listen(6)
print("Listening to 6 clients...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Client connected: {addr}")
    client_socket.close()
