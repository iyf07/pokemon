import requests
import os

def form_message(item, item_url, in_stock, store):
    message_list = [
        "🐣上货了！" if in_stock else "🥚缺货了！",
        f"{item} @{store}",
        item_url
    ]
    return "\n".join(message_list)

def send_message(message, log=False):
    if log:
        webhook_url = os.environ.get("DISCORD_LOGS_WEBHOOK")
    else:
        prod = os.environ.get("PRODUCTION") == "true"
        webhook_url = os.environ.get("DISCORD_WEBHOOK") if prod else os.environ.get("DISCORD_TEST_WEBHOOK")
    payload = {
        "content": message
    }
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()