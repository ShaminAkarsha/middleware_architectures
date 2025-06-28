import socket

c = socket.socket()

c.connect(('localhost', 9999))

name = input("Enter your name: ")
c.send(name.encode('utf-8'))

responce = c.recv(1024)

print(responce.decode('utf-8'))


