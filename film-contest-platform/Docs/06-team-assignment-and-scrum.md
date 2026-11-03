# Phân công nhóm và vận hành Scrum

Dự án kéo dài 8 tuần (9/10 - 4/12/2026) với 5 thành viên và 4 sprint. Tài liệu này gắn phân công với backlog trong [jira_tasks_film_contest.csv](jira_tasks_film_contest.csv), bảng WBS trong [02-scope-estimation.md](02-scope-estimation.md) và các yêu cầu trong [05-srs.md](05-srs.md). Mọi số giờ được tính tự động từ file Jira (tổng 802 giờ).

## 1. Vai trò Scrum

| Vai trò | Người đảm nhiệm | Trách nhiệm |
| --- | --- | --- |
| Product Owner | Giảng viên hướng dẫn (cần xác nhận) | Chốt thứ tự ưu tiên Must, Should, Could và nghiệm thu ở Sprint Review |
| Scrum Master và Maintainer | Đinh Quang Thọ (M1, trưởng nhóm) | Tổ chức các nghi thức Scrum, gỡ vướng mắc, merge pull request vào `main` |
| Development Team | Đinh Quang Thọ, Hà Anh Quân, Đặng Minh Hiếu, Nguyễn Minh Đạt, Nguyễn Tấn Lộc | Làm story, review code của nhau, kiểm thử |

## 2. Thành viên và khối lượng

Nhãn M1-M5 đã gắn sẵn trên từng story trong Jira. Mỗi cột sprint gồm giờ cá nhân cộng 1/5 giờ của các việc chung (nhãn `All`, mục 4). Việc ghép M2-M5 với từng người là đề xuất ban đầu (theo thứ tự danh sách), có thể đổi.

| Nhãn Jira | Họ tên | Mảng phụ trách chính (giờ) | Số story | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Tổng giờ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | Đinh Quang Thọ | Backend (80), Participant (30), Organizer (16) | 17 | 40.4 | 40.4 | 38.6 | 46.6 | 166 |
| M2 | Hà Anh Quân | Participant (67), Judge (38), Mobile (34) | 15 | 19.4 | 50.4 | 46.6 | 52.6 | 169 |
| M3 | Đặng Minh Hiếu | Organizer (73), Archive (28), Judge (24) | 12 | 19.4 | 34.4 | 50.6 | 52.6 | 157 |
| M4 | Nguyễn Minh Đạt | AI (92), Organizer (30), Participant (8) | 12 | 16.4 | 36.4 | 50.6 | 50.6 | 154 |
| M5 | Nguyễn Tấn Lộc | QA (54), Backend (24), Admin (18) | 13 | 24.4 | 30.4 | 50.6 | 50.6 | 156 |

Năng lực mỗi người khoảng 50-60 giờ mỗi sprint (25-30 giờ mỗi tuần). Mức cao nhất trong bảng là khoảng 53 giờ ở Sprint 4. Ở Sprint 3 và Sprint 4 vài người vượt 50 giờ, nên nếu chậm hãy cắt các story Should và Could trước.

## 3. Việc của từng thành viên theo sprint

Thứ tự trong mỗi sprint là Must trước, rồi Should, rồi Could (đúng thứ tự trong backlog Jira).

### M1 - Đinh Quang Thọ

**Sprint 1 (9/10 - 23/10/2026)**

- [1.1] Đăng ký, đăng nhập, đăng xuất và quên mật khẩu (JWT) (12 giờ, Must)
- [1.3] RBAC cho 4 vai trò: middleware/policy bảo vệ endpoint (8 giờ, Must)
- [17.1] Rà soát, chốt baseline SRS và use case 4 vai trò (3 giờ, Must)
- [17.1] Thiết kế kiến trúc modular và chốt công nghệ (5 giờ, Must)
- [17.1] Thiết kế ERD và database schema (5 giờ, Must)
- [17.1] Thiết lập repo, branch protection, skeleton backend và CI cơ bản (5 giờ, Must)

**Sprint 2 (23/10 - 6/11/2026)**

- [3.1] API cuộc thi: CRUD, vòng đời trạng thái, khóa cấu hình (8 giờ, Must)
- [5.2] Xem danh sách cuộc thi và đăng ký tham gia (14 giờ, Must)
- [7.1] Upload ảnh scan lên cloud storage (16 giờ, Must)

