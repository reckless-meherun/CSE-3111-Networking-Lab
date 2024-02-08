import socket
import threading
import pickle
import os


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090



def server_init():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    print(f'Server active on {HOST}:{PORT}')
    print('Listening')
    server.listen()

    while True:
        conn,addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,addr))
        client_thread.start()

def list(conn):
    print('List')
    file_list = os.listdir('./server_files')
    print(file_list)
    response = '\n'.join(file_list)
    conn.send(response.encode())

def upload(conn):
    print('Upload')
    conn.send('upload'.encode())

    length = conn.recv(1024).decode()
    conn.send('OK'.encode())

    response = b''
    got_len=0
    while got_len<int(length):
        data = conn.recv(1024)
        response+=data
        got_len+=len(data)

    response = pickle.loads(response)

    if response['status'] == 'ERROR': return

    filepath = os.path.join('./server_files',response['filename'])
    
    with open(filepath,'wb') as f:
        f.write(response['content'])
    
    print('Received')

def download(conn):
    print('Download')
    conn.send('download'.encode())
    filename = conn.recv(1024).decode()
    filepath = os.path.join('./server_files',filename)

    try:
        with open(filepath,'rb') as f:
            content = f.read()
        response = {
            'status': 'OK',
            'filename': filename,
            'content': content
        }

    except FileNotFoundError:
        print('File does not exist')
        response = {
            'status': 'ERROR',
        }
    
    response = pickle.dumps(response)
    conn.send(f'{len(response)}'.encode())
    conn.recv(1024).decode()
    conn.send(response)
    conn.recv(1024).decode()


def handle_client(conn,addr):
    print(f'New connection from {addr}')

    options = '''Select one:
    1. List
    2. Upload
    3. Download'''
    while True:
        conn.send(options.encode())
        selected = conn.recv(1024).decode()
        print(selected)

        match selected:
            case '1':
                list(conn)
            case '2':
                upload(conn)
            case '3':
                download(conn)
                # conn.recv(1024)



if __name__=='__main__':
    server_init()
    
# print('helo')
