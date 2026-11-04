# HƯỚNG DẪN TRIỂN KHAI VÀ TÀI LIỆU CÔNG VIỆC (JIRA TASK)

## 1. THÔNG TIN CHUNG (TASK OVERVIEW)
* **Mã công việc (Issue Key):** CNPM-142
* **Epic/Parent:** CNPM-103
* **Tiêu đề:** [7.2] Form nộp bài và metadata kỹ thuật
* **Loại công việc:** Feature / User Story
* **Độ ưu tiên:** Must (Bắt buộc)
* **Thời gian ước lượng:** 20 giờ
* **Mã tài liệu liên quan:** FE7 (Docs/01) | WBS 7.2 (Docs/02) | SRS: FR-7.2, FR-7.3

---

## 2. PHÂN TÍCH YÊU CẦU NGHỆP VỤ (BUSINESS & SRS REQUIREMENTS)

### 2.1. Tóm tắt yêu cầu
Xây dựng chức năng cho phép thí sinh chọn hạng mục dự thi, chọn khung hình (frame) từ cuộn phim (film roll) đã lưu, nhập tiêu đề/mô tả tác phẩm. Hệ thống sẽ tự động trích xuất và hiển thị metadata kỹ thuật của cuộn phim/frame đó, đồng thời thực hiện các ràng buộc validation (trường bắt buộc, giới hạn số lượng ảnh, thời hạn nộp bài).

### 2.2. Các yêu cầu chức năng (FR Alignment)
* **FR-7.2 (Tạo & Quản lý Form Nộp Bài):**
  * Thí sinh chọn hạng mục thi (`contestCategoryId`).
  * Chọn khung hình (`frameId`) đã lưu từ cuộn phim (`film roll`) cá nhân.
  * Nhập tiêu đề (`title`) và mô tả (`description`).
  * Hệ thống tự động trích xuất và hiển thị (chế độ chỉ đọc - Read-only) các thông số metadata từ Roll và Frame: Hãng phim/Loại phim, ISO, Thân máy (Camera), Ống kính (Lens), Lab tráng rửa, Thông số scan.
* **FR-7.3 (Validation & Ràng buộc nghiệp vụ):**
  * Kiểm tra thời hạn nộp bài của cuộc thi: `Thời gian hiện tại <= SubmissionDeadline`.
  * Kiểm tra giới hạn số lượng bài dự thi của thí sinh trong cuộc thi/hạng mục: `Số bài đã nộp < MaxSubmissionsAllowed`.
  * Kiểm tra ràng buộc bắt buộc nhập đối với các trường: `contestCategoryId`, `frameId`, `title`.

---

## 3. THIẾT KẾ CƠ SỞ DỮ LIỆU & BACKEND API

### 3.1. DTO Đầu vào (Request DTO - SubmitContestEntryRequest)
```json
{
  "contestId": "string (UUID)",
  "contestCategoryId": "string (UUID)",
  "frameId": "string (UUID)",
  "title": "string",
  "description": "string"
}
```

### 3.2. DTO Trả về (Response DTO - ContestSubmissionDetailDto)
```json
{
  "submissionId": "string (UUID)",
  "contestId": "string (UUID)",
  "categoryId": "string (UUID)",
  "title": "string",
  "description": "string",
  "status": "PendingVerification",
  "submittedAt": "2026-11-04T17:30:00Z",
  "metadata": {
    "filmStock": "Kodak Vision3 250D",
    "camera": "Leica M6",
    "lens": "Summicron 35mm f/2",
    "iso": 250,
    "lab": "Zone5 Film Lab",
    "scanResolution": "3000x2000"
  }
}
```

### 3.3. Xử lý Logic tại Backend (Business Flow)
1. **Kiểm tra thời hạn:**
   * Lấy thông tin cuộc thi theo `contestId`.
   * Nếu `DateTime.UtcNow > Contest.SubmissionEndDate` $\rightarrow$ Trả về `400 Bad Request ("Cuộc thi đã hết thời hạn nộp bài")`.
2. **Kiểm tra số lượng bài dự thi:**
   * Đếm số lượng bài thi hiện tại của người dùng: `currentSubmissionsCount`.
   * Nếu `currentSubmissionsCount >= Contest.MaxSubmissionsPerUser` $\rightarrow$ Trả về `400 Bad Request ("Bạn đã vượt quá số lượng bài nộp cho phép")`.
