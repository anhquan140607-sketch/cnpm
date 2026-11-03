# Tóm tắt quy trình Git cho nhóm (Git Quick Reference)

Sổ tay tra cứu nhanh các lệnh Git hàng ngày dành cho 5 thành viên nhóm dự án.

---

## 1. Bắt đầu một tính năng mới (Start a Task)
Luôn luôn lấy code mới nhất từ nhánh `main` trước khi tạo nhánh mới:
```bash
git checkout main
git pull origin main
git checkout -b <MÃ_JIRA>-<tên-chức-năng-ngắn>
```
*Ví dụ:* `git checkout -b CNPM-12-film-roll-form`

---

## 2. Lưu lại tiến độ làm việc (Save & Commit)
Kiểm tra các file đã chỉnh sửa:
```bash
git status
```
Đưa các file vào danh sách chuẩn bị lưu (Staging):
```bash
git add .
```
Lưu lại (Commit) kèm mã Jira và mô tả việc đã làm:
```bash
git commit -m "CNPM-12: add film roll creation form and validation"
```

---

## 3. Đẩy nhánh lên GitHub (Push)
Đẩy nhánh lần đầu tiên:
```bash
git push -u origin <tên-nhánh-của-bạn>
```
*Ví dụ:* `git push -u origin CNPM-12-film-roll-form`

Các lần push sau chỉ cần:
```bash
git push
```

---

## 4. Tạo Pull Request & Hoàn tất
1. Mở GitHub trên trình duyệt -> Nhấn nút **Compare & pull request**.
2. Tag ít nhất 1 thành viên trong nhóm vào mục **Reviewers**.
3. Khi PR được duyệt (Approve) và không có lỗi xung đột (conflict):
   - **Chỉ Maintainer (Thọ)** mới bấm nút **Merge pull request**.
4. Xóa nhánh tính năng sau khi đã merge để kho lưu trữ luôn gọn gàng:
   ```bash
   git checkout main
   git pull origin main
   git branch -d CNPM-12-film-roll-form
   ```
