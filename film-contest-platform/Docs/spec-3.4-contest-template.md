# Đặc tả Chức năng — [3.4] Template Cuộc thi Tái sử dụng

- **Task Jira:** CNPM-148 (FE3 / WBS 3.4)
- **Mức ưu tiên:** Could (Tính năng linh hoạt, ưu tiên làm sau các tính năng Must/Should)
- **Ước tính:** 10 man-hours
- **Công nghệ:** Node.js Express, PostgreSQL (JSONB column)

---

## 1. Mục tiêu & Quy tắc Nghiệp vụ

### 1.1 Mục tiêu
Cho phép Ban tổ chức (Organizer) sao chép cấu hình của một cuộc thi đã có (hạng mục, thể lệ, giải thưởng, tiêu chí chấm) thành mẫu (Template) và khởi tạo cuộc thi mới nhanh chóng.

### 1.2 Quy tắc Nghiệp vụ (Business Rules)
- **BR-1:** Template lưu dưới dạng ảnh chụp cấu hình (Snapshot data). Thay đổi ở cuộc thi gốc không làm thay đổi Template đã lưu.
- **BR-2:** Cuộc thi mới tạo từ Template sẽ ở trạng thái `DRAFT` (Nháp).
- **BR-3:** Mốc thời gian (ngày mở đăng ký, ngày nộp bài, ngày chấm) không lưu mốc cố định mà bắt buộc Organizer nhập mới khi khởi tạo từ Template.
- **BR-4:** Template thuộc sở hữu riêng của Organizer tạo ra nó (không chia sẻ giữa các bên theo LI6).
- **BR-5:** Xóa Template là xóa mềm (`deleted_at`).

---

## 2. Mô hình Dữ liệu (PostgreSQL)

Cấu hình chi tiết của Template được lưu trữ dưới dạng định dạng JSON (`JSONB`) để đảm bảo tính linh hoạt khi cấu hình cuộc thi thay đổi.

```sql
CREATE TABLE contest_templates (
    id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_contest_id INT REFERENCES contests(id) ON DELETE SET NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

### Cấu trúc JSON dữ liệu `config`:
```json
{
  "categories": [
    { "name": "Chân dung Analog", "description": "Ảnh chụp chân dung" }
  ],
  "regulations": {
    "max_submissions_per_user": 3,
    "allowed_file_types": ["jpg", "jpeg", "png"],
    "max_file_size_mb": 25
  },
  "prizes": [
    { "rank": "Nhất", "reward": "10.000.000 VNĐ + Cúp" }
  ],
  "criteria_preset_id": 1
}
```

---

## 3. Thiết kế RESTful API

- `POST /api/v1/contests/:id/save-as-template`: Lưu cuộc thi `:id` thành Template mới.
- `GET /api/v1/templates`: Lấy danh sách Template của Organizer đang đăng nhập.
- `GET /api/v1/templates/:tid`: Xem chi tiết cấu hình Template `:tid`.
- `POST /api/v1/contests/from-template/:tid`: Khởi tạo cuộc thi nháp mới từ Template `:tid`.
- `DELETE /api/v1/templates/:tid`: Xóa mềm Template.
