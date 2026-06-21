import os
from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
DATABASE_PATH = "housedda.db"