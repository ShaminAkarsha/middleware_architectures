import socket
from functions import sendData
from functions import receiveData

c = socket.socket()
#port = int(input("my_client_app 01 port: "))
port = 9999
if port < 1024 or port > 65535:
    print("Invalid port number. Please enter a port number between 1024 and 65535.")
    exit(1)

role = input() # 'publisher' or 'subscriber'
if role not in ['publisher', 'subscriber']:
    print("Invalid role. Please enter 'publisher' or 'subscriber'.")
    exit(1)

c.connect(('localhost', port))

sendData(c, 0, role)  # Send role to the server
print(receiveData(c)['content']) 

name = input("Enter your name: ")
sendData(c, 1, name)
responce = receiveData(c)
print(responce['content'])

msgLine = 1
while True:
    if(role == 'publisher'):
        msg = input(str(msgLine) + ": ")
        sendData(c, 1, msg)
        responce = receiveData(c)
        print(responce['content'])
        if responce['status'] == -1:
            print("Connection terminated.")
            c.close()
            break
    elif (role == 'subscriber'):
        responce = receiveData(c)
        if responce['status'] == 2:
            print(responce['content'])
        elif responce['status'] == -1:
            print("Connection terminated.")
            c.close()
            break
        else:
            print("Unknown response from server:", responce)
    msgLine += 1
