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

## 6. Biên bản kết quả họp và thống nhất nhóm (CNPM-145)

Buổi họp toàn thể 5 thành viên nhóm diễn ra nghiêm túc với sự tham gia đầy đủ của M1-M5 dưới sự chủ trì của Scrum Master Đinh Quang Thọ. Các nội dung quan trọng đã được thống nhất 100% như sau:

### 6.1. Quyết định công nghệ chính thức (Chốt cho SWP)
- **Backend Framework:** **ASP.NET Core Web API (.NET 8)** - Đúng chuẩn chương trình môn học SWP và hướng dẫn của giảng viên. Kiến trúc phân tầng 3-Tier/Clean Architecture, tích hợp Swagger OpenAPI tại `/api/docs`.
- **Cơ sở dữ liệu:** **PostgreSQL 16** kết hợp **Entity Framework Core 8 (EF Core)**. Đã thiết kế và ánh xạ đầy đủ 18 bảng theo bản vẽ ERD chuẩn.
- **Xác thực & Bảo mật:** **JWT Bearer Token** kết hợp phân quyền RBAC 4 vai trò (`administrator`, `organizer`, `judge`, `participant`). Mật khẩu băm an toàn bằng thuật toán `BCrypt`.
- **Frontend Web:** **ReactJS / Next.js** (kết hợp Tailwind CSS) dành cho cổng thông tin Ban tổ chức, Giám khảo, Thí sinh và Quản trị viên.
- **Ứng dụng Mobile:** **Flutter** phục vụ Thí sinh khai báo cuộn phim, khung hình và chụp/nộp ảnh trực tiếp.
- **Công nghệ AI:** Perceptual Hash (pHash) và vector embedding để phát hiện ảnh trùng lặp/tương tự (FE9). Tích hợp OpenAI API cho phân tích và gán nhãn ảnh tự động (FE14).
- **Lưu trữ đám mây:** Cloud Storage với cơ chế URL ký có thời hạn (Signed URL) nhằm đảm bảo ảnh dự thi hoàn toàn riêng tư cho đến khi công bố triển lãm (NFR-2).

### 6.2. Thống nhất mốc thời gian và kế hoạch các Sprint
- **Sprint 1 (Tuần 1-2):** Nền tảng (Foundation) - Hoàn thành 100% kiến trúc, ERD/Schema 18 bảng, Skeleton Backend, JWT Auth, RBAC, Master Data. *(Đã nghiệm thu đạt yêu cầu)*.
- **Sprint 2 (Tuần 3-4):** Nghiệp vụ Cuộc thi & Thí sinh (Contest & Submission) - Cấu hình cuộc thi, hạng mục, tiêu chí chấm, đăng ký tham gia, quản lý cuộn phim, khung hình, nộp bài dự thi (FE3-FE7).
- **Sprint 3 (Tuần 5-6):** Kiểm tra bài & Chấm điểm (Verification & Judging) - Duyệt bài dự thi, kiểm tra ảnh bằng AI, phân công giám khảo, không gian chấm thi, tổng hợp điểm và xếp hạng (FE8-FE11).
- **Sprint 4 (Tuần 7-8):** Kết quả & Đóng gói (Publication & Delivery) - Trao giải, triển lãm trực tuyến, lưu trữ số, kiểm thử UAT, đóng gói và báo cáo tổng kết (FE12-FE16).

### 6.3. Phân công trách nhiệm và cam kết tiến độ
1. **M1 - Đinh Quang Thọ (Scrum Master, Backend Lead, Maintainer):**
   - Chịu trách nhiệm quản lý dự án, duy trì board Jira và tiến độ chung.
   - Quản lý kho mã nguồn GitHub, phê duyệt các Pull Request vào nhánh `main`.
   - Hoàn thành trọn vẹn phần Backend core và database của Sprint 1. Tiếp tục triển khai các API nghiệp vụ cuộc thi cho Sprint 2.
2. **M2 - Hà Anh Quân (Frontend Web Lead):**
   - Chịu trách nhiệm xây dựng giao diện Web Next.js.
   - Cam kết hoàn thành Wireframe và giao diện đăng ký, quản lý hồ sơ trong Sprint 2.
3. **M3 - Đặng Minh Hiếu (Frontend & Mobile Developer):**
   - Phụ trách giao diện Master Data và Wireframe không gian chấm thi.
   - Bắt đầu khởi tạo khung ứng dụng Flutter cho Mobile.
4. **M4 - Nguyễn Minh Đạt (AI Specialist & DevOps):**
   - Triển khai script PoC so sánh ảnh bằng pHash trên 20-30 ảnh mẫu để chọn ngưỡng similarity.
   - Hỗ trợ cấu hình CI/CD tự động kiểm tra code khi tạo Pull Request.
