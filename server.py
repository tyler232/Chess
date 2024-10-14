import socket
import pickle
import threading
import random

SERVER_IP = "localhost"
SERVER_PORT = 9060
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

clients = []
client_lock = threading.Lock()

def handle_client(conn, addr):
    global clients
    print(f"Connected to {addr}")
    
    with conn:
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                move = pickle.loads(data)
                print(f"Move received from {addr}: {move}")

                # Send the move to the other client
                with client_lock:
                    for client in clients:
                        if client != conn:
                            client.sendall(data)
            except Exception as e:
                print(f"Error: {e}")
                break

    print(f"Disconnected from {addr}")
    with client_lock:
        clients.remove(conn)

def main():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(SERVER_ADDRESS)
    server.listen(2)  # Allow only 2 connections

    print("Waiting for clients to connect...")
    
    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

    print("Both clients connected. Starting the game...")
    
    random.shuffle(clients)
    for i, client in enumerate(clients):
        color = "WHITE" if i == 0 else "BLACK"
        client.sendall(pickle.dumps(color))
    
    # Keep the server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        for client in clients:
            client.close()
        server.close()

if __name__ == "__main__":
    main()
