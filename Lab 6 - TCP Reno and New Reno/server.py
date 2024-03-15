import socket
import threading
import time
import os
import packet


cwnd = 1
ssthresh = 16
dup_ack = 0
last_ack = -1
last_seq = -1
timeout = 5

FILENAME = 'tcp_flow.png'


def congestion_avoidance(curr_cwnd):
    return curr_cwnd + 1

def slow_start(curr_cwnd):
    return curr_cwnd * 2

def fast_recovery(curr_cwnd):
    return curr_cwnd // 2 + 3


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

print(f'Listening on {HOST}:{PORT}')

client_sock,addr = server.accept()
client_sock.settimeout(5)
window_size = 1460
rwnd = 5
mss = 1460

seq = 0
ack = 0

with open(FILENAME,'rb') as file:
    file_size = os.path.getsize('file_to_send.txt')

    while True:
        curr_sent = 0
        max_cap = min(rwnd,cwnd)
        print(f"Max cap: {max_cap}")

        while curr_sent < max_cap:
            data = file.read(mss)
            if not data:
                break
            pkt = packet.make_pkt(12345,12345,curr_sent,0,window_size,data,1)
            client_sock.send(pkt)
            curr_sent += 1
            ack += len(data)
            seq += len(data)

            last_send_time = time.time()
        print(f'curr_sent: {curr_sent}')


        try:
            ack_pkt = client_sock.recv(1589)
        except socket.timeout:
            print('No ack received in 5 seconds')
            break
        if ack_pkt:
            ack_pkt = packet.extract(ack_pkt)
            print(f'ack_pkt: {ack_pkt}')
            if ack_pkt['ack_num'] == ack:
                dup_ack = 0
                print('Received correct ack')
                if cwnd < ssthresh:
                    cwnd = slow_start(cwnd)
                else:
                    cwnd = congestion_avoidance(cwnd)
            else:
                print('Received duplicate ack')
                dup_ack += 1
                if dup_ack == 3:
                    ssthresh = cwnd // 2
                    cwnd = fast_recovery(cwnd)
                    dup_ack = 0
                    print(f'cwnd: {cwnd}')
                    print(f'ssthresh: {ssthresh}')
                    print(f'dup_ack: {dup_ack}')
            if time.time() - last_send_time > timeout:
                ssthresh = cwnd // 2
                cwnd = 1
                print(f'cwnd: {cwnd}')
                print(f'ssthresh: {ssthresh}')
                print(f'dup_ack: {dup_ack}')

        else:
            print('No ack received')
            break

        if curr_sent < max_cap:
            break
    
print('File sent')
    
print(f'Throughput: {file_size/(time.time()-last_send_time)} bytes/sec')

client_sock.close()
server.close()






            








