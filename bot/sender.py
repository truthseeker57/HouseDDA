import httpx
from config import TELEGRAM_CHAT_ID, TELEGRAM_BOT_TOKEN



def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    httpx.post(url, json=payload, timeout=30.0)