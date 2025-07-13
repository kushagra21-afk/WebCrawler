import os
from pymongo import MongoClient
from dotenv import load_dotenv
from threading import Lock

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client["webcrawler"]
collection = db["pages"]
lock = Lock()

def insert_content_to_db(url, title, content, depth):
    try:
        doc = {
            "title": title,
            "content": content,
            "depth": depth
        }
        with lock:
            if collection.update_one({"url": url},{"$set":doc}, upsert =True):
                print("doc updated")   
            else:
                print("doc inserted")
    except Exception as e:
        print(f"[MongoDB Insert Error] {url}: {e}")
