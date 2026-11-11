# Đặc tả Database Schema & ERD Cập nhật Sprint 3

- **Task Jira:** CNPM-122 ([17.1] Thiết kế ERD và database schema)
- **Cơ sở dữ liệu:** PostgreSQL 15+

## 1. Cập nhật Bảng Sprint 3
- `roles` & `user_roles`: Quản lý phân quyền 4 vai trò (Admin, Organizer, Judge, Participant) cho **CNPM-115**.
- `submission_reviews`: Lưu lịch sử duyệt bài thủ công cho **CNPM-120**.
- `ai_check_results`: Lưu kết quả cờ AI cho **CNPM-71/59**.
- `evaluations` & `evaluation_scores`: Lưu phiếu chấm điểm cho **CNPM-64**.

## 2. Ràng buộc Toàn vẹn (Integrity Constraints)
- Khóa ngoại `ON DELETE CASCADE` trên các quan hệ phụ thuộc.
- Unique constraints trên `(judge_id, submission_id)` để đảm bảo mỗi giám khảo chỉ chấm 1 phiếu cho mỗi bài thi.
