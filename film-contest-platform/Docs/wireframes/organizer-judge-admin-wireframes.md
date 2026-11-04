# Đặc tả Wireframe & UI Mockup: Organizer, Judge và Admin
**Mã công việc:** CNPM-31 / [17.1] Wireframe: Organizer, Judge và Admin  
**Người đảm nhận (Scrum Master tiếp quản):** Đinh Quang Thọ (M1)  
**Thời lượng:** 3 giờ | **Mức ưu tiên:** Must  
**Liên kết tài liệu:** [05-srs.md](../05-srs.md), [08-architecture-and-erd.md](../08-architecture-and-erd.md), [07-sprint1-meeting-kit.md](../07-sprint1-meeting-kit.md)

---

## 1. Tổng quan kiến trúc giao diện các vai trò nội bộ

Hệ thống cung cấp không gian làm việc chuyên biệt cho 3 vai trò quản trị và chuyên môn theo chuẩn RBAC:
1. **Ban tổ chức (Organizer)**: Quản lý vòng đời cuộc thi, cấu hình hạng mục/thể lệ, duyệt hồ sơ đăng ký của thí sinh.
2. **Ban giám khảo (Judge)**: Không gian chấm điểm độc lập, xem ảnh scan độ phân giải cao kèm thông số EXIF/Film Roll, bảng chấm theo tiêu chí trọng số.
3. **Quản trị hệ thống (Administrator)**: Quản lý danh mục dùng chung (Master Data), phân quyền và tra cứu nhật ký hệ thống (Audit Logs).

```
+---------------------------------------------------------------------------------------+
|  Top Navigation: Logo | [Chuyển Workspace: Organizer / Judge / Admin] | User Profile  |
+---------------------------------------------------------------------------------------+
| Sidebar Menu          | Workspace Content Area                                        |
| - Tổng quan           | - Header thao tác: Tiêu đề, Breadcrumbs, Nút hành động chính |
| - Quản lý cuộc thi    | - Thẻ tóm tắt chỉ số (KPI Cards)                              |
| - Duyệt đăng ký (FE5) | - Bảng dữ liệu / Form cấu hình chi tiết                       |
| - Master Data (FE2)   | - Thanh phân trang & Bộ lọc tìm kiếm nhanh                    |
+---------------------------------------------------------------------------------------+
```

---

## 2. Wireframe Ban tổ chức (Organizer Portal)

### 2.1. UI Tạo & Cấu hình cuộc thi (CNPM-132 / SRS: FR-3.1, FR-3.2)
- **Mục tiêu:** Cho phép Organizer tạo mới cuộc thi, nhập timeline và quản lý trạng thái khóa cấu hình.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Organizer] > Cuộc thi > Tạo cuộc thi mới                                             |
+---------------------------------------------------------------------------------------+
| [ Tên cuộc thi: Cuộc thi Nhiếp ảnh Phim Mùa Thu 2026_________________________ ]       |
| [ Chủ đề: Hà Nội - Những khung hình thời gian_________________________________ ]       |
|                                                                                       |
| Timeline cuộc thi:                                                                    |
| Mở nhận bài: [ 2026-11-01 00:00 ]       Đóng nhận bài: [ 2026-11-20 23:59 ]          |
| Bắt đầu chấm: [ 2026-11-21 00:00 ]      Công bố giải:  [ 2026-11-30 18:00 ]          |
|                                                                                       |
| Phí tham gia (VND): [ 100,000      ]   Trạng thái hiện tại: [ DRAFT (Bản nháp) v ]    |
| [x] Khóa cấu hình sau khi mở nhận bài (config_locked)                                 |
|                                                                                       |
| Thể lệ chi tiết (Markdown/Rich Text):                                                 |
| +-----------------------------------------------------------------------------------+ |
| | - Chỉ chấp nhận ảnh chụp bằng máy ảnh phim (35mm, 120, Large Format).             | |
| | - Bắt buộc cung cấp ảnh cuộn phim / file scan lab có đối chiếu frame.             | |
| +-----------------------------------------------------------------------------------+ |
|                                                    [ Hủy bỏ ]   [ Lưu bản nháp ] [ Tạo cuộc thi ] |
+---------------------------------------------------------------------------------------+
```

### 2.2. UI Quản lý Hạng mục & Thể lệ (CNPM-133 / SRS: FR-3.4, FR-3.5)
- **Mục tiêu:** Cấu hình các hạng mục ảnh (Đen trắng, Phong cảnh, Chân dung) và tiêu chí chấm điểm có trọng số $\le 100\%$.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Organizer] > Cuộc thi #1 > Quản lý Hạng mục & Tiêu chí chấm                          |
+---------------------------------------------------------------------------------------+
| Danh sách Hạng mục (Categories):                                  [ + Thêm hạng mục ] |
| | Tên hạng mục    | Số ảnh tối đa | Định dạng phim áp dụng   | Thao tác              |
| |-----------------|---------------|--------------------------|-----------------------|
| | Ảnh Đen Trắng   | 5 ảnh         | 35mm B&W (ISO 100-400)   | [ Sửa ] [ Xóa ]       |
| | Ảnh Màu         | 3 ảnh         | 35mm / 120 Color         | [ Sửa ] [ Xóa ]       |
|                                                                                       |
| Tiêu chí chấm điểm (Criteria) - Tổng trọng số: 100% / 100%        [ + Thêm tiêu chí ] |
| | Tiêu chí                    | Trọng số (%) | Điểm tối đa | Mô tả                 |
| |-----------------------------|--------------|-------------|-----------------------|
| | Kỹ thuật phơi sáng & tráng  | 30%          | 10.0        | Độ sắc nét, hạt phim  |
| | Bố cục và Ánh sáng          | 40%          | 10.0        | Tính thẩm mỹ thị giác |
| | Cảm xúc & Tính câu chuyện   | 30%          | 10.0        | Chiều sâu tác phẩm    |
+---------------------------------------------------------------------------------------+
```

