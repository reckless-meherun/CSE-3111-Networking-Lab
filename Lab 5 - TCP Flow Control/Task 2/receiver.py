import socket
import time
import os
import random
import packet

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9991
ADDR = (HOST,PORT)

FILENAME = 'received.txt'

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(ADDR)
client_sock.settimeout(5)

print(f'Connected to {HOST}:{PORT}')


rcv_window = 1400
rcv_ack = 1400
rcv_seq = 0

pkt = packet.make_pkt(0,PORT,rcv_seq,rcv_ack,rcv_window,'',0)
client_sock.send(pkt)

print('Receiving data...')

start = time.time()

with open(FILENAME,'wb') as file:
    while True:
        try:
            segment = client_sock.recv(1529)

            if not segment:
                print('No packet received')
                break

            pkt = packet.extract(segment)
            send_seq = pkt['seq_num']
            send_ack = pkt['ack_num']
            print(f'Received packet with seq {send_seq} and ack {send_ack}')
            print(f'Payload: {len(pkt["payload"])}')

            if send_seq == rcv_ack:
                rcv_ack += len(pkt['payload'])
                print(f'Updated ack to {rcv_ack}')
                file.write(pkt['payload'])
                print(f'Received {send_seq} and wrote to file')
                pkt = packet.make_pkt(0,PORT,rcv_seq,rcv_ack,rcv_window,'ACK',0)
                client_sock.send(pkt)
                print(f'Sent ACK for {rcv_ack}')
            elif pkt['window']<rcv_window:
                file.write(pkt['payload'])
                print(f'File received completely')
                break
            else:
                print(f'Packet with seq {send_seq} dropped')
                pkt = packet.make_pkt(0,PORT,rcv_seq,rcv_ack,rcv_window,'ACK',0)
                client_sock.send(pkt)
                print(f'Sent ACK for {rcv_ack}')
        except socket.timeout:
            print('Timeout')
            break
        except ConnectionResetError:
            print('Connection aborted')
            break
        # time.sleep(1)

end = time.time()
print(f'Time taken: {end-start} secs')
file_size = os.path.getsize(FILENAME)
print(f'File size: {file_size} bytes')
print(f'Throughput: {file_size/(end-start)} bytes/sec')
client_sock.close()
print('Connection closed')