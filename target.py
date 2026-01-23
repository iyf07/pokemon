from playwright.sync_api import sync_playwright
from discord import send_message, form_message
import logging
import time
import os
import time
import random

SLEEP_MIN = 2
SLEEP_MAX = 6

logger = logging.getLogger('Target')

class Target():
    def __init__(self, mongodb):
        self.store = 'Target'
        self.mongodb = mongodb
        # self.amazon_username = os.environ.get('AMAZON_USERNAME')
        # self.amazon_password = os.environ.get('AMAZON_PASSWORD')
        try:
            send_message("🐶Target Bot已上线")
            self.run()
        except Exception as e:
            logger.error(e)
            send_message("📴Target Bot已掉线")
        
    def run(self):
        logger.info("Starting Target worker")
        with sync_playwright() as p:
            self.browser = p.webkit.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            
            while True:
                for item in self.mongodb.find_items_by_store(self.store):
                    logger.info(f"Visiting {item['alias']}")
                    self.page.goto(
                        item['url'],
                        wait_until='domcontentloaded',
                        timeout=60000
                    )
                    
                    # Click Virginia health button
                    health_button = self.page.locator("#VA_HEALTH_CONSENT_BUTTON")
                    try:
                        health_button.wait_for(state="visible", timeout=1000)
                    except:
                        pass
                    if health_button.count() > 0 and health_button.is_visible():
                        health_button.click()
                        
                    # Check availability
                    availability = self.check_availability()
                    if not availability:
                        logger.info(f"{item['alias']} is out of stock")
                        self.send_discord_message(item, False)
                        continue
                    else:
                        logger.info(f"{item['alias']} is in stock")
                        
                    # Check price
                    current_price = self.check_price()
                    if float(current_price) <= float(item['price']):
                        logger.info(f"{item['alias']} has a good deal ${current_price}. Threshold is ${item['price']}")
                        self.send_discord_message(item, True, current_price)
                        # self.buy_item()
                    else:
                        logger.info(f"{item['alias']} is too expensive ${current_price}. Threshold is ${item['price']}")
                        self.send_discord_message(item, True, current_price)
                        
                    time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))
                
    def check_availability(self):
        for each in ['Preorders have sold out', 'Item not available.', 'Out of stock']:
            if self.page.get_by_text(each).count() > 0:
                return False
        if self.page.locator("button", has_text="Add to cart").count() == 0:
            return False
        if self.page.locator("button", has_text="Add to cart").is_disabled():
            return False
        
        return True
    
    def check_price(self):
        self.page.wait_for_selector('[data-module-type="ProductDetailPrice"]', timeout=60000)
        price_parent_div = self.page.locator('[data-module-type="ProductDetailPrice"]')
        raw_current_price = price_parent_div.locator('> div').locator('> div').locator('div').first.locator('span').locator('span').inner_text()
        current_price = raw_current_price[1:]
        return current_price
    
    def buy_item(self):
        buy_button = self.page.locator('input[id="buy-now-button"]')
        buy_button.click()
        self.page.wait_for_selector('[id="placeOrder"]', timeout=60000)
        exit
    
    def send_discord_message(self, item, cur_in_stock, current_price=None):
        prev_in_stock = self.mongodb.find_item_in_stock(item['url'])
        if cur_in_stock != prev_in_stock:
            self.mongodb.update_item_in_stock(item['url'], cur_in_stock)
            send_message(form_message(item, cur_in_stock, current_price))
                        
    def sign_in(self):
        logger.info("Signing in")
        
        # Get login url
        self.page.goto("https://www.amazon.com")
        self.page.wait_for_selector('[id="nav-link-accountList"]', timeout=60000)
        login_url = self.page.locator('[id="nav-link-accountList"]').locator('> a').get_attribute('href')
        
        # Get login form
        self.page.goto(login_url)
        self.page.wait_for_selector('[id="authportal-center-section"]', timeout=60000)
        
        # Enter email
        login_form = self.page.locator("#ap_login_form")
        login_form.locator('input[name="email"]').type(
            self.amazon_username,
            delay=80
        )
        login_form.locator('input[type="submit"]').click()
        self.page.wait_for_selector('[id="ap_password"]', timeout=60000)
        
        # Enter password
        login_form = self.page.locator('form[name="signIn"]')
        login_form.locator('input[name="password"]').type(
            self.amazon_password,
            delay=80
        )
        login_form.locator('input[type="submit"]').click()
        
        
                
                
                