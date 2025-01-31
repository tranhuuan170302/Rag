import sys
import os

# Lấy đường dẫn thư mục gốc (RAG)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Import settings
from API.settings import settings

print(settings.TELEGRAM_BOT_TOKEN)  # Kiểm tra import thành công

from fastapi import FastAPI
import uvicorn
from controller import ChatController

app = FastAPI()

app.include_router(ChatController.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
