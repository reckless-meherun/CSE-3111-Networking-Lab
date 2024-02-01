import socket
import sys #to implement command line and terminal commands into python file
from users import users
import threading
import random
import uuid
import pickle

ERROR_RATE = 3

conn: socket.socket

def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False

def create_socket():
    try:
        global host
        global port
        global sock
        host = socket.gethostbyname(socket.gethostname()) #empty because we are goting to put this server.py file into our server and the IP address of the host is gonna be itself
        port = 9005
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error " + str(msg))
        
        
# why binding? Might be able to open up a line of communication with sockets, but it needs to know about the info of the device it is supposed to be communicating with

def bind_socket():
    try:
        global host
        global port
        global sock

        sock.bind((host, port))
        print("binding the port "+str(port)) 
        sock.listen() 
        # why important? the server should be continuously listening to the connections from various computers
        # 5 is the number of connections it is going to tolerate and after that it is going to throw error
        
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying...")
        sock.close()
        bind_socket()


def create_transID():
    random_uuid = uuid.uuid4()
    print(f'Transaction ID: {random_uuid}')
    return random_uuid

    
def socket_accept():
    while True:
        global conn
        conn, address = sock.accept() #gives us two data : object of a connection and a list of IP address and a port
        # the next line will be executed only when a connection is accepted
        print("Connection has been established! "+ "\nIP : " + address[0] + "\nAddress : " + str(address[1]))

        while True:
            name = conn.recv(1024).decode()
            password= conn.recv(1024).decode()
            print(name,password)

            logged_user = None
            for user in users:
                if name in user['name'] and password in user['pass']:
                    logged_user = user
                    break
            
            print(logged_user)
            if logged_user == None:
                conn.send('WRONG_CRED'.encode())
                continue
            
            conn.send('LOGGED_IN'.encode())
            status = conn.recv(1024).decode()

            if status != 'LOGGED_IN':
                continue

            while True:
                available_options = '''\nSelect one
                1. Check Balance
                2. Withdraw 
                3. Deposit'''
                conn.send(available_options.encode())

                option = conn.recv(1024).decode()
                print(f'option 1= {option}')

                if not option.isdigit() or int(option) not in [1,2,3]:
                    conn.send('INVALID_OPTION'.encode())
                    acknowledge = conn.recv(1024).decode()
                    continue
                else:
                    # print('valid option')
                    conn.send('VALID_OPTION'.encode())
                    print('VALID')
                    acknowledge = conn.recv(1024)
                    print(acknowledge.decode())
                    # print('VALID')
                
                
                    
                print(f'option = {option}')

                if option=='1':
                    check_balance(logged_user)
                    
                            
                    
                elif option == '2':  
                    withdraw(logged_user)          
                                          
                    
                elif option == '3':
                    deposit(logged_user)
                    

def check_balance(logged_user):
    print('selected 1')
    # conn.send(str(logged_user['balance']).encode())
    print(f'Balance: {logged_user['balance']}')
    conn.send(str(logged_user['balance']).encode())
    ack = conn.recv(1024).decode()

def withdraw(logged_user):
    conn.send('AMOUNT'.encode())
    withdrawal_amount = conn.recv(1024).decode()
    print(f'with_amount = {float(withdrawal_amount)}')

    if not is_float(withdrawal_amount):
        data = {
            'status':'ERROR',
            'message': 'INVALID_IN'
        }
        message = pickle.dumps(data)
        conn.send(message)
        stat = conn.recv(1024).decode()
        print(f'stat = {stat}')
        return
    

    elif float(withdrawal_amount)>logged_user['balance']:
        data = {
            'status':'ERROR',
            'message': 'NO_BLNC'
        }
        message = pickle.dumps(data)
        conn.send(message)
        stat = conn.recv(1024).decode()
        print(f'stat = {stat}')
        return
    

    logged_user['balance'] -= float(withdrawal_amount)
    tranXID = f'WITH_{create_transID()}'
    data = {
        'status': 'OK',
        'tid': tranXID,
        'withdraw': float(withdrawal_amount),
        'balance': logged_user['balance']
    }
    message = pickle.dumps(data)
    conn.send(message)
    status = conn.recv(1024).decode()
    print(f'status = {status}')
    
    if status == 'ERROR_WITHDRAW':
        logged_user['balance'] += float(withdrawal_amount)
        send_msg = 'ROLLED_BACK'
        conn.send(send_msg.encode())      
        conn.recv(1024).decode()

    elif status == 'WITHDRAW_RECV':
        print('WITHDRAW RECEIVED')

def deposit(logged_user):
    conn.send('AMOUNT'.encode())
    deposit_amount = conn.recv(1024).decode()
    print(deposit_amount)

    if not is_float(deposit_amount):
        data = {
            'status':'ERROR',
            'message': 'INVALID_IN'
        }
        message = pickle.dumps(data)
        conn.send(message)
        return
    

    logged_user['balance'] += float(deposit_amount)
    tranXID = f'DEP_{create_transID()}'
    data = {
        'status': 'OK',
        'tid': tranXID,
        'deposit': float(deposit_amount),
        'balance': logged_user['balance']
    }
    message = pickle.dumps(data)
    conn.send(message)
    
    status = conn.recv(1024).decode()

def main():
    create_socket()
    bind_socket()
    socket_accept()
    
if __name__=='__main__':  
    main()   