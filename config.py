import logging

# Costco
COSTCO_URL = 'https://www.costco.com/s?keyword=Pokemon'
COSTCO_VALID_ITEMS = ['upc', 'ultra premium collection', 'charizard']

# App
SLEEP_INTERVAL = 300

def setup_logging():
    logging.basicConfig(level=logging.INFO)