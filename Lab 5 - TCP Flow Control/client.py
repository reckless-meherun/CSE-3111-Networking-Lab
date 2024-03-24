import socket
import funcs
import os
import sys

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
ADDR = (HOST, PORT)
HEADER_SIZE = 21
SIZE = 1024 + HEADER_SIZE

seq = 0
ack = 0

WINDOW_SIZE = 3072
window = WINDOW_SIZE

FILENAME = 'hi.pdf'


def client_init():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.settimeout(0.1)
    return client


def handshake(client: socket.socket):
    global seq, ack

    tcp_packet = funcs.create_tcp_packet(PORT, PORT, seq, ack, 0, 'SYN', 1)
    client.send(tcp_packet)

    response = client.recv(SIZE)
    response = funcs.decode_tcp_packet(response)

    seq = response['acknowledgment_number']
    ack = response['sequence_number']+1

    tcp_packet = funcs.create_tcp_packet(
        PORT, PORT, seq, ack, WINDOW_SIZE, 'ACK', 1)
    client.send(tcp_packet)

    print(response)
    return response


def main():
    global seq, ack, window, WINDOW_SIZE
    client = client_init()
    response = handshake(client)

    file_body = b''
    # packet_before_ack = WINDOW_SIZE//(SIZE-HEADER_SIZE)

    try:
        while True:
            data = client.recv(SIZE)

            response = funcs.decode_tcp_packet(data)

            ack = response['sequence_number'] + SIZE - HEADER_SIZE + 1

            if not data or response['payload'] == 'EOF'.encode() or response['payload'][-3:] == b'EOF':
                if response['payload'][-3:] == b'EOF':
                    file_body = response['payload'][:-3]
                break

            filtered_dict = {k: v for k, v in response.items() if k not in [
                'payload', 'source_port', 'destination_port', 'data_flag']}
            print(filtered_dict)

            # print(response)
            file_body += response['payload']

            window = response['window_size']
            # packet_before_ack-=1
            seq = response['acknowledgment_number']

            print(f'Window size: {window}')
            if window <= 0:
                # print(f'seq: {seq} ack: {ack} WINDOW_SIZE: {window}')
                client.send(funcs.create_tcp_packet(
                    PORT, PORT, seq, ack, 0, 'ACK', 0))

                print('Writing to file')
                with open(FILENAME, 'ab') as file:
                    file.write(file_body)
                    file_body = b''
                window = WINDOW_SIZE

        print('Done receiving file')

        if client.timeout:
            with open(FILENAME, 'ab') as file:
                file.write(file_body)
                file_body = b''

            seq = response['acknowledgment_number']
            ack = seq+1
            client.settimeout(None)
    except TimeoutError:
        with open(FILENAME, 'ab') as file:
            file.write(file_body)
            file_body = b''

        seq = response['acknowledgment_number']
        ack = seq+1
        client.settimeout(None)

    client.send(funcs.create_tcp_packet(
        PORT, PORT, seq, ack, window, 'FIN', 0))

    client.close()


if __name__ == "__main__":
    main()
