import socket
import pickle
import os
import tqdm

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
sock: socket.socket

def list(sock):
    print('\nFiles:')
    response = sock.recv(1024).decode()
    print(f'{response}\n')

def upload(sock):
    response = sock.recv(1024).decode()
    print(response)
    filename = input('Enter filename: ')
    filepath = os.path.join('./client_files',filename)

    try:
        with open(filepath,'rb') as f:
            content = f.read()
        response = {
            'status': 'OK',
            'filename': filename,
            'content': content
        }
        success = True

    except FileNotFoundError:
        print('File does not exist')
        response = {
            'status': 'ERROR',
        }
        success = False

    response = pickle.dumps(response)
    sock.send(f'{len(response)}'.encode())
    sock.recv(1024).decode()
    sock.send(response)

    if success: print(f'Uploaded {filepath}')
    else: print('Try again.')
    
def download(sock):
    response = sock.recv(1024).decode()
    print(response)
    filename = input('Enter filename: ')
    sock.send(filename.encode())

    length = sock.recv(1024).decode()
    sock.send('OK'.encode())

    response = b''
    got_len = 0
    with tqdm.tqdm(total=int(length), unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
        while got_len < int(length):
            data = sock.recv(1024)
            response += data
            got_len += len(data)
            progress_bar.update(len(data))

    response = pickle.loads(response)
    sock.send('RECV'.encode())

    if response['status'] == 'ERROR':
        print('File does not exist')
        return

    filepath = os.path.join('./client_files', filename)

    with open(filepath, 'wb') as f:
        f.write(response['content'])

    print(f'Downloaded {filepath}')

def client_init():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
    try:
        while True:
            options = sock.recv(1024).decode()
            print(options)

            selected = input('-> ')
            sock.send(selected.encode())

            match selected:
                case '1':
                    list(sock)
                case '2':
                    upload(sock)
                case '3':
                    download(sock)
    except KeyboardInterrupt:
        print('Disconnected')
  
client_init()