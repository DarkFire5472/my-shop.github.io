from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import templating

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            conn.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(templating.render('index.html', products=products).encode())
        elif self.path == '/account':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT balance, purchases FROM users WHERE username=?", ('username',))  # заменить 'username' на реальное имя пользователя
            user = cursor.fetchone()
            conn.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(templating.render('account.html', balance=user[0], purchases=user[1]).encode())

    def do_POST(self):
        if self.path == '/purchase':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            product_id = post_data.decode().split('=')[1]
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM products WHERE id=?", (product_id,))
            price = cursor.fetchone()[0]
            cursor.execute("SELECT balance, purchases FROM users WHERE username=?", ('username',))  # заменить 'username' на реальное имя пользователя
            user = cursor.fetchone()
            if user[0] >= price:
                cursor.execute("UPDATE users SET balance=?, purchases=? WHERE username=?", (user[0] - price, user[1] + 1, 'username'))  # заменить 'username' на реальное имя пользователя
                conn.commit()
                conn.close()
                self.send_response(302)
                self.send_header('Location', '/account')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Недостаточно средств')

def run_api():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, RequestHandler)
    print('API started on port 8001')
    httpd.serve_forever()

if __name__ == '__main__':
    run_api()