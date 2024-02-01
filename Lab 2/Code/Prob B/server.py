import socket
import users
import threading

server_socket: socket.socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9080

def handle_connection():
    client_socket,client_address = server_socket.accept()

    print(f'Connection from {client_address}')

    # handle_request(client_socket)

    return client_socket,client_address

def authenticate(client_socket:socket.socket):
    name = client_socket.recv(1024).decode()
    if name:
        print(f'Name: {name}')
    password = client_socket.recv(1024).decode()
    if password:
        print(f'Password: {password}')
    logged_in = False
    logged_user = None
    if not name:
        return None
    
    for user in users.users:
        if user['name'] == name and user['pass']==password:
            logged_in=True
            logged_user = user
            break
    if not logged_in:
        client_socket.send(f'OUT'.encode())
        return None

    client_socket.send('IN'.encode())
    return logged_user

def select_comm(client_socket:socket.socket):
    comm_list = '''Please Select
    1. CHECK BALANCE
    2. CASH WITHDRAWAL
    3. CASH DEPOSIT'''

    client_socket.send(comm_list.encode())

    command = client_socket.recv(1024).decode()

    if (not command.isdigit()) or  int(command) not in [1,2,3]:
        client_socket.send('OUT'.encode())
        return None
    
    client_socket.send('IN'.encode())
    return int(command)


def handle_request(client_socket: socket.socket):
    while True:

        logged_user = authenticate(client_socket)
        if logged_user is None:
            continue
        
        
        while True:
            command = None

            while command is None:
                command = select_comm(client_socket)
            print(command)
            
            match command:
                case 1:
                    balance_check(logged_user,client_socket)
                case 2:
                    withdrawal(logged_user,client_socket)
                case 3:
                    deposit(logged_user,client_socket)
        
                
def balance_check(logged_user,client_socket):
    client_socket.send(str(logged_user['balance']).encode())

def withdrawal(logged_user,client_socket):
    while True:
        amount = client_socket.recv(1024).decode()

        if not amount.isdigit():
            client_socket.send('NO_IN'.encode())
            continue
        

        if int(amount)>logged_user['balance']:
            client_socket.send('NO_BLNC'.encode())
            continue
        else: break 
    
    logged_user['balance'] -= int(amount)

    client_socket.send(f'{str(amount)} {logged_user['balance']}'.encode())

def deposit(logged_user,client_socket):
    amount = client_socket.recv(1024).decode()

    if not amount.isdigit():
        client_socket.send('NO_IN'.encode())
        return

    
    logged_user['balance']+=int(amount)
    client_socket.send(f'{amount} {logged_user['balance']}'.encode())

    


def server_init():
    global server_socket

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))
    print(f'Server live on {HOST}:{PORT}')

    server_socket.listen()

    while True:
        client_socket,client_address = handle_connection()

        client_thread = threading.Thread(target=handle_request, args=(client_socket,))
        client_thread.start()

    # handle_request(client_socket)


if __name__=='__main__':
    server_init()