# HƯỚNG DẪN TRIỂN KHAI VÀ TÀI LIỆU CÔNG VIỆC (JIRA TASK)

## 1. THÔNG TIN CHUNG (TASK OVERVIEW)

* **Mã công việc (Issue Key):** CNPM-24
* **Epic/Parent:** CNPM-5
* **Tiêu đề:** [2.1] Cấu hình hệ thống
* **Loại công việc:** Feature / User Story
* **Độ ưu tiên:** Must (Bắt buộc)
* **Thời gian ước lượng:** 6 giờ
* **Mã tài liệu liên quan:** FE2 (Docs/01) | WBS 2.1 (Docs/02) | SRS: FR-2.1

---

## 2. PHÂN TÍCH YÊU CẦU NGHỆP VỤ (BUSINESS & SRS REQUIREMENTS)

### 2.1. Tóm tắt yêu cầu
Xây dựng phân hệ/trang quản trị dành cho **Administrator** để cấu hình các thiết lập dùng chung trên toàn hệ thống, bao gồm:
1. **Định dạng ảnh cho phép:** Quản lý danh sách các đuôi file ảnh được chấp nhận khi tải lên (ví dụ: `.jpg`, `.jpeg`, `.png`, `.tiff`).
2. **Dung lượng tối đa:** Giới hạn dung lượng tải lên tối đa cho từng file ảnh (tính bằng MB, ví dụ: 25 MB).
3. **Chất lượng ảnh tối thiểu:** Cấu hình độ phân giải tối thiểu (pixel) hoặc DPI để đảm bảo ảnh scan đạt chuẩn cho việc chấm giải và lưu trữ.
4. **Thiết lập thông báo:** Quản lý các kênh/trạng thái bật tắt thông báo (Email, Push notification, In-app) gửi tới người dùng.

### 2.2. Các yêu cầu chức năng (FR Alignment)
* **FR-2.1 (Quản lý cấu hình toàn hệ thống):**
  * Cho phép Admin xem, chỉnh sửa và lưu các thông số cấu hình hệ thống.
  * Các tham số cấu hình phải có hiệu lực ngay lập tức (hoặc qua cơ chế Cache refresh) trên toàn hệ thống.
  * Áp dụng tự động các luật validation này vào các luồng upload ảnh (Thí sinh nộp bài, Upload frame).

---

## 3. THIẾT KẾ CƠ SỞ DỮ LIỆU & BACKEND API

### 3.1. Cấu trúc bảng Database (`SystemSettings`)

| Tên trường (Column) | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `Key` (PK) | `VARCHAR(100)` | Mã cấu hình (ví dụ: `ALLOWED_IMAGE_EXTENSIONS`) |
| `Value` | `TEXT` | Giá trị cấu hình (ví dụ: `jpg,jpeg,png,tiff`) |
| `Description` | `NVARCHAR(255)` | Mô tả ý nghĩa của tham số |
| `UpdatedAt` | `DATETIME` | Thời gian cập nhật gần nhất |
| `UpdatedBy` | `UUID` | ID của Admin thực hiện cập nhật |

### 3.2. API Endpoints

* **GET `/api/v1/admin/settings`**
  * *Mô tả:* Lấy danh sách toàn bộ cấu hình hệ thống hiện tại.
  * *Quyền truy cập:* Admin (`Role: Administrator`).

* **PUT `/api/v1/admin/settings`**
  * *Mô tả:* Cập nhật giá trị cấu hình hệ thống.
  * *Request Body DTO:*
    ```json
    {
      "allowedExtensions": ["jpg", "jpeg", "png", "tiff"],
      "maxFileSizeMb": 25,
      "minImageWidthPx": 2000,
      "minImageHeightPx": 1500,
      "enableEmailNotifications": true,
      "enablePushNotifications": true
    }
    ```

---

## 4. GIAO DIỆN MẪU FRONTEND (REACTJS / NEXT.JS)

Đoạn mã mã nguồn dưới đây minh họa trang cấu hình hệ thống cho Quản trị viên:

