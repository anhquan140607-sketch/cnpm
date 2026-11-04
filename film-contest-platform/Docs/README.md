# 📚 Chỉ Mục Tài Liệu & Sơ Đồ Dự Án (Docs Directory Index)

Trang tổng hợp, điều hướng toàn bộ tài liệu quản lý, đặc tả yêu cầu, kiểm thử, sơ đồ kiến trúc và hướng dẫn triển khai của dự án.

---

## 📌 1. Quản Lý & Quy Trình Dự Án
* 📄 [01-project-scope.md](./01-project-scope.md) — Phạm vi & giới hạn dự án (Chức năng FE1-FE16, Giới hạn LI1-LI21)
* 📄 [02-scope-estimation.md](./02-scope-estimation.md) — Bảng phân rã công việc WBS, độ phức tạp & Ước lượng Man-hours
* 📄 [03-management-approach.md](./03-management-approach.md) — Phương pháp quản lý Scrum, vai trò nhóm & kiểm soát chất lượng
* 📄 [04-git-workflow-guide.md](./04-git-workflow-guide.md) — Hướng dẫn quy chuẩn đặt tên nhánh, commit & Pull Request (PR)
* 📄 [06-team-assignment-and-scrum.md](./06-team-assignment-and-scrum.md) — Phân công 5 thành viên & Lịch trình 4 Sprint

---

## 📐 2. Đặc Tả Yêu Cầu, Kiến Trúc & Kiểm Thử
* 📄 [05-srs.md](./05-srs.md) — Tài liệu Đặc tả yêu cầu phần mềm (SRS)
* 📄 [08-architecture-and-erd.md](./08-architecture-and-erd.md) — Thiết kế kiến trúc hệ thống & Mô hình cơ sở dữ liệu (ERD)
* 📄 [test-plan-and-test-cases.md](./test-plan-and-test-cases.md) — Kế hoạch kiểm thử & 20 Test Cases cho 5 Core Flows (CNPM-144)

---

## ⚙️ 3. Đặc Tả Chức Năng & Hướng Dẫn Triển Khai (Feature Specs & Implementation)
* 📄 [spec-3.4-contest-template.md](./spec-3.4-contest-template.md) — Template cuộc thi tái sử dụng (CNPM-148)
* 📄 [spec-4.1-scoring-criteria.md](./spec-4.1-scoring-criteria.md) — Thiết lập tiêu chí chấm điểm có trọng số 100% (CNPM-135)
* 📄 [spec-4.2-film-preset-criteria.md](./spec-4.2-film-preset-criteria.md) — Bộ tiêu chí mẫu đặc thù nhiếp ảnh phim (CNPM-146)
* 📄 [spec-5.1-participant-profile.md](./spec-5.1-participant-profile.md) — Hồ sơ & Portfolio thí sinh (CNPM-136)
* 📄 [spec-7.4-submission-lifecycle.md](./spec-7.4-submission-lifecycle.md) — Quản lý vòng đời bài nộp, sửa & rút bài (CNPM-50)
* 📄 [cnpm_24_implementation_document.md](./cnpm_24_implementation_document.md) — HD Triển khai: Cấu hình hệ thống (Admin)
* 📄 [cnpm_36_implementation_guide.md](./cnpm_36_implementation_guide.md) — HD Triển khai: Hồ sơ cá nhân & Bảo mật (Đổi mật khẩu)
* 📄 [cnpm_142_implementation_document.md](./cnpm_142_implementation_document.md) — HD Triển khai: Form nộp bài & Trích xuất Metadata

---

## 📊 4. Sơ Đồ Kiến Trúc & Luồng Màn Hình (Diagrams & Screen Flows)
* 🖼️ [Web Application Judge Screen Flow.drawio.png](./Web%20Application%20Judge%20Screen%20Flow.drawio.png) — Sơ đồ luồng màn hình dành cho Giám khảo (Judge)
* 🖼️ [Web Application Manager Screen Flow.drawio.png](./Web%20Application%20Manager%20Screen%20Flow.drawio.png) — Sơ đồ luồng màn hình dành cho Quản lý (Manager)
* 🖼️ [Web Application Organizer's Screen Flow.drawio.png](./Web%20Application%20Organizer%20s%20Screen%20Flow.drawio.png) — Sơ đồ luồng màn hình Ban tổ chức (Organizer)
* 🖼️ [use.drawio.png](./use.drawio.png) — Sơ đồ Use Case tổng quan dự án

---

## 💻 5. Liên Kết Mã Nguồn Giao Diện & CSDL (Source Code References)
* 🌐 **Frontend UI Mockups (`FE/`):**
  * [`../FE/negative-contact-sheet-manager.html`](../FE/negative-contact-sheet-manager.html) — Giao diện Tham chiếu Negative & Contact Sheet
  * [`../FE/submission-management-system.html`](../FE/submission-management-system.html) — Giao diện Quản lý & Rút bài nộp
  * [`../FE/test-case-management-dashboard.html`](../FE/test-case-management-dashboard.html) — Dashboard Quản lý Kiểm thử
* 🗄️ **Database Schema (`BE/`):**
  * [`../BE/database-schema-erd.sql`](../BE/database-schema-erd.sql) — Script khởi tạo 9 bảng PostgreSQL DDL

---

## 🔬 6. Thử Nghiệm Kỹ Thuật & AI (PoC)
* 📄 [poc-ai-image-verification.md](./poc-ai-image-verification.md) — Báo cáo PoC phát hiện ảnh trùng lặp & ảnh AI (CNPM-26)

---

## 📦 7. Tài Nguyên & Dữ Liệu Khác
* 📄 [07-sprint1-meeting-kit.md](./07-sprint1-meeting-kit.md) — Bộ tài liệu và chương trình họp hoàn thiện Sprint 1
* 📊 [jira_tasks_film_contest.csv](./jira_tasks_film_contest.csv) — File dữ liệu import 76 công việc lên Jira
