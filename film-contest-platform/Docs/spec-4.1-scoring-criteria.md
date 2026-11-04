# Đặc tả Chức năng — [4.1] Thiết lập Tiêu chí Chấm điểm có Trọng số

- **Task Jira:** CNPM-135 (FE4 / WBS 4.1)
- **Mức ưu tiên:** Must (Tính năng bắt buộc)
- **Ước tính:** 12 man-hours
- **Công nghệ:** Node.js Express, PostgreSQL

---

## 1. Mục tiêu & Quy tắc Nghiệp vụ

### 1.1 Mục tiêu
Cho phép Organizer cấu hình bộ tiêu chí chấm điểm cho từng cuộc thi. Tổng trọng số của tất cả các tiêu chí phải đạt chính xác **100%** trước khi cuộc thi chuyển sang giai đoạn chấm điểm.

### 1.2 Quy tắc Nghiệp vụ (Business Rules)
- **BR-1:** Mỗi tiêu chí gồm: Tên tiêu chí, Mô tả, Trọng số (`weight_percent`), Điểm tối đa (`max_score`).
- **BR-2:** Tên tiêu chí là duy nhất trong cùng một cuộc thi.
- **BR-3:** Cho phép lưu nháp bộ tiêu chí khi tổng trọng số chưa đủ 100%. Tuy nhiên, hệ thống sẽ **khóa không cho chuyển cuộc thi sang trạng thái chấm** nếu tổng trọng số khác 100.0%.
- **BR-4:** Khi cuộc thi bắt đầu vòng chấm đầu tiên (`is_locked = true`), bộ tiêu chí sẽ bị khóa hoàn toàn. Không ai (kể cả Organizer) có quyền chỉnh sửa, thêm hoặc xóa tiêu chí.
- **BR-5:** Trọng số hỗ trợ tối đa 1 chữ số thập phân (ví dụ: 12.5%).

---

## 2. Công thức Tính điểm Trung bình có Trọng số

Điểm số của bài dự thi được tính theo công thức:

$$Tổng điểm = \sum_{i=1}^{n} \left( rac{Điểm chấm_i}{Điểm tối đa_i} 	imes Trọng số_i ight)$$

*Ví dụ:*
- Tiêu chí A: Điểm chấm 8/10, Trọng số 30% -> 0.8 * 30 = 24 điểm.
- Tiêu chí B: Điểm chấm 7/10, Trọng số 70% -> 0.7 * 70 = 49 điểm.
- **Tổng điểm cuối cùng:** 24 + 49 = 73 / 100 điểm.

---

## 3. Mô hình Dữ liệu (PostgreSQL)

```sql
CREATE TABLE scoring_criteria (
    id SERIAL PRIMARY KEY,
    contest_id INT NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    weight_percent DECIMAL(4,1) NOT NULL CHECK (weight_percent > 0 AND weight_percent <= 100),
    max_score INT NOT NULL DEFAULT 10 CHECK (max_score > 0),
    display_order INT DEFAULT 0,
    is_locked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_criterion_name_per_contest UNIQUE(contest_id, name)
);
```

---

## 4. Thiết kế RESTful API

- `GET /api/v1/contests/:id/criteria`: Lấy danh sách tiêu chí và tổng trọng số hiện tại.
- `POST /api/v1/contests/:id/criteria`: Thêm tiêu chí mới.
- `PUT /api/v1/contests/:id/criteria/:cid`: Cập nhật tiêu chí `:cid` (Trả về HTTP 409 Conflict nếu bộ tiêu chí đã bị khóa).
- `DELETE /api/v1/contests/:id/criteria/:cid`: Xóa tiêu chí.
