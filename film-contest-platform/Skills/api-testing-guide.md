# Hướng dẫn kiểm thử REST API (API Testing Guide)

Tài liệu hướng dẫn các thành viên (Frontend Web, Flutter Mobile, Tester) cách gọi và kiểm thử các API của Backend thông qua Swagger UI và Postman.

---

## 1. Kiểm thử trực tiếp qua giao diện Swagger UI

Sau khi Backend đã chạy (`npm run dev`), mở trình duyệt vào:
👉 **[http://localhost:5000/api/docs](http://localhost:5000/api/docs)**

### Quy trình 3 bước kiểm thử một API bảo mật:

#### Bước 1: Đăng nhập lấy Bearer Token
1. Mở endpoint `POST /api/v1/auth/login`.
2. Bấm **Try it out** -> Nhập tài khoản phù hợp với vai trò bạn muốn test:
   - **Admin:** `admin@filmcontest.vn` / `password123`
   - **Organizer:** `organizer@filmcontest.vn` / `password123`
   - **Judge:** `judge@filmcontest.vn` / `password123`
   - **Participant:** `participant@filmcontest.vn` / `password123`
3. Bấm **Execute**.
4. Sao chép toàn bộ chuỗi ký tự trong trường `"accessToken"` (bắt đầu bằng `eyJhbGciOi...`).

#### Bước 2: Gắn Token vào Swagger
1. Cuộn lên đầu trang Swagger -> Bấm nút **Authorize** (biểu tượng ổ khóa màu xanh lá).
2. Dán chuỗi `accessToken` vào ô **Value** -> Bấm **Authorize** -> Bấm **Close**.

#### Bước 3: Gọi các API được phân quyền
- Nếu đang là **Organizer**: Bạn có thể gọi `POST /api/v1/contests` (Tạo cuộc thi) hoặc `GET /api/v1/verification/submissions` (Duyệt ảnh).
- Nếu đang là **Participant**: Bạn có thể gọi `POST /api/v1/participant/film-rolls` (Khai báo cuộn phim) hoặc `POST /api/v1/participant/submissions` (Nộp ảnh thi).
- Nếu đang là **Judge**: Bạn có thể gọi `GET /api/v1/judging/workspace` (Không gian chấm) và `POST /api/v1/judging/submissions/{id}/evaluate` (Chấm điểm).

---

## 2. Kiểm thử bằng Postman (Hoặc cURL)

### Cấu hình Header bắt buộc:
- `Content-Type: application/json`
- `Authorization: Bearer <chuỗi_access_token_của_bạn>`

### Ví dụ lệnh cURL kiểm tra danh sách cuộn phim cá nhân:
```bash
curl -X GET "http://localhost:5000/api/v1/participant/film-rolls/my" \
  -H "Authorization: Bearer eyJhbGciOi..." \
  -H "Content-Type: application/json"
```

---

## 3. Các mã trạng thái HTTP chuẩn (HTTP Status Codes)

| Mã HTTP | Ý nghĩa | Khi nào gặp |
| --- | --- | --- |
| **200 OK** | Thành công | Lấy dữ liệu hoặc cập nhật thành công |
| **201 Created** | Tạo mới thành công | Đăng ký tài khoản, tạo cuộc thi, nộp ảnh |
| **400 Bad Request** | Dữ liệu gửi lên sai | Thiếu trường bắt buộc, vượt giới hạn điểm |
| **401 Unauthorized** | Chưa xác thực | Thiếu token, token sai hoặc đã hết hạn |
| **403 Forbidden** | Không có quyền | Dùng tài khoản Participant gọi API của Admin |
| **404 Not Found** | Không tìm thấy | ID cuộc thi hoặc tài khoản không tồn tại |
| **409 Conflict** | Trùng lặp dữ liệu | Email đã tồn tại, đã đăng ký hạng mục rồi |
| **500 Server Error** | Lỗi nội bộ máy chủ | Lỗi cơ sở dữ liệu hoặc crash logic |
