import socket
import addresses
import pickle
import funcs

dic={
    "www.google.com":('9992','NS',86400),
    "www.cse.du.ac.bd": ('192.0.2.3','A',86400),
    "www.yahoo.com":('4489',"NS",86400)
}

def handle_client(dns_message,local_addr,server:socket.socket):
    print(f'From Root {dns_message}')
    name = dns_message['body']['name']
    type = dns_message['body']['type']
    id = dns_message['header']['id']

    if name in dic.keys():
        response = dic[name]
        
        dns_message['body']['type'] = response[1]
        dns_message['body']['value'] = response[0]

        
        response = funcs.build_response(name,response,id)
    
    
    else:
        response = funcs.build_response(name,(),id,ans_no=0)
        print('Not available')

    print(pickle.loads(response))
    server.sendto(response,local_addr)



def tld_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(addresses.TLD_ADDR)
    print(f'Server started on {addresses.TLD_ADDR}')

    while True:
        query,addr = server.recvfrom(1024)
        query = funcs.extract_query(query)

        print(f'Recv from local {query}')
        handle_client(query,addr,server)

if __name__=='__main__':
    tld_server()