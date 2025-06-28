import socket
import threading
from functions import sendData, receiveData

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

subscribers_by_topic = {}  # topic: list of (socket, addr, name)

def handle_client(c, addr):
    try:
        # Get role
        role = receiveData(c)['content']
        if role not in ['publisher', 'subscriber']:
            sendData(c, -1, 'Invalid role. Please connect with a valid role (publisher or subscriber).')
            c.close()
            return
        sendData(c, 0, 'Welcome to the server\nYou are connected as a ' + role)

        # Get topic
        topic = receiveData(c)['content'].strip()

        # Ensure topic exists in dictionary
        if topic not in subscribers_by_topic:
            subscribers_by_topic[topic] = []

        # Get name
        name = receiveData(c)['content']
        print(f"Got connection from {addr} with name {name} on topic '{topic}'")

        # Respond to client based on role
        if role == 'publisher':
            sendData(c, 1, f"You can start sending messages to topic '{topic}'. Type 'terminate' to end.")
        else:
            subscribers_by_topic[topic].append((c, addr, name))
            sendData(c, 1, f"You are now listening to topic '{topic}'. Waiting for messages...")

        # Main loop
        while True:
            msg = receiveData(c)['content']
            if msg == 'terminate':
                print(f"Terminating connection with {addr}, user {name}, topic '{topic}'")
                sendData(c, -1, 'Connection terminated')
                break

            if role == 'publisher':
                print(f"{addr}/{topic}/{name}: {msg}")
                if topic in subscribers_by_topic:
                    for subscriber in subscribers_by_topic[topic]:
                        try:
                            sendData(subscriber[0], 2, f"[{topic}] {name} :: {msg}")
                        except:
                            continue
                sendData(c, 1, 'Message delivered to topic subscribers.')
            elif role == 'subscriber':
                sendData(c, 1, 'Waiting for messages...')
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        # Clean up on exit
        if role == 'subscriber' and topic in subscribers_by_topic:
            subscribers_by_topic[topic] = [s for s in subscribers_by_topic[topic] if s[0] != c]
        c.close()
        print(f"Connection with {addr} closed.")

while True:
    c, addr = s.accept()
    threading.Thread(target=handle_client, args=(c, addr)).start()
