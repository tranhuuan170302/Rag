import requests
import time
import pandas as pd
import random
from bs4 import BeautifulSoup
from config import databaseConnect 
from bson import ObjectId
from utils.embedding import get_embedding
from  utils.pipelinePreprocessingData import pipeline_processing, load_stopwords


cookie = {"_trackity": "e3890ca8-616a-2d9b-8fa4-915ab67c69b5", 
          "TOKENS": "{%22access_token%22:%22rEktsviFLx4Wh12pJdYBSQU8CnOaceVN%22}", 
          "delivery_zone": "Vk4wMjUwMDMwMDM=", 
		  "_ga": "GA1.1.1455002598.1725280955", 
          "_gcl_au": "1.1.436087193.1725280959", 
          "_hjSessionUser_522327": "eyJpZCI6IjQxOTkzNDkxLTlmOGQtNWM5MS1iZGQzLTAwYjU1ZDI2NTA3MyIsImNyZWF0ZWQiOjE3MTQyNjQ2MzIzOTEsImV4aXN0aW5nIjp0cnVlfQ==", 
          "_hjSession_522327": "eyJpZCI6ImNkZmM1MGNlLWY3NmItNDk4Yi04YTJmLWU4ODBmZGQ0YjQ2NCIsImMiOjE3MjUyODA5NTk5MzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=", 
          "tiki_client_id": "1455002598.1725280955", 
          "cto_bundle": "PB0Hc19XUiUyQm5NRndObnBlVG0yQUFYeU03TzBaSEZzSmhtSWFWSEVOeXRjdCUyRjBRbU14eHJaJTJCdHNjR3hrZ1hCYXQlMkZjenYyb2pubk9RTG5HbkM2VkglMkJaS0VPZjJSc0I5VFptQmRqRk4wJTJCUlBwYUw5VVVlMUpqYXlPcFhsczU0NTQ5c2Z3M2FhUEpXRHd4VlJxTThaVDhhdjNMeEElM0QlM0Q", 
		  "amp_99d374": "5tvru-dH9knPYv1RUajiPt...1i6pc48t5.1i6pcv0cr.1f.1n.36", 
		  "_ga_S9GLR1RQFJ": "GS1.1.1725280954.1.1.1725281859.10.0.0"}

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36 Edg/128.0.0.0",
    "Referer": "https://tiki.vn/nha-sach-tiki/c8322",
    "x-gusest-token": "rEktsviFLx4Wh12pJdYBSQU8CnOaceVN",
    "Connection": "Keep-Alive",
    "TE": "Trailers",
}

params = {
    "limit": "40",
    "include": "advertisement",
    "is_mweb": "1",
    "aggregations": "2",
    "version": "home-persionalized",
    "_v": "",
    "trackity_id": "e3890ca8-616a-2d9b-8fa4-915ab67c69b5",
    "category": "8322",
    "page": "1",
}

url = "https://tiki.vn/api/personalish/v1/blocks/listings"



def get_id_product():
    product_id = []
    for i in range(1, 20):
        params["page"] = str(i)
        response = requests.get(url, headers=headers, params=params, cookies=cookie)
        if response.status_code == 200:
            print(f"request successful")
            for record in response.json().get('data'):
                product_id.append({"id": record.get('id')})
        time.sleep(random.randrange(1, 10))
    return product_id
    
def parser_product(json):
    
    
    d = dict()
    d['id'] = json.get('id')
    d['name'] = json.get('name')
    d["type"] = json.get('type')
    d['current_seller'] = json.get('current_seller')['price']
    d['images']  = json.get('images')
    d['short_url'] = json.get('short_url')
    d['thumbnail_url'] = json.get('thumbnail_url')
    
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
        str(d.get('short_description', '')),
        str(d.get('description', ''))
    ])
    stopWord = load_stopwords("D:\WorkSpace\RAG\src\services\stopWord.txt")
    clean_text_string = pipeline_processing(merged_string, stopWord)
    
    d['embedding'] = get_embedding(clean_text_string)
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
        db = databaseConnect.get_database()
        product_collection = db['productsBook']  # Tên collection
        result = product_collection.insert_one(product_data)
        # Lấy sản phẩm mới chèn từ MongoDB, bao gồm cả ObjectId
        inserted_product = product_collection.find_one({"_id": ObjectId(result.inserted_id)})
        return inserted_product
    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu sản phẩm: {e}")
        return None

def get_product_collection(product_id):
    product_details = []
    for i, product in enumerate(product_id):
        print(product['id'])
        product_url = "https://tiki.vn/api/v2/products/{}".format(product['id'])
        response = requests.get(product_url, headers=headers, cookies=cookie, params=params)
        if response.status_code == 200:
            try:
                product_details.append(parser_product(response.json()))
                print("Crawl data {} Sucess !!!".format(product['id']))
                product_item = parser_product(response.json())
                insert_product(product_item)
                
            except Exception as e:
                print(f"Error when crawl data {product['id']} : {e}")
                continue
            
            
# # main function
def raw_service():
    product_id = get_id_product()
    get_product_collection(product_id)
    