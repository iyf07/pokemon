from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
from costco import costco_main
from mongodb import MongoDB
from discord import send_message
from dotenv import load_dotenv
from config import SLEEP_INTERVAL
import os
import time

def main():
    load_dotenv()

    mongodb = MongoDB()
    with sync_playwright() as p:
        while True:
            for each in (p.webkit, p.firefox, p.chromium):
                try:
                    send_message("Launching browser...", log=True)
                    browser = each.launch(headless=False)

                    costco_main(browser, mongodb)

                    browser.close()

                    send_message(f"Sleeping for {SLEEP_INTERVAL} seconds...", log=True)
                    time.sleep(SLEEP_INTERVAL)
                except PlaywrightTimeoutError:
                    send_message("Playwright times out", log=True)
                except PlaywrightError:
                    send_message("Playwright error", log=True)
                except Exception as e:
                    send_message(f"Unknown error {e}", log=True)


if __name__ == '__main__':
    main()