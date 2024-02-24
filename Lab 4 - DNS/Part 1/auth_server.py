import os
import socket
import funcs
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 4487
ADDR = (IP, PORT)
SIZE = 1024

dic = {}

# def encode_msg(name,value,type,ttl):
#     message = f'{name} {value} {}'

def handle_client(data, addr, server):
    try:
        print(f'Received message from {addr} is: {data}')
        id = data['header']['id']
        data = data['body']
        domain_name, domain_type = data['name'], data['type']

        message = (None, None, None)
        with open('dns_records.txt', 'r') as f:
            for line in f:
                name, value, type, ttl = line.split()

                if name == domain_name and type == domain_type:
                    print(value)
                    message = value, type, ttl
                    break
        message = funcs.build_response(domain_name, message, id)
        print(f'message: {funcs.extract_query(message)}')
        server.sendto(message, addr)
    except:
        print(f'{addr} disconnected')


def main():
    print(f'Server starting')

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(ADDR)

    print(f'Server active on {IP}:{PORT}')

    while True:
        data, addr = server.recvfrom(SIZE)

        data = funcs.extract_query(data)

        client_thread = threading.Thread(
            target=handle_client, args=(data, addr, server))

        print(f'New connection from {addr}')
        client_thread.start()
        print(f'[Active connections] {threading.active_count()-1}')


if __name__ == '__main__':
    main()
