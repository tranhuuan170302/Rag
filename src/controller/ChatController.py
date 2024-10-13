from fastapi import APIRouter, Depends, Request
from services import ChatService, RawData

# create routes
router = APIRouter()

@router.post('/chat')
async def chat(message: Request):
    
    jsonBody = await message.json()
    print(jsonBody['Heloo'])
    result = ChatService.chat_service(jsonBody['Heloo'])
    return {
        "message": result
    }