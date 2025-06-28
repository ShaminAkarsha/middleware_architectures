import socket
from functions import sendData
from functions import receiveData

c = socket.socket()

c.connect(('localhost', 9999))

name = input("Enter your name: ")
sendData(c, 1, name)
responce = receiveData(c)
print(responce['content'])
print("You can start sending messages now. Type 'terminate' to end the connection.")
msgLine = 1
while True:
    msg = input(str(msgLine) + ": ")
    sendData(c, 1, msg)
    responce = receiveData(c)
    print(responce)
    if responce['status'] == -1:
        print("Connection terminated.")
        c.close()
        break
    msgLine += 1
