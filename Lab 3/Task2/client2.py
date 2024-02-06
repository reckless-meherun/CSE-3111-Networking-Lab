import requests
fil=input('Enter File Name: ')
x = requests.get(f'http://files///D:/du/3 1/CSE-3101/CSE-3111-Networking-Lab/Lab 3/05_07_Meherun_Jamal/Task2/{fil}')
if x.status_code == 200:
    with open(fil, "wb") as f:
        f.write(x.content)
    print("File successfully received")
    print("Content: ",x.text)
else:
    print("Error: Could not receive file")