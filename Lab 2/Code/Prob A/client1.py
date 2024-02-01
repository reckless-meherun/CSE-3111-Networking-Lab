import socket

HOST = socket.gethostbyname(socket.gethostname()) 
PORT = 9005
client_socket: socket.socket

def client_init():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

    while True:
        text = input('Enter text or number with an operation:')
        client_socket.send(text.encode())

        print(client_socket.recv(1024).decode())

client_init()
