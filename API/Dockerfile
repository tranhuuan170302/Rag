# Sử dụng Python nhẹ nhất có thể
FROM python:3.10-slim

# Đặt thư mục làm việc
WORKDIR /API

# Copy file requirements trước để cache
COPY requirements.txt .

# Cài đặt thư viện Python
RUN pip install -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY ./src ./src
COPY ./ETL ./ETL
COPY ./Rag ./Rag
COPY ./settings ./settings
COPY .env .env

EXPOSE 8000
# Chạy ứng dụng bằng Uvicorn
CMD ["uvicorn", "src.app:app", "--reload"]