**Sprint 3 (6/11 - 20/11/2026)**

- [9.3] Tích hợp AI service với backend và quy trình duyệt tay (10 giờ, Must)
- [11.1] Tổng hợp điểm và xếp hạng tự động (14 giờ, Must)
- [9.2] Ngưỡng cảnh báo cấu hình được và hiển thị cờ AI (12 giờ, Should)

**Sprint 4 (20/11 - 4/12/2026)**

- [12.1] Công bố kết quả chính thức (10 giờ, Must)
- [12.2] Ghi nhận giải thưởng (6 giờ, Must)
- [17.3] Triển khai bản cuối (4 giờ, Must)
- [16.1] Thông báo qua email (10 giờ, Should)
- [16.2] Thông báo trong ứng dụng (6 giờ, Could)

### M2 - Hà Anh Quân

**Sprint 1 (9/10 - 23/10/2026)**

- [2.1] Cấu hình hệ thống (6 giờ, Must)
- [17.1] Wireframe: Participant web và mobile (3 giờ, Must)
- [1.2] Hồ sơ cá nhân và bảo mật (đổi mật khẩu) (8 giờ, Should)

**Sprint 2 (23/10 - 6/11/2026)**

- [6.1] Quản lý Film Roll (14 giờ, Must)
- [6.2] Quản lý Frame và liên kết roll → frame → submission (14 giờ, Must)
- [7.2] Form nộp bài và metadata kỹ thuật (20 giờ, Must)

**Sprint 3 (6/11 - 20/11/2026)**

- [10.2] Không gian làm việc của giám khảo (16 giờ, Must)
- [10.5] Xác nhận kết quả cuối của giám khảo (4 giờ, Must)
- [8.3] Hàng đợi bài bị gắn cờ (6 giờ, Should)
- [10.4] Nhiều vòng chấm (18 giờ, Should)

**Sprint 4 (20/11 - 4/12/2026)**

- [6.3] Flutter: màn hình film roll và frame (14 giờ, Should)
- [7.5] Flutter: khung app, đăng nhập, danh sách cuộc thi (8 giờ, Should)
- [7.5] Flutter: màn hình nộp ảnh và theo dõi bài (12 giờ, Should)
- [16.3] Hiển thị kết quả và nhận xét của giám khảo (4 giờ, Should)
- [5.4] Lịch sử cuộc thi của thí sinh (4 giờ, Could)

### M3 - Đặng Minh Hiếu

**Sprint 1 (9/10 - 23/10/2026)**

- [2.2] Quản lý master data (14 giờ, Must)
- [17.1] Wireframe: Organizer, Judge và Admin (3 giờ, Must)

**Sprint 2 (23/10 - 6/11/2026)**

- [3.1] UI tạo và cấu hình cuộc thi (Organizer) (8 giờ, Must)
- [3.2] Quản lý hạng mục và thể lệ cuộc thi (12 giờ, Must)
- [3.3] Cấu trúc giải thưởng theo hạng mục (6 giờ, Must)
- [5.3] Organizer duyệt hoặc từ chối đăng ký (6 giờ, Must)

**Sprint 3 (6/11 - 20/11/2026)**

- [8.2] UI duyệt bài của Organizer (14 giờ, Must)
- [10.1] Phân công giám khảo theo hạng mục và vòng chấm (10 giờ, Must)
- [10.3] Chấm điểm theo tiêu chí và nhận xét (24 giờ, Must)

**Sprint 4 (20/11 - 4/12/2026)**

- [12.3] Triển lãm online (14 giờ, Should)
- [13.2] Tìm kiếm và lọc archive (14 giờ, Should)
- [15.2] Dashboard và biểu đồ thống kê (14 giờ, Should)

### M4 - Nguyễn Minh Đạt

**Sprint 1 (9/10 - 23/10/2026)**

- [9.1] Thử nghiệm AI (PoC): similarity và AI-generated detection (8 giờ, Must)
- [17.4] Tài liệu lý thuyết (RBL) (6 giờ, Must)

**Sprint 2 (23/10 - 6/11/2026)**

