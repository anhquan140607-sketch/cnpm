# Hướng dẫn viết User Story trên Jira (Jira Story Guide)

Tài liệu hướng dẫn các thành viên tạo và mô tả User Story trên Jira theo chuẩn phương pháp luận Agile Scrum.

---

## 1. Cấu trúc chuẩn của một User Story

Mỗi Story phải được viết theo mẫu 3 phần kinh điển:

```text
Là một [Vai trò người dùng / Role]
Tôi muốn [Hành động hoặc Chức năng / Action]
Để [Lợi ích hoặc Mục đích đạt được / Benefit]
```

### Ví dụ thực tế trong dự án:
- **Story FE1.1 (Đăng nhập):**
  > *"Là một Thí sinh tham gia cuộc thi nhiếp ảnh phim,*  
  > *Tôi muốn đăng nhập vào hệ thống bằng Email và Mật khẩu,*  
  > *Để tôi có thể truy cập vào trang cá nhân và xem các cuộn phim của mình."*

- **Story FE6.1 (Khai báo cuộn phim):**
  > *"Là một Thí sinh,*  
  > *Tôi muốn khai báo thông tin cuộn phim (Hãng phim, ISO, máy ảnh, ống kính, lab tráng),*  
  > *Để làm dữ liệu nguồn gắn vào các bức ảnh dự thi sau này."*

- **Story FE10.3 (Chấm điểm):**
  > *"Là một Giám khảo cuộc thi,*  
  > *Tôi muốn chấm điểm từng tiêu chí và để lại nhận xét cho bức ảnh được phân công,*  
  > *Để đánh giá khách quan và gửi kết quả vào bảng xếp hạng."*

---

## 2. Tiêu chí chấp nhận (Acceptance Criteria - Given/When/Then)

Mỗi Story bắt buộc phải có ít nhất 2-3 kịch bản chấp nhận để Developer và Tester dựa vào đó làm bài:

```text
Kịch bản 1: Đăng nhập thành công với thông tin chính xác
- Given: Người dùng đã có tài khoản trạng thái active trên hệ thống
- When: Người dùng nhập đúng Email và Mật khẩu hợp lệ
- Then: Hệ thống trả về mã 200, cấp Access Token và điều hướng vào trang Dashboard.

Kịch bản 2: Đăng nhập thất bại khi sai mật khẩu
- Given: Người dùng nhập đúng Email nhưng sai mật khẩu
- When: Người dùng bấm Đăng nhập
- Then: Hệ thống trả về mã 401 với thông báo "Email hoặc mật khẩu không chính xác".
```

---

## 3. Quy tắc điền thông tin Story trên Jira
1. **Summary:** Bắt đầu bằng mã nhóm/mô-tả, ví dụ: `[FE1.1] Đăng nhập hệ thống bằng JWT`.
2. **Issue Type:** Chọn `Story` (hoặc `Task`/`Bug`).
3. **Epic Link:** Gắn vào đúng Epic tương ứng (`FE1 Tài khoản`, `FE3 Cuộc thi`, v.v.).
4. **Original Estimate:** Điền số giờ ước tính (ví dụ: `8h`, `12h`).
5. **Assignee:** Gán đúng người thực hiện (M1-M5).
6. **Sprint:** Chọn Sprint hiện tại (ví dụ: `Sprint 1`).
