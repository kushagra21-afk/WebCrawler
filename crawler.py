from bs4 import BeautifulSoup
import requests
import dotenv
import os
from threading import Lock, get_ident
from urllib.parse import urljoin, urlparse, urlunparse, urldefrag
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from db import insert_content_to_db

dotenv.load_dotenv()

class Crawler:
    
    def __init__(self, source_url, user_agent):
        self.source_url = source_url
        self.user_agent = user_agent
        self.visited_urls = set()
        self.queue = deque([(source_url, 0)])
        self.headers = {"User-Agent": user_agent}
        self.max_depth = 2
        self.token_limit = 10000
        self.content_limit = 10000
        self.domain = urlparse(source_url).netloc
        self.lock = Lock()
        self.worker_nodes = 4
        self.i=0
        print(self.queue)

    def add_url(self, url, depth, base_url):
        try:
            abs_url = urljoin(base_url, url)
            abs_url, _ = urldefrag(abs_url)  # Remove #fragment
            parsed = urlparse(abs_url)

            if parsed.netloc != self.domain:
                return False
            
            # Normalize path
            normalized_path = parsed.path.rstrip('/')
            final_url = urlunparse((parsed.scheme, parsed.netloc, normalized_path, '', '', ''))

            with self.lock:
                if final_url not in self.visited_urls:
                    self.queue.append((final_url, depth))
                    return True
            return False
        except Exception as e:
            print(f"[Add URL Error]: {e}")
            return False
            
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
                try:
                    thread_id = get_ident()
                    with self.lock:
                        current_count = self.i
                        self.i += 1
                    print(f"[Thread-{thread_id}] Crawl #{current_count}: {url}")
                    response = requests.get(url, headers=self.headers, timeout=1)
                    response.raise_for_status()
                    with self.lock:
                        self.visited_urls.add(url)

                    soup = self.parse_html(response.text)
                    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
                    content = self.extract_content(soup)

                    print(f"[{len(self.visited_urls)}] {url} - {title[:50]}")
                    
                    try:
                        insert_content_to_db(url, title, content, depth)
                        print(f"[Inserted] {url}")
                    except Exception as db_err:
                        print(f"[DB Error] {url}: {db_err}")
                    # Extract and enqueue same-domain links
                    for link in soup.find_all("a", href=True):
                        self.add_url(link['href'], depth + 1, url)
                    print(len(self.queue))
                except requests.RequestException as e:
                    print(f"[Error] {url}: {e}")

                return list(self.visited_urls)
    
    def workers(self):
        with ThreadPoolExecutor(max_workers=self.worker_nodes) as executor:
            futures = set()
            
            while True:
                # Submit new tasks if we have capacity
                while len(futures) < self.worker_nodes and self.queue:
                    with self.lock:
                        if not self.queue:
                            break
                        url, depth = self.queue.popleft()
                    
                    if url in self.visited_urls or depth > self.max_depth:
                        continue
                        
                    future = executor.submit(self.crawl, url, depth)
                    futures.add(future)
                    print(f"Submitted {url} to executor")

                if not futures:
                    break  # No more work to do

                # Wait for at least one task to complete
                done, futures = as_completed(futures), set()
                for future in done:
                    try:
                        result = future.result()
                    except Exception as e:
                        print(f"Task failed: {e}")

        print(f"\nCrawled {len(self.visited_urls)} pages.")
        print(f"Final queue size: {len(self.queue)}")
