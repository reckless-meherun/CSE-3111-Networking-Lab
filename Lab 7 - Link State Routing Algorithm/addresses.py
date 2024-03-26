import socket

HOST = socket.gethostbyname(socket.gethostname())

address = {
    'A':(HOST,9001),
    'B':(HOST,9002),
    'C':(HOST,9003),
    'D':(HOST,9004)
}