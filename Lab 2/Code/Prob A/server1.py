import socket
import sys #to implement command line and terminal commands into python file
import sympy

def create_socket():
    try:
        global host
        global port
        global sock
        host = socket.gethostbyname(socket.gethostname()) #empty because we are goting to put this server.py file into our server and the IP address of the host is gonna be itself
        port = 9005
        sock = socket.socket()
    except socket.error as msg:
        print("Socket creation error " + str(msg))
        
        
# why binding? Might be able to open up a line of communication with sockets, but it needs to know about the info of the device it is supposed to be communicating with

def bind_socket():
    try:
        global host
        global port
        global sock

        print("binding the port "+str(port))
        sock.bind((host, port))
        sock.listen(5) 
        # why important? the server should be continuously listening to the connections from various computers
        # 5 is the number of connections it is going to tolerate and after that it is going to throw error
        
    except socket.error as msg:
        print("Socket binding error " + str(msg) + "\n" + "Retrying...")
        bind_socket()

def isPalindrome(s):
    return s == s[::-1]

def socket_accept():
    conn, address = sock.accept() #gives us two data : object of a connection and a list of IP address and a port
    # the next line will be executed only when a connection is accepted
    print("Connection has been established! "+ "\nIP : " + address[0] + "\nPort : " + str(address[1]))
    
    while True:
        text = conn.recv(1024).decode()

        if(text[0].isdigit()):
            num, operation = text.split()
            if operation == 'prime':
                if(sympy.isprime(int(num))):
                    conn.send('It is a prime number.'.encode())
                else:
                    conn.send('It is not a prime number.'.encode())

            elif operation == 'palindrome':
                if(isPalindrome(num)):
                    conn.send('It is palindrome.'.encode())
                else:
                    conn.send('It is not palindrome.'.encode())

            else:
                conn.send('Operation not available'.encode())

        else:
            conn.send(text.lower().encode())
            

    conn.close()



def main():
    create_socket()
    bind_socket()
    socket_accept()
    
    
main()    




    
            
        
    
    
    
    
    
