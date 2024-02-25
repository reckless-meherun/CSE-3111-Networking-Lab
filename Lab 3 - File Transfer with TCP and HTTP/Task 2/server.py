import http.server
import socketserver
import os
import json

filepath = os.getcwd()+"/files"

PORT = 12349

def list(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json') # response er content type
    self.end_headers()
    files = os.listdir(filepath)
    print(files)
    self.wfile.write(json.dumps(files).encode()) 

def download(self): # client download korche
    filename = self.path[10:]
    try:
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream') # unknown type file
        self.end_headers()
        with open(os.path.join('files', filename), 'rb') as file:
            self.wfile.write(file.read()) # nije packet banai nibe and send kore dibe
    except FileNotFoundError:
        self.send_error(404, "Sorry! Did not find the file!")

def upload(self): # client upload korche
    filename = self.path[8:]
    content_length = int(self.headers['Content-Length'])
    file_content = self.rfile.read(content_length)
    with open(os.path.join('files', filename), 'wb') as file:
        file.write(file_content)

    self.send_response(201)
    self.send_header('Content-type', 'text/plain')
    self.end_headers()
    self.wfile.write(b'Successfully uploaded the file!')
    
class FileHandler(http.server.SimpleHTTPRequestHandler): # inhereting class of http server in python
    def do_GET(self):        
        if self.path == '/list':
            list(self)            
        elif self.path.startswith('/download/'):
            download(self)                
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/upload/'):
            upload(self)

if __name__ == "__main__":
    os.makedirs('files', exist_ok=True) # downloadable files
    handler = FileHandler # the object of a class
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Hello client!")
        httpd.serve_forever()
