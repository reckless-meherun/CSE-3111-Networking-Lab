import socket
import addresses
import pickle
import funcs
import threading
import socket
import addresses
import pickle
import funcs
import threading
import time

dic={
    # "www.google.com":('100.20.8.1','A',86400),
    'www.google.com': ('9994','NS',86400),
    "www.cse.du.ac.bd": ('9994','NS',86400),
    "www.yahoo.com":('1.2.3.9999',"A",86400)
}

def ask_someone(dns_message,port,server,client_addr):
    PORT_ADDR = (socket.gethostbyname(socket.gethostname()),port)
    dns_message = pickle.dumps(dns_message)

    print(f'Asking {port} server')
    server.sendto(dns_message,PORT_ADDR)
    response,port_addr = server.recvfrom(1024)
    response = funcs.extract_response(response)
    print(f'From {port} server')
    print(response)


    # response = pickle.dumps(response)

    return response


def handle_client(dns_message,client_addr,server:socket.socket):
    name = dns_message['body']['name']
    type = dns_message['body']['type']
    id = dns_message['header']['id']

    response_type = ''

    # while response_type != 'A':
    if name in dic.keys():
        response = dic[name]
        print(response)
        
        #checking local cache
        if response[1] == type:
            response = funcs.build_response(name,response,id)
            server.sendto(response,client_addr)
            return
        elif response[1]=='NS':
            dns_message['body']['type'] = response[1]
            dns_message['body']['value'] = response[0]
            port = int(response[0])

            #checking root server
            response = ask_someone(dns_message,port,server,client_addr)

            print(response)

            if response['body'][2] == type:
                if response['body'][1:] != (None,None,None):
                    print('Adding to cache')
                    dic[response['body'][0]] = response['body'][1],response['body'][2],response['body'][3]
                response = pickle.dumps(response)
                server.sendto(response,client_addr)
                return
 
    else:
        response = ask_someone(dns_message,addresses.ROOT_PORT,server,client_addr)
        if response['body'][1:] != (None,None,None):
            print('Adding to cache')
            dic[response['body'][0]] = response['body'][1],response['body'][2],response['body'][3]
        # response = pickle.dumps(response)
        # server.sendto(response,client_addr)

    if response['body'][1:] == (None,None,None):
        response = pickle.dumps(response)
        server.sendto(response,client_addr)
        return

    response_type = response['body'][2]
    if response_type == type:
        response = pickle.dumps(response)
        server.sendto(response,client_addr)
        return
        
    port = int(response['body'][1])

    while response_type != type:

        response = ask_someone(dns_message,port,server,client_addr)

        if response['body'][2] == type:
            response = pickle.dumps(response)
            server.sendto(response,client_addr)
            return
        
        port = int(response['body'][1])



def local_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(addresses.LOCAL_ADDR)
    print(f'Server started on {addresses.LOCAL_ADDR}')

    while True:
        query,addr = server.recvfrom(1024)
        query = funcs.extract_query(query)
        print(f'Recv from client {query}')

        start_time = time.time()
        handle_client(query,addr,server)
        end_time = time.time()
        
        print("Total time to get a response : " + str((end_time - start_time)*10e3) + " ms")


if __name__=='__main__':
    local_server()


