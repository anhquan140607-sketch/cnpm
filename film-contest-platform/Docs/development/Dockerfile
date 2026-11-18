# [CNPM-79] Dockerfile Production
FROM python:3.10-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements và cài đặt
COPY BE_Flask/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code Backend
COPY BE_Flask/ .

# Expose port
EXPOSE 5000

# Chạy bằng Gunicorn cho môi trường production
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:app"]
