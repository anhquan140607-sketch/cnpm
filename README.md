# Nền tảng tổ chức và quản lý cuộc thi nhiếp ảnh phim tích hợp trí tuệ nhân tạo

English: AI-powered Film Photography Contest Management Platform

## Giới thiệu

Nhiếp ảnh phim đang hồi sinh mạnh mẽ, kéo theo nhiều cuộc thi dành cho cộng đồng yêu thích ảnh analog. Khác với cuộc thi ảnh kỹ thuật số, cuộc thi ảnh phim cần quản lý thêm thông tin kỹ thuật của từng bức ảnh: loại phim, máy ảnh, ống kính, khổ phim, phòng lab rửa phim, thông số scan, và đôi khi cả tham chiếu âm bản hoặc contact sheet. Hiện nay nhiều ban tổ chức vẫn dùng rời rạc biểu mẫu online, bảng tính, email và mạng xã hội, nên khó kiểm tra bài dự thi, khó chấm điểm và khó lưu trữ lâu dài.

Dự án xây dựng một nền tảng web và mobile giúp quản lý trọn vẹn cuộc thi nhiếp ảnh phim, từ lập kế hoạch, đăng ký, kiểm tra bài dự thi, chấm điểm, công bố kết quả đến lưu trữ số các tác phẩm đoạt giải. Trí tuệ nhân tạo (AI) hỗ trợ ban tổ chức phát hiện ảnh trùng lặp, nhận diện ảnh do AI tạo ra, tự động gắn từ khóa, phân loại ảnh và lập báo cáo thống kê.

## Thông tin dự án

| Mục | Nội dung |
| --- | --- |
| Quy mô nhóm | 5 thành viên |
| Thời gian | 8 tuần, chia thành 4 sprint (mỗi sprint 2 tuần) |
| Phương pháp | Agile Scrum |
| Quản lý công việc | Jira (backlog, sprint, theo dõi lỗi) |
| Quản lý mã nguồn và tài liệu | GitHub |
| Tổng ước lượng | 802 man-hours (Must 566, Should 192, Could 44) |

## Vai trò trong hệ thống

| Vai trò | Nhiệm vụ chính |
| --- | --- |
| Quản trị viên (Administrator) | Quản lý người dùng và phân quyền, cấu hình hệ thống, quản lý dữ liệu danh mục, theo dõi hoạt động nền tảng |
| Ban tổ chức (Contest Organizer) | Tạo và cấu hình cuộc thi, hạng mục, tiêu chí chấm, duyệt đăng ký, kiểm tra bài dự thi, phân công giám khảo, công bố kết quả, quản lý giải thưởng |
| Giám khảo (Judge) | Xem các bài được phân công, chấm điểm theo tiêu chí, nhận xét, tham gia nhiều vòng chấm, xác nhận kết quả cuối |
| Người tham gia (Participant) | Quản lý hồ sơ, đăng ký cuộc thi, quản lý cuộn phim và khung hình, nộp ảnh, theo dõi trạng thái bài, nhận kết quả và phản hồi |

## Chức năng chính

Phạm vi gồm 16 chức năng (FE1-FE16) và 21 giới hạn, loại trừ (LI1-LI21). Chi tiết ở [Docs/01-project-scope.md](Docs/01-project-scope.md).

| Nhóm | Chức năng |
| --- | --- |
| Nền tảng | FE1 Tài khoản và phân quyền, FE2 Cấu hình hệ thống và dữ liệu danh mục |
| Chuẩn bị cuộc thi | FE3 Lập kế hoạch và cấu hình cuộc thi, FE4 Thiết lập tiêu chí chấm |
| Người tham gia | FE5 Hồ sơ và đăng ký, FE6 Quản lý cuộn phim và khung hình, FE7 Nộp ảnh và theo dõi |
| Kiểm tra bài dự thi | FE8 Kiểm tra bài dự thi, FE9 Kiểm tra ảnh bằng AI (trùng lặp, ảnh do AI tạo) |
| Chấm điểm | FE10 Phân công giám khảo và không gian chấm, FE11 Tổng hợp điểm và xếp hạng |
| Kết quả và lưu trữ | FE12 Công bố kết quả và triển lãm online, FE13 Kho lưu trữ số |
| Hỗ trợ bằng AI và vận hành | FE14 Gắn từ khóa và phân loại tự động, FE15 Thống kê và báo cáo, FE16 Thông báo và phản hồi |

Các chức năng được gắn mức ưu tiên **Must** (luôn hoàn thành), **Should** (làm nếu kịp tiến độ) và **Could** (cắt đầu tiên nếu chậm). Xem [Docs/02-scope-estimation.md](Docs/02-scope-estimation.md).

## Công nghệ sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Web | ReactJS / Next.js |
| Mobile (dành cho người tham gia) | Flutter |
| Backend | ASP.NET Core Web API hoặc Node.js (Express), chốt ở giai đoạn thiết kế |
| Cơ sở dữ liệu | PostgreSQL hoặc MySQL, chốt ở giai đoạn thiết kế |
| AI | Computer Vision, OpenAI API, nhận diện ảnh tương tự (Image Similarity) |
| Lưu trữ ảnh | Firebase Storage hoặc Azure Blob Storage |
| Triển khai | Microsoft Azure / Firebase |
| Quản lý mã nguồn | GitHub |

Xác thực bằng JWT kết hợp phân quyền theo vai trò (RBAC).

## Cấu trúc repository

```
film-contest-platform/
├── Docs/            Tài liệu dự án (.md), thành viên đẩy lên bằng Git
├── BE/              Mã nguồn backend
├── FE/              Mã nguồn frontend (web, mobile)
├── Skills/          Các file hướng dẫn, prompt dùng chung cho nhóm
├── README.md        Tệp giới thiệu này
└── Check_list.md    Danh sách việc cần làm của nhóm
```

## Danh mục tài liệu

| Tài liệu | Nội dung |
| --- | --- |
| [Docs/01-project-scope.md](Docs/01-project-scope.md) | Chức năng chính (FE1-FE16), giới hạn và loại trừ (LI1-LI21) |
| [Docs/02-scope-estimation.md](Docs/02-scope-estimation.md) | WBS, độ phức tạp, mức ưu tiên, ước lượng effort (man-hours) và kế hoạch 8 tuần |
| [Docs/03-management-approach.md](Docs/03-management-approach.md) | Mục tiêu, rủi ro, quy trình Scrum, cấu hình Jira, quản lý chất lượng |
| [Docs/04-git-workflow-guide.md](Docs/04-git-workflow-guide.md) | Hướng dẫn thao tác Git và GitHub cho nhóm |

Lưu ý: các tài liệu 01-03 viết bằng tiếng Anh theo mẫu báo cáo, tài liệu 04 viết bằng tiếng Việt.

## Kế hoạch 4 sprint

| Sprint | Thời gian | Nội dung chính |
| --- | --- | --- |
| Sprint 1 | Tuần 1-2 | Phân tích, thiết kế kiến trúc và cơ sở dữ liệu, thiết lập dự án, xác thực và phân quyền, dữ liệu hệ thống (FE1, FE2), thử nghiệm AI |
| Sprint 2 | Tuần 3-4 | Cấu hình cuộc thi, đăng ký, cuộn phim và khung hình, nộp ảnh (FE3-FE7) |
| Sprint 3 | Tuần 5-6 | Kiểm tra bài dự thi, kiểm tra bằng AI, chấm điểm, tổng hợp và xếp hạng (FE8-FE11) |
| Sprint 4 | Tuần 7-8 | Kết quả, triển lãm, kho lưu trữ (FE12-FE13), các chức năng Should (FE14-FE16, màn hình Flutter), kiểm thử hệ thống, UAT, triển khai, báo cáo |

## Bắt đầu nhanh

```bash
git clone https://github.com/<owner>/film-contest-platform.git
cd film-contest-platform
git checkout -b <MA-JIRA>-mo-ta-ngan
```

Ví dụ tên nhánh: `FILM-12-film-roll-form`. Hãy đọc [Docs/04-git-workflow-guide.md](Docs/04-git-workflow-guide.md) trước khi commit lần đầu.

## Quy tắc làm việc nhóm

- Không push trực tiếp lên nhánh `main`. Làm việc trên nhánh riêng đặt theo mã Jira và tạo pull request.
- Mọi commit bắt đầu bằng mã Jira, ví dụ `FILM-12: add film roll form`.
- Mỗi pull request cần ít nhất 1 thành viên review (2 người với module xác thực và chấm điểm), chỉ Maintainer merge vào `main`.
- Không commit thông tin bí mật như API key, chuỗi kết nối cơ sở dữ liệu, file `.env`.
- Hoàn thành việc nào thì tick vào [Check_list.md](Check_list.md).
