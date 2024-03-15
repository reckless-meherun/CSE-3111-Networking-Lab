import socket
import threading
import time
import os
import packet


cwnd = 1
ssthresh = 400
dup_ack = 0
last_ack = -1
last_seq = -1
timeout = 5

FILENAME = 'alu.pdf'


def congestion_avoidance(curr_cwnd):
    return curr_cwnd + 1

def slow_start(curr_cwnd):
    return curr_cwnd * 2

def fast_recovery(curr_cwnd):
    global ssthresh
    ssthresh = curr_cwnd//2
    return ssthresh + 3


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

print(f'Listening on {HOST}:{PORT}')

client_sock,addr = server.accept()
client_sock.settimeout(5)
dest_port = addr[1]

pkt = client_sock.recv(1589)
data = packet.extract(pkt)
# print(data)
rwnd = data['window']
recv_ack = data['seq_num']+1

window_size = 1460
mss = 1460

seq = 0
ack = 0

with open(FILENAME,'rb') as file:
    file_size = os.path.getsize('file_to_send.txt')
    send_seq=0


    last_send_time = time.time()
    while True:
        curr_sent = 0   
        max_cap = min(rwnd,cwnd)
        print(f"Max cap: {max_cap}")

        while curr_sent < max_cap:
            data = file.read(mss)
            if not data:
                break
            # print(f'curr_sent: {curr_sent}')
            print(len(data))
            pkt = packet.make_pkt(PORT,dest_port,seq,recv_ack,window_size,data,1)
            client_sock.send(pkt)
            curr_sent += len(data)
            seq+=len(data)
            print(f'curr_sent: {curr_sent}')

        print(f'curr_sent: {curr_sent}')


        try:
            ack_pkt = client_sock.recv(1589)
        except socket.timeout:
            print('No ack received in 5 seconds')
            break
        if ack_pkt:
            ack_pkt = packet.extract(ack_pkt)
            recv_ack = ack_pkt['seq_num']+1
            print(f'ack_pkt: {ack_pkt}')
            if recv_ack == ack:
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






            








