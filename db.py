import os
from pymongo import MongoClient
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["webcrawler"]
collection = db["pages"]
lock = Lock()

def insert_content_to_db(url, title, content, depth):
    try:
        doc = {
            "url": url,
            "title": title,
            "content": content,
            "depth": depth
        }
        with lock:
            collection.insert_one(doc)
    except Exception as e:
        print(f"[MongoDB Insert Error] {url}: {e}")
