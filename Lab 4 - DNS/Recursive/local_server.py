import socket
import addresses
import pickle
import funcs
import threading
import time

dic = {
    "www.alu.com":('100.20.8.1','A',10),
    'www.google.com': ('9994', 'NS', 86400),
    "www.cse.du.ac.bd": ('9994', 'NS', 86400),
    "www.yahoo.com": ('1.2.3.9999', "A", 86400)
}

def check_time():
    global dic

    while True:
        time.sleep(1)
        
        keys_to_delete = []

        for name, val in dic.items():
            val = list(val)
            val[2] -= 1
            dic[name] = tuple(val)
            # print(val)
            if val[2] == 0:
                print(f'Deleting {name} entry')
                keys_to_delete.append(name)

        for key in keys_to_delete:
            dic.pop(key)




def ask_someone(dns_message, port, server):
    PORT_ADDR = (socket.gethostbyname(socket.gethostname()), port)
    dns_message = pickle.dumps(dns_message)

    print(f'Asking {port} server')
    server.sendto(dns_message, PORT_ADDR)
    response, port_addr = server.recvfrom(1024)
    response = funcs.extract_response(response)
    print(f'From {port} server')
    print(response)

    # response = pickle.dumps(response)

    return response


def handle_client(dns_message, client_addr, server: socket.socket):
    name = dns_message['body']['name']
    type = dns_message['body']['type']
    id = dns_message['header']['id']

    response_type = ''

    if name in dic.keys():
        response = dic[name]
        print(response)

        # checking local cache
        if response[1] == 'A':
            response = funcs.build_response(name, response, id)
            server.sendto(response, client_addr)
            return
        elif response[1] == 'NS':
            dns_message['body']['type'] = response[1]
            dns_message['body']['value'] = response[0]
            port = int(response[0])

            # checking root server
            response = ask_someone(dns_message, port, server)
            print(response)
            if response['body'][1:] != (None,None,None):
                print('Adding to cache')
                dic[response['body'][0]] = response['body'][1],response['body'][2],response['body'][3]
            print(dic)
            response = pickle.dumps(response)
            server.sendto(response, client_addr) # sending the final ans to client
            return
        
            # if response['body'][2] == 'A':
            #     response = pickle.dumps(response)
            #     server.sendto(response, client_addr)
            #     return

    else:
        response = ask_someone(dns_message, addresses.ROOT_PORT, server)
        if response['body'][1:] != (None,None,None):
            print('Adding to cache')
            dic[response['body'][0]] = response['body'][1],response['body'][2],response['body'][3]
        response = pickle.dumps(response)
        server.sendto(response, client_addr)
        return

    # response_type = response['body'][2]

    # port = int(response['body'][1])

    # while response_type != 'A':

    #     response = ask_someone(dns_message, port, server)

    #     if response['body'][2] == 'A':
    #         response = pickle.dumps(response)
    #         server.sendto(response, client_addr)
    #         return

    #     port = int(response['body'][1])


def local_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(addresses.LOCAL_ADDR)
    print(f'Server started on {addresses.LOCAL_ADDR}')
    time_thread = threading.Thread(target=check_time)
    time_thread.start()

    while True:
        query, addr = server.recvfrom(1024)
        query = funcs.extract_query(query)
        print(f'Recv from client {query}')

        handle_client(query, addr, server)


if __name__ == '__main__':
    local_server()
