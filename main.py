from socket_server import start_http_server, crawl_queue
from threading import Thread 
from robot import robot_worker
if __name__ == "__main__":
    Thread(target=start_http_server, daemon=True).start()
    Thread(target=robot_worker, daemon=True).start()

    while True:
        pass 