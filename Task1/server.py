import socket

s = socket.socket()
print("Socket successfully created")
port = 9999

s.bind(('localhost', port))
print(f"Socket binded to {port}")

s.listen(3)
print("Socket is listening")

while True:
    c, addr = s.accept()
    name = c.recv(1024).decode('utf-8')
    print(f"Got connection from {addr} with name {name}")
    c.send(b'Welcome to the server!')
    c.close()