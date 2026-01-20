from config import COSTCO_URL, COSTCO_VALID_ITEMS
from discord import send_message, form_message
import re

STORE = "Costco"

def costco_main(browser, mongodb):
    send_message(f"Starting to search Costco items. Keywords are {', '.join(COSTCO_VALID_ITEMS)}", log=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(COSTCO_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_load_state("networkidle", timeout=60000)
    items = fetch_items(page)
    if len(items) == 0:
        send_message("No items found", log=True)
    update_items(items, mongodb)
    page.close()

def fetch_items(page):
    page.wait_for_selector('[id^="ProductTile"]', timeout=60000)
    elements = page.locator('[id^="ProductTile"][id$="title"]')
    items = []
    for i in range(elements.count()):
        el = elements.nth(i)
        if el.inner_text().lower() in COSTCO_VALID_ITEMS:
            items.append(el)
    return items
                
def update_items(items, mongodb):
    in_stock_item_urls = []
    for item in items:
        item_name = item.inner_text()
        item_url = find_item_url(item)
        if not mongodb.check_in_stock(item_url):
            send_message(form_message(item_name, item_url, True, STORE))
            mongodb.update_item(item_name, item_url, True, STORE)
        in_stock_item_urls.append(item_url)
    for item in mongodb.find_out_of_stock_items(in_stock_item_urls):
        if mongodb.check_in_stock(item["url"]):
            send_message(form_message(item["item"], item["url"], False, STORE))
    mongodb.update_out_of_stock_items(in_stock_item_urls)

def find_item_url(element):
    container = element.locator('..').locator('..').locator('..').locator('..')
    link = container.locator('a')
    href = link.get_attribute('href')
    return href