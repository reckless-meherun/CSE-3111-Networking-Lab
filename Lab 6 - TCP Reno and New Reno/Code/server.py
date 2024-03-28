import socket
import threading
import time
import os
import packet
import matplotlib
matplotlib.use('TkAgg')  # Select TkAgg backend
import matplotlib.pyplot as plt
import numpy as np


RTT_ARRAY = []
CWND_ARRAY = []

cwnd = 16
ssthresh = 16**20
dup_ack = 0
last_ack = -1
last_seq = -1
timeout = 5

FILENAME = 'alu.pdf'


def congestion_avoidance():
    global cwnd
    cwnd = cwnd + 1


def slow_start():
    global cwnd
    cwnd= cwnd * 2


def fast_recovery():
    global ssthresh,cwnd
    ssthresh = cwnd//2
    cwnd= ssthresh + 3


HOST = socket.gethostbyname(socket.gethostname())
PORT = 12346
ADDR = (HOST, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

print(f'Listening on {HOST}:{PORT}')

client_sock, addr = server.accept()
client_sock.settimeout(0.5)
dest_port = addr[1]

pkt = client_sock.recv(1589)
data = packet.extract(pkt)
# print(data)
last_rwnd= data['window']
rwnd = data['window']
recv_ack = data['seq_num']+1

window_size = 1460
mss = 1460

seq = 0
ack = 1

with open(FILENAME, 'rb') as file:
    file_size = os.path.getsize('file_to_send.txt')
    send_seq = 0

    last_send_time = time.time()
    while True:
        curr_sent = 0
        max_cap = min(rwnd, cwnd)
        print(f'rwnd: {rwnd}, cwnd: {cwnd}')
        print(f"Max cap: {max_cap}")

        while curr_sent < max_cap:
            data = file.read(mss)
            if not data:
                break
            # print(f'curr_sent: {curr_sent}')
            print(len(data))
            pkt = packet.make_pkt(PORT, dest_port, seq,
                                  recv_ack, window_size, data, 1)
            client_sock.send(pkt)
            curr_sent += len(data)
            seq += len(data)
            ack+=len(data)
            print(f'ack {ack}')
            print(f'curr_sent: {curr_sent}')

        print(f'curr_sent: {curr_sent}')

        try:
            ack_pkt = client_sock.recv(1589)
        except socket.timeout:
            print('No ack received in 1 seconds')
            print('Back to slow start')
            ssthresh = cwnd//2
            cwnd = 1
            continue
        if ack_pkt:
            ack_pkt = packet.extract(ack_pkt)
            ack = ack_pkt['ack_num']
            print(f'Expecting {seq} got ack_pkt: {ack}')
            if seq == ack:
                CWND_ARRAY.append(cwnd)
                print(f"CWND appended to Array: {cwnd}")
                dup_ack = 0
                print('Received correct ack')
                if cwnd < ssthresh:
                    print('Slow start')
                    slow_start()
                else:
                    print('Congestion avoidance')
                    congestion_avoidance()
            else:
                print('Received duplicate ack')
                dup_ack += 1
                if dup_ack == 3:
                    print('Fast recovery')
                    fast_recovery()
                    dup_ack = 0
                    print(f'cwnd: {cwnd}')
                    print(f'ssthresh: {ssthresh}')
                    print(f'dup_ack: {dup_ack}')

        else:
            print('No ack received')
            break

        if curr_sent < max_cap:
            break
        # time.sleep(1)

print('File sent')

print(f'Throughput: {file_size/(time.time()-last_send_time)} bytes/sec')
print(f'Last rwnd: {last_rwnd}')

client_sock.close()
server.close()


# reno_cwnd = np.array([1, 2, 4, 8, 4, 8, 16, 8, 16, 32])
# reno_time = np.arange(len(reno_cwnd))

# plt.plot(reno_time, reno_cwnd, label='TCP Reno')

# # Labels and title
# plt.xlabel('Time')
# plt.ylabel('Congestion Window Size')
# plt.title('CWND vs Time (TCP Reno vs. New Reno)')
# plt.legend()

# # Show the plot
# plt.grid(True)
# plt.show()
