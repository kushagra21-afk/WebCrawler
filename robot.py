import time
from concurrent.futures import ThreadPoolExecutor
import dotenv
import os
from crawler import Crawler
from socket_server import crawl_queue
from threading import Lock
dotenv.load_dotenv()
workers = int(os.getenv("robot_workers", "2"))
interval = 600 
lock = Lock()
seeds = []
def crawl_url(url):
    crawler = Crawler(source_url=url,user_agent=os.getenv("USER_AGENT", "WebCrawler/1.0 contact gamerkuah21@gmail.com (educational purposes)")) 
    crawler.workers()
    print("Crawler started", crawler)
def robot_worker():
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        while True:
            with lock:
                while crawl_queue:
                    seeds.append(crawl_queue.popleft())
            if seeds:
                print(f"[Robot] Launching {len(seeds)} seed crawls")
                for url in seeds:
                    executor.submit(crawl_url, url)
            else:
                print("[Robot] No new seeds")
                time.sleep(10)
                continue
            time.sleep(interval)

            