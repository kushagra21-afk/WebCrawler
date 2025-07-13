import time
import socket
import threading
import http.server 
from utils import respond_with_error, respond_with_success
from crawler import Crawler
from collections import deque
import json

crawl_queue = deque()

MAX_CLIENTS = 5
semaphore = threading.Semaphore(MAX_CLIENTS)
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                html = self.template()
                respond_with_success(self, 200, html, content_type="text/html")

            except Exception as e:
                respond_with_error(self, 500, "Internal Server Error")

        elif self.path == "/health":
            try: 
                respond_with_success(self, 200, "Server is healthy")
            except Exception as e:
                self.log_message(f"Health check failed: {e}")
                respond_with_error(self, 500, "Internal Server Error")
                    
        # elif self.path == "/crawl":
        #     if not semaphore.acquire(blocking=False):
        #         respond_with_error(self, 429, "Too many crawl requests. Try again later.")
        #         return
        #     try:
    
        #         crawler = Crawler(source_url="https://example.com", user_agent="WebCrawler/1.0")
        #         crawler.run()  # or crawler.start() — whichever is your method
        #         respond_with_success(self, 200, "Crawl request processed successfully")
        #     except Exception as e:
        #         respond_with_error(self, 500, f"Internal Server Error: {e}")
        #     finally:
        #         semaphore.release()
        else:
            respond_with_error(self, 404, "Not Found")
    def do_POST(self):
        if self.path == "/crawl":
            if not semaphore.acquire(blocking=False):
                respond_with_error(self, 429, "Too many crawl requests. Try again later.")
                return
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)
                url = data.get("url")
                if not url:
                    respond_with_error(self, 400, "Missing 'url' in request body")
                    return
                crawl_queue.append(url)
                respond_with_success(self, 202, f"URL '{url}' enqueued for crawling")
            finally:
                semaphore.release()
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

def start_http_server(host='localhost', port=8000):
        server = http.server.ThreadingHTTPServer((host, port), RequestHandler)
        print(f"🌐 HTTP server running at http://{host}:{port}")
        server.serve_forever()
