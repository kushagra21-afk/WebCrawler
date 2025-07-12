from socket_server import start_http_server, crawl_queue
from threading import Thread 
from robot import crawl_url
if __name__ == "__main__":
    Thread(target=start_http_server, daemon=True).start()
    Thread(target=start_crawling, daemon=True).start()

    while True:
        pass 