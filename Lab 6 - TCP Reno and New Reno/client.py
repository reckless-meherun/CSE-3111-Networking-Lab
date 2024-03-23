import socket
import time
import packet
import os
import random

FILENAME = 'balu.pdf'

mss = 1460
header_size = 129

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12346
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.settimeout(0.5)

buffer = b''
max_buff_size = 1460*50
curr_buff_size = 0
seq=0
ack=0

# buffered_packet = b''

pkt = packet.make_pkt(PORT,PORT,seq,ack,max_buff_size,b'',0)
client.send(pkt)

last_rcv = -1

def packet_dropper():
    return random.randint(1,10)<3


start_time = time.time()
try:
    with open(FILENAME,'wb') as file:
        while True:
            try:
                if packet_dropper(): 
                    print('Packet dropped')
                    if not buffered_packet: client.send(buffered_packet)
                    time.sleep(0.5)
                    continue
                pkt = client.recv(mss+header_size)
            except socket.timeout:
                print('No packet received in 5 seconds')
                continue

            if not pkt:
                break
            
            data = packet.extract(pkt)
            # print(data)
            buffer += data['payload']
            curr_buff_size += len(data['payload'])
            last_rcv = data['seq_num']
            print(f'last_rcv: {last_rcv}')
            seq+=1
            ack+=len(data['payload'])
            

            rwnd = (max_buff_size - curr_buff_size)//mss
            last_rcv+=len(data['payload'])
            print(f'Sending ack for {last_rcv}')
            pkt = packet.make_pkt(PORT,PORT,0,last_rcv,rwnd,b'',0)
            client.send(pkt)
            buffered_packet=pkt

            if curr_buff_size >= max_buff_size:
                file.write(buffer)
                buffer = b''
                curr_buff_size = 0
        if buffer:
            file.write(buffer)
        print('File received')
        client.close()
        print(f'Time taken: {time.time()-start_time}')

except:
    # print('Error occurred')
    client.close()
    print(f'Time taken: {time.time()-start_time}')

file_size = os.path.getsize('balu.pdf')
print(f'Throughput: {(file_size/ (time.time()-start_time))} B/s')

            

            