import socket
import sys #to implement command line and terminal commands into python file
from users import users
import threading

conn: socket.socket

def create_socket():
    try:
        global host
        global port
        global sock
        host = '10.33.3.9' #empty because we are goting to put this server.py file into our server and the IP address of the host is gonna be itself
        port = 9004
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

def handle_client():
    while True:
        name = conn.recv(1024).decode()
        password= conn.recv(1024).decode()
        print(name,password)

        logged_user = None
        for user in users:
            if name in user['name'] and password in user['pass']:
                logged_user = user
                break

        if logged_user == None:
            conn.send('400'.encode())
            continue
        
        conn.send('200'.encode())

        while True:
            available_options = '''\nSelect one
            1. Check Balance
            2. Withdraw 
            3. Deposit'''
            conn.send(available_options.encode())

            option = conn.recv(1024).decode()

            if not option.isdigit() or int(option) not in [1,2,3]:
                conn.send('500'.encode())
                continue
            else:
                conn.send('200'.encode())
            
            # conn.send(str(logged_user['balance']).encode())
            # print('habijabi')

            if option=='1':
                conn.send(str(logged_user['balance']).encode())
                ack = conn.recv(1024).decode()
            elif option == '2':            
                conn.send('200'.encode())
                withdrawal_amount = conn.recv(1024).decode()
                logged_user['balance'] -= float(withdrawal_amount)
                send_msg = 'Withdrawal was successful! Current balance : ' + str(logged_user['balance'])
                conn.send(send_msg.encode())
                
            else:
                conn.send('200'.encode())
                deposit_amount = conn.recv(1024).decode()
                logged_user['balance'] += float(deposit_amount)
                send_msg = 'Deposit was successful! Current balance : ' + str(logged_user['balance'])
                conn.send(send_msg.encode())


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

            if logged_user == None:
                conn.send('400'.encode())
                continue
            
            conn.send('200'.encode())

            while True:
                available_options = '''\nSelect one
                1. Check Balance
                2. Withdraw 
                3. Deposit'''
                conn.send(available_options.encode())

                option = conn.recv(1024).decode()

                if not option.isdigit() or int(option) not in [1,2,3]:
                    conn.send('500'.encode())
                    continue
                else:
                    conn.send('200'.encode())
                
                # conn.send(str(logged_user['balance']).encode())
                # print('habijabi')

                if option=='1':
                    conn.send(str(logged_user['balance']).encode())
                    ack = conn.recv(1024).decode()
                elif option == '2':            
                    conn.send('200'.encode())
                    withdrawal_amount = conn.recv(1024).decode()
                    logged_user['balance'] -= float(withdrawal_amount)
                    send_msg = 'Withdrawal was successful! Current balance : ' + str(logged_user['balance'])
                    conn.send(send_msg.encode())
                    
                else:
                    conn.send('200'.encode())
                    deposit_amount = conn.recv(1024).decode()
                    logged_user['balance'] += float(deposit_amount)
                    send_msg = 'Deposit was successful! Current balance : ' + str(logged_user['balance'])
                    conn.send(send_msg.encode())
        

    conn.close()

def main():
    create_socket()
    bind_socket()
    socket_accept()
    
    
    
main()    