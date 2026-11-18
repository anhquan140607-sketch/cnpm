# CNPM-90: Dashboard và Biểu Đồ Thống Kê - API Specification

**Task ID:** CNPM-90  
**Tên task:** [15.2] Dashboard và biểu đồ thống kê  
**Người thực hiện:** Đinh Quang Thọ (M1 - nhận từ M3)  
**Dự án:** Film Contest Platform  
**Ngày tạo:** 2026-11-18  

---

## 1. Tổng quan

Dashboard thống kê cung cấp trang tổng quan cho Admin/Organizer để xem các số liệu quan trọng của cuộc thi:
- Số người tham gia
- Số tác phẩm
- Tiến độ chấm điểm
- Phân bố giải thưởng

---

## 2. Authentication

Tất cả các endpoint đều yêu cầu JWT Bearer Token.

```
Authorization: Bearer <jwt_token>
```

**Roles được phép truy cập:** `administrator`, `organizer`

---

## 3. API Endpoints

---

### 3.1 GET /api/statistics/overview

**Mô tả:** Lấy tổng quan số liệu toàn hệ thống.

**Method:** `GET`  
**URL:** `/api/statistics/overview`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Request

Không có body/params.

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "total_users": 247,
    "total_contests": 12,
    "total_registrations": 310,
    "total_submissions": 583,
    "total_evaluations": 412,
    "total_awards": 36,
    "evaluation_completion_rate": 70.7,
    "active_contests": 3,
    "pending_submissions": 171,
    "generated_at": "2026-11-18T09:00:00Z"
  }
}
```

#### Response Fields

| Field | Type | Mô tả |
|-------|------|--------|
| `total_users` | integer | Tổng số người dùng đã đăng ký |
| `total_contests` | integer | Tổng số cuộc thi |
| `total_registrations` | integer | Tổng số đăng ký tham dự |
| `total_submissions` | integer | Tổng số tác phẩm nộp |
| `total_evaluations` | integer | Tổng số tác phẩm đã được chấm |
| `total_awards` | integer | Tổng số giải thưởng đã trao |
| `evaluation_completion_rate` | float | Tỉ lệ chấm điểm (%) |
| `active_contests` | integer | Số cuộc thi đang hoạt động |
| `pending_submissions` | integer | Số tác phẩm chưa chấm |
| `generated_at` | string (ISO 8601) | Thời điểm sinh dữ liệu |

#### Error Responses

| Code | Mô tả |
|------|--------|
| 401 | Unauthorized – Token không hợp lệ hoặc hết hạn |
| 403 | Forbidden – Role không được phép |
| 500 | Internal Server Error |

---

### 3.2 GET /api/statistics/contest/{id}

**Mô tả:** Thống kê chi tiết một cuộc thi theo ID.

**Method:** `GET`  
**URL:** `/api/statistics/contest/{id}`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Path Parameters

| Param | Type | Required | Mô tả |
|-------|------|----------|--------|
| `id` | integer | ✅ | ID của cuộc thi |

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "contest": {
      "id": 1,
      "name": "Cuộc Thi Ảnh Nghệ Thuật 2026",
      "status": "active",
      "start_date": "2026-09-01",
      "end_date": "2026-12-31"
    },
    "statistics": {
      "total_registrations": 85,
      "total_submissions": 210,
      "evaluated_submissions": 158,
      "pending_submissions": 52,
      "evaluation_rate": 75.2,
      "total_awards": 10,
      "awards_distributed": 7,
      "rounds": [
        {
          "round_id": 1,
          "round_name": "Vòng 1",
          "submissions_count": 210,
          "evaluated_count": 200,
          "completion_rate": 95.2
        },
        {
          "round_id": 2,
          "round_name": "Vòng 2",
          "submissions_count": 80,
          "evaluated_count": 62,
          "completion_rate": 77.5
        },
        {
          "round_id": 3,
          "round_name": "Vòng Chung Kết",
          "submissions_count": 20,
          "evaluated_count": 9,
          "completion_rate": 45.0
        }
      ],
      "categories": [
        {
          "category_id": 1,
          "category_name": "Chân dung",
          "submissions_count": 80
        },
        {
          "category_id": 2,
          "category_name": "Phong cảnh",
          "submissions_count": 65
        }
      ]
    }
  }
}
```

#### Error Responses

| Code | Mô tả |
|------|--------|
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Contest not found |
| 500 | Internal Server Error |

---

### 3.3 GET /api/statistics/registrations

**Mô tả:** Thống kê đăng ký theo thời gian (time series).

**Method:** `GET`  
**URL:** `/api/statistics/registrations`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Query Parameters

| Param | Type | Required | Default | Mô tả |
|-------|------|----------|---------|--------|
| `contest_id` | integer | ❌ | null | Lọc theo cuộc thi |
| `from_date` | string (YYYY-MM-DD) | ❌ | 30 ngày trước | Từ ngày |
| `to_date` | string (YYYY-MM-DD) | ❌ | hôm nay | Đến ngày |
| `group_by` | string | ❌ | `day` | Nhóm theo: `day`, `week`, `month` |

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "period": {
      "from_date": "2026-10-01",
      "to_date": "2026-11-18",
      "group_by": "week"
    },
    "series": [
      { "date": "2026-10-01", "count": 12 },
      { "date": "2026-10-08", "count": 25 },
      { "date": "2026-10-15", "count": 18 },
      { "date": "2026-10-22", "count": 34 },
      { "date": "2026-10-29", "count": 29 },
      { "date": "2026-11-05", "count": 41 },
      { "date": "2026-11-12", "count": 38 }
    ],
    "total": 197,
    "average_per_period": 28.1
  }
}
```

#### Error Responses

| Code | Mô tả |
|------|--------|
| 400 | Bad Request – Tham số không hợp lệ |
| 401 | Unauthorized |
| 403 | Forbidden |
| 500 | Internal Server Error |

---

### 3.4 GET /api/statistics/submissions-by-category

**Mô tả:** Phân bố tác phẩm theo hạng mục.

**Method:** `GET`  
**URL:** `/api/statistics/submissions-by-category`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Query Parameters

| Param | Type | Required | Mô tả |
|-------|------|----------|--------|
| `contest_id` | integer | ❌ | Lọc theo cuộc thi cụ thể |

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "total_submissions": 583,
    "categories": [
      {
        "category_id": 1,
        "category_name": "Chân dung",
        "submissions_count": 180,
        "percentage": 30.9
      },
      {
        "category_id": 2,
        "category_name": "Phong cảnh",
        "submissions_count": 150,
        "percentage": 25.7
      },
      {
        "category_id": 3,
        "category_name": "Đường phố",
        "submissions_count": 120,
        "percentage": 20.6
      },
      {
        "category_id": 4,
        "category_name": "Kiến trúc",
        "submissions_count": 90,
        "percentage": 15.4
      },
      {
        "category_id": 5,
        "category_name": "Khác",
        "submissions_count": 43,
        "percentage": 7.4
      }
    ]
  }
}
```

#### Error Responses

| Code | Mô tả |
|------|--------|
| 401 | Unauthorized |
| 403 | Forbidden |
| 500 | Internal Server Error |

---

### 3.5 GET /api/statistics/awards

**Mô tả:** Thống kê giải thưởng toàn hệ thống hoặc theo cuộc thi.

**Method:** `GET`  
**URL:** `/api/statistics/awards`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Query Parameters

| Param | Type | Required | Mô tả |
|-------|------|----------|--------|
| `contest_id` | integer | ❌ | Lọc theo cuộc thi |

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "total_awards_defined": 48,
    "total_awards_distributed": 36,
    "distribution_rate": 75.0,
    "awards_by_type": [
      {
        "award_type": "Giải Nhất",
        "count": 12,
        "distributed": 10
      },
      {
        "award_type": "Giải Nhì",
        "count": 12,
        "distributed": 10
      },
      {
        "award_type": "Giải Ba",
        "count": 12,
        "distributed": 10
      },
      {
        "award_type": "Giải Khuyến Khích",
        "count": 12,
        "distributed": 6
      }
    ],
    "awards_by_contest": [
      {
        "contest_id": 1,
        "contest_name": "Cuộc Thi Ảnh Nghệ Thuật 2026",
        "total_awards": 12,
        "distributed": 10
      }
    ]
  }
}
```

#### Error Responses

| Code | Mô tả |
|------|--------|
| 401 | Unauthorized |
| 403 | Forbidden |
| 500 | Internal Server Error |

---

### 3.6 GET /api/statistics/evaluation-progress

**Mô tả:** Tiến độ chấm điểm theo vòng và cuộc thi.

**Method:** `GET`  
**URL:** `/api/statistics/evaluation-progress`  
**Auth:** JWT required | Role: `administrator`, `organizer`

#### Query Parameters

| Param | Type | Required | Mô tả |
|-------|------|----------|--------|
| `contest_id` | integer | ❌ | Lọc theo cuộc thi |
| `round_id` | integer | ❌ | Lọc theo vòng cụ thể |

#### Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "overall_progress": {
      "total_submissions": 583,
      "evaluated": 412,
      "pending": 171,
      "completion_rate": 70.7
    },
    "by_round": [
      {
        "round_id": 1,
        "round_name": "Vòng 1",
        "contest_id": 1,
        "contest_name": "Cuộc Thi Ảnh Nghệ Thuật 2026",
        "total_submissions": 210,
        "evaluated": 200,
        "pending": 10,
        "completion_rate": 95.2
      },
      {
        "round_id": 2,
        "round_name": "Vòng 2",
        "contest_id": 1,
        "contest_name": "Cuộc Thi Ảnh Nghệ Thuật 2026",
        "total_submissions": 80,
        "evaluated": 62,
        "pending": 18,
        "completion_rate": 77.5
      },
      {
        "round_id": 3,
        "round_name": "Vòng Chung Kết",
        "contest_id": 1,
        "contest_name": "Cuộc Thi Ảnh Nghệ Thuật 2026",
        "total_submissions": 20,
        "evaluated": 9,
        "pending": 11,
        "completion_rate": 45.0
      }
    ],
    "by_judge": [
      {
        "judge_id": 5,
        "judge_name": "Nguyễn Văn A",
        "assigned_submissions": 50,
        "evaluated": 42,
        "completion_rate": 84.0
      }
    ]
  }
}
```

#### Error Responses

| Code | Mô tả |
|------|--------|
| 401 | Unauthorized |
| 403 | Forbidden |
| 500 | Internal Server Error |

---

## 4. Data Models (từ ERD)

### User
```
id, username, email, role (administrator | organizer | judge | participant), created_at
```

### Contest
```
id, name, description, status (draft | active | completed | cancelled), start_date, end_date, organizer_id
```

### Registration
```
id, user_id, contest_id, registered_at, status
```

### Submission
```
id, registration_id, category_id, round_id, title, file_url, submitted_at, status
```

### Evaluation
```
id, submission_id, judge_id, score, comment, evaluated_at
```

### Award
```
id, contest_id, category_id, name, type, winner_submission_id, awarded_at
```

### Category
```
id, contest_id, name, description
```

### Round
```
id, contest_id, name, sequence, start_date, end_date, status
```

---

## 5. Backend Implementation Notes

### File structure (Flask Clean Architecture)

```
app/
├── api/
│   └── statistics/
│       ├── __init__.py
│       └── routes.py          # Blueprint: /api/statistics
├── services/
│   └── statistics_service.py  # Business logic
├── repositories/
│   └── statistics_repository.py  # DB queries (SQLAlchemy)
└── schemas/
    └── statistics_schema.py   # Marshmallow schemas
```

### SQLAlchemy Query Example (overview)

```python
from sqlalchemy import func
from app.models import User, Contest, Submission, Evaluation, Award

def get_overview():
    total_users = db.session.query(func.count(User.id)).scalar()
    total_contests = db.session.query(func.count(Contest.id)).scalar()
    total_submissions = db.session.query(func.count(Submission.id)).scalar()
    total_evaluations = db.session.query(func.count(Evaluation.id)).scalar()
    total_awards = db.session.query(func.count(Award.id)).filter(Award.winner_submission_id != None).scalar()
    rate = round((total_evaluations / total_submissions * 100), 1) if total_submissions else 0
    return {
        "total_users": total_users,
        "total_contests": total_contests,
        "total_submissions": total_submissions,
        "total_evaluations": total_evaluations,
        "total_awards": total_awards,
        "evaluation_completion_rate": rate
    }
```

---

## 6. Acceptance Criteria

- [ ] `GET /api/statistics/overview` trả về đúng các số tổng hợp
- [ ] `GET /api/statistics/contest/{id}` trả về đúng thống kê cho cuộc thi
- [ ] `GET /api/statistics/registrations` hỗ trợ lọc theo ngày và `group_by`
- [ ] `GET /api/statistics/submissions-by-category` trả về phân bố theo hạng mục
- [ ] `GET /api/statistics/awards` trả về thống kê giải thưởng
- [ ] `GET /api/statistics/evaluation-progress` trả về tiến độ chấm điểm theo vòng
- [ ] Tất cả endpoint yêu cầu JWT, chỉ cho phép role `administrator` hoặc `organizer`
- [ ] Response format nhất quán: `{ "status": "success", "data": {...} }`
- [ ] Xử lý đúng các error codes: 400, 401, 403, 404, 500
- [ ] Viết unit test cho service layer
- [ ] Viết integration test cho các route

---

## 7. Liên kết tài liệu

- ERD: `Docs/database/erd.md`
- Auth API: `Docs/auth-api-spec.md`
- Contest API: `Docs/contest-api-spec.md`

---

*Tài liệu này được tạo cho task CNPM-90 | Thực hiện: Đinh Quang Thọ*
