import socket
from functions import sendData, receiveData

c = socket.socket()
port = 9999

if port < 1024 or port > 65535:
    print("Invalid port number. Please enter a port number between 1024 and 65535.")
    exit(1)

print("Enter the role (publisher or subscriber): ")
role = input().strip().lower()

if role not in ['publisher', 'subscriber']:
    print("Invalid role. Please enter 'publisher' or 'subscriber'.")
    exit(1)

print("Enter the topic: ")
topic = input().strip()

c.connect(('localhost', port))

# Send role and topic
sendData(c, 0, role)
print(receiveData(c)['content'])

sendData(c, 1, topic)

name = input("Enter your name: ")
sendData(c, 1, name)

response = receiveData(c)
print(response['content'])

msgLine = 1
while True:
    if role == 'publisher':
        msg = input(f"{msgLine}: ")
        sendData(c, 1, msg)
        response = receiveData(c)
        print(response['content'])
        if response['status'] == -1:
            print("Connection terminated.")
            c.close()
            break
    elif role == 'subscriber':
        response = receiveData(c)
        if response['status'] == 2:
            print(response['content'])
        elif response['status'] == -1:
            print("Connection terminated.")
            c.close()
            break
        else:
            print("Unknown response from server:", response)
    msgLine += 1
