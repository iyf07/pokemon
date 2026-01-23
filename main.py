from playwright.sync_api import sync_playwright
from amazon import Amazon
from target import Target
from mongodb import MongoDB
from discord import send_message
from config import setup_logging
from dotenv import load_dotenv
import threading
import logging
   

def main():
    load_dotenv()
    setup_logging()
    mongodb = MongoDB()
    threads = []

    with sync_playwright() as p:
        browser = p.webkit.launch(headless=False)
        
        t = threading.Thread(
            target=Amazon,
            args=(mongodb,),
            daemon=True
        )
        threads.append(t)
        
        t = threading.Thread(
            target=Target,
            args=(mongodb,),
            daemon=True
        )
        threads.append(t)
        
        for each in threads:
            each.start()
        
        for each in threads:
            each.join()
        
        browser.close()

if __name__ == "__main__":
    main()