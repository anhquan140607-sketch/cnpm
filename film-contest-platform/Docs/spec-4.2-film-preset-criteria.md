# Đặc tả Chức năng — [4.2] Bộ Tiêu chí Mẫu đặc thù Nhiếp ảnh Phim

- **Task Jira:** CNPM-146 (FE4 / WBS 4.2)
- **Mức ưu tiên:** Should
- **Ước tính:** 4 man-hours
- **Công nghệ:** Seed data Node.js / PostgreSQL

---

## 1. Mục tiêu

Cung cấp sẵn bộ tiêu chí chấm điểm chuẩn hóa dành riêng cho nhiếp ảnh analog. Organizer có thể áp dụng ngay bộ tiêu chí này vào cuộc thi chỉ với 1 click và tùy chỉnh lại nếu cần.

---

## 2. Danh sách Bộ Tiêu chí Mẫu Mặc định (Tổng 100%)

| STT | Tên Tiêu chí | Mô tả Đề xuất | Trọng số | Điểm tối đa |
| :-: | :--- | :--- | :-: | :-: |
| 1 | **Sáng tạo** | Ý tưởng thể hiện, góc nhìn độc đáo, tính nghệ thuật của tác phẩm. | 15% | 10 |
| 2 | **Bố cục** | Sự cân bằng, đường dẫn ánh mắt, tỉ lệ khung hình. | 15% | 10 |
| 3 | **Kể chuyện** | Khả năng truyền tải thông điệp, cảm xúc tới người xem. | 15% | 10 |
| 4 | **Kỹ thuật phơi sáng** | Độ chuẩn xác về khẩu độ/tốc độ, lấy nét và kiểm soát ánh sáng. | 10% | 10 |
| 5 | **Hạt film (Film Grain)** | Vẻ đẹp, độ mịn/nổi của hạt film đặc trưng phù hợp với ý đồ. | 10% | 10 |
| 6 | **Dải tông màu (Tonal Range)**| Chi tiết vùng sáng (Highlight), vùng tối (Shadow) và chuyển tông. | 10% | 10 |
| 7 | **Đặc đặc trưng màu film** | Màu sắc hài hòa, giữ được đặc trưng chất màu của loại film sử dụng. | 10% | 10 |
| 8 | **Chất lượng Scan** | Độ nét, độ phân giải scan, không dính bụi xước làm hỏng tác phẩm. | 15% | 10 |

---

## 3. Mô hình Dữ liệu & Khởi tạo (Seed Data)

```sql
CREATE TABLE criteria_presets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE criteria_preset_items (
    id SERIAL PRIMARY KEY,
    preset_id INT REFERENCES criteria_presets(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    weight_percent DECIMAL(4,1) NOT NULL,
    max_score INT DEFAULT 10,
    display_order INT DEFAULT 0
);
```

### API Áp dụng Bộ mẫu:
- `GET /api/v1/criteria-presets`: Xem danh sách các bộ mẫu có sẵn.
- `POST /api/v1/contests/:id/criteria/apply-preset`: Sao chép toàn bộ tiêu chí từ mẫu vào cuộc thi `:id`.
