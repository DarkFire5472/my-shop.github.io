from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('register.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/account':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('account.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not found')

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            username, password = post_data.decode().split('&')
            username = username.split('=')[1]
            password = password.split('=')[1]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, balance, purchases) VALUES (?, ?, 0, 0)", (username, password))
            conn.commit()
            conn.close()
            self.send_response(302)
            self.send_header('Location', '/login')
            self.end_headers()
        elif self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            username, password = post_data.decode().split('&')
            username = username.split('=')[1]
            password = password.split('=')[1]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                self.send_response(302)
                self.send_header('Location', '/account')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Invalid username or password')

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server started on port 8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()