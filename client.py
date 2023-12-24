import socket


def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 11234))
    # send msg
    client.send(b'hello')


client()
