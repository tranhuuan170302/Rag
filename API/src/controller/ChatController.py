from fastapi import APIRouter, Depends, Request
from services.ChatService import chatMessageRepository
from config.databaseConnect import get_database
from API.Rag.embedding import get_embedding
from API.Rag.chat_model import model_storage
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
        if is_answer and is_answer[0]['score'] > 0.95:
            result = is_answer[0]['answer']
            await chat_service.send_message(result, id)
            return result

        result = await chat_service.chat(query)
        await chat_service.send_message(result, id)

        data = {
            "question": query,
            "answer": result,
            "embedding": get_embedding.encoder_query(query)
        }
        is_storage = model_storage.implement(data['question'], data['answer'])
        is_valid = is_storage['is_valid']
        print(f"prediction: {is_valid}")
        if is_valid:
            print("the pass")
            await chat_service.data_storage(data)
        return result
    except Exception as e:
        print(e)