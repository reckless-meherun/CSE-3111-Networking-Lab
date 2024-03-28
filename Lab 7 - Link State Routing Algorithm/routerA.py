import socket
import funcs
import addresses
import threading
import graph
import os
import random
import time

node = os.path.basename(__file__).split('.')[0][-1]


ADDR = addresses.address[node]

adj = funcs.get_adj(node)
print(adj)

messages_received = set()

neighbors = [vertex for vertex in adj[node].keys()]
print(neighbors)

message_serial = 1

def send_msg():
    global message_serial
    message = funcs.encode_message(node,message_serial,adj)
    message_serial+=1
    funcs.broadcast(message,neighbors)
    
    
def updateLinkWeight():
    global adj,neighbors,message_serial
    print("Broadcast starting")
    while True:
        time.sleep(30)
        dest = neighbors[random.randint(0,len(neighbors)-1)]
        adj[node][dest]=random.randint(1,10)
        print(f'Edge {node} {dest} changed to {adj[node][dest]}')
        message = funcs.encode_message(node,message_serial,adj)
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
    
    update_thread = threading.Thread(target=updateLinkWeight)
    update_thread.start()

    while True:
        client_sock,addr = router_sock.accept()
        flood_receive_thread = threading.Thread(target=funcs.handle_client,args=(client_sock,adj,messages_received,node,neighbors))        
        flood_receive_thread.start()

if __name__=='__main__':
    main()