- [4.1] Tiêu chí chấm điểm có trọng số (12 giờ, Must)
- [5.1] Hồ sơ và portfolio thí sinh (8 giờ, Must)
- [4.2] Bộ tiêu chí mẫu cho nhiếp ảnh phim (4 giờ, Should)
- [3.4] Template cuộc thi tái sử dụng (10 giờ, Could)

**Sprint 3 (6/11 - 20/11/2026)**

- [9.1] Module phát hiện ảnh trùng/tương tự (24 giờ, Must)
- [9.2] Module phát hiện ảnh do AI tạo (24 giờ, Should)

**Sprint 4 (20/11 - 4/12/2026)**

- [14.1] Tự động tạo từ khóa cho ảnh (OpenAI API) (14 giờ, Should)
- [15.1] Tính toán thống kê cuộc thi (12 giờ, Should)
- [14.2] Gợi ý hạng mục và chỉnh tay (10 giờ, Could)
- [15.3] Xuất báo cáo cuộc thi (4 giờ, Could)

### M5 - Nguyễn Tấn Lộc

**Sprint 1 (9/10 - 23/10/2026)**

- [1.3] Giao diện Admin: quản lý người dùng và phân quyền (8 giờ, Must)
- [17.3] Cấu hình cloud storage và quản lý mã nguồn (4 giờ, Must)
- [2.3] Nhật ký hoạt động và giám sát (10 giờ, Could)

**Sprint 2 (23/10 - 6/11/2026)**

- [7.4] Theo dõi trạng thái, sửa và rút bài nộp (12 giờ, Must)
- [17.2] Viết test plan và test case theo 5 Core Flow (12 giờ, Must)
- [7.3] Tham chiếu negative / contact sheet (tùy chọn) (4 giờ, Should)

**Sprint 3 (6/11 - 20/11/2026)**

- [8.1] Xác minh tự động theo luật (16 giờ, Must)
- [11.2] Lưu vết đánh giá minh bạch (8 giờ, Must)
- [17.2] Kiểm thử tích hợp API (Postman/Swagger) (18 giờ, Must)
- [17.3] Thiết lập CI/CD và môi trường staging (6 giờ, Must)

**Sprint 4 (20/11 - 4/12/2026)**

- [13.1] Digital archive cho ảnh đoạt giải (10 giờ, Must)
- [13.3] Trang chi tiết tác phẩm trong archive (6 giờ, Must)
- [17.2] Kiểm thử hệ thống end-to-end và load test (24 giờ, Must)

## 4. Việc chung của cả nhóm (nhãn All)

| Sprint | Việc | Giờ cả nhóm |
| --- | --- | --- |
| Sprint 1 | [17.5] Họp và quản lý dự án - Sprint 1 | 12 |
| Sprint 2 | [17.5] Họp và quản lý dự án - Sprint 2 | 12 |
| Sprint 3 | [17.5] Họp và quản lý dự án - Sprint 3 | 13 |
| Sprint 4 | [17.2] UAT và sửa lỗi | 16 |
| Sprint 4 | [17.4] Tài liệu kỹ thuật và hướng dẫn sử dụng | 10 |
| Sprint 4 | [17.4] Báo cáo Capstone | 14 |
| Sprint 4 | [17.5] Họp và quản lý dự án - Sprint 4 | 13 |

Số giờ của các việc này đã được chia đều cho 5 người ở bảng mục 2. Trong Jira, các việc chung được gán cho trưởng nhóm (M1) để theo dõi.

## 5. Lịch 4 sprint

| Sprint | Thời gian | Mục tiêu | Must | Should | Could | Tổng giờ |
| --- | --- | --- | --- | --- | --- | --- |
| Sprint 1 | 9/10 - 23/10/2026 | Nền tảng: kiến trúc, cơ sở dữ liệu, thiết lập dự án, đăng nhập và phân quyền, dữ liệu hệ thống, thử nghiệm AI | 102 | 8 | 10 | 120 |
| Sprint 2 | 23/10 - 6/11/2026 | Cuộc thi và nộp ảnh: cấu hình cuộc thi, tiêu chí, đăng ký, film roll và frame, nộp ảnh với metadata | 174 | 8 | 10 | 192 |
| Sprint 3 | 6/11 - 20/11/2026 | Xác minh và chấm điểm: kiểm tra bài, AI trùng lặp và ảnh AI tạo, chấm điểm, xếp hạng, staging | 177 | 60 | 0 | 237 |
| Sprint 4 | 20/11 - 4/12/2026 | Kết quả và bàn giao: công bố, archive, tính năng Should, app Flutter, kiểm thử hệ thống, UAT, triển khai, báo cáo | 113 | 116 | 24 | 253 |

Nghi thức trong mỗi sprint:

- **Sprint Planning:** ngày đầu sprint. Kiểm tra tổng giờ không vượt năng lực, lấy story Must trước.
- **Daily stand-up:** 15 phút mỗi ngày làm việc, ngay trên tab Board. Mỗi người nói việc hôm qua, việc hôm nay, vướng mắc.
- **Sprint Review:** ngày cuối sprint, trình bày cho giảng viên. Sau đó bấm Complete sprint, story chưa xong tự chuyển sang sprint sau.
- **Retrospective:** ngay sau Review. Ghi lại điều làm tốt, điều cần cải thiện, hành động (dùng tab Docs hoặc Whiteboard trong space Jira).

## 6. Definition of Done

Một story chỉ được chuyển sang Done khi đủ các điều kiện sau:

- Code đã được review bởi ít nhất 1 thành viên khác (2 người với xác thực và chấm điểm).
- Đã kiểm thử đạt tiêu chí của giai đoạn tương ứng trong [03-management-approach.md](03-management-approach.md) (logic lõi có unit test, API có test Postman).
- Đã merge vào `main` qua pull request; tên nhánh và commit có mã Jira.
- Tài liệu liên quan trong `Docs/` được cập nhật nếu nội dung thay đổi.

## 7. Cách dùng trong Jira

1. **Ước lượng theo giờ:** trong Space settings → Features đổi Estimation sang Original time estimate để mỗi sprint hiện tổng số giờ.
2. **Cột Board:** To Do → In Progress → In Review → Testing → Done.
3. **Xem việc của một người trong một sprint:** dùng bộ lọc JQL, ví dụ `labels = M2 AND sprint = "Sprint 2" ORDER BY Rank`.
4. **Gán người:** file CSV đã có cột Assignee (email của từng người). Mọi thành viên phải có trong space Jira trước khi import (Space settings → Access). Nếu import báo lỗi người dùng, bỏ tick cột Assignee rồi gán sau: Filters → Advanced search, nhập `labels = M1`, chọn tất cả, Bulk change → Edit work items → Assignee, lặp lại cho M2-M5.
5. **Theo dõi tiến độ:** xem Burndown trong Reports hoặc Summary, bấm Complete sprint ở cuối mỗi sprint.
6. **Đưa story vào sprint:** nếu lúc import không map được cột Sprint, mỗi story đã có nhãn Sprint1 đến Sprint4. Tạo 4 sprint trong Backlog (Create sprint), bấm Filter → Labels chọn Sprint1, chọn tất cả story (giữ Shift) rồi kéo vào sprint tương ứng. Lặp lại cho Sprint2, Sprint3, Sprint4.

## 8. Lưu ý và việc cần xác nhận

- Mục 17.5 trong WBS (50 giờ) vừa đủ cho daily stand-up: 15 phút × 5 người × 10 ngày × 4 sprint. Sprint Planning, Review và Retrospective chưa được tính. Nếu mỗi sprint dùng khoảng 4 giờ cho mỗi người (Planning 2 giờ, Review 1 giờ, Retrospective 1 giờ) thì thêm khoảng 80 giờ cho cả dự án, vẫn nằm trong phần dự phòng (1.200 giờ năng lực trừ 802 giờ ước lượng).
- Đinh Quang Thọ là trưởng nhóm nên là M1 (Scrum Master và Maintainer). Việc ghép M2-M5 với Hà Anh Quân, Đặng Minh Hiếu, Nguyễn Minh Đạt, Nguyễn Tấn Lộc theo thứ tự danh sách là đề xuất ban đầu, nhóm xác nhận hoặc đổi. Vai trò Product Owner của giảng viên cũng cần xác nhận.
- Tiến độ thực tế: Sprint 1 (9/10 - 23/10) đã kết thúc và Sprint 2 đang diễn ra. Sau khi import, hãy đánh dấu Done cho các story đã xong và chuyển phần chưa xong sang sprint kế tiếp khi Complete sprint.
