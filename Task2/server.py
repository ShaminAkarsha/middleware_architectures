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


s.listen(128)
print("Socket is listening...")

subscribers = []

def handle_client(c, addr):
    try:
        role = receiveData(c)['content']
        if role not in ['publisher', 'subscriber']:
            sendData(c, -1, 'Invalid role. Please connect with a valid role (publisher or subscriber).')
            c.close()
            return
        sendData(c, 0, 'Welcome to the server\nYou are connected as a ' + role)
        name = receiveData(c)['content']
        print(f"Got connection from {addr} with name {name}")

        if role == 'publisher':
            sendData(c, 1, "You can start sending messages now. Type 'terminate' to end the connection.")
        else:
            subscribers.append((c, addr, name))
            sendData(c, 1, "You can start receiving messages now. Type 'terminate' to end the connection.")

        while True:
            msg = receiveData(c)['content']
            if msg == 'terminate':
                print("Terminating connection with", addr, "user", name)
                sendData(c, -1, 'Connection terminated')
                c.close()
                break
            else:
                if(role == 'publisher'):
                    #print(f"{addr}:{name}:: {msg}")
                    for subscriber in subscribers:
                        sendData(subscriber[0], 2, f"{name}:: {msg}")
                    sendData(c, 1, 'received')
                elif(role == 'subscriber'):
                    #print(f"{addr}:{name}:: {msg}")
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