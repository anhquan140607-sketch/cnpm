# API Specification: CNPM-87 - Tìm Kiếm và Lọc Archive

> **Task:** CNPM-87 [13.2] Tìm kiếm và lọc archive  
> **Người thực hiện:** Đinh Quang Thọ (M1 - nhận từ M3)  
> **Dự án:** Film Contest Platform  
> **Phiên bản:** 1.0  
> **Ngày tạo:** 2026-11-18  

---

## Tổng quan

Kho lưu trữ số (Archive) là hệ thống lưu trữ và tra cứu tất cả tác phẩm từ các cuộc thi đã kết thúc. Module này cung cấp các API public cho phép tìm kiếm full-text và lọc đa điều kiện trên các Archive Item.

### Authentication
- **Tất cả endpoint đều là PUBLIC** – không yêu cầu token xác thực.
- Rate limiting: 100 requests/phút mỗi IP.

### Base URL
```
/api/archive
```

### Content-Type
```
application/json
```

---

## Data Models (từ ERD)

### Archive_Item
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER (PK) | Khóa chính |
| submission_id | INTEGER (FK) | Liên kết Submission |
| archived_at | TIMESTAMP | Thời điểm lưu trữ |
| archive_note | TEXT | Ghi chú lưu trữ |
| is_featured | BOOLEAN | Được đánh dấu nổi bật |

### Submission (liên quan)
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER (PK) | Khóa chính |
| title | VARCHAR(255) | Tên tác phẩm |
| description | TEXT | Mô tả |
| user_id | INTEGER (FK) | Tác giả (User) |
| contest_id | INTEGER (FK) | Cuộc thi (Contest) |
| category_id | INTEGER (FK) | Hạng mục (Category) |
| score | FLOAT | Điểm số |
| award | VARCHAR(100) | Giải thưởng (nullable) |
| submitted_at | TIMESTAMP | Ngày nộp |
| film_roll_id | INTEGER (FK) | Cuộn phim (Film_Roll) |

### User (liên quan)
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER (PK) | Khóa chính |
| full_name | VARCHAR(255) | Họ tên |
| username | VARCHAR(100) | Tên đăng nhập |

### Contest (liên quan)
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER (PK) | Khóa chính |
| name | VARCHAR(255) | Tên cuộc thi |
| year | INTEGER | Năm tổ chức |
| status | VARCHAR(50) | Trạng thái (ended) |

### Category (liên quan)
| Trường | Kiểu | Mô tả |
|--------|------|-------|
| id | INTEGER (PK) | Khóa chính |
| name | VARCHAR(100) | Tên hạng mục |

---

## Endpoints

---

### 1. GET /api/archive
**Mô tả:** Lấy danh sách các tác phẩm đã được lưu trữ, hỗ trợ phân trang và lọc đa điều kiện.

#### Query Parameters

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
|---------|------|----------|----------|-------|
| `page` | integer | Không | 1 | Số trang hiện tại |
| `per_page` | integer | Không | 20 | Số item mỗi trang (tối đa 100) |
| `year` | integer | Không | — | Lọc theo năm cuộc thi (vd: 2024) |
| `category_id` | integer | Không | — | Lọc theo ID hạng mục |
| `has_award` | boolean | Không | — | `true` = chỉ tác phẩm có giải; `false` = chưa có giải |
| `sort_by` | string | Không | `archived_at` | Sắp xếp: `archived_at`, `score`, `title` |
| `sort_order` | string | Không | `desc` | Thứ tự: `asc` hoặc `desc` |
| `is_featured` | boolean | Không | — | Lọc tác phẩm nổi bật |

#### Ví dụ Request
```
GET /api/archive?page=1&per_page=10&year=2024&has_award=true&sort_by=score&sort_order=desc
```

#### Response 200 OK
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "archived_at": "2024-12-15T10:30:00Z",
        "archive_note": "Tác phẩm xuất sắc cuộc thi 2024",
        "is_featured": true,
        "submission": {
          "id": 42,
          "title": "Ánh Bình Minh",
          "description": "Bức ảnh chụp bình minh tại Hà Giang",
          "score": 9.5,
          "award": "Giải Nhất",
          "submitted_at": "2024-11-01T08:00:00Z",
          "thumbnail_url": "/static/uploads/thumbnails/submission_42.jpg",
          "author": {
            "id": 7,
            "full_name": "Nguyễn Văn A",
            "username": "nguyenvana"
          },
          "contest": {
            "id": 3,
            "name": "Cuộc Thi Nhiếp Ảnh 2024",
            "year": 2024
          },
          "category": {
            "id": 2,
            "name": "Phong Cảnh"
          }
        }
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 10,
      "total_items": 158,
      "total_pages": 16,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

