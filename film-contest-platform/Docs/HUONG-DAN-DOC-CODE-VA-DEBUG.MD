# BÍ KÍP ĐỌC HIỂU SOURCE CODE, LUỒNG ĐI (DEBUG) & VẤN ĐÁP
**Học phần:** Software Project (SWP) / Đồ án phát triển phần mềm  
**Dự án:** Nền tảng quản lý cuộc thi nhiếp ảnh phim tích hợp AI (Film Photography Contest Platform)  
**Kiến trúc:** Flask Clean Architecture & SQLAlchemy ORM  
**Dành cho sinh viên:** Đinh Quang Thọ (M1 - Scrum Master & Backend Lead)  

---

## 1. TỔNG QUAN KIẾN TRÚC CLEAN ARCHITECTURE

Dự án áp dụng nguyên lý **Clean Architecture** (Kiến trúc phân tầng sạch của Robert C. Martin). Điểm cốt lõi là **sự độc lập**: Nghiệp vụ (Business Logic) không bị phụ thuộc vào Framework (Flask) hay Hệ quản trị CSDL (PostgreSQL, MySQL, MSSQL).

```
+---------------------------------------------------------------------------------+
|  1. TẦNG API (Giao diện bên ngoài - Controllers & Schemas)                     |
|     - File: src/api/controllers/auth_controller.py, contest_controller.py       |
|     - Nhận HTTP Request (JSON), gọi Service, trả về HTTP Response               |
+---------------------------------------------------------------------------------+
                                       │ (gọi qua Service)
                                       ▼
+---------------------------------------------------------------------------------+
|  2. TẦNG SERVICES (Quy tắc nghiệp vụ - Business Logic / Use Cases)             |
|     - File: src/services/auth_service.py, contest_service.py                    |
|     - Xử lý logic: kiểm tra mật khẩu, khóa cấu hình, tính tổng trọng số = 100% |
+---------------------------------------------------------------------------------+
                                       │ (gọi qua Repository)
                                       ▼
+---------------------------------------------------------------------------------+
|  3. TẦNG INFRASTRUCTURE (Hạ tầng, ORM Models & Cơ sở dữ liệu)                   |
|     - Models: src/infrastructure/models/*.py (18 bảng ánh xạ từ ERD.MD)         |
|     - Databases: FactoryDatabase, database_postgres.py, database_mysql.py       |
|     - Repositories: user_repository.py, contest_repository.py                   |
+---------------------------------------------------------------------------------+
                                       ▲
                                       │ (phụ thuộc vào Domain)
+---------------------------------------------------------------------------------+
|  4. TẦNG DOMAIN (Lõi nghiệp vụ độc lập - Constants & Exceptions)               |
|     - File: src/domain/constants.py, src/domain/exceptions.py                   |
|     - Định nghĩa hằng số vai trò (RBAC), trạng thái cuộc thi, ngoại lệ lỗi      |
+---------------------------------------------------------------------------------+
```

---

## 2. LUỒNG ĐI CỦA MỘT REQUEST (DEBUG TRACE TỪ A - Z)

Khi giảng viên yêu cầu: *"Em hãy chỉ ra luồng dữ liệu đi như thế nào từ khi Client gọi API đến khi lưu vào Database?"* ➔ Bạn trình bày ví dụ luồng **Tạo cuộc thi (`POST /api/v1/contests`)** như sau:

```
[1. Client / Swagger]
       │ Gửi Request: POST http://localhost:5000/api/v1/contests
       │ Kèm Header: Authorization: Bearer <JWT_Token>
       │ Kèm Body: {"title": "Hà Nội 2026", "theme": "Phố cổ", "submission_start": ...}
       ▼
[2. Middleware: src/api/middleware.py]
       │ Hàm @authenticate_token giải mã JWT bằng SECRET_KEY
       │ Hàm @authorize_roles('organizer', 'administrator') kiểm tra vai trò
       │ Lưu thông tin người dùng vào biến ngữ cảnh: g.user
       ▼
[3. Controller: src/api/controllers/contest_controller.py]
       │ Hàm create_contest() bóc tách dữ liệu JSON
       │ Kiểm tra validate các trường bắt buộc (title, theme, timeline)
       │ Gọi: contest_service.create_contest(organizer_id, data)
       ▼
[4. Service: src/services/contest_service.py]
       │ Khởi tạo đối tượng ContestModel với status = 'draft', config_locked = False
       │ Gọi: self.contest_repo.create(contest)
       ▼
[5. Repository: src/infrastructure/repositories/contest_repository.py]
       │ Lấy session từ FactoryDatabase: session = self.db.get_session()
       │ Thực hiện lệnh SQLAlchemy: session.add(contest) -> session.commit()
       │ Trả về đối tượng vừa được ghi xuống CSDL
       ▼
[6. Database (PostgreSQL / MySQL / MSSQL)]
       │ Thực thi lệnh INSERT INTO contests (...) VALUES (...)
       ▼
[7. Trả ngược kết quả]:
       │ Repository ➔ Service (.to_dict()) ➔ Controller (success_response(..., 201)) ➔ Client nhận JSON 201 Created.
```

---

## 3. CÁCH CHUYỂN ĐỔI GIỮA CÁC HỆ QUẢN TRỊ CSDL (POSTGRESQL / MYSQL / MSSQL)

Theo đúng yêu cầu của Giảng viên: *"Dễ dàng chuyển đổi và cấu hình để kết nối với các HQT CSDL"*.

### Cơ chế hoạt động:
- Lớp **`FactoryDatabase`** tại `src/infrastructure/databases/factory_database.py` áp dụng **Factory Design Pattern**.
- Khi ứng dụng khởi chạy, hệ thống đọc biến môi trường **`DB_TYPE`** từ file `.env`:
  + `DB_TYPE=POSTGREE`: Khởi tạo `DatabasePostgres` kết nối cổng 5432.
  + `DB_TYPE=MYSQL`: Khởi tạo `DatabaseMySQL` kết nối cổng 3306.
  + `DB_TYPE=MSSQL`: Khởi tạo `DatabaseMSSQL` kết nối cổng 1433.

### Trả lời thầy khi được hỏi:
> *"Thưa thầy, nhờ áp dụng Clean Architecture và SQLAlchemy ORM, toàn bộ logic nghiệp vụ và 18 Models không phụ thuộc vào SQL riêng của từng hệ quản trị. Khi cần đổi từ PostgreSQL sang MySQL hoặc MS SQL Server, em **chỉ cần sửa đúng 1 dòng trong file `.env`**: `DB_TYPE=MYSQL`, toàn bộ bảng và quan hệ sẽ tự động ánh xạ sang CSDL mới mà không cần sửa bất kỳ dòng code nào trong nghiệp vụ."*

---

## 4. BỘ 5 CÂU HỎI VẤN ĐÁP GIẢNG VIÊN CHẮC CHẮN SẼ HỎI & CÂU TRẢ LỜI MẪU

### Câu hỏi 1: ORM (Object-Relational Mapping) là gì và em đã áp dụng nó như thế nào?
- **Trả lời:**
  > *"Dạ thưa thầy, ORM là kỹ thuật ánh xạ giữa các Lớp (Class/Object) trong lập trình hướng đối tượng với các Bảng (Table) trong cơ sở dữ liệu quan hệ.*  
  > *Trong dự án này, em sử dụng thư viện **SQLAlchemy ORM**. Đầu vào là tài liệu **`ERD.MD`** mô tả 18 thực thể. Em đã ánh xạ 1:1 thành 18 file Model trong thư mục `src/infrastructure/models/` (ví dụ `ContestModel`, `UserModel`, `SubmissionModel`) kế thừa từ `Base = declarative_base()`. Các thuộc tính như khóa chính `primary_key=True`, khóa ngoại `ForeignKey('users.id')` và ràng buộc `UniqueConstraint` được mô hình hóa trực tiếp trong code Python."*

---

### Câu hỏi 2: Tại sao phải tách Repository và Service riêng biệt?
- **Trả lời:**
  > *"Dạ thưa thầy, việc tách biệt giúp tuân thủ nguyên lý **Single Responsibility Principle (Trách nhiệm duy nhất)**:*  
  > *- **Repository** chỉ tập trung vào việc đọc/ghi CSDL (CRUD, câu lệnh ORM query).*  
  > *- **Service** chịu trách nhiệm xử lý các quy tắc nghiệp vụ (Business Rules), ví dụ: kiểm tra cuộc thi có bị khóa cấu hình không, tổng trọng số tiêu chí có vượt quá 100% không, kiểm tra băm mật khẩu. Nhờ vậy nếu sau này thay đổi cách lưu trữ dữ liệu thì chỉ cần sửa Repository mà toàn bộ Service không bị ảnh hưởng."*

---

### Câu hỏi 3: Làm thế nào để phân quyền (RBAC) 4 vai trò trong hệ thống?
- **Trả lời:**
  > *"Dạ thưa thầy, em sử dụng cơ chế **JWT (JSON Web Token)** kết hợp với Python Decorator:*  
  > *1. Khi đăng nhập thành công, token được ký chứa payload gồm `id`, `email`, và `role` (`administrator`, `organizer`, `judge`, `participant`).*  
  > *2. Tại các endpoint, em gắn decorator `@authenticate_token` để xác thực danh tính và `@authorize_roles('organizer', 'administrator')` để kiểm tra quyền truy cập. Nếu người dùng không đủ quyền, middleware chặn lại ngay lập tức và trả về mã lỗi `403 Forbidden`."*

---

### Câu hỏi 4: Khi debug một lỗi trong chương trình, em sẽ bắt đầu từ đâu?
- **Trả lời:**
  > *"Dạ thưa thầy, quy trình debug của em đi theo chiều ngược lại của luồng dữ liệu:*  
  > *1. Đầu tiên, em kiểm tra **HTTP Status Code và mã lỗi** trả về từ API (ví dụ 400 Bad Request, 401 Unauthorized, hay 500 Internal Error).*  
  > *2. Tiếp theo, em kiểm tra log terminal của Flask để xem dòng code (Traceback) gây ra Exception.*  
  > *3. Em đặt breakpoint hoặc in log kiểm tra giá trị tại tầng **Controller** xem dữ liệu đầu vào đã đúng định dạng chưa.*  
  > *4. Sau đó kiểm tra logic tại **Service**, và cuối cùng kiểm tra câu lệnh ORM tại **Repository** để xem phiên làm việc CSDL (`session`) có commit thành công hay bị rollback."*

---

### Câu hỏi 5: Đầu vào `ERD.MD` có quan hệ gì với mã nguồn Backend?
- **Trả lời:**
  > *"Dạ thưa thầy, `ERD.MD` là tài liệu thiết kế đặc tả chi tiết toàn bộ thế giới thực thể của dự án (tên cột, kiểu dữ liệu, quan hệ 1-N, N-N, ràng buộc toàn vẹn). Mã nguồn Backend tại `src/infrastructure/models/` chính là sự hiện thực hóa (implementation) chuẩn xác 100% của `ERD.MD` sang ngôn ngữ Python để máy tính và hệ CSDL có thể vận hành được."*
