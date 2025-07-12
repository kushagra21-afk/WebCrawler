import time
from crawler import crawl
def start_crawling():
    while True:
        time.sleep(60) 
        try:
            # Simulate crawling process
            print("Crawling in progress...")
            crawl()
        except Exception as e:
            print(f"Error during crawling: {e}")
            break  # Exit the loop on error