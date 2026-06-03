import os
from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
RAPIDAPI_KEY = os.environ["RAPIDAPI_KEY"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
DATABASE_PATH = "housedda.db"