import socket
import packet
import os
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9992
ADDR = (HOST, PORT)
SIZE = 1629
WINDOW = 4500

FILENAME = 'new.jpg'

rcv_seq = 0
rcv_ack = 0

file_body = b''

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

print(f"Connected to {HOST}:{PORT}")
pkt = packet.make_pkt(0,PORT,rcv_seq,rcv_ack,WINDOW,b'',0)
client_socket.send(pkt)

with open(FILENAME,'wb') as file:
    while True:
        segment = client_socket.recv(SIZE)
        # print(segment)
        pkt = packet.extract(segment)
        # print(pkt)
        print(f'Received packet with seq={pkt["seq_num"]} and ack={pkt["ack_num"]}')

        if pkt['payload'] == b'FIN':
            print(f'File has been received')
            file.write(file_body)
            break
        
        WINDOW -= len(pkt['payload'])
        print(f'Window size: {WINDOW}')
        file_body += pkt['payload']

        if WINDOW <=0:
            WINDOW = 4500
            print(f'Wrote {len(file_body)} bytes to file')
            file.write(file_body)
            file_body = b''
            pkt = packet.make_pkt(0,PORT,rcv_seq,pkt['seq_num']+SIZE-130,WINDOW,b'ACK',0)
            client_socket.send(pkt)
            print(f'Sent ACK with seq={rcv_seq} and ack={rcv_ack}')
        else:
            rcv_seq = pkt['ack_num']
            rcv_ack = rcv_seq+SIZE-30
            

        # time.sleep(1)