5. **M5 - Nguyễn Tấn Lộc (QA/QC & Business Analyst):**
   - Hoàn thiện tài liệu SRS, use case chi tiết và bộ Test Cases cho các chức năng Sprint 1 & 2.
   - Đảm bảo chất lượng tài liệu và kiểm thử API theo tiêu chí Acceptance Criteria.

### 6.4. Kế hoạch vận hành và kiểm soát chất lượng
- **Lịch họp Daily Stand-up:** 21:30 các tối Thứ Hai, Thứ Tư, Thứ Sáu qua Google Meet (thời lượng 10-15 phút).
- **Quy tắc Git:** Tuyệt đối không commit thẳng vào `main`. Mỗi task tạo một nhánh riêng theo mã Jira `CNPM-<mã-task>-<mô-tả>`, tạo Pull Request và phải có ít nhất 1 thành viên review/approve trước khi Merge.
- **Ngày Sprint Review & Demo với Giảng viên:** Dự kiến vào cuối Tuần 4 của môn học.


---

## 7. Quyết định của Scrum Master về điều chỉnh nhân sự & Tái phân bổ công việc

- **Thời gian lập:** 19:30 ngày 04/11/2026
- **Người ký quyết định:** Đinh Quang Thọ (Scrum Master & Trưởng nhóm, M1)
- **Thành viên liên quan:** Đặng Minh Hiếu (M3 - minhhieu2k7777777@gmail.com)

### 7.1. Lý do điều chỉnh
Trong quá trình vận hành Sprint 1, thành viên Đặng Minh Hiếu (M3) không tham gia trao đổi, không phản hồi các thông báo quan trọng trên kênh làm việc nhóm, không tham dự các phiên họp kỹ thuật và không cập nhật trạng thái thực hiện các User Story được giao trên Jira board. Để đảm bảo tính kỷ luật của nhóm và cam kết tiến độ với Giảng viên môn học (Product Owner), Scrum Master quyết định loại thành viên Đặng Minh Hiếu khỏi nhóm dự án.

### 7.2. Phương án tiếp quản & Tái phân công công việc
Toàn bộ 6 User Story tồn đọng của M3 trong Sprint 1 được **Scrum Master Đinh Quang Thọ (M1)** chính thức tiếp quản và hoàn thiện:

| Mã Jira | Tên User Story | Thời lượng gốc | Phương án thực hiện của Scrum Master |
| --- | --- | --- | --- |
| **CNPM-25** | [2.2] Quản lý master data | 1d 6h (14 giờ) | Hoàn thiện DB schema `master_data`, API `GET/POST /api/v1/system/master-data` và seed dữ liệu chuẩn hóa (phim, ISO, camera, lens, lab). |
| **CNPM-31** | [17.1] Wireframe: Organizer, Judge và Admin | 3 giờ | Hoàn thành tài liệu đặc tả [organizer-judge-admin-wireframes.md](wireframes/organizer-judge-admin-wireframes.md) và Interactive HTML Prototype [prototype.html](wireframes/prototype.html). |
| **CNPM-132** | [3.1] UI tạo và cấu hình cuộc thi (Organizer) | 8 giờ | Thiết kế Wireframe Form tạo cuộc thi, liên kết trực tiếp với API `POST /api/v1/contests` (CNPM-38). |
| **CNPM-133** | [3.2] Quản lý hạng mục và thể lệ cuộc thi | 12 giờ | Thiết kế giao diện cấu hình hạng mục và tiêu chí chấm điểm, khớp với API `POST /api/v1/contests/:id/categories` và criteria. |
| **CNPM-134** | [3.3] Cấu trúc giải thưởng theo hạng mục | 6 giờ | Thiết kế Wireframe cơ cấu giải thưởng khớp với bảng `awards` trong database. |
| **CNPM-138** | [5.3] Organizer duyệt hoặc từ chối đăng ký | 6 giờ | Hiện thực hóa API `GET /api/v1/contests/:id/registrations` và `PUT /api/v1/contests/registrations/:regId/review` trong Backend, kèm giao diện duyệt đơn. |

### 7.3. Cam kết kết quả nghiệm thu Sprint 1
Nhóm cam kết chất lượng sản phẩm cuối Sprint 1 không bị suy giảm, mã nguồn Backend và tài liệu kiến trúc/Wireframe vẫn được tích hợp đồng bộ 100% trên GitHub repository và sẵn sàng trình bày trong buổi Sprint Review với Giảng viên.
