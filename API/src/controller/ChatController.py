from fastapi import APIRouter, Depends, Request
from services.ChatService import chatMessageRepository
from config.databaseConnect import get_database
import sys
sys.path.append('d:/WorkSpace/RAG/API')
from Rag.embedding import get_embedding
from dotenv import load_dotenv
load_dotenv()
# create routes
router = APIRouter()
db = get_database()
chat_service = chatMessageRepository(db=db)

@router.post('/webhook')
async def chat(message: Request):
    try:
        jsonBody = await message.json()
        print(jsonBody)
        query = jsonBody['message']['text']
        id = jsonBody['message']['from']['id']

        is_answer = await chat_service.anwser_storage(query)
        if is_answer[0]['score'] > 0.98:
            result = is_answer[0]['answer']
            await chat_service.send_message(result, id)
            return

        result = await chat_service.chat(query)
        await chat_service.send_message(result, id)

        data = {
            "question": query,
            "answer": result,
            "embedding": get_embedding.encoder_query(query)
        }
        await chat_service.data_storage(data)
    except Exception as e:
        print(e)