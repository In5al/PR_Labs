#server.py
import socket
import threading
import json
import base64

# ... (Code from Step 1)
# Server configuration
HOST = '127.0.0.1'  # Loopback address for localhost
PORT = 8070       # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

# Function to handle a client's messages
def handle_client(client_socket, client_address, client_id):
    print(f"Accepted connection from {client_address}")
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break  # Exit the loop when the client disconnects

        print(f"Received from {client_address}: {message}")

        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            print("Received message is not valid JSON.")
            continue  # Skip further processing for this message

        if message['type'] == "connect_ack":
            clients[client_id]["name"] = message["payload"]["name"]
            clients[client_id]["room"] = message["payload"]["room"]
        elif message['type'] == "message":
            text = message["payload"]["text"]
            # Broadcast the message to all clients
            for sk in sockets:
                for c in clients.keys():
                    if clients[c]["socket"] == sk:
                        if clients[c]["room"] == message["payload"]["room"]:
                            if sk != client_socket:
                                sk.send(str(message).encode('utf-8'))
        elif message['type'] == "image":
            # Received an image/file from the client
            filename = message["payload"]["filename"]
            filedata = message["payload"]["filedata"]

            with open("server_" + filename, "wb") as file:
                file.write(base64.b64decode(filedata))

            # Broadcast the file to clients in the same room
            for sk in sockets:
                for c in clients.keys():
                    if clients[c]["socket"] == sk:
                        if clients[c]["room"] == message["payload"]["room"]:
                            if sk != client_socket:
                                sk.send(str(message).encode('utf-8'))
    sockets.remove(client_socket)
    del clients[client_id]
    client_socket.close()


clients = {}
cid = 0
sockets = []
while True:
    client_socket, client_address = server_socket.accept()
    sockets.append(client_socket)
    clients[f"user{cid}"] = {
                        "socket": client_socket,
                        "name":None,
                        "room":None
                        }
    # Start a thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, f"user{cid}"))
    client_thread.start()
    cid += 1