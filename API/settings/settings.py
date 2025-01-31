import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

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

categories = [
    {
        "nameCategory": "Thư viện - Sách", 
        "idCategory": "8322"
    },
    {
        "nameCategory": "Nhà Cửa - Đời sống",
        "idCategory": "1883"
    }, 
    {
        "nameCategory": "Điện thoại - Máy tính bảng", 
        "idCategory": "1789"
    }, 
    {
        "nameCategory": "Đồ chơi - Trẻ em", 
        "idCategory": "2549"
    }, {
        "nameCategory": "Thiết bị số - Phụ kiện số", 
        "idCategory": "1815"
    }, {
        "nameCategory": "Điện gia dụng", 
        "idCategory": "1882"
    }, {
        "nameCategory": "Làm đẹp - sức khỏe", 
        "idCategory": "1520"
    }, {
        "nameCategory": "Ô Tô - Xe đạp - xe máy", 
        "idCategory": "8594"
    }, {
        "nameCategory": "Thời trang nữ", 
        "idCategory": "931"
    }, {
        "nameCategory": "Bách hóa Online",
        "idCategory": "4384"
    }, {
        "nameCategory": "Thể Thao - Giả ngoại", 
        "idCategory": "1975"
    }, {
        "nameCategory": "Hàng quốc tế", 
        "idCategory": "17166"
    }, {
        "nameCategory": "Laptop - phụ kiện máy tính", 
        "idCategory": "1846"
    }
]

file_stopword  = "API/ETL/stopWord.txt"
embedding_model = "API/Model_LLM/models--thenlper--gte-large/snapshots/4bef63f39fcc5e2d6b0aae83089f307af4970164"