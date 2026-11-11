# [CNPM-121] Thiết kế Kiến trúc Modular & Chốt Công nghệ Backend

## 1. Kiến trúc Clean Architecture (Modular Pattern)
- **Routes Layer (`src/routes/`)**: Xử lý HTTP Request/Response, validate payload và phân routing.
- **Service Layer (`src/services/`)**: Chứa toàn bộ Business Logic của hệ thống.
- **Model Layer (`src/models/`)**: Định nghĩa ORM Schema (SQLAlchemy/PostgreSQL).

## 2. Công nghệ Chốt cho Project
- **Backend**: Python 3.11+, Flask Web Framework, SQLAlchemy ORM.
- **Database**: PostgreSQL 15+ với `pgvector` extension.
- **Authentication**: JWT (JSON Web Token) với Hashing Werkzeug.
