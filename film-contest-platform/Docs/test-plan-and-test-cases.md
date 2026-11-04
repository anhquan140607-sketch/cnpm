# TEST PLAN & TEST CASES — [17.2] Kiểm thử 5 Core Flows

- **Task Jira:** CNPM-144 | **WBS:** 17.2 | **Mức ưu tiên:** Must
- **SRS Alignment:** NFR-3 (JWT / RBAC), NFR-4 (Cloud Storage), NFR-9 (Bảo toàn dữ liệu chấm điểm)
- **Công nghệ tích hợp:** Node.js Express (TypeScript), PostgreSQL

---

## 1. Tổng quan & Phạm vi kiểm thử

### 1.1 Mục tiêu
Kiểm tra và đảm bảo chất lượng cho 05 luồng nghiệp vụ cốt lõi (Core Flows) của hệ thống quản lý cuộc thi nhiếp ảnh phim:
- **Flow 1:** Lập kế hoạch và cấu hình cuộc thi (Organizer).
- **Flow 2:** Người tham gia quản lý cuộn phim (Film Roll) và nộp bài dự thi kèm thông tin kỹ thuật (Participant).
- **Flow 3:** Ban tổ chức kiểm tra hồ sơ, xác minh bài nộp và xử lý cờ cảnh báo AI (Organizer).
- **Flow 4:** Giám khảo chấm điểm có trọng số, tổng hợp điểm và xếp hạng (Judge).
- **Flow 5:** Công bố kết quả và lưu trữ số nghệ thuật (Organizer/Archive).

### 1.2 Giới hạn ngoài phạm vi (Non-Scope - Theo LI7, LI12, LI13, LI16)
- Không đánh giá tính nghệ thuật đẹp/xấu của tác phẩm.
- AI không tự động chấm điểm hay loại bài (LI7, LI13).
- Hệ thống không tự động chứng minh ảnh chụp bằng phim thật (LI12).
- Khi dịch vụ AI bên thứ 3 lỗi, chuyển sang duyệt thủ công (LI16).

---

## 2. Kế hoạch & Danh sách Test Cases (20 Test Cases)

### Flow 1 — Lập kế hoạch và Cấu hình cuộc thi
- **TC-01:** Organizer tạo cuộc thi với đầy đủ thông tin hợp lệ -> *Kết quả:* Cuộc thi tạo ở trạng thái `DRAFT`. (Mức: Cao)
- **TC-02:** Không cho tạo cuộc thi khi thiếu trường bắt buộc -> *Kết quả:* Báo lỗi Validation. (Mức: Cao)
- **TC-03:** Kiểm tra mốc thời gian cuộc thi không hợp lệ -> *Kết quả:* Từ chối lưu khi hạn nộp sau thời gian chấm. (Mức: Cao)
- **TC-04:** Chặn Participant truy cập trang cấu hình cuộc thi -> *Kết quả:* Trả về HTTP 403 Forbidden (NFR-3 RBAC). (Mức: Rất cao)

### Flow 2 — Nộp ảnh phim & Thông tin Kỹ thuật
- **TC-05:** Participant nộp ảnh phim hợp lệ kèm metadata (Film Stock, Camera, Lens, Format, Lab) -> *Kết quả:* Bài nộp chuyển trạng thái `SUBMITTED`. (Mức: Rất cao)
- **TC-06:** Từ chối bài nộp thiếu thông tin kỹ thuật phim bắt buộc -> *Kết quả:* Hiển thị lỗi thiếu metadata. (Mức: Cao)
- **TC-07:** Kiểm tra tải tệp quá dung lượng (> 25MB) hoặc sai định dạng -> *Kết quả:* Chặn upload (NFR-4 Cloud Storage). (Mức: Cao)
- **TC-08:** Không cho nộp bài khi cuộc thi đã quá hạn (`CLOSED`) -> *Kết quả:* Chặn gửi submission mới. (Mức: Rất cao)

### Flow 3 — Xác minh Hồ sơ & Hỗ trợ AI
- **TC-09:** Organizer duyệt bài nộp hợp lệ -> *Kết quả:* Trạng thái chuyển `VERIFIED`/`APPROVED`. (Mức: Rất cao)
- **TC-10:** Organizer từ chối bài nộp vi phạm và nhập lý do -> *Kết quả:* Bài nộp chuyển `REJECTED`, lưu lịch sử lý do. (Mức: Cao)
- **TC-11:** AI phát hiện ảnh trùng lặp hoặc AI-generated -> *Kết quả:* Gắn cờ cảnh báo nghi ngờ, chờ Organizer duyệt thủ công (LI13). (Mức: Cao)
- **TC-12:** Người dùng không đúng quyền gọi API duyệt bài -> *Kết quả:* Trả về lỗi 403 Forbidden. (Mức: Rất cao)

### Flow 4 — Chấm điểm & Xếp hạng
- **TC-13:** Judge nhập điểm theo bộ tiêu chí có trọng số -> *Kết quả:* Điểm lưu đúng tiêu chí và tính tổng theo công thức trọng số. (Mức: Rất cao)
- **TC-14:** Chặn nhập điểm vượt quá thang điểm (nhập điểm âm hoặc > max_score) -> *Kết quả:* Báo lỗi input out of range. (Mức: Cao)
- **TC-15:** Tổng hợp điểm nhiều giám khảo và xếp hạng -> *Kết quả:* Tính trung bình điểm có trọng số, xử lý đồng điểm nhất quán (NFR-9). (Mức: Rất cao)
- **TC-16:** Khóa sửa điểm trái quyền hoặc khi bộ tiêu chí đã bị khóa -> *Kết quả:* Trả về lỗi HTTP 409 Conflict. (Mức: Rất cao)

### Flow 5 — Công bố Kết quả & Lưu trữ
- **TC-17:** Organizer công bố kết quả sau khi hoàn tất chấm -> *Kết quả:* Đổi trạng thái cuộc thi sang `PUBLISHED`, gửi thông báo cho thí sinh. (Mức: Rất cao)
- **TC-18:** Chặn công bố khi còn bài chưa chấm xong -> *Kết quả:* Cảnh báo điều kiện chưa đủ. (Mức: Cao)
- **TC-19:** Đưa dữ liệu cuộc thi vào kho lưu trữ (Digital Archive) -> *Kết quả:* Tạo snapshot dữ liệu JSONB trong bảng `archives`. (Mức: Cao)
- **TC-20:** Chặn chỉnh sửa/xóa dữ liệu cuộc thi sau khi đã công bố -> *Kết quả:* Dữ liệu lưu trữ được bảo vệ toàn vẹn (NFR-9). (Mức: Rất cao)
