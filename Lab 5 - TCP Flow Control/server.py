import socket
import os
import funcs
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (HOST, PORT)
SIZE = 1024

FILENAME = 'file_sent.txt'

seq = 0
ack = 0

def server_init():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print(f"Server is listening on {HOST}:{PORT}")
    return server

def handshake(conn:socket.socket,addr):
    global seq,ack

    response = conn.recv(SIZE)
    response = funcs.decode_tcp_packet(response)

    print(response)

    seq = response['acknowledgment_number']
    ack = response['sequence_number']+1

    tcp_packet = funcs.create_tcp_packet(PORT,PORT,seq,ack,0,'SYN/ACK',0)
    conn.send(tcp_packet)

    response = conn.recv(SIZE)
    response = funcs.decode_tcp_packet(response)
    seq = response['acknowledgment_number']
    ack = response['sequence_number']+1
    
    print(response)
    return response

    


def handle_client(conn:socket.socket, addr):
    global seq,ack
    print(f"[NEW CONNECTION] {addr} connected.")

    response = handshake(conn,addr)
    seq = 1
    ack = 1

    WINDOW_SIZE = response['window_size']

    # packets_before_ack = WINDOW_SIZE//SIZE
    # print(f"Pack: {packets_before_ack}")

    
    file_path = os.path.join(os.getcwd(),FILENAME)


    with open(file_path, 'rb') as file:
        while True:
            data = file.read(SIZE)
            if not data:
                break

            ack = seq+len(data)
            WINDOW_SIZE -= SIZE
            tcp_packet = funcs.create_tcp_packet(PORT,PORT,seq,ack,WINDOW_SIZE,data,1)
            conn.send(tcp_packet)

            print(f"Sent {seq} to {ack}")

            seq = ack
            # packets_before_ack-=1

            if WINDOW_SIZE <= 0:
                response = conn.recv(SIZE)
                response = funcs.decode_tcp_packet(response)
                print(response)
                seq = response['acknowledgment_number']
                ack = response['acknowledgment_number']+SIZE
                WINDOW_SIZE = 3072
                # packets_before_ack = WINDOW_SIZE//SIZE
    print('Done sending file')
    conn.send(funcs.create_tcp_packet(PORT,PORT,0,0,WINDOW_SIZE,'EOF',0))

    response = conn.recv(SIZE)
    response = funcs.decode_tcp_packet(response)
    print(response)


    conn.close()

def main():
    server = server_init()
    while True:
        conn, addr = server.accept()
        # conn.settimeout(5)
        handle_client(conn, addr)


if __name__ == "__main__":
    main()