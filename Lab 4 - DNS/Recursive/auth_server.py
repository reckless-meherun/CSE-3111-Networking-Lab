import socket
import addresses
import pickle
import funcs
import time
import threading

dic = {
    "www.google.com": ('100.20.8.1', 'A', 86400),
    "www.cse.du.ac.bd": ('192.0.2.3', 'A', 86400),
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


def handle_client(dns_message, tld_addr, server: socket.socket):
    print(f'From TLD {dns_message}')
    name = dns_message['body']['name']
    type = dns_message['body']['type']
    id = dns_message['header']['id']

    if name in dic.keys():
        response = dic[name]

        dns_message['body']['type'] = response[1]
        dns_message['body']['value'] = response[0]

        response = funcs.build_response(name, response, id)

    else:
        response = funcs.build_response(name, (None,None,None), id, ans_no=0)
        print('Not available')

    print(pickle.loads(response))
    server.sendto(response, tld_addr)


def tld_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(addresses.AUTH_ADDR)
    print(f'Server started on {addresses.AUTH_ADDR}')
    time_thread = threading.Thread(target=check_time)
    time_thread.start()

    while True:
        query, addr = server.recvfrom(1024)
        query = funcs.extract_query(query)

        print(f'Recv from local {query}')
        handle_client(query, addr, server)


if __name__ == '__main__':
    tld_server()
