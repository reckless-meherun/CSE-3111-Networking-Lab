import socket
import funcs
import addresses


def client_init():
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # client_sock.sendto(b'',addresses.LOCAL_ADDR)

    while True:

        message = input('Enter url and type separated by spaces: ')
        id,message = funcs.build_query(message,)
        client_sock.sendto(message,addresses.LOCAL_ADDR)
        response,addr = client_sock.recvfrom(1024)

        response = funcs.extract_response(response)
        # print(response)
        # print(response['body'][1])

        if response["body"][1] is not None:
            print(f'Value= {response["body"][1]}')
        else: print('Value not available')


if __name__=='__main__':
    client_init()