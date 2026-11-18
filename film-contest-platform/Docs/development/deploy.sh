#!/bin/bash
# [CNPM-79] Script tự động triển khai (Deployment Script) cho bản Release cuối

echo "🚀 Bắt đầu quá trình triển khai bản cuối (Sprint 4)..."

# 1. Cập nhật mã nguồn
echo "Kéo mã nguồn mới nhất từ nhánh main..."
git pull origin main

# 2. Build và khởi động lại Docker containers
echo "Đang build lại các image và khởi động Docker..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 3. Chạy migration database (nếu có)
echo "Chạy Database Migration..."
docker exec -it backend_container flask db upgrade

echo "✅ Triển khai thành công! Hệ thống đang chạy ở môi trường Production."
