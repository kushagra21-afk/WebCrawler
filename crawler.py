from bs4 import BeautifulSoup
import requests
import dotenv
import os
from threading import Lock, Thread
from urllib.parse import urljoin, urlparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from db import insert_content_to_db

dotenv.load_dotenv()

class Crawler:
    def __init__(self, source_url, user_agent):
        self.source_url = source_url
        self.user_agent = user_agent
        self.visited_urls = set()
        self.queue = deque([(source_url, 0)])
        self.headers = {"User-Agent": user_agent}
        self.max_depth = 10
        self.token_limit = 10000
        self.content_limit = 10000
        self.domain = urlparse(source_url).netloc
        self.lock = Lock()
        self.worker_nodes = 4
        print(self.queue)

    def add_url(self, url, depth):
        try:
            parsed = urlparse(url)
                
            if not parsed.scheme:
                url = urljoin(self.source_url, url)
            elif parsed.netloc != self.domain:
                return False
            with self.lock:
                if url not in self.visited_urls:
                    self.queue.append((url, depth))
                    return True
            return False
        except Exception as e:
            print(f"[Error] : {e}")
    def parse_html(self, html):
        try:
            return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            print(f"[Error] : {e}")

    def extract_content(self, soup):
        try:
            content = []
            count = 0
            for elem in soup.find_all(string=True):
                if elem.parent.name in ['script', 'style', 'noscript', 'header', 'footer', 'nav', 'aside']:
                    continue
                text = elem.strip()
                if text:
                    content.append(text)
                    count += len(text)
                    if count >= self.content_limit:
                        break
            return ' '.join(content[:self.token_limit])
        except Exception as e:
            print(f"[Error] : {e}")

    def crawl(self,url,depth):
        with self.lock:
                try:
                    response = requests.get(url, headers=self.headers, timeout=5)
                    response.raise_for_status()
                    self.visited_urls.add(url)

                    soup = self.parse_html(response.text)
                    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
                    content = self.extract_content(soup)

                    print(f"[{len(self.visited_urls)}] {url} - {title[:50]}")
                    
                    #insert into mongodb
                    insert_content_to_db(url, title, content, depth)
                    
                    # Extract and enqueue same-domain links
                    for link in soup.find_all("a", href=True):
                        self.add_url(link['href'], depth + 1)

                except requests.RequestException as e:
                    print(f"[Error] {url}: {e}")

        return list(self.visited_urls)
    
    def workers(self):
        with ThreadPoolExecutor(max_workers=self.worker_nodes) as executor:
            futures = []
            while True:
                with self.lock:
                    if not self.queue:
                        break
                    url, depth = self.queue.popleft()
                if url in self.visited_urls or depth > self.max_depth:
                    continue
                futures.append(executor.submit(self.crawl, url, depth))
            for f in futures:
                f.result()
        print(f"\nCrawled {len(self.visited_urls)} pages.")
