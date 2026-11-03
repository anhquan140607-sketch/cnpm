# Bộ tài liệu họp hoàn thiện Sprint 1

Dùng cho buổi họp tối 3/11/2026. Mục tiêu: chốt quyết định kỹ thuật, nhận việc rõ ràng, cập nhật Jira và hoàn thành các việc còn lại của Sprint 1.

## 1. Chương trình họp (60 phút)

| Thời gian | Nội dung | Ai dẫn |
| --- | --- | --- |
| 0-10 phút | Mỗi người báo cáo: đã xong gì, đang làm gì, vướng gì. Cập nhật trạng thái trên Jira ngay trong lúc họp | Scrum Master (Thọ) |
| 10-25 phút | Chốt công nghệ (mục 2) | Thọ |
| 25-35 phút | Chốt các câu hỏi mở (mục 3) | Cả nhóm |
| 35-50 phút | Nhận việc còn lại, đặt hạn chót từng việc (mục 4) | Từng người |
| 50-60 phút | Thiết lập repo GitHub cùng nhau (mục 5), hẹn giờ stand-up và buổi review | Thọ |

## 2. Quyết định công nghệ (cần chốt tối nay, vì chặn FE1, FE2 và mọi API sau đó)

| Hạng mục | Đề xuất mặc định | Phương án thay thế | Cách chọn |
| --- | --- | --- | --- |
| Backend | Node.js (Express hoặc NestJS) | ASP.NET Core Web API | Nếu từ 3 người trở lên đã dùng C# thành thạo thì chọn ASP.NET Core; nếu không chọn Node.js để cùng ngôn ngữ JavaScript/TypeScript với web (ReactJS/Next.js) |
| Cơ sở dữ liệu | PostgreSQL | MySQL | PostgreSQL mạnh về ràng buộc và JSON; chọn MySQL nếu cả nhóm đã quen |
| Lưu ảnh | Firebase Storage (đi cùng Node.js) | Azure Blob (đi cùng ASP.NET Core) | Theo backend đã chọn; bật quyền truy cập riêng tư |
| AI trùng ảnh | Thử so sánh ảnh bằng perceptual hash và vector embedding | Gọi API bên ngoài | PoC 8h do M4 làm: chạy thử trên 20-30 ảnh mẫu rồi chọn ngưỡng |
| AI ảnh do AI tạo | Gọi API/mô hình có sẵn, kết quả chỉ là cảnh báo | Bỏ nếu chậm (mức Should) | Đã quy ước trong Docs/02 |
| Web / Mobile | ReactJS hoặc Next.js / Flutter (mobile là Should) | - | Giữ như kế hoạch |

Ghi kết quả vào story CNPM-28 (kiến trúc và chốt công nghệ) và cập nhật Docs/03, README.

## 3. Câu hỏi mở cần chốt

1. **Mốc thời gian:** giữ lịch gốc (9/10-4/12) hay dời? Hiện Jira có "Sprint 1" ngày 2/11-16/11 đang chứa cả story Sprint 1 và Sprint 2. Cần tách theo nhãn Sprint1/Sprint2 (hoặc dời lịch và sửa tài liệu).
2. Xác nhận M1-M5 đúng tên (M1 Thọ, M2 Quân, M3 Hiếu, M4 Đạt, M5 Lộc) và email Jira của Lộc, Hiếu.
3. Ai là chủ repo GitHub và ai sẽ merge (Maintainer = Thọ).
4. Có nâng "nhật ký hoạt động" (FE2.3) lên Must không, vì NFR-7 yêu cầu ghi log thao tác quan trọng.
5. Có thành viên nào quá tải hoặc vắng ở Sprint 2 để chia lại việc.

## 4. Việc Sprint 1 theo từng thành viên

Mỗi người đọc phần của mình, báo trạng thái thật (To Do, In Progress, Done) và hạn hoàn thành. Việc xong thì kéo thẻ sang Done kèm link pull request.


### M1 - Đinh Quang Thọ (38 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [1.1] Đăng ký, đăng nhập, đăng xuất và quên mật khẩu (JWT) | Must | 12 | [ ] | |
| [1.3] RBAC cho 4 vai trò: middleware/policy bảo vệ endpoint | Must | 8 | [ ] | |
| [17.1] Rà soát, chốt baseline SRS và use case 4 vai trò | Must | 3 | [ ] | |
| [17.1] Thiết kế kiến trúc modular và chốt công nghệ | Must | 5 | [ ] | |
| [17.1] Thiết kế ERD và database schema | Must | 5 | [ ] | |
| [17.1] Thiết lập repo, branch protection, skeleton backend và CI cơ bản | Must | 5 | [ ] | |

### M2 - Hà Anh Quân (17 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [2.1] Cấu hình hệ thống | Must | 6 | [ ] | |
| [17.1] Wireframe: Participant web và mobile | Must | 3 | [ ] | |
| [1.2] Hồ sơ cá nhân và bảo mật (đổi mật khẩu) | Should | 8 | [ ] | |

### M3 - Đặng Minh Hiếu (17 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [2.2] Quản lý master data | Must | 14 | [ ] | |
| [17.1] Wireframe: Organizer, Judge và Admin | Must | 3 | [ ] | |

### M4 - Nguyễn Minh Đạt (14 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [9.1] Thử nghiệm AI (PoC): similarity và AI-generated detection | Must | 8 | [ ] | |
| [17.4] Tài liệu lý thuyết (RBL) | Must | 6 | [ ] | |

### M5 - Nguyễn Tấn Lộc (22 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [1.3] Giao diện Admin: quản lý người dùng và phân quyền | Must | 8 | [ ] | |
| [17.3] Cấu hình cloud storage và quản lý mã nguồn | Must | 4 | [ ] | |
| [2.3] Nhật ký hoạt động và giám sát | Could | 10 | [ ] | |

### All - Cả nhóm (12 giờ trong Sprint 1)

| Việc | Ưu tiên | Giờ | Tình trạng | Hạn |
| --- | --- | --- | --- | --- |
| [17.5] Họp và quản lý dự án - Sprint 1 | Must | 12 | [ ] | |

Mỗi việc chỉ tính là xong khi đạt Definition of Done: code hoặc tài liệu được ít nhất 1 người review (2 người với xác thực và chấm điểm), kiểm thử đạt tiêu chí, merge vào main bằng pull request và thẻ Jira chuyển Done.

## 5. Thiết lập repo GitHub (làm cùng nhau trong buổi họp)

1. Thọ tạo repo private `film-contest-platform` và mời 4 thành viên với quyền Write.
2. Giải nén bộ file `film-contest-platform.zip` rồi đẩy lên nhánh main.
3. Bật branch protection cho main (yêu cầu pull request và 1 approval).
4. Mỗi người clone repo, cấu hình tên và email Git, tạo một nhánh thử: `git checkout -b CNPM-xx-mo-ta` rồi push và mở thử pull request.
5. Trong Jira cài app GitHub for Jira và kết nối repo.

Hướng dẫn đầy đủ nằm ở Docs/04-git-workflow-guide.md. Mã Jira dùng cho nhánh và commit là CNPM (ví dụ `CNPM-28: chot cong nghe`).

## 6. Kết quả họp (ghi trong buổi họp)

- Công nghệ đã chốt: ......
- Mốc thời gian chọn: ......
- Người chưa làm và cam kết: ......
- Ngày Sprint Review với giảng viên: ......