3. **Kiểm tra tính hợp lệ của Frame:**
   * Xác nhận `frameId` thuộc sở hữu của người dùng hiện tại và chưa được nộp trong cuộc thi này.
4. **Tự động gắn Metadata:**
   * Trích xuất trực tiếp metadata từ bản ghi `Frame` và `FilmRoll` trong Cơ sở dữ liệu.
   * *Lưu ý:* Không cho phép client truyền các trường metadata lên API để đảm bảo tính minh bạch và chống giả mạo thông tin kỹ thuật.
5. **Lưu bản ghi Submission:**
   * Tạo bản ghi mới với trạng thái khởi tạo `PendingVerification`.

---

## 4. GIAO DIỆN MẪU FRONTEND (REACTJS / NEXT.JS)

Đoạn mã mã nguồn dưới đây minh họa component Form nộp bài tích hợp kiểm tra ràng buộc và tự động hiển thị metadata:

```jsx
import React, { useState, useEffect } from 'react';

const SubmissionForm = ({ contest, userFrames, onSubmit }) => {
  const [formData, setFormData] = useState({
    contestCategoryId: '',
    frameId: '',
    title: '',
    description: '',
  });

  const [selectedFrameMetadata, setSelectedFrameMetadata] = useState(null);
  const [errors, setErrors] = useState({});

  // Tự động trích xuất Metadata khi thí sinh chọn Frame từ danh sách
  useEffect(() => {
    if (formData.frameId) {
      const frame = userFrames.find((f) => f.id === formData.frameId);
      if (frame) {
        setSelectedFrameMetadata({
          filmStock: frame.filmRoll?.filmStockName || 'Kodak Gold 200',
          camera: frame.filmRoll?.cameraBody || 'Leica M6',
          lens: frame.filmRoll?.lens || 'Summicron 35mm f/2',
          iso: frame.filmRoll?.iso || 200,
          lab: frame.filmRoll?.devLab || 'Zone5 Film Lab',
          scanResolution: frame.scanResolution || '3000x2000',
        });
      }
    } else {
      setSelectedFrameMetadata(null);
    }
  }, [formData.frameId, userFrames]);

  const validate = () => {
    const errs = {};
    // Kiểm tra thời hạn cuộc thi
    if (new Date() > new Date(contest.submissionDeadline)) {
      errs.general = 'Cuộc thi đã hết thời hạn nộp bài!';
    }
    // Kiểm tra các trường bắt buộc
    if (!formData.contestCategoryId) errs.contestCategoryId = 'Vui lòng chọn hạng mục dự thi.';
    if (!formData.frameId) errs.frameId = 'Vui lòng chọn Frame ảnh từ cuộn phim.';
    if (!formData.title.trim()) errs.title = 'Vui lòng nhập tiêu đề bức ảnh.';
    
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 bg-white rounded-lg shadow-md max-w-2xl mx-auto space-y-4">
      <h2 className="text-xl font-bold border-b pb-2">Nộp bài dự thi nhiếp ảnh phim</h2>

      {errors.general && (
        <div className="p-3 bg-red-100 text-red-700 rounded-md">
          {errors.general}
        </div>
      )}

      {/* 1. Chọn Hạng mục */}
      <div>
        <label className="block font-medium mb-1">
          Hạng mục dự thi <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.contestCategoryId}
          onChange={(e) => setFormData({ ...formData, contestCategoryId: e.target.value })}
          className="w-full border rounded-md p-2"
        >
          <option value="">-- Chọn hạng mục --</option>
          {contest.categories.map((cat) => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
        {errors.contestCategoryId && (
          <p className="text-red-500 text-sm mt-1">{errors.contestCategoryId}</p>
        )}
      </div>

      {/* 2. Chọn Frame từ Roll */}
      <div>
        <label className="block font-medium mb-1">
          Chọn Frame phim <span className="text-red-500">*</span>
        </label>
        <select
          value={formData.frameId}
          onChange={(e) => setFormData({ ...formData, frameId: e.target.value })}
          className="w-full border rounded-md p-2"
        >
          <option value="">-- Chọn khung hình đã lưu --</option>
          {userFrames.map((frame) => (
            <option key={frame.id} value={frame.id}>
              Frame #{frame.frameNumber} - {frame.filmRoll?.filmStockName} ({frame.title || 'Không tiêu đề'})
            </option>
          ))}
        </select>
        {errors.frameId && (
          <p className="text-red-500 text-sm mt-1">{errors.frameId}</p>
        )}
      </div>

      {/* 3. Tiêu đề & Mô tả */}
      <div>
        <label className="block font-medium mb-1">
          Tiêu đề tác phẩm <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          className="w-full border rounded-md p-2"
          placeholder="Nhập tiêu đề..."
        />
        {errors.title && (
          <p className="text-red-500 text-sm mt-1">{errors.title}</p>
        )}
      </div>

      <div>
        <label className="block font-medium mb-1">Mô tả tác phẩm</label>
        <textarea
          rows={3}
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          className="w-full border rounded-md p-2"
          placeholder="Chia sẻ câu chuyện đằng sau bức ảnh..."
        />
      </div>

      {/* 4. Metadata kỹ thuật tự động điền (Read-only Display) */}
      {selectedFrameMetadata && (
        <div className="bg-gray-50 p-4 rounded-md border text-sm space-y-1 text-gray-700">
          <p className="font-semibold text-gray-900 border-b pb-1 mb-2">
            Thông số kỹ thuật tự động trích xuất (Metadata):
          </p>
          <div className="grid grid-cols-2 gap-2">
            <div><strong>Loại phim:</strong> {selectedFrameMetadata.filmStock}</div>
            <div><strong>Máy ảnh:</strong> {selectedFrameMetadata.camera}</div>
            <div><strong>Ống kính:</strong> {selectedFrameMetadata.lens}</div>
            <div><strong>ISO:</strong> {selectedFrameMetadata.iso}</div>
            <div><strong>Lab tráng:</strong> {selectedFrameMetadata.lab}</div>
            <div><strong>Độ phân giải scan:</strong> {selectedFrameMetadata.scanResolution}</div>
          </div>
        </div>
      )}

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-md font-medium hover:bg-blue-700"
      >
        Gửi bài dự thi
      </button>
    </form>
  );
};

export default SubmissionForm;
```

