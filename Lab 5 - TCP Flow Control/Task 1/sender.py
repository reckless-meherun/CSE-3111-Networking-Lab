import socket
import packet
import os
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9992
ADDR = (HOST, PORT)
SIZE = 1500
WINDOW = 0

FILENAME = 'WitcherWall.jpg'
file_size = os.path.getsize(FILENAME)

send_seq = 0
send_ack = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

client_socket, client_addr = server_socket.accept()
CLIENT_PORT = client_addr[1]

print(f"Connection from {client_addr} has been established!")

segment = client_socket.recv(SIZE)
pkt = packet.extract(segment)
rcv_seq = pkt['seq_num']
rcv_ack = pkt['ack_num']
print(f'Received packet with seq={rcv_seq} and ack={rcv_ack}')

WINDOW = pkt['window']
print(f'Window size: {WINDOW}')
send_seq = pkt['ack_num']
send_ack = pkt['seq_num']+1
# send_ack = rcv_seq+SIZE-1
ack_received = 0
total_time = 0

with open(FILENAME,'rb') as file:
    start = time.time()
    while True:
        data = file.read(SIZE)
        if not data:
            print(f'File has been sent')
            client_socket.send(packet.make_pkt(CLIENT_PORT,PORT,send_seq, send_ack, WINDOW, b'FIN',0))
            break
        print(f'Size of data: {len(data)}')
        pkt = packet.make_pkt(CLIENT_PORT,PORT,send_seq, send_ack, WINDOW, data,1)
        # print(pkt)
        client_socket.send(pkt)
        print(f'Sent packet with seq={send_seq} and ack={send_ack}')
        send_seq += len(data)
        # send_ack += len(data)
        WINDOW-=len(data)

        if WINDOW<=0:
            print(f'Window filled')
            end= time.time()
            ack_segment = client_socket.recv(SIZE)
            ack_pkt = packet.extract(ack_segment)
            ack_received+=1
            WINDOW = ack_pkt['window']
            send_ack = ack_pkt['seq_num'] + 1
            send_seq = ack_pkt['ack_num']
            print(f'Window size: {WINDOW}')
            # print(f'Updated ack: {send_ack}')
            # print(f'Updated seq: {send_seq}')
            total_time += (end-start)*1000
            print(f'Time taken: {(end-start)*1000} ms')
            start = time.time()
        # time.sleep(1)

print(f'Average time between cumulative acks: {total_time/ack_received} ms')