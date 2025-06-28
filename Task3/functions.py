import json

def sendData(socket, status, data):
    """
    Sends data to the socket in JSON format.
    """
    message = {'status': status, 'content': data.strip()}
    socket.send(json.dumps(message).encode('utf-8'))

def receiveData(socket, buffer_size=1024):
    """
    Receives data from the socket and decodes it from JSON format.
    """
    data = socket.recv(buffer_size).decode('utf-8')
    return json.loads(data)
