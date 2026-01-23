import requests
import os

def form_message(item, in_stock, current_price=None):
    message_list = [
        "🐣呆呆鸭发车！" if in_stock else "🥚呆呆鸭下车！",
        f"{item['store']}: {item['alias']} @${current_price}" if current_price else f"{item['store']}: {item['alias']}",
        f"限价: ${item['price']}",
        item['url']
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