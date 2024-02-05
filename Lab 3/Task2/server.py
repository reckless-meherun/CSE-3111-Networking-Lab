from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f"GET request,\nPath: {self.path}\nHeaders:\n{self.headers}\n")
        file_path = self.path
        # print(file_path) 
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()

        except FileNotFoundError:
            logging.error("File not found: %s", file_path)
            self.send_error(404, "File not found")
            return
        nam=f.name.encode("utf-8")
        self._set_response()
        self.wfile.write(file_content)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length) 
        print("hello", self.responses)
        with open('output.in', 'wb') as local_file:
            for chunk in post_data.iter_content(chunk_size=content_length):
                local_file.write(chunk)
        logging.info(f"POST request,\nPath: {self.path}\nHeaders:\n{self.headers}\n\nBody:\n{post_data}\n".decode('utf-8'))

        self._set_response()
        self.wfile.write(f"POST request for {self.path}".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()