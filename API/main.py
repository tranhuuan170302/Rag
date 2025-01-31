import requests
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ.get("TELEGRAM_BOT_TOKEN")
url = f"https://api.telegram.org/bot{token}/setWebhook?url=https://5425-2001-ee1-f401-a5e0-a008-91d5-a42c-41e6.ngrok-free.app/webhook"

response = requests.get(url)
print(response.json())
