import requests
import os
import time 

server_url = 'http://localhost:12349'

while True:
    options = '''Select one :
    1. list
    2. upload
    3. download
    '''
        
    print(options)

    selected_operation = input()   
    start_time = time.time()
    
    
    match selected_operation:
        case '1': #list
            response = requests.get(f'{server_url}/list')
            files = response.json()
            print("Available Files : ")            
            for file in files:
                print(file)
                
        case '2': #upload
            filename = input('Enter the filename: ')   
            try:     
                with open(filename, 'rb') as file:
                    response = requests.post(f'{server_url}/upload/{filename}', data=file)
                print(response.text)
            except FileNotFoundError:
                print('File not found')


        case '3': # download
            filename = input('Enter the filename: ')
            response = requests.get(f'{server_url}/download/{filename}')
            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                print('Successfully downloaded the file!')
            else:
                print('Sorry! Failed to download file!')
    
    end_time = time.time()
    print("Total time : " + str((end_time - start_time)))
 
            

