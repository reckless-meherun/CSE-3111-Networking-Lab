import socket
import threading
import time
import os
import packet
import matplotlib
matplotlib.use('TkAgg')  # Select TkAgg backend
import matplotlib.pyplot as plt
import numpy as np

cwnd = 16
ssthresh = 16**20
dup_ack = 0
last_ack = -1
last_seq = -1
timeout = 5

FILENAME = 'alu.pdf'

RTT_ARRAY = []
CWND_ARRAY = []

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
rwnd = data['window']
recv_ack = data['seq_num']+1

window_size = 1460
mss = 1460

seq = 0
ack = 0

half_window_time = 0.5
dup_flag = False

with open(FILENAME, 'rb') as file:
    file_size = os.path.getsize('file_to_send.txt')
    send_seq = 0
    duplicate_start = time.time()
    fast_recovery_on = True
    
    last_send_time = time.time()
    while True:
        RTT_start = time.time()
        curr_sent = 0
        max_cap = min(rwnd, cwnd)
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
            recv_ack = ack_pkt['seq_num']+1
            if recv_ack == ack:                
                dup_ack = 0
                print('Received correct ack')
                if cwnd < ssthresh:
                    slow_start()
                else:
                    congestion_avoidance()
            else:
                CWND_ARRAY.append(cwnd)
                print(f"CWND appended to Array: {cwnd}")
                print('Received duplicate ack')
                dup_ack += 1
                if dup_ack == 3:
                    duplicate_end = time.time()
                    if(duplicate_end - duplicate_start > half_window_time):
                        fast_recovery()
                        dup_ack = 0
                        print(f'cwnd: {cwnd}')
                        print(f'ssthresh: {ssthresh}')
                        print(f'dup_ack: {dup_ack}')
                        if(dup_flag == False):
                            dup_flag = True 
                    elif dup_flag:
                        dup_ack = 0 

        else:
            print('No ack received')
            break

        if curr_sent < max_cap:
            break
        
        RTT_end = time.time()
        RTT = RTT_start - RTT_end
        RTT_ARRAY.append(RTT)

        # time.sleep(1)
        
    
print('File sent')

print(f'Throughput: {file_size/(time.time()-last_send_time)} bytes/sec')

client_sock.close()
server.close()


# # Simulate a sawtooth pattern for Reno's CWND
# reno_cwnd = np.array([1, 2, 4, 8, 4, 8, 16, 8, 16, 32])
# reno_time = np.arange(len(reno_cwnd))

# # Simulate a smoother curve for New Reno's CWND with "recover" point
# new_reno_cwnd = np.array([1, 2, 4, 8, 6, 10, 16, 12, 18, 32])
# new_reno_time = np.arange(len(new_reno_cwnd))

# # Plot CWND vs Time for Reno and New Reno
# plt.plot(reno_time, reno_cwnd, label='TCP Reno')
# plt.plot(new_reno_time, new_reno_cwnd, label='TCP New Reno')

# # Labels and title
# plt.xlabel('Number of RTTs')
# plt.ylabel('Congestion Window Size (in segments)')
# plt.title('CWND vs Number of RTTs (TCP Reno vs. New Reno)')
# plt.legend()

# # Show the plot
# plt.grid(True)
# plt.show()
