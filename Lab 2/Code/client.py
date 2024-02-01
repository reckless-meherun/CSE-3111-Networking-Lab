import socket
import users
import random
import time
import pickle
import numpy as np
# import matplotlib.pyplot as plt


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9005
ERROR_RATE = 0
ITERATIONS = 100
logged_in = False
avg_times = []

times = []

client_socket: socket.socket
count = 0

# def detect_error(response, handle_case, error_rate):
#     chance = random.randint(1,10)

#     if chance <= (error_rate*10)/100:
#         client_socket.send('ERROR'.encode())
#     else:
#         handle_case(response)

def authenticate():
    name = input('Enter name: ')
    client_socket.send(name.encode())

    password = input('Enter password: ')
    client_socket.send(password.encode())

    message= client_socket.recv(1024).decode()

    logged_in = message=='LOGGED_IN'

    if logged_in:
        client_socket.send('LOGGED_IN'.encode())
    
    return message == 'LOGGED_IN'

def select_comm(client_socket):
    options = client_socket.recv(1024).decode()
    print(options)

    selected_comm = input('Enter: ')

    client_socket.send(selected_comm.encode())
    select_response = client_socket.recv(1024).decode()
    print(f'option response={select_response}')
    
    return select_response=='VALID_OPTION',selected_comm


def respond(client_socket):
    global logged_in
    global count
    global start_time
    global end_time
    

    selected_comm:int

    iteration = 0
    
    # start_time = time.time()
    while iteration<ITERATIONS:
        options = client_socket.recv(1024).decode()
        print(options)
        # is_valid, selected_comm = select_comm(client_socket)
        chance = -1
        while chance<=ERROR_RATE: 
            chance = random.randint(1,100)
        print(chance)
        selected_comm = random.randint(1,3)
        print(f'selected option={selected_comm}')
        # selected_comm = 1
        client_socket.send(f'{selected_comm}'.encode())
        is_valid = True

        select_response = client_socket.recv(1024).decode()
        # print(f'option response={select_response}')
        is_valid= (select_response == 'VALID_OPTION')

        start = time.time()

        if not is_valid: 
            print('Invalid option. Try again.')
            client_socket.send('INVALID_OPTION'.encode())
            continue
        else:
            client_socket.send('VALID_OPTION'.encode())
        # print(selected_comm)
        selected_comm = int(selected_comm)

        match selected_comm:
            case 1:
                balance_check(client_socket)
                # count += 1
            case 2:
                # print('withdraw')
                withdrawal(client_socket)
            case 3:
                deposit(client_socket)
        
        end = time.time()
        iteration+=1
        times.append(end-start)
        print(f'Time to send = {end-start}')

    # end_time = time.time()

def client_init():
    global client_socket
    global ERROR_RATE
    global logged_in
    global avg_times

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))

    while not logged_in:
        if not authenticate():
            print('Wrong credentials. Try again.')
        else:
            print('Logged in')
            logged_in = True

    while ERROR_RATE<10:
        respond(client_socket)

        time_array = np.array(times)
        # print(times)
        mean = time_array.mean()*1000
        print(f'Avg time = {mean} ms')
        avg_times.append(mean)
        ERROR_RATE+=1
    print(avg_times)
    

def balance_check(client_socket):
    balance = client_socket.recv(1024).decode()
    client_socket.send('BALANCE'.encode())
    print(f'Balance: {balance}')

def withdrawal(client_socket):
    # while True:
    print(client_socket.recv(1024).decode())
    amount = random.randint(1,5000)
    # amount = input('Enter amount: ')
    print(f'with_amount: {amount}')
    client_socket.send(f'{float(amount)}'.encode())
    response_pickle = client_socket.recv(1024)
    response = pickle.loads(response_pickle)

    chance = random.randint(1,10)
    print(chance)
    if chance <= ERROR_RATE:
        client_socket.send('ERROR_WITHDRAW'.encode())
        response = client_socket.recv(1024).decode()
        print(response)
        if response == 'ROLLED_BACK':
            print('An error occurred. Try again')
            client_socket.send('ROLLBACK_RECV'.encode())
            return
    else:
        client_socket.send('WITHDRAW_RECV'.encode())
        if response['status'] == 'ERROR' and response['message'] == 'INVALID_IN':
            print('Not a valid input. Try again.')
            return
        elif response['status'] == 'ERROR' and response['message'] == 'NO_BLNC':
            print('Insufficient balance. Try again. ')
            return
    print(response)
    withdraw=response['withdraw']
    balance = response['balance']

    print(f'{withdraw} withdrawn. Total balance: {balance}')

def deposit(client_socket):
    print(client_socket.recv(1024).decode())
    # amount = input('Enter amount: ')
    amount = random.randint(1,5000)
    print(f'dep_amount={amount}')
    client_socket.send(str(amount).encode())
    response_pickle = client_socket.recv(1024)
    response = pickle.loads(response_pickle)

    if response['status'] == 'ERROR' and response['message'] == 'NO_IN':
        print('Not a valid input. Try again.')
        return
    
    print(response)
    client_socket.send('DEPOSIT_RECV'.encode())
    deposit=response['deposit']
    balance = response['balance']

    print(f'{str(deposit)} deposited. New balance: {balance}')

    
    

if __name__=='__main__':
    client_init()

    # x = [ i for i in np.arange(start=0,stop=100,step=10)]
    # y = avg_times

    # plt.plot(x, y, marker='o', linestyle='-')
    # plt.title('Average Times Over X')
    # plt.xlabel('Error Rate(%)')
    # plt.ylabel('Average Times (ms)')
    # plt.xticks(np.arange(0, 101, step=10))
    # plt.grid(True)

    
    # plt.show()
    