# Đặc tả Chức năng — [5.1] Hồ sơ & Portfolio Thí sinh

- **Task Jira:** CNPM-136 (FE5 / WBS 5.1)
- **Mức ưu tiên:** Must
- **Ước tính:** 8 man-hours
- **Công nghệ:** Node.js Express, PostgreSQL, Cloud Storage (Firebase/Azure)

---

## 1. Mục tiêu & Giới hạn

### 1.1 Mục tiêu
Quản lý hồ sơ cá nhân của người tham gia (Participant) và cung cấp trang Portfolio cá nhân tổng hợp các bức ảnh đã nộp dự thi qua các mùa giải.

### 1.2 Giới hạn (Theo LI3, LI6, LI10)
- **LI3:** Không phát triển các tính năng mạng xã hội (không nút Like, bình luận công khai hay Theo dõi tác giả).
- **LI10:** Không tích hợp công cụ chỉnh sửa ảnh hay đóng dấu bản quyền watermark trên trang hồ sơ.
- **LI3:** Hồ sơ thí sinh là riêng tư. Chỉ cá nhân thí sinh và Organizer (duyệt bài) mới có quyền xem thông tin hồ sơ này.

---

## 2. Mô hình Dữ liệu (PostgreSQL)

```sql
CREATE TABLE participant_profiles (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(150) NOT NULL,
    display_name VARCHAR(100),
    phone VARCHAR(20),
    country VARCHAR(100),
    city VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(500),
    gear_notes TEXT, -- Thiết bị phim/ống kính hay sử dụng
    website_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

*Lưu ý:* Danh mục **Portfolio** không tạo bảng riêng trong CSDL mà sử dụng truy vấn linh hoạt từ bảng `submissions` lọc theo `user_id` của thí sinh.

---

## 3. Thiết kế RESTful API

- `GET /api/v1/me/profile`: Lấy thông tin hồ sơ của cá nhân đang đăng nhập.
- `PUT /api/v1/me/profile`: Cập nhật thông tin hồ sơ cá nhân.
- `POST /api/v1/me/profile/avatar`: Tải ảnh đại diện lên Cloud Storage (Chấp nhận JPEG/PNG, tối đa 5MB).
- `GET /api/v1/me/portfolio`: Lấy danh sách ảnh dự thi cá nhân đã nộp (Hỗ trợ phân trang và lọc theo trạng thái cuộc thi).
- `GET /api/v1/contests/:id/registrations/:uid/profile`: Ban tổ chức xem thông tin hồ sơ của thí sinh `:uid` khi duyệt đăng ký cuộc thi.