```jsx
import React, { useState, useEffect } from 'react';

const SystemConfigAdmin = () => {
  const [config, setConfig] = useState({
    allowedExtensions: 'jpg, jpeg, png, tiff',
    maxFileSizeMb: 25,
    minImageWidthPx: 2000,
    minImageHeightPx: 1500,
    enableEmailNotifications: true,
    enablePushNotifications: true,
  });

  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Gọi API lưu cấu hình
    setMessage('Cập nhật cấu hình hệ thống thành công!');
    setTimeout(() => setMessage(''), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-bold mb-6 border-b pb-3">Cấu hình Hệ thống [2.1]</h1>

      {message && <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-md">{message}</div>}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Phần 1: Cấu hình tải lên tệp ảnh */}
        <div className="bg-gray-50 p-4 rounded-md space-y-4">
          <h2 className="text-lg font-semibold text-gray-800">1. Quy định Tải lên Hình ảnh</h2>
          
          <div>
            <label className="block text-sm font-medium mb-1">Định dạng ảnh cho phép (phân cách bằng dấu phẩy)</label>
            <input
              type="text"
              value={config.allowedExtensions}
              onChange={(e) => setConfig({ ...config, allowedExtensions: e.target.value })}
              className="w-full border rounded-md p-2 bg-white"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Dung lượng tối đa mỗi ảnh (MB)</label>
            <input
              type="number"
              value={config.maxFileSizeMb}
              onChange={(e) => setConfig({ ...config, maxFileSizeMb: Number(e.target.value) })}
              className="w-full border rounded-md p-2 bg-white"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Chiều rộng tối thiểu (px)</label>
              <input
                type="number"
                value={config.minImageWidthPx}
                onChange={(e) => setConfig({ ...config, minImageWidthPx: Number(e.target.value) })}
                className="w-full border rounded-md p-2 bg-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Chiều cao tối thiểu (px)</label>
              <input
                type="number"
                value={config.minImageHeightPx}
                onChange={(e) => setConfig({ ...config, minImageHeightPx: Number(e.target.value) })}
                className="w-full border rounded-md p-2 bg-white"
              />
            </div>
          </div>
        </div>

        {/* Phần 2: Cấu hình Thông báo */}
        <div className="bg-gray-50 p-4 rounded-md space-y-4">
          <h2 className="text-lg font-semibold text-gray-800">2. Thiết lập Thông báo</h2>
          
          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="emailNotif"
              checked={config.enableEmailNotifications}
              onChange={(e) => setConfig({ ...config, enableEmailNotifications: e.target.checked })}
              className="h-4 w-4"
            />
            <label htmlFor="emailNotif" className="text-sm font-medium">Kích hoạt gửi thông báo qua Email</label>
          </div>

          <div className="flex items-center space-x-3">
            <input
              type="checkbox"
              id="pushNotif"
              checked={config.enablePushNotifications}
              onChange={(e) => setConfig({ ...config, enablePushNotifications: e.target.checked })}
              className="h-4 w-4"
            />
            <label htmlFor="pushNotif" className="text-sm font-medium">Kích hoạt gửi thông báo đẩy (Push Notifications / In-app)</label>
          </div>
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-md font-medium hover:bg-blue-700"
        >
          Lưu cấu hình
        </button>
      </form>
    </div>
  );
};

export default SystemConfigAdmin;
```

---

## 5. DANH SÁCH KỊCH BẢN KIỂM THỬ (TEST CASES)

| Mã TC | Tên Test Case | Các bước thực hiện | Kết quả mong đợi |
| :---: | :--- | :--- | :--- |
| **TC-01** | Lưu cấu hình hệ thống hợp lệ | 1. Đăng nhập tài khoản Admin<br>2. Thay đổi dung lượng ảnh tối đa thành 30 MB<br>3. Bật gửi Email<br>4. Nhấn Lưu cấu hình | Hệ thống lưu thành công, hiển thị thông báo thành công và áp dụng quy định mới cho các luồng upload. |
| **TC-02** | Chặn upload file sai định dạng | 1. Admin cấu hình `allowedExtensions = "jpg, png"`<br>2. Thí sinh upload file `.bmp` hoặc `.pdf` | Hệ thống báo lỗi "Định dạng file không được hỗ trợ". |
| **TC-03** | Chặn upload file vượt dung lượng | 1. Admin cấu hình `maxFileSizeMb = 10`<br>2. Thí sinh upload file kích thước 15 MB | Hệ thống ngăn nộp bài và báo lỗi "File vượt quá dung lượng tối đa 10 MB". |
| **TC-04** | Phân quyền truy cập | Người dùng có role `Participant` hoặc `Judge` cố gắng truy cập URL cấu hình `/admin/settings` | Hệ thống từ chối truy cập và báo lỗi 403 Forbidden. |
