import socket

HOST = '10.33.3.9'
PORT = 9004
client_socket: socket.socket

def client_init():
    global client_socket

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

    request_service()

def request_service():
    while True:
        if authenticated(): 
            break
        
    
    print('hello')
    while True:
        options = client_socket.recv(1024).decode()
        print(options)
        select_option()


def authenticated():
    name: str
    password: str

    name = input('Enter name: ')
    client_socket.send(name.encode())
    password = input('Enter password: ')
    client_socket.send(password.encode())

    confirmation = client_socket.recv(1024).decode()
    # print(confirmation)  
    if confirmation!='200':
        print('Wrong credentials. Try again.')
    return confirmation=='200'

def select_option():
    option = input('Select: ')

    client_socket.send(option.encode())
    confirmation = client_socket.recv(1024).decode()
    if confirmation=='500':
        print('Error selecting. Try again.')
        return
    
    match option:
        case '1':
            check_balance()
        case '2':
            withdraw()
        case '3':
            deposit()
    


def check_balance():
    balance = client_socket.recv(1024).decode()
    print(f'Your balance is: {balance}')
    client_socket.send('200'.encode())

def withdraw():
    acknowledge = client_socket.recv(1024).decode()

    if not acknowledge == '200':
        print('Error. Try again')
        return
    amount = input('Enter amount:')
    client_socket.send(amount.encode())
    print(client_socket.recv(1024).decode())

def deposit():
    acknowledge = client_socket.recv(1024).decode()

    if not acknowledge == '200':
        print('Error. Try again')
        return
    amount = input('Enter amount:')
    client_socket.send(amount.encode())
    print(client_socket.recv(1024).decode())



client_init()