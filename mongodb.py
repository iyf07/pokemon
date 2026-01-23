from pymongo import MongoClient
from datetime import datetime
import os

class MongoDB():
    def __init__(self):
        self.connect_mongodb()

    def connect_mongodb(self):    
        mongodb_project = 'pokemon'
        mongodb_items_cluster = 'items'
        uri = os.environ.get("MONGODB_URI")
        client = MongoClient(uri)
        db = client[mongodb_project]
        self.collection = db[mongodb_items_cluster]

    def find_items_by_store(self, store):
        items = self.collection.find({"store": store})
        return items
    
    def find_item_in_stock(self, url):
        item = self.collection.find_one({"url": url})
        return item["in_stock"]
    
    def update_item_in_stock(self, url, in_stock):
        self.collection.update_one(
            {"url": url},
            {"$set": {"in_stock": in_stock}}
        )

    def find_out_of_stock_items(self, in_stock_item_urls):
        res = self.collection.find(
            {
                "url": {"$nin": in_stock_item_urls}
            }
        )
        return res

    def update_out_of_stock_items(self, in_stock_item_urls):
        self.collection.update_many(
            {
                "url": {"$nin": in_stock_item_urls},
                "in_stock": True,
            },
            {
                "$set": {"in_stock": False}
            }
        )

    def update_item(self, item, item_url, in_stock, store):
        self.collection.update_one(
            {"url": item_url},
            {
                "$set": {
                    "item": item,
                    "store": store,
                    "url": item_url,
                    "in_stock": in_stock,
                    "created_at": datetime.utcnow(),
                }
            },
            upsert=True
        )