---

## 5. DANH SÁCH KỊCH BẢN KIỂM THỬ (TEST CASES)

| Mã TC | Tên Test Case | Các bước thực hiện | Kết quả mong đợi |
| :---: | :--- | :--- | :--- |
| **TC-01** | Nộp bài thành công hợp lệ | 1. Chọn Hạng mục hợp lệ<br>2. Chọn Frame khả dụng<br>3. Nhập tiêu đề, mô tả đầy đủ<br>4. Nhấn Nộp bài | Hệ thống lưu bài thành công, tự động trích xuất metadata từ Roll/Frame và chuyển trạng thái bài thi sang `PendingVerification`. |
| **TC-02** | Kiểm tra tự động điền Metadata | Chọn một `FrameId` bất kỳ từ danh sách lựa chọn | Khối thông tin Metadata (Camera, Film Stock, ISO, Lens, Lab) tự động hiển thị chính xác theo thông tin đã lưu của Frame đó và ở dạng chỉ đọc (Read-only). |
| **TC-03** | Bỏ trống các trường bắt buộc | Để trống Tiêu đề hoặc chưa chọn Hạng mục/Frame $\rightarrow$ Nhấn Nộp | Hệ thống chặn gửi form và hiển thị thông báo lỗi tương ứng bên dưới các trường bắt buộc. |
| **TC-04** | Nộp bài khi đã quá thời hạn cuộc thi | Thí sinh vào form nộp bài sau mốc `submissionDeadline` | Hệ thống hiển thị cảnh báo cuộc thi đã đóng/hết hạn nộp bài và vô hiệu hóa (disable) nút Nộp bài. |
| **TC-05** | Vượt giới hạn số lượng ảnh cho phép | Thí sinh đã nộp đủ số lượng ảnh tối đa cố gắng nộp thêm bài mới | Hệ thống Backend trả về lỗi validation: Thông báo thí sinh đã đạt giới hạn bài nộp tối đa cho phép. |