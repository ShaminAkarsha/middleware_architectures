import json

def sendData(socket ,status, date):
    """
    Sends data to the socket in JSON format.
    
    Parameters:
    socket (socket.socket): The socket to send data through.
    status (int): The status code to send.
    date (str): The content to send.
    
    Returns:
    None
    """
    data = {'status': status, 'content': date.strip()}
    socket.send(json.dumps(data).encode('utf-8'))


def receiveData(socket, buffer_size=1024):
    """
    Receives data from the socket and decodes it from JSON format.
    
    Parameters:
    socket (socket.socket): The socket to receive data from.
    
    Returns:
    dict: The decoded data as a dictionary.
    """
    data = socket.recv(buffer_size).decode('utf-8')
    return json.loads(data)