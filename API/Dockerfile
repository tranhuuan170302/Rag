# Sử dụng Python nhẹ nhất có thể
FROM python:3.10-slim

# Đặt thư mục làm việc
WORKDIR /API

# Copy file requirements trước để cache
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project vào container
COPY . .

# Thêm thư mục `src` vào PYTHONPATH để đảm bảo có thể import các module bên trong `src`
ENV PYTHONPATH=/API/src

# Expose cổng 8000 (cổng chạy FastAPI)
EXPOSE 8000

# Chạy ứng dụng bằng Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]