# [CNPM-81] Báo Cáo Capstone - Nền tảng Cuộc thi Nhiếp ảnh Phim

## 1. Tổng quan dự án (Project Overview)
- **Tên dự án:** Nền tảng Cuộc thi Nhiếp ảnh Phim (Film Contest Platform)
- **Mục tiêu:** Số hóa toàn diện quy trình tổ chức cuộc thi ảnh phim, từ khâu đăng ký, quản lý cuộn phim (film rolls), nộp tác phẩm, đến chấm điểm tự động và công bố triển lãm.
- **Phạm vi (Scope):** Bao gồm cổng thông tin cho Thí sinh, Không gian chấm điểm cho Giám khảo, và Dashboard quản trị cho Ban tổ chức.

## 2. Kiến trúc hệ thống (System Architecture)
- **Mô hình:** Client-Server kết hợp Clean Architecture / Modular.
- **Backend:** Python/Flask (RESTful API), Node.js (tính toán điểm), PostgreSQL (Cơ sở dữ liệu chính).
- **Frontend:** Giao diện Web (HTML/CSS/JS) và tích hợp Mobile App (Flutter).
- **Triển khai:** Docker, GitHub Actions (CI/CD), triển khai trên server Linux.

## 3. Các tính năng cốt lõi (Core Features)
- Quản lý tài khoản & Phân quyền (RBAC).
- Nộp bài thi & Quản lý Negative / Contact Sheet.
- Tích hợp AI phát hiện ảnh trùng lặp và ảnh AI (PoC).
- Tổng hợp điểm, xếp hạng tự động & Trao giải.

## 4. Kiểm thử và Đánh giá (Testing & Evaluation)
- Kết quả kiểm thử UAT: Đạt 100% các luồng nghiệp vụ chính.
- Hiệu năng: Thời gian phản hồi API trung bình < 500ms.

## 5. Kết luận & Hướng phát triển
- Dự án đáp ứng tốt nhu cầu thực tế của các CLB nhiếp ảnh.
- Hướng phát triển: Tích hợp ví điện tử trả phí dự thi, phát triển mạng xã hội thu nhỏ cho cộng đồng chụp phim.
