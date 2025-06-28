import socket
import threading
from functions import sendData
from functions import receiveData


print("Enter the port number: ")
port = int(input("my_server_app port: "))
if port < 1024 or port > 65535:
    print("Invalid port number. Please enter a port number between 1024 and 65535.")
    exit(1)

s = socket.socket()
s.bind(('localhost', port))
print(f"Socket binded to {port}")


s.listen(3)
print("Socket is listening...")

def handle_client(c, addr):
    try:
        name = receiveData(c)['content']
        print(f"Got connection from {addr} with name {name}")
        sendData(c, 0, 'Welcome to the server')
        while True:
            request = receiveData(c)['content']
            if request == 'terminate':
                print("Terminating connection with", addr, "user", name)
                sendData(c, -1, 'Connection terminated')
                c.close()
                break
            else:
                print(f"{addr}:{name}:: {request}")
                sendData(c, 1, 'received')
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        c.close()
        print(f"Connection with {addr} closed.")

while True:
    c, addr = s.accept()
    client_thread = threading.Thread(target=handle_client, args=(c, addr))
    client_thread.start()