import time
import socket
import threading
import http.server 
from utils import respond_with_error

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.template().encode('utf-8'))
                self.log_message("Root request processed successfully")
            except Exception as e:
                respond_with_error(self, 500, "Internal Server Error")
                
        elif self.path == "/health":
            try: 
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"The crawler server is healthy")
                self.log_message("Health check passed")
            except Exception as e:
                self.log_message(f"Health check failed: {e}")
                respond_with_error(self, 500, "Internal Server Error")
                    
        elif self.path == "/crawl":
            try:
                data=crawl()  
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(data.encode('utf-8'))
                self.log_message("Crawl request processed successfully")
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
       
           