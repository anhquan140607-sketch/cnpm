# Hướng dẫn chạy Backend cục bộ (Local Backend Setup)

Tài liệu hướng dẫn các thành viên trong nhóm thiết lập và chạy Backend API trên máy cá nhân để phát triển hoặc kiểm thử.

---

## 1. Yêu cầu môi trường
- **Node.js**: Phiên bản 20+ hoặc 22+ LTS ([Tải tại nodejs.org](https://nodejs.org/))
- **PostgreSQL**: Phiên bản 16+ ([Tải tại postgresql.org](https://www.postgresql.org/download/))
- **Git**: Đã cài đặt và cấu hình SSH hoặc Personal Access Token

---

## 2. Các bước cài đặt chi tiết

### Bước 1: Mở thư mục Backend
```bash
cd film-contest-platform/BE
```

### Bước 2: Cài đặt các gói phụ thuộc (Dependencies)
```bash
npm install
```

### Bước 3: Cấu hình file môi trường (.env)
Sao chép file mẫu `.env.example` thành file `.env`:
```bash
cp .env.example .env
```
Mở file `.env` và kiểm tra cấu hình kết nối cơ sở dữ liệu:
```env
PORT=5000
NODE_ENV=development
API_PREFIX=/api/v1

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=mat_khau_postgres_cua_ban
DB_NAME=film_contest_db

JWT_SECRET=super_secret_jwt_key_film_contest_2026_change_in_production
JWT_REFRESH_SECRET=super_secret_refresh_key_film_contest_2026
```

### Bước 4: Khởi tạo Database và nạp dữ liệu mẫu (Seed Data)
Chạy lệnh tự động tạo database `film_contest_db`, 18 bảng dữ liệu và tài khoản mẫu:
```bash
npm run db:seed
```

> **Danh sách tài khoản kiểm thử mặc định (Mật khẩu: `password123`):**
> - **Quản trị viên (Admin):** `admin@filmcontest.vn`
> - **Ban tổ chức (Organizer):** `organizer@filmcontest.vn`
> - **Giám khảo (Judge):** `judge@filmcontest.vn`
> - **Thí sinh (Participant):** `participant@filmcontest.vn`

### Bước 5: Chạy máy chủ ở chế độ phát triển
```bash
npm run dev
```

---

## 3. Kiểm tra kết quả
- **Tài liệu Swagger tương tác:** [http://localhost:5000/api/docs](http://localhost:5000/api/docs)
- **Kiểm tra tình trạng sức khỏe máy chủ:** [http://localhost:5000/api/health](http://localhost:5000/api/health)
