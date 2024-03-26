import socket
import funcs
import addresses
import threading
import graph

ADDR = addresses.address['D']

adj = funcs.get_adj('D')
# print(adj)

messages_received = set()

neighbors = ['B']

message_serial = 1

def send_msg():
    global message_serial
    print(message_serial)
    message = funcs.encode_message('D',message_serial,adj)
    message_serial+=1
    funcs.broadcast(message,neighbors)



        

def main():
    router_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    router_sock.bind(ADDR)
    router_sock.listen()
    print(f'Server running on {ADDR}. Press Enter to start')
    start = input()

    flood_send_thread = threading.Thread(target=send_msg)
    flood_send_thread.start()

    while True:
        client_sock,addr = router_sock.accept()
        flood_receive_thread = threading.Thread(target=funcs.handle_client,args=(client_sock,addr,adj,messages_received,'D',neighbors))
        flood_receive_thread.start()

if __name__=='__main__':
    main()
