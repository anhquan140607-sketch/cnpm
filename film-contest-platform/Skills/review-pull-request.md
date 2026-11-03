# Quy trình duyệt Pull Request (Code Review Checklist)

Tài liệu quy định các bước và tiêu chí kiểm tra bắt buộc khi một thành viên review Pull Request (PR) của thành viên khác trước khi merge vào nhánh `main`.

---

## 1. Quy tắc chung
- Không ai được tự merge Pull Request của chính mình.
- Mỗi Pull Request phải có ít nhất **1 approval** từ thành viên khác (2 approval với module Xác thực `auth` hoặc Chấm điểm `judging`).
- Chỉ **Maintainer (Thọ)** mới có quyền nhấn nút **Merge pull request** vào nhánh `main`.

---

## 2. Checklist kiểm tra Pull Request (Dành cho Reviewer)

### A. Kiểm tra tiêu đề và thông tin Pull Request
- [ ] Tên nhánh có đúng định dạng `<MÃ-JIRA>-<mô-tả-ngắn>` không? (Ví dụ: `CNPM-28-backend-foundation`).
- [ ] Tiêu đề PR có chứa mã Jira tương ứng không?
- [ ] PR có mô tả rõ ràng: Đã làm gì? Cách test như thế nào?

### B. Kiểm tra bảo mật và tệp rác (Rất quan trọng)
- [ ] **Tuyệt đối không có file `.env`** chứa mật khẩu thật hay API key bí mật.
- [ ] **Không có thư mục nặng** như `node_modules/`, `dist/`, `.vscode/`, `.DS_Store`.
- [ ] Mật khẩu người dùng được băm an toàn bằng `bcrypt` trước khi lưu vào database.
- [ ] Các endpoint nhạy cảm đều có middleware xác thực JWT `authenticateToken` và phân quyền vai trò `authorizeRoles`.

### C. Kiểm tra chất lượng mã nguồn
- [ ] Mã nguồn có tuân thủ cấu trúc thư mục modular không?
- [ ] Code có được định dạng sạch sẽ, dễ đọc, không thừa mã debug (`console.log`) không cần thiết?
- [ ] Có xử lý bắt lỗi (`try/catch`) đầy đủ và trả về mã HTTP chuẩn (200, 201, 400, 401, 403, 404, 500)?
- [ ] Có tài liệu API hoặc cập nhật Swagger tương ứng với các endpoint mới thêm?

### D. Kiểm tra chạy thử thực tế
- [ ] Reviewer kéo nhánh về máy hoặc kiểm tra logic xem code có biên dịch thành công (`npm run build`) không.
- [ ] Các chức năng hoạt động đúng theo tiêu chí chấp nhận (Acceptance Criteria) trong Jira issue.

---

## 3. Các bước duyệt trên GitHub
1. Vào tab **Pull requests** của repository -> Chọn PR cần duyệt.
2. Bấm vào tab **Files changed** để xem từng dòng code thay đổi.
3. Nếu có góp ý: Nhấp chuột vào dòng code để để lại bình luận nhận xét.
4. Khi mọi thứ đạt yêu cầu:
   - Bấm vào nút xanh **Review changes** ở góc trên bên phải.
   - Chọn **Approve** và viết nhận xét động viên (ví dụ: *"Code chuẩn, đã test chạy ổn định"*).
   - Bấm **Submit review**.
