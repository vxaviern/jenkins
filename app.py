from http.server import HTTPServer, BaseHTTPRequestHandler


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from my app!")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Handler)
    print("Starting server on port 8080...")
    server.serve_forever()