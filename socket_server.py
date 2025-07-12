import time
import socket
import threading
import http.server 
from utils import respond_with_error, respond_with_success
from crawler import crawl

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                respond_with_success(self, 200, "Welcome to the Socket Server")
            except Exception as e:
                respond_with_error(self, 500, "Internal Server Error")

        elif self.path == "/health":
            try: 
                respond_with_success(self, 200, "Server is healthy")
            except Exception as e:
                self.log_message(f"Health check failed: {e}")
                respond_with_error(self, 500, "Internal Server Error")
                    
        elif self.path == "/crawl":
            try:
                data=crawl()  
                respond_with_success(self, 200, "Crawl request processed successfully")
            except Exception as e:
                respond_with_error(self, 500, "Internal Server Error") 
                  
        else:
            respond_with_error(self, 404, "Not Found")
    
    def template(self):
        return f"""
        <html>
            <head><title>Socket Server</title></head>
            <body>
                <h1>Socket Server is running</h1>
                <p>Use /health to check server status</p>
                <p>Use /crawl to initiate a crawl</p>
            </body>
        </html>
        """
    def log_message(self, format, *args):
        return  # Suppress default console logging

def start_http_server(host='localhost', port=8080):
        server = http.server.HTTPServer((host, port), RequestHandler)
        print(f"🌐 HTTP server running at http://{host}:{port}")
        server.serve_forever()
            