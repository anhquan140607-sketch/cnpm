# BE_Flask - Film Contest Platform Backend

Backend Flask với Clean Architecture cho hệ thống quản lý cuộc thi phim.

## Tech Stack
- Python + Flask
- SQLAlchemy ORM (18 models từ ERD.MD)
- PostgreSQL / MySQL / MSSQL (Factory Pattern)
- JWT Authentication

## Cài đặt

```bash
pip install -r requirements.txt
cp .env.example .env
# Sửa .env với thông tin database của bạn
python run.py
```

## Cấu trúc (Clean Architecture)