### 2.3. UI Cấu trúc Giải thưởng (CNPM-134 / SRS: FR-3.6)
- **Mục tiêu:** Cấu hình hệ thống giải thưởng theo từng hạng mục để tự động xếp hạng ở Sprint 4.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Organizer] > Cuộc thi #1 > Cấu trúc giải thưởng                  [ + Thêm giải thưởng ] |
+---------------------------------------------------------------------------------------+
| | Hạng mục     | Thứ hạng | Tên giải thưởng | Giá trị giải thưởng | Số lượng giải    |
| |--------------|----------|-----------------|---------------------|------------------|
| | Ảnh Đen Trắng| 1        | Giải Nhất       | 15,000,000 VND      | 01 giải          |
| | Ảnh Đen Trắng| 2        | Giải Nhì        | 8,000,000 VND       | 02 giải          |
| | Toàn cuộc thi| Đặc biệt | Best of Contest | 25,000,000 VND      | 01 giải          |
+---------------------------------------------------------------------------------------+
```

### 2.4. UI Duyệt / Từ chối đơn đăng ký tham gia (CNPM-138 / SRS: FR-5.3, FR-5.4)
- **Mục tiêu:** Ban tổ chức kiểm tra danh sách thí sinh nộp đơn đăng ký tham gia (FE5) và phê duyệt/từ chối kèm phản hồi.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Organizer] > Quản lý Đăng ký tham gia (Contest: "Hà Nội Phim 2026")                 |
+---------------------------------------------------------------------------------------+
| Bộ lọc: [ Trạng thái: Tất cả v ] [ Hạng mục: Tất cả v ] [ Tìm kiếm thí sinh... ]     |
|                                                                                       |
| | Mã đơn | Thí sinh          | Email                     | Hạng mục     | Ngày nộp   | Trạng thái  | Thao tác           |
| |--------|-------------------|---------------------------|--------------|------------|-------------|--------------------|
| | #101   | Nguyễn Văn A      | participant@filmcontest.vn| Đen Trắng    | 04/11/2026 | [ PENDING ] | [ Duyệt ] [Từ chối]|
| | #102   | Trần Thị B        | thib@gmail.com            | Màu          | 04/11/2026 | [ APPROVED ]| [ Xem chi tiết ]   |
|                                                                                       |
| [ Modal Phê duyệt / Từ chối đơn đăng ký ]                                             |
| Trạng thái: (o) Duyệt (Approved)     ( ) Từ chối (Rejected)                           |
| Lý do / Ghi chú gửi thí sinh:                                                        |
| [ Đủ điều kiện thể lệ cuộn phim và thiết bị hợp lệ_________________________ ]         |
|                                                      [ Hủy ]  [ Xác nhận cập nhật ]   |
+---------------------------------------------------------------------------------------+
```

---

## 3. Wireframe Ban Giám Khảo (Judge Workspace - CNPM-31 / SRS: FR-10.1 -> FR-10.5)

