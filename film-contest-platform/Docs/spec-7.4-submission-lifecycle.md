# Đặc tả Chức năng — [7.4] Vòng đời Bài nộp, Chỉnh sửa & Rút bài

- **Task Jira:** CNPM-50 / CNPM-143 (FE7 / WBS 7.4)
- **Mức ưu tiên:** Must
- **Ước tính:** 8 man-hours
- **Công nghệ:** Node.js Express, PostgreSQL, HTML5/Tailwind UI Mockup

---

## 1. Mục tiêu & Luồng Trạng thái (State Machine)

### 1.1 Mục tiêu
Quản lý luồng xử lý bài nộp của thí sinh từ lúc khởi tạo, qua các bước kiểm tra tự động/thủ công cho tới khi vào danh sách chấm chính thức hoặc rút bài.

### 1.2 Luồng chuyển trạng thái:
1. `submitted`: Bài nộp mới tạo, chờ AI kiểm tra sơ bộ.
2. `needs_revision`: AI/BTC phát hiện thiếu metadata hoặc lỗi file nhẹ, cho phép thí sinh cập nhật lại.
3. `under_verification`: BTC đang rà soát hồ sơ.
4. `accepted`: Bài nộp đạt yêu cầu, sẵn sàng chấm điểm (Khóa chỉnh sửa).
5. `rejected`: Bài vi phạm thể lệ hoặc bị loại bởi BTC.
6. `withdrawn`: Thí sinh chủ động rút bài nộp trước hạn.

---

## 2. Quy tắc Nghiệp vụ

- **BR-1 (Quyền sửa):** Thí sinh chỉ được chỉnh sửa thông tin/file khi trạng thái là `submitted` hoặc `needs_revision` VÀ cuộc thi chưa đóng sổ nộp bài.
- **BR-2 (Khóa cứng):** Khi bài ở trạng thái `under_verification`, `accepted`, `rejected` hoặc quá hạn cuộc thi, giao diện ẩn nút Sửa/Rút và API trả về HTTP 403 Forbidden.
- **BR-3 (Rút bài):** Thí sinh có thể rút bài bất kỳ lúc nào trước hạn. Cuộn phim (Roll) liên kết sẽ được trả về trạng thái tự do.
