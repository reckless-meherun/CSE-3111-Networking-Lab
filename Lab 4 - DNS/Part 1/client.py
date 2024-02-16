import socket
import struct
import funcs

ADDR = (socket.gethostbyname(socket.gethostname()),4487)
SIZE = 1024

def main():
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    try:
        while True:
            message = input('Enter url: ')
            id,message = funcs.build_query(message)

            client_sock.sendto(message,ADDR)

            msg, addr = client_sock.recvfrom(SIZE)

            message = funcs.extract_response(msg)
            print(message)

            header,data = message['header'],message['body']

            print(f'{header}{data}')

            if data[1] is not None:
                print(f'Value= {data[1]}')
            else: print('Value not available')
    except KeyboardInterrupt:
        print('Disconnected!')

if __name__=='__main__':
    main()