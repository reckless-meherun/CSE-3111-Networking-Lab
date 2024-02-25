import socket
import funcs
import addresses
import time

def client_init():
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    while True:

        message = input('Enter url and type separated by spaces: ')
        id,message = funcs.build_query(message,)
        start_time = time.time()
        client_sock.sendto(message,addresses.LOCAL_ADDR)
        response,addr = client_sock.recvfrom(1024)

        response = funcs.extract_response(response)
        # print(response)
        if response["body"][1] is not None:
            print(f'Value= {response["body"][1]}')
        else: print('Value not available')
        end_time = time.time()
        
        print("Total time to get the response " + str(end_time-start_time))


if __name__=='__main__':
    client_init()