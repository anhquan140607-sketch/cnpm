# Film Photography Contest Platform - Backend API (BE)

Hệ thống Backend REST API phục vụ nền tảng tổ chức và quản lý cuộc thi nhiếp ảnh phim tích hợp trí tuệ nhân tạo.

## 1. Công nghệ sử dụng

- **Ngôn ngữ & Runtime:** Node.js (v20+ / v22+ LTS), TypeScript
- **Framework:** Express.js với kiến trúc phân tầng Modular
- **Cơ sở dữ liệu:** PostgreSQL 16+
- **Xác thực & Phân quyền:** JWT (Access Token & Refresh Token), Middleware RBAC (4 vai trò: `administrator`, `organizer`, `judge`, `participant`)
- **Tài liệu API:** Swagger / OpenAPI 3.0 (tích hợp sẵn tại `/api/docs`)
- **Mã hóa:** Bcrypt băm mật khẩu

---

## 2. Cấu trúc thư mục Modular

```
BE/
├── src/
│   ├── modules/
│   │   ├── auth/            # FE1: Đăng ký, đăng nhập, JWT, RBAC, phân quyền 4 vai trò
│   │   ├── system/          # FE2: Quản lý danh mục master data (brand, stock, iso, format, camera, lens, lab, scanner), Activity log
│   │   ├── contest/         # FE3, FE4: Quản lý cuộc thi, hạng mục, tiêu chí chấm điểm (tổng trọng số 100%)
│   │   ├── participant/     # FE5, FE6, FE7: Đăng ký thi, quản lý cuộn phim, khung hình, nộp bài thi
│   │   ├── verification/    # FE8, FE9: Kiểm tra bài dự thi, duyệt ảnh, lưu kết quả AI (trùng lặp, AI-generated)
│   │   ├── judging/         # FE10, FE11: Phân công giám khảo, không gian chấm thi, tổng hợp điểm & xếp hạng
│   │   ├── publication/     # FE12, FE13: Trao giải thưởng, công bố kết quả triển lãm trực tuyến, kho lưu trữ số
│   │   └── support/         # FE14, FE15, FE16: Báo cáo thống kê, dashboard, hoạt động vận hành
│   ├── common/              # Middleware JWT/RBAC, Error Handler, Response Helper, Logger
│   ├── config/              # Cấu hình biến môi trường (.env)
│   ├── database/            # schema.sql (18 bảng), seed.sql, migrate.ts, connection pool
│   ├── docs/                # Swagger / OpenAPI specification
│   ├── app.ts               # Khởi tạo Express App, middleware và router
│   └── server.ts            # Entrypoint lắng nghe cổng, kiểm tra database
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

---

## 3. Hướng dẫn cài đặt & Chạy dự án

### Bước 1: Cài đặt dependencies

Mở terminal tại thư mục `BE/`:

```bash
npm install
```

### Bước 2: Cấu hình biến môi trường

Tạo file `.env` từ file mẫu `.env.example`:

```bash
cp .env.example .env
```

Chỉnh sửa thông số kết nối PostgreSQL trong file `.env`:
```env
PORT=5000
NODE_ENV=development
API_PREFIX=/api/v1

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=film_contest_db

JWT_SECRET=super_secret_jwt_key_film_contest_2026_change_in_production
JWT_REFRESH_SECRET=super_secret_refresh_key_film_contest_2026
```

### Bước 3: Khởi tạo Cơ sở dữ liệu & Dữ liệu mẫu (Seed Data)

Chạy lệnh migration để tự động tạo database `film_contest_db`, 18 bảng dữ liệu và nạp dữ liệu mẫu (các dòng phim, hãng phim, phòng lab, máy scan và tài khoản demo):

```bash
npm run db:seed
```

> **Tài khoản mặc định được khởi tạo (Mật khẩu: `password123`):**
> - **Administrator:** `admin@filmcontest.vn`
> - **Organizer:** `organizer@filmcontest.vn`
> - **Judge:** `judge@filmcontest.vn`
> - **Participant:** `participant@filmcontest.vn`

### Bước 4: Chạy máy chủ phát triển (Development)

```bash
npm run dev
```

Máy chủ sẽ chạy tại: **http://localhost:5000**  
Giao diện Swagger tương tác: **http://localhost:5000/api/docs**  
Kiểm tra tình trạng máy chủ: **http://localhost:5000/api/health**

---

## 4. Danh sách các nhóm API chính

| Endpoint | Mô tả | Vai trò |
| --- | --- | --- |
| `POST /api/v1/auth/register` | Đăng ký tài khoản mới | Công khai |
| `POST /api/v1/auth/login` | Đăng nhập nhận Access & Refresh Token | Công khai |
| `GET /api/v1/auth/profile` | Xem hồ sơ cá nhân | Đã đăng nhập |
| `GET /api/v1/system/master-data` | Lấy danh mục phim, máy ảnh, lab tráng | Công khai / Tất cả |
| `GET /api/v1/system/activity-logs` | Xem nhật ký thao tác hệ thống | Administrator |
| `GET /api/v1/contests` | Xem danh sách cuộc thi | Công khai |
| `POST /api/v1/contests` | Tạo cuộc thi mới | Organizer, Admin |
| `POST /api/v1/participant/film-rolls` | Khai báo cuộn phim & thiết bị chụp | Participant |
| `POST /api/v1/participant/submissions` | Nộp ảnh dự thi kèm số khung hình | Participant |
| `GET /api/v1/verification/submissions` | Kiểm tra và duyệt bài dự thi | Organizer, Admin |
| `GET /api/v1/judging/workspace` | Không gian chấm thi của giám khảo | Judge |
| `POST /api/v1/judging/submissions/:id/evaluate` | Chấm điểm bài thi theo tiêu chí | Judge |
| `GET /api/v1/publication/exhibition/:id` | Triển lãm trực tuyến cuộc thi đã công bố | Công khai |
| `GET /api/v1/support/dashboard-stats` | Thống kê số liệu toàn hệ thống | Organizer, Admin |
