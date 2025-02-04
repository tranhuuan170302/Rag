import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TELEGRAM_BOT_TOKEN")
url = f"https://api.telegram.org/bot{token}/setWebhook?url=https://b953-2001-ee1-f401-a5e0-20fb-511a-d986-5c47.ngrok-free.app/webhook"

response = requests.get(url)
print(response.json())
