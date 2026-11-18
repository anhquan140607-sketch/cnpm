# CNPM-86: [12.3] Triển lãm Online - API Specification
## Người thực hiện: Đinh Quang Thọ (M1 - nhận từ M3)
## Sprint 4 | FE12 Công bố kết quả

---

### 1. Mô tả tính năng

Triển lãm Online là trang hiển thị tác phẩm đoạt giải theo dạng gallery công khai, có thể xem sau khi cuộc thi kết thúc. Cho phép người dùng xem ảnh, thông tin tác phẩm và giải thưởng đạt được mà không cần đăng nhập.

---

### 2. API Endpoints

#### GET /api/exhibitions
- **Mô tả:** Lấy danh sách tác phẩm đoạt giải (gallery công khai)
- **Auth:** Không cần (public)
- **Query params:**
  - `page` (int, default=1): Trang hiện tại
  - `per_page` (int, default=12): Số tác phẩm mỗi trang
  - `contest_id` (int, optional): Lọc theo cuộc thi
  - `category_id` (int, optional): Lọc theo hạng mục
- **Response:**
```json
{
  "submissions": [
    {
      "submission_id": 1,
      "title": "Tên tác phẩm",
      "author": "Tên tác giả",
      "thumbnail_url": "...",
      "award": {
        "award_id": 1,
        "name": "Giải nhất",
        "rank": 1
      },
      "category": {
        "category_id": 2,
        "name": "Phong cảnh"
      },
      "contest": {
        "contest_id": 1,
        "name": "Cuộc thi 2026"
      }
    }
  ],
  "total": 50,
  "page": 1,
  "per_page": 12
}
```

---

#### GET /api/exhibitions/{submission_id}
- **Mô tả:** Chi tiết 1 tác phẩm triển lãm
- **Auth:** Không cần (public)
- **Path params:**
  - `submission_id` (int): ID của tác phẩm
- **Response:**
```json
{
  "submission_id": 1,
  "title": "Tên tác phẩm",
  "description": "Mô tả tác phẩm",
  "submitted_at": "2026-05-10T08:00:00Z",
  "author": {
    "user_id": 10,
    "full_name": "Nguyễn Văn A",
    "avatar_url": "..."
  },
  "award": {
    "award_id": 1,
    "name": "Giải nhất",
    "rank": 1,
    "description": "Tác phẩm xuất sắc nhất"
  },
  "category": {
    "category_id": 2,
    "name": "Phong cảnh"
  },
  "contest": {
    "contest_id": 1,
    "name": "Cuộc thi Nhiếp ảnh 2026",
    "ended_at": "2026-04-30T23:59:59Z"
  },
  "archive_items": [
    {
      "item_id": 1,
      "file_url": "...",
      "file_type": "image/jpeg"
    }
  ]
}
```

---

#### GET /api/exhibitions/contests
- **Mô tả:** Danh sách các cuộc thi có triển lãm (đã kết thúc và có tác phẩm đoạt giải)
- **Auth:** Không cần (public)
- **Response:**
```json
{
  "contests": [
    {
      "contest_id": 1,
      "name": "Cuộc thi Nhiếp ảnh 2026",
      "ended_at": "2026-04-30T23:59:59Z",
      "total_awarded": 12
    }
  ]
}
```

---

### 3. Data Models liên quan

Từ ERD của hệ thống:

| Model | Vai trò |
|---|---|
| `Submission` | Tác phẩm dự thi, nguồn chính của gallery |
| `Award` | Thông tin giải thưởng liên kết với Submission |
| `Archive_Item` | File ảnh/video đính kèm tác phẩm |
| `User` | Thông tin tác giả (participant) |
| `Category` | Hạng mục của tác phẩm |
| `Contest` | Cuộc thi mà tác phẩm thuộc về |

---

### 4. Use Cases

- **UC1:** Người xem truy cập gallery công khai → xem danh sách tác phẩm đoạt giải dạng lưới
- **UC2:** Lọc theo cuộc thi / hạng mục → thu hẹp kết quả gallery
- **UC3:** Xem chi tiết tác phẩm → modal/trang chi tiết hiển thị ảnh lớn, thông tin giải thưởng, tác giả

---

### 5. Acceptance Criteria

- [ ] Hiển thị gallery tác phẩm đoạt giải dạng lưới (grid)
- [ ] Lọc được theo cuộc thi và hạng mục
- [ ] Xem chi tiết tác phẩm và thông tin giải thưởng
- [ ] Responsive, public access (không cần đăng nhập)
- [ ] Phân trang hoạt động đúng
- [ ] API trả về HTTP 404 nếu `submission_id` không tồn tại hoặc chưa được trao giải
