import requests
import time
import pandas as pd
import json
import random
from bs4 import BeautifulSoup

from bson import ObjectId
import logging
from API.Rag.embedding import get_embedding
from pipelinePreprocessingData import pipeline_processing, load_stopwords
from API.Settings.settings import cookie, headers, params, url, categories
from API.src.config import databaseConnect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_id_product(category: dict, numPage: int):
    product_id = []
    params["category"] = category['idCategory']
    logger.info(f"====start crawl data {category['nameCategory']}===")
    for i in range(1, numPage):
        logger.info(f"page: {i}")
        params["page"] = str(i)
        response = requests.get(url, headers=headers, params=params, cookies=cookie)
        if response.status_code == 200:
            logger.info(f"request successful")
            for record in response.json().get('data'):
                product_id.append({"id": record.get('id')})
        time.sleep(random.randrange(1, 10))
    return product_id
    
def parser_product(json, nameCategory: str):
    
    
    d = dict()
    d['id'] = json.get('id')
    d['name'] = json.get('name')
    d["type"] = json.get('type')
    d['current_seller'] = json.get('current_seller')['price']
    d['images']  = json.get('images')
    d['short_url'] = json.get('short_url')
    d['thumbnail_url'] = json.get('thumbnail_url')
    d['nameCategory'] = nameCategory
    content_short_description = json.get('short_description')
    content_description = json.get('description')
    
    soup_description = BeautifulSoup(content_description, "html.parser")
    clean_description = soup_description.get_text()
    
    soup_short_description = BeautifulSoup(content_short_description, "html.parser") 
    clean_short_description = soup_short_description.get_text()
    
    d['short_description'] = clean_short_description
    d['description'] = clean_description
    d['rating_average'] = json.get('rating_average')
    d['quantity_sold'] = json.get('quantity_sold')['value']
    
    merged_string = " ".join([
        str(d.get('name', '')),
        str(d.get('type', '')),
        str(d.get('short_description', ''))
    ])
    stopWord = load_stopwords("D:\WorkSpace\RAG\API\ETL\stopWord.txt")
    clean_text_string = pipeline_processing(merged_string, stopWord)
    
    d['embedding'] = get_embedding.encoder_query(clean_text_string)
    return d

def insert_product(product_data: dict):
    """
    Chèn dữ liệu sản phẩm vào collection 'products'.
    
    Args:
    - product_data (dict): Dữ liệu sản phẩm bao gồm các cột như 'name', 'type', 'current_seller', ...
    
    Returns:
    - dict: Dữ liệu sản phẩm được chèn kèm với `_id`.
    - None: Nếu có lỗi xảy ra.
    """
    try:
        logger.info(f"inserting data {product_data['name']}")
        db = databaseConnect.get_database()
        product_collection = db['Products']  # Tên collection
        result = product_collection.insert_one(product_data)
        # Lấy sản phẩm mới chèn từ MongoDB, bao gồm cả ObjectId
        inserted_product = product_collection.find_one({"_id": ObjectId(result.inserted_id)})
        logger.info(f"inserted data {product_data['name']}")
        return inserted_product
    except Exception as e:
        logger.error(f"Error inserting data {product_data['name']}: {e}")
        return None

def get_product_collection(product_id, nameCategory: str):
    # product_details = []
    for i, product in enumerate(product_id):
        logger.info(f"====start crawl data {product['id']}===")
        product_url = "https://tiki.vn/api/v2/products/{}".format(product['id'])
        response = requests.get(product_url, headers=headers, cookies=cookie, params=params)
        if response.status_code == 200:
            try:
                # product_details.append(parser_product(response.json(), nameCategory))
                logger.info(f"Crawl data {product['id']} Sucess !!!")
                product_item = parser_product(response.json(), nameCategory)
                insert_product(product_item)
                
            except Exception as e:
                logger.error(f"Error when crawl data {product['id']} : {e}")
                continue
            
            
# main function
def run_pipeline():
    numPage = 30
    for category in categories:
        print(category)
        nameCategory = category['nameCategory']
        product_id = get_id_product(category, numPage)
        get_product_collection(product_id, nameCategory)

if __name__ == "__main__":
    run_pipeline()