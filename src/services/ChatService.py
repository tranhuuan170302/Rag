from utils.embedding import get_embedding
from config import databaseConnect
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

uri = os.environ.get("API_TOKEN")
llm = ChatOpenAI(api_key=uri)

# load models from openai
def load_openai(user_message: str):
    
    get_message = llm.invoke(user_message)
    return get_message

# Helper function để chuyển ObjectId thành chuỗi
def serialize_document(doc):
    """Chuyển đổi ObjectId thành chuỗi để trả về JSON hợp lệ."""
    doc["_id"] = str(doc["_id"])
    return doc

def chat_service(text):
    print("thành công 1")
    db_product = databaseConnect.get_database()['product_new']
    text_embedding = get_embedding(text)
    
    
    
    docs = db_product.find({})
    
    products = [serialize_document(doc) for doc in docs]
    
    # Trích xuất embedding từ tất cả sản phẩm
    embeddings = np.array([doc["embedding"][0] for doc in products])
    
    # Tính cosine similarity giữa input_embedding và tất cả embedding trong database
    input_embedding = np.array(text_embedding).reshape(1, -1)
   
    similarities = cosine_similarity(input_embedding, embeddings)
    print('thành công 2')
    # Lấy chỉ số của 4 embedding gần nhất (sắp xếp theo cosine similarity)
    top_indices = np.argsort(similarities[0])[::-1][:4]  # Sắp xếp giảm dần và lấy 4 chỉ số đầu tiên

    # Lấy ra 4 sản phẩm tương ứng
    closest_products = [products[i] for i in top_indices]

    
    prompt = f""" vai trò của bạn là một người tư vấn bán hàng hãy sử dụng các thông tin tôi cung cấp về mặt hàng dưới đây để tra lời cho khách hàng:
    - tên sản phẩm thứ nhất: {closest_products[0]["name"]}
    - đường dẫn sản phẩm thứ nhất: {closest_products[0]["short_url"]}
    - mô tả sản phẩm thứ nhất: {closest_products[0]["short_description"]}v n
    - đánh giá trung bình của sản phẩm thứ nhất: {closest_products[0]["rating_average"]}
    - số lượt bán của sản phẩm thứ nhất: {closest_products[0]["quantity_sold"]} 
    - tên sản phẩm thứ hai: {closest_products[1]["name"]}
    - đường dẫn sản phẩm thứ hai: {closest_products[1]["short_url"]}
    - mô tả sản phẩm thứ hai: {closest_products[1]["short_description"]}v n
    - đánh giá trung bình của sản phẩm thứ hai: {closest_products[1]["rating_average"]}
    - số lượt bán của sản phẩm thứ hai: {closest_products[1]["quantity_sold"]} 
    - tên sản phẩm thứ ba: {closest_products[2]["name"]}
    - đường dẫn sản phẩm thứ ba: {closest_products[2]["short_url"]}
    - mô tả sản phẩm thứ ba: {closest_products[2]["short_description"]}v n
    - đánh giá trung bình của sản phẩm thứ ba: {closest_products[2]["rating_average"]}
    - số lượt bán của sản phẩm thứ ba: {closest_products[2]["quantity_sold"]} 
    """
    
    result = load_openai(prompt)
    # result = {"message": prompt}
    print(type(result))
    return result.content