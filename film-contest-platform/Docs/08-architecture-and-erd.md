# Kiến trúc hệ thống và thiết kế cơ sở dữ liệu (bản nháp Sprint 1)

Phục vụ các story CNPM-28 (kiến trúc modular và chốt công nghệ) và CNPM-29 (ERD và database schema). Đây là bản nháp để nhóm duyệt trong buổi họp tối 3/11/2026. Nội dung bám theo [05-srs.md](05-srs.md) mục 5.1 và NFR-1 đến NFR-10. Mermaid hiển thị trực tiếp trên GitHub.

## 1. Quyết định công nghệ (ghi lại sau buổi họp)

| Hạng mục | Đề xuất mặc định | Trạng thái |
| --- | --- | --- |
| Backend | Node.js (Express + TypeScript), REST API, Swagger | Đã chốt & triển khai |
| Cơ sở dữ liệu | PostgreSQL 16 | Đã chốt & thiết kế DDL 18 bảng |
| Lưu ảnh | Firebase Storage / Cloud Storage, riêng tư, URL ký thời hạn | Chờ cấu hình bucket |
| Web | ReactJS / Next.js | Theo kế hoạch |
| Mobile | Flutter (mức Should) | Theo kế hoạch |
| AI | OpenAI API và dịch vụ Computer Vision / so sánh ảnh | Theo kế hoạch |
| Xác thực | JWT (Access & Refresh Token) và RBAC (4 vai trò) | Đã hoàn thành |

Thiết kế dưới đây độc lập với ngôn ngữ backend và hệ quản trị cơ sở dữ liệu, nên không phải làm lại nếu nhóm chọn ASP.NET Core hoặc MySQL.

## 2. Kiến trúc modular (NFR-3)

```mermaid
flowchart LR
  subgraph Client
    W[Web: ReactJS/Next.js]
    M[Mobile: Flutter]
  end
  subgraph Backend[Backend API - REST, JWT, Swagger]
    AUTH[Auth và RBAC - FE1]
    SYS[System và Master data - FE2]
    CON[Contest và Criteria - FE3, FE4]
    PAR[Participant: đăng ký, roll, frame, submission - FE5-FE7]
    VER[Verification - FE8, FE9]
    JUD[Judging và Ranking - FE10, FE11]
    PUB[Results và Archive - FE12, FE13]
    EXT[AI keywords, Report, Notification - FE14-FE16]
    LOG[Activity log]
  end
  DB[(Database)]
  ST[(Cloud storage: ảnh và thumbnail)]
  AI[AI services: OpenAI, Image similarity]
  MAIL[Email service]
  W --> Backend
  M --> Backend
  Backend --> DB
  PAR --> ST
  PUB --> ST
  VER --> AI
  EXT --> AI
  EXT --> MAIL
  AUTH --> MAIL
```

Quy tắc của kiến trúc:

- Mỗi module (thư mục riêng trong `BE/`) sở hữu bảng dữ liệu của mình và chỉ gọi module khác qua service/interface, không truy cập thẳng vào bảng của nhau.
- Middleware xác thực JWT và kiểm tra vai trò áp dụng cho mọi endpoint (FR-1.5).
- Dịch vụ AI và lưu trữ được bọc sau một lớp adapter. Khi dịch vụ lỗi, hệ thống ghi lỗi, đánh dấu "AI check pending" và chuyển sang duyệt tay (NFR-6).
- Ảnh luôn riêng tư; chỉ trả URL ký có thời hạn. Chỉ công khai sau khi cuộc thi chuyển sang published (NFR-2).
- Bản ghi đánh giá đã xác nhận và kết quả đã công bố không sửa được (NFR-7).

Cấu trúc thư mục gợi ý cho `BE/`:

```
BE/
├── src/
│   ├── modules/
│   │   ├── auth/            # FE1
│   │   ├── system/          # FE2: cấu hình, master data
│   │   ├── contest/         # FE3, FE4
│   │   ├── participant/     # FE5, FE6, FE7
│   │   ├── verification/    # FE8, FE9
│   │   ├── judging/         # FE10, FE11
│   │   ├── publication/     # FE12, FE13
│   │   └── support/         # FE14, FE15, FE16
│   ├── common/              # middleware JWT/RBAC, error, logger, adapter storage/AI
│   └── config/
├── tests/
└── README.md
```

## 3. ERD

```mermaid
erDiagram
  USER ||--o{ REGISTRATION : makes
  USER ||--o{ FILM_ROLL : owns
  USER ||--o{ JUDGE_ASSIGNMENT : "is judge in"
  USER ||--o{ EVALUATION : scores
  USER ||--o{ ACTIVITY_LOG : performs
  CONTEST ||--o{ CATEGORY : has
  CONTEST ||--o{ CRITERION : defines
  CONTEST ||--o{ REGISTRATION : receives
  CONTEST ||--o{ ROUND : has
  CATEGORY ||--o{ REGISTRATION : "chosen in"
  CATEGORY ||--o{ SUBMISSION : contains
  CATEGORY ||--o{ JUDGE_ASSIGNMENT : "assigned for"
  CATEGORY ||--o{ AWARD : grants
  ROUND ||--o{ JUDGE_ASSIGNMENT : "assigned in"
  FILM_ROLL ||--o{ FRAME : contains
  FRAME ||--o{ SUBMISSION : "used by"
  SUBMISSION ||--o{ AI_CHECK_RESULT : "checked by"
  SUBMISSION ||--o{ EVALUATION : "evaluated in"
  SUBMISSION ||--o| AWARD : wins
  SUBMISSION ||--o| ARCHIVE_ITEM : "archived as"
  EVALUATION ||--o{ EVALUATION_SCORE : has
  CRITERION ||--o{ EVALUATION_SCORE : "scored on"
  MASTER_DATA ||--o{ FILM_ROLL : "referenced by"

  USER {
    int id PK
    string name
    string email UK
    string password_hash
    string role "administrator, organizer, judge, participant"
    string status "active, inactive"
    datetime created_at
  }
  CONTEST {
    int id PK
    string title
    string theme
    text description
    text regulations
    datetime submission_start
    datetime submission_end
    datetime judging_start
    datetime judging_end
    string status "draft, open, closed, judging, published, archived"
    bool config_locked
    int created_by FK
  }
  CATEGORY {
    int id PK
    int contest_id FK
    string name
    int max_photos_per_participant
    text submission_rules
    text award_structure
  }
  CRITERION {
    int id PK
    int contest_id FK
    int category_id FK "null nếu dùng chung cả cuộc thi"
    string name
    text description
    decimal weight "tổng trọng số = 100"
    decimal max_score
  }
  ROUND {
    int id PK
    int contest_id FK
    string name
    int sequence
    string status
  }
  REGISTRATION {
    int id PK
    int participant_id FK
    int contest_id FK
    int category_id FK
    string status "pending, approved, rejected"
    text reason
    datetime created_at
  }
  MASTER_DATA {
    int id PK
    string type "film_brand, film_stock, iso, film_format, camera, lens, lab, scanner"
    string value
    string status "active, inactive"
  }
  FILM_ROLL {
    int id PK
    int participant_id FK
    int film_brand_id FK
    int film_stock_id FK
    int iso_id FK
    int film_format_id FK
    int camera_id FK
    int lens_id FK
    int lab_id FK
    int scanner_id FK
    text scan_specs
  }
  FRAME {
    int id PK
    int film_roll_id FK
    int frame_number "duy nhất trong roll"
    string shooting_location
  }
  SUBMISSION {
    int id PK
    int frame_id FK
    int category_id FK
    int participant_id FK
    string title
    text description
    string image_path
    string thumbnail_path
    string negative_ref_path "tùy chọn"
    string status "submitted, under_verification, accepted, rejected, needs_revision, withdrawn"
    string keywords
    datetime submitted_at
  }
  AI_CHECK_RESULT {
    int id PK
    int submission_id FK
    string type "duplicate, ai_generated"
    decimal score
    int matched_submission_id FK
    string decision "pending, flagged, cleared"
    datetime checked_at
  }
  JUDGE_ASSIGNMENT {
    int id PK
    int judge_id FK
    int category_id FK
    int round_id FK
  }
  EVALUATION {
    int id PK
    int judge_id FK
    int submission_id FK
    text comment
    bool confirmed "đã xác nhận thì khóa"
    datetime updated_at
  }
  EVALUATION_SCORE {
    int id PK
    int evaluation_id FK
    int criterion_id FK
    decimal score
  }
  AWARD {
    int id PK
    int category_id FK
    int submission_id FK
    string title "hạng, giải đặc biệt"
    int rank
  }
  ARCHIVE_ITEM {
    int id PK
    int submission_id FK
    json metadata_snapshot
    text judging_comments
    datetime archived_at
  }
  ACTIVITY_LOG {
    int id PK
    int user_id FK
    string action
    string entity_type
    int entity_id
    datetime created_at
  }
```

### Ràng buộc quan trọng

| Ràng buộc | Lý do (nguồn) |
| --- | --- |
| `USER.email` duy nhất; mật khẩu chỉ lưu dạng băm | FR-1.1, NFR-1 |
| `REGISTRATION` duy nhất theo (participant, contest, category); không đăng ký sau hạn | FR-5.3 |
| `FRAME` duy nhất theo (film_roll, frame_number) | FR-6.2 |
| Không xóa `FILM_ROLL`/`FRAME` đã gắn `SUBMISSION` | FR-6.3 |
| Số `SUBMISSION` của một participant trong một category không vượt `max_photos_per_participant` | FR-7.3 |
| Tổng `CRITERION.weight` của một cuộc thi hoặc hạng mục bằng 100; khóa khi bắt đầu chấm | FR-4.1, FR-4.3 |
| `EVALUATION` duy nhất theo (judge, submission); sau khi `confirmed` thì không sửa | FR-10.5, NFR-7 |
| `EVALUATION_SCORE` duy nhất theo (evaluation, criterion), điểm không vượt `max_score` | FR-10.3 |
| `MASTER_DATA` đang được dùng thì chỉ chuyển `inactive`, không xóa | FR-2.2 |
| Chỉ submission `accepted` mới được giao cho giám khảo | FR-8.3 |
| Ảnh riêng tư cho đến khi `CONTEST.status = published` | NFR-2 |

## 4. Trạng thái chính

Cuộc thi: `draft → open → closed → judging → published → archived` (chỉ nhận bài khi `open`).

Bài nộp: `submitted → under_verification → accepted | rejected | needs_revision`; thí sinh có thể `withdrawn` trước hạn.

## 5. Việc tiếp theo cho CNPM-28 và CNPM-29

- [ ] Nhóm duyệt bản nháp, chốt công nghệ ở mục 1, cập nhật cột "Trạng thái".
- [ ] Sinh migration/schema đầu tiên cho các bảng `USER`, `MASTER_DATA` (FE1, FE2 ở Sprint 1); các bảng còn lại làm theo từng sprint.
- [ ] Dựng skeleton `BE/` theo cấu trúc thư mục ở mục 2 và đẩy lên nhánh `CNPM-32-...`.
- [ ] Đính kèm ảnh xuất ERD và liên kết tài liệu này vào story CNPM-28, CNPM-29 trên Jira.
