import socket
import threading
import os
import time
import packet
import plot

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9991
ADDR = (HOST, PORT)
SIZE = 1500

FILENAME = 'test.txt'

send_buffer = {}

send_seq = 0
send_ack = 0
last_ack = 0
duplicate_count = 0
alpha = 0.125
beta = 0.25
est_RTT = 0
dev_RTT = 0


def getEstRTT(sampleRTT, est_RTT):
    return (1-alpha)*est_RTT + alpha*sampleRTT


def getDevRTT(sampleRTT, est_RTT, dev_RTT):
    return (1-beta)*dev_RTT + beta*abs(sampleRTT-est_RTT)


def getTimeoutInterval(est_RTT, dev_RTT):
    return est_RTT + 4*dev_RTT


server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(ADDR)
server_sock.listen()

print(f'Server active on {HOST}:{PORT}')

client_sock, addr = server_sock.accept()
dest_port = addr[1]
client_sock.settimeout(5)

print(f'Connection from {addr}')

sampleRTT_file = open('sampleRTT.csv', 'w')
sampleRTT_file.write('SL,SampleRTT\n')
estRTT_file = open('estRTT.csv', 'w')
estRTT_file.write('SL,EstimatedRTT\n')

with open(FILENAME, 'rb') as file:
    file_size = os.path.getsize(FILENAME)

    segment = client_sock.recv(SIZE)

    pkt = packet.extract(segment)

    rcv_payload = pkt['payload']
    rcv_seq = pkt['seq_num']
    rcv_ack = pkt['ack_num']
    rcv_window = pkt['window']
    print(f'Window = {rcv_window}')

    iteration = 1

    while True:
        payload: bytes = file.read(rcv_window)

        if not payload:
            print('Nothing read from file')
            break

        print(f'Size of payload: {len(payload)}')
        send_seq = rcv_ack

        send_ack = rcv_seq+1
        pkt = packet.make_pkt(PORT,dest_port,send_seq,send_ack,rcv_window,payload,1)

        send_ack = rcv_seq+len(rcv_payload)
        pkt = packet.make_pkt(PORT, dest_port, send_seq,
                              send_ack, rcv_window, payload, 1)

        send_buffer[send_seq] = pkt
        client_sock.send(pkt)
        print(f'Sent packet with seq {send_seq} and ack {send_ack}')
        start = time.time()

        try:
            ack_segment = client_sock.recv(SIZE)
        except BlockingIOError:
            continue
        except socket.timeout:
            print('No ACK withing 5 secs')
            break
            # client_sock.send(pkt)
            # print(f'Retransmitted packet')

            

        if ack_segment:
            ack_pkt = packet.extract(ack_segment)
            print(ack_pkt)
            rcv_seq = ack_pkt['seq_num']
            rcv_ack = ack_pkt['ack_num']
            rcv_window = ack_pkt['window']

            if rcv_ack == send_seq+len(payload):
                print(f'Received ACK {rcv_ack}')
                send_buffer.pop(send_seq)
                window = ack_pkt['window']
                last_ack = rcv_ack
                send_seq = rcv_ack
                duplicate_count = 0

            elif rcv_ack == last_ack:
                duplicate_count += 1
                print(f'Duplicate ACK for {last_ack}')

                # fast retransmit
                if duplicate_count == 3:
                    print('3 duplicate ACKs')
                    send_seq = last_ack
                    pkt = send_buffer[send_seq]
                    client_sock.send(pkt)
                    print(
                        f'Retransmitted packet with seq {send_seq} and ack {send_ack}')
                    start = time.time()
                    duplicate_count = 0

            else:
                expected_ack = send_seq+len(payload)
                print(f'Expected ACK: {expected_ack}, Received ACK: {rcv_ack}')

                client_sock.send(pkt)
                print(
                    f'Retransmitted packet with seq {send_seq} and ack {send_ack}')
        else:
            print('No ACK received')

        end = time.time()

        sampleRTT = end-start
        est_RTT = getEstRTT(sampleRTT, est_RTT)
        dev_RTT = getDevRTT(sampleRTT, est_RTT, dev_RTT)
        timeout_interval = getTimeoutInterval(est_RTT, dev_RTT)
        client_sock.settimeout(timeout_interval)
        print(
            f'SampleRTT: {sampleRTT}\nEstimated RTT: {est_RTT}\nDev RTT: {dev_RTT} \nTimeout Interval: {timeout_interval}')

        sampleRTT_file.write(f'{iteration},{round(sampleRTT*1000,4)}\n')
        estRTT_file.write(f'{iteration},{round(est_RTT*1000,4)}\n')

        iteration += 1
        # time.sleep(1)


sampleRTT_file.close()
estRTT_file.close()
try:
    print(f'Throughput: {(file_size/(end-start))/1000.0} bytes/sec')
except ZeroDivisionError:
    # print('Dividing by zero')
    pass
                            
client_sock.close()
server_sock.close()

print('Done!')
# plot.get_line_plot()
