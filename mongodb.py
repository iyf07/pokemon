from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_PROJECT, MONGODB_ITEMS_CLUSTER, MONGODB_ITEMS_TEST_CLUSTER
import os

class MongoDB():
    def __init__(self):
        self.connect_mongodb()

    def connect_mongodb(self):
        uri = os.environ.get("MONGODB_URI")
        prod = os.environ.get("PRODUCTION") == "true"
        client = MongoClient(uri)
        db = client[MONGODB_PROJECT]
        collection = db[MONGODB_ITEMS_CLUSTER] if prod else db[MONGODB_ITEMS_TEST_CLUSTER]
        self.collection = collection

    def check_in_stock(self, url):
        item_info = self.collection.find_one(
            {"url": url},
            {"in_stock": 1}
        )
        in_stock = item_info["in_stock"] if item_info else None
        return in_stock

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