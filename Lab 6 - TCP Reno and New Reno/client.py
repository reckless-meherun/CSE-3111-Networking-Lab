import socket
import time
import packet

FILENAME = 'recv.png'

mss = 1460
header_size = 129

HOST = socket.gethostbyname(socket.gethostname())
PORT = 12345
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client.settimeout(5)

buffer = b''
max_buff_size = 1460*50
curr_buff_size = 0

last_rcv = -1

start_time = time.time()
try:
    with open(FILENAME,'wb') as file:
        while True:
            try:
                pkt = client.recv(mss+header_size)
            except socket.timeout:
                print('No packet received in 5 seconds')
                continue

            if not pkt:
                break
                
            data = packet.extract(pkt)
            buffer += data['payload']
            curr_buff_size += len(data['payload'])
            last_rcv = data['seq_num']
            print(f'last_rcv: {last_rcv}')
            

            rwnd = (max_buff_size - curr_buff_size)//mss
            pkt = packet.make_pkt(PORT,PORT,0,last_rcv+len(data['payload']),rwnd,b'',0)
            client.send(pkt)

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

            

            