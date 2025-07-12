import time
from crawler import Crawler
def start_crawling():
    while True:
        time.sleep(60) 
        try:
            print("Crawling in progress...")
        except Exception as e:
            print(f"Error during crawling: {e}")
            break  