- **Mục tiêu:** Cung cấp môi trường chấm bài tập trung, hiển thị ảnh chất lượng cao kèm cuộn phim đối chứng và bảng chấm điểm chi tiết.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Giám khảo] > Chấm thi Cuộc thi #1 > Tác phẩm #301 ("Góc phố sương sớm")              |
+---------------------------------------------------------------------------------------+
| [ KHUNG XEM ẢNH GỐC ]                 | [ BẢNG ĐÁNH GIÁ CỦA GIÁM KHẢO ]               |
|                                       | Thí sinh: Thí sinh ẩn danh #101               |
| +-----------------------------------+ | Hạng mục: Ảnh Đen Trắng                       |
| |                                   | | Thông số phim: Kodak Tri-X 400 | Leica M3     |
| |       [ ẢNH DỰ THI SCAN GỐC ]     | | Lab: AEG Lab Hà Nội | Scanner: Noritsu HS-1800|
| |                                   | |                                               |
| |                                   | | Tiêu chí chấm điểm:                           |
| +-----------------------------------+ | 1. Kỹ thuật phơi sáng (30%):  [ 8.5 / 10 ]     |
|                                       | 2. Bố cục & Ánh sáng (40%):   [ 9.0 / 10 ]     |
| [ ĐỐI CHỨNG CUỘN PHIM (Film Roll) ]  | 3. Cảm xúc tác phẩm (30%):    [ 8.0 / 10 ]     |
| Frame #12 trong Roll: "Hanoi-Autumn"  |                                               |
| Trạng thái AI Check: [ HỢP LỆ (0.12) ]| >> Điểm tổng kết: [ 8.55 / 10.0 ]             |
|                                       | Nhận xét chuyên môn:                          |
|                                       | [ Tương phản vùng tối rất tốt, hạt phim mịn..]|
|                                       | [ Lưu tạm điểm ]      [ Nộp bảng điểm chính thức ] |
+---------------------------------------------------------------------------------------+
```

---

## 4. Wireframe Quản trị viên (Admin - Master Data - CNPM-25 / SRS: FR-2.2)

- **Mục tiêu:** Cung cấp giao diện quản lý các bảng danh mục chuẩn hóa: `film_brand`, `film_stock`, `iso`, `camera`, `lens`, `lab`, `scanner`.
- **Wireframe Layout:**
```
+---------------------------------------------------------------------------------------+
| [Admin] > Quản trị hệ thống > Danh mục dùng chung (Master Data)                       |
+---------------------------------------------------------------------------------------+
| Tabs: [ Hãng phim ] [ Dòng phim ] [ ISO ] [ Máy ảnh ] [ Ống kính ] [ Lab tráng ]     |
|                                                                                       |
| Danh sách Hãng phim (film_brand):                                   [ + Thêm mục mới ] |
| | ID | Mã / Tên hãng      | Mô tả                           | Trạng thái | Thao tác   |
| |----|--------------------|---------------------------------|------------|------------|
| | 1  | Kodak              | Eastman Kodak Company           | Hoạt động  | [Sửa] [Ẩn] |
| | 2  | Fujifilm           | Fujifilm Corporation            | Hoạt động  | [Sửa] [Ẩn] |
| | 3  | Ilford             | Harman Technology (B&W)         | Hoạt động  | [Sửa] [Ẩn] |
| | 4  | Cinestill          | Motion Picture Film for Stills  | Hoạt động  | [Sửa] [Ẩn] |
|                                                                                       |
| Modal Thêm Master Data:                                                               |
| Phân loại: [ film_brand v ]                                                           |
| Giá trị (Value): [ Kodak________________ ]                                            |
| Mô tả: [ Hãng phim chụp ảnh truyền thống Hoa Kỳ_________________________ ]            |
| Trạng thái: [ Hoạt động (active) v ]                  [ Hủy ]  [ Lưu vào hệ thống ]   |
+---------------------------------------------------------------------------------------+
```

---

## 5. Bảng ma trận đối chiếu (Traceability Matrix)

| Task ID | Tiêu đề Story | Vai trò | Endpoint API tương ứng trong Backend | Trạng thái kỹ thuật |
| --- | --- | --- | --- | --- |
| **CNPM-25** | [2.2] Quản lý master data | Admin | `GET/POST /api/v1/system/master-data` | Sẵn sàng 100% |
| **CNPM-31** | [17.1] Wireframe: Organizer, Judge, Admin | Toàn nhóm | Tài liệu Wireframe & Prototype tương tác | Hoàn thành |
| **CNPM-132**| [3.1] UI tạo và cấu hình cuộc thi | Organizer | `POST /api/v1/contests` | Khớp với CNPM-38 |
| **CNPM-133**| [3.2] Quản lý hạng mục và thể lệ | Organizer | `POST /api/v1/contests/:id/categories` | Khớp với schema DB |
| **CNPM-134**| [3.3] Cấu trúc giải thưởng | Organizer | Bảng `awards` & tiêu chí xếp hạng | Khớp với schema DB |
| **CNPM-138**| [5.3] Organizer duyệt/từ chối đăng ký | Organizer | `GET/PUT /api/v1/contests/registrations` | Sẵn sàng 100% |
