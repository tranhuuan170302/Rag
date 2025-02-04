import requests
from API.settings.settings import TELEGRAM_BOT_TOKEN
from API.Rag.vectorSearch import VectorSearchImpl, VectorSearchQaImpl, SearchResultImpl
from API.Rag.chat_model import model_reflection, model_retrivel, model_generator, model_router
from API.ETL.pipelinePreprocessingData import pipeline_processing, load_stopwords
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# given a Token bot telegram
TELEGRAM_TOKEN = TELEGRAM_BOT_TOKEN


def serialize_document(doc):
    """Chuyển đổi ObjectId thành chuỗi để trả về JSON hợp lệ."""
    doc["_id"] = str(doc["_id"])
    return doc


vector_search_qa = VectorSearchQaImpl()
vector_search = VectorSearchImpl()
search_result = SearchResultImpl()

class chatMessageRepository:
    def __init__(self, db):
        self.db = db
        self.history = []

    async def chat(self, chatMessage):

            try:
                collection = self.db["Products"]

                # reflection model   
                logger.info(f"question from client: {chatMessage}")
                reflection_sentence = chatMessage
                if len(self.history) != 0:
                    reflection_sentence = model_reflection.implement(self.history, chatMessage)

                logger.info(f"Reflection sentence from model Reflection: {reflection_sentence}") 
                
                # routing model
                classify_question = model_router.implement(reflection_sentence)
                logger.info(f"""question from model Category: {classify_question['category']} 
                                and Sentence: {classify_question['message']}""")

                if classify_question['category'] == "Khác":
                    generate_answer = model_generator.implement(classify_question)
                    logger.info(f"generate the answer from model Generate: {generate_answer}")
                    return generate_answer
                else:
                    # preprocessing reflection sentence
                    stopWord = load_stopwords()
                    clean_sentence = pipeline_processing(reflection_sentence, stopWord)
                    get_knowledge = vector_search.vector_search(clean_sentence, classify_question['category'], collection)
                    
                    results = search_result.get_search_result(get_knowledge)

                    logger.info(f"smoth result: {results}")
                    retrivel = model_retrivel.implement(reflection_sentence, results)
                    logger.info(f"question from model Retrivel: {retrivel}")
                    
                    return retrivel['assistant']
            except Exception as e:
                print(e)
                return False

    async def data_storage(self, data: dict) -> bool:
        try:
            collection = self.db["AnswersandQuestions"]

            collection.insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False

    async def anwser_storage(self, query: str) -> str:
        try:
            embedd_query = vector_search_qa.vector_search(query, self.db["AnswersandQuestions"])
            return embedd_query
        except Exception as e:
            print(e)

    async def send_message(self, text: str, id: str):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": id,
            "parse_mode": "Markdown",
            "text": text,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gửi tin nhắn: {e}")

    