import requests
import os
from dotenv import load_dotenv
load_dotenv()
token = os.environ.get("TELEGRAM_BOT_TOKEN")
url = f"https://api.telegram.org/bot{token}/setWebhook?url=https://5fdd-2402-800-6205-ce29-8c31-bf76-8928-5a94.ngrok-free.app/webhook"

response = requests.get(url)
print(response.json())