#### Response 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "INVALID_PARAMS",
    "message": "Tham số 'per_page' phải nằm trong khoảng 1-100"
  }
}
```

---

### 2. GET /api/archive/search
**Mô tả:** Tìm kiếm full-text trong kho lưu trữ theo tên tác phẩm, mô tả, tên tác giả, và tên cuộc thi.

#### Query Parameters

| Tham số | Kiểu | Bắt buộc | Mặc định | Mô tả |
|---------|------|----------|----------|-------|
| `q` | string | **Có** | — | Từ khóa tìm kiếm (tối thiểu 2 ký tự) |
| `page` | integer | Không | 1 | Số trang |
| `per_page` | integer | Không | 20 | Số item mỗi trang |
| `year` | integer | Không | — | Lọc thêm theo năm |
| `category_id` | integer | Không | — | Lọc thêm theo hạng mục |
| `has_award` | boolean | Không | — | Lọc thêm theo giải thưởng |
| `sort_by` | string | Không | `relevance` | Sắp xếp: `relevance`, `score`, `archived_at` |

#### Phạm vi tìm kiếm
Full-text search sẽ tìm trong các trường:
- `Submission.title` (trọng số cao nhất)
- `Submission.description`
- `User.full_name` / `User.username`
- `Contest.name`
- `Category.name`
- `Archive_Item.archive_note`

#### Ví dụ Request
```
GET /api/archive/search?q=bình+minh+hà+giang&year=2024&sort_by=relevance
```

#### Response 200 OK
```json
{
  "success": true,
  "data": {
    "query": "bình minh hà giang",
    "items": [
      {
        "id": 1,
        "archived_at": "2024-12-15T10:30:00Z",
        "is_featured": true,
        "relevance_score": 0.95,
        "highlight": {
          "title": "Ánh <mark>Bình Minh</mark>",
          "description": "Bức ảnh chụp <mark>bình minh</mark> tại <mark>Hà Giang</mark>"
        },
        "submission": {
          "id": 42,
          "title": "Ánh Bình Minh",
          "score": 9.5,
          "award": "Giải Nhất",
          "thumbnail_url": "/static/uploads/thumbnails/submission_42.jpg",
          "author": {
            "id": 7,
            "full_name": "Nguyễn Văn A",
            "username": "nguyenvana"
          },
          "contest": {
            "id": 3,
            "name": "Cuộc Thi Nhiếp Ảnh 2024",
            "year": 2024
          },
          "category": {
            "id": 2,
            "name": "Phong Cảnh"
          }
        }
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_items": 3,
      "total_pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

#### Response 400 – Query quá ngắn
```json
{
  "success": false,
  "error": {
    "code": "QUERY_TOO_SHORT",
    "message": "Từ khóa tìm kiếm phải có ít nhất 2 ký tự"
  }
}
```

#### Response 400 – Thiếu `q`
```json
{
  "success": false,
  "error": {
    "code": "MISSING_QUERY",
    "message": "Tham số 'q' là bắt buộc"
  }
}
```

---

### 3. GET /api/archive/{id}
**Mô tả:** Lấy thông tin chi tiết của một archive item theo ID.

#### Path Parameters

| Tham số | Kiểu | Mô tả |
|---------|------|-------|
| `id` | integer | ID của Archive_Item |

#### Ví dụ Request
```
GET /api/archive/1
```

#### Response 200 OK
```json
{
  "success": true,
  "data": {
    "id": 1,
    "archived_at": "2024-12-15T10:30:00Z",
    "archive_note": "Tác phẩm xuất sắc nhất cuộc thi 2024, đạt điểm tuyệt đối từ ban giám khảo",
    "is_featured": true,
    "submission": {
      "id": 42,
      "title": "Ánh Bình Minh",
      "description": "Bức ảnh chụp bình minh tại Hà Giang, khoảnh khắc ánh sáng đầu ngày chiếu rọi qua những đám mây mù trên đỉnh núi.",
      "score": 9.5,
      "award": "Giải Nhất",
      "submitted_at": "2024-11-01T08:00:00Z",
      "thumbnail_url": "/static/uploads/thumbnails/submission_42.jpg",
      "full_image_url": "/static/uploads/originals/submission_42.jpg",
      "author": {
        "id": 7,
        "full_name": "Nguyễn Văn A",
        "username": "nguyenvana"
      },
      "contest": {
        "id": 3,
        "name": "Cuộc Thi Nhiếp Ảnh 2024",
        "year": 2024,
        "status": "ended"
      },
      "category": {
        "id": 2,
        "name": "Phong Cảnh"
      },
      "film_roll": {
        "id": 5,
        "roll_name": "Roll #5 - Hà Giang Series",
        "frames": [
          {
            "id": 101,
            "frame_number": 12,
            "image_url": "/static/uploads/frames/frame_101.jpg"
          }
        ]
      }
    }
  }
}
```

#### Response 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "ARCHIVE_ITEM_NOT_FOUND",
    "message": "Không tìm thấy tác phẩm lưu trữ với ID = 1"
  }
}
```

---

### 4. GET /api/archive/filters
**Mô tả:** Lấy danh sách tất cả các tùy chọn filter hiện có (dùng để render dropdown/checkbox trên UI).

#### Query Parameters
_Không có_

#### Ví dụ Request
```
GET /api/archive/filters
```

#### Response 200 OK
```json
{
  "success": true,
  "data": {
    "years": [2026, 2025, 2024, 2023, 2022],
    "categories": [
      { "id": 1, "name": "Chân Dung", "count": 42 },
      { "id": 2, "name": "Phong Cảnh", "count": 67 },
      { "id": 3, "name": "Đường Phố", "count": 31 },
      { "id": 4, "name": "Kiến Trúc", "count": 18 },
      { "id": 5, "name": "Thiên Nhiên", "count": 24 }
    ],
    "awards": [
      { "value": "Giải Nhất", "count": 15 },
      { "value": "Giải Nhì", "count": 25 },
      { "value": "Giải Ba", "count": 35 },
      { "value": "Giải Khuyến Khích", "count": 60 }
    ],
    "sort_options": [
      { "value": "archived_at_desc", "label": "Mới lưu trữ nhất" },
      { "value": "archived_at_asc", "label": "Cũ nhất" },
      { "value": "score_desc", "label": "Điểm cao nhất" },
      { "value": "score_asc", "label": "Điểm thấp nhất" },
      { "value": "title_asc", "label": "Tên A-Z" }
    ],
    "total_archived": 158
  }
}
```

---

## Mã lỗi chung

| Mã lỗi | HTTP Status | Ý nghĩa |
|--------|-------------|---------|
| `INVALID_PARAMS` | 400 | Tham số không hợp lệ |
| `MISSING_QUERY` | 400 | Thiếu tham số bắt buộc |
| `QUERY_TOO_SHORT` | 400 | Từ khóa quá ngắn |
| `ARCHIVE_ITEM_NOT_FOUND` | 404 | Không tìm thấy item |
| `INTERNAL_SERVER_ERROR` | 500 | Lỗi server nội bộ |
| `RATE_LIMIT_EXCEEDED` | 429 | Vượt giới hạn request |

---

## Acceptance Criteria

### AC-1: Lấy danh sách archive
- [ ] Trả về danh sách tác phẩm đã lưu trữ từ cuộc thi **đã kết thúc** (Contest.status = 'ended')
- [ ] Hỗ trợ phân trang với `page` và `per_page`
- [ ] Lọc được theo `year`, `category_id`, `has_award`, `is_featured`
- [ ] Sắp xếp được theo `archived_at`, `score`, `title`
- [ ] Response đúng format JSON với đầy đủ thông tin submission, author, contest, category

### AC-2: Tìm kiếm full-text
- [ ] Tìm kiếm được trong: title, description, author name, contest name, category name, archive_note
- [ ] Từ khóa tối thiểu 2 ký tự, trả về lỗi nếu ngắn hơn
- [ ] Hỗ trợ dấu tiếng Việt (unicode-aware search)
- [ ] Trả về `highlight` với từ khóa được đánh dấu `<mark>...</mark>`
- [ ] Kết hợp được với các filter (year, category_id, has_award)
- [ ] Sắp xếp theo `relevance` (mặc định) hoặc `score`, `archived_at`

### AC-3: Chi tiết archive item
- [ ] Trả về đầy đủ thông tin: submission + author + contest + category + film_roll + frames
- [ ] Trả về 404 khi ID không tồn tại
- [ ] `full_image_url` phải trỏ đến file ảnh gốc (không phải thumbnail)

### AC-4: Filter options
- [ ] Trả về danh sách năm thực tế có dữ liệu (sắp xếp giảm dần)
- [ ] Mỗi category kèm `count` số tác phẩm
- [ ] Mỗi award kèm `count` số tác phẩm
- [ ] `total_archived` = tổng số tác phẩm trong kho lưu trữ

### AC-5: Non-functional
- [ ] Thời gian phản hồi < 500ms với dataset 10,000 records (cần index trên `submission_id`, `archived_at`)
- [ ] Rate limit 100 requests/phút mỗi IP
- [ ] Tất cả endpoint public, không cần auth

---

## Ghi chú triển khai (Flask)

```python
# Blueprint đề xuất
archive_bp = Blueprint('archive', __name__, url_prefix='/api/archive')

# Full-text search với PostgreSQL
# Dùng: func.to_tsvector và func.to_tsquery (PostgreSQL native)
# Hoặc: SQLAlchemy-searchable / ilike cho đơn giản hơn

# Index đề xuất (PostgreSQL)
# CREATE INDEX idx_archive_item_submission_id ON archive_item(submission_id);
# CREATE INDEX idx_archive_item_archived_at ON archive_item(archived_at DESC);
# CREATE INDEX idx_submission_contest_id ON submission(contest_id);
# CREATE INDEX idx_submission_category_id ON submission(category_id);
```

---

*Tài liệu này được tạo cho CNPM-87 | Thực hiện: Đinh Quang Thọ*
