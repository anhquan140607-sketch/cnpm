# Báo cáo Thử nghiệm AI (PoC) — Image Similarity & AI-Generated Detection

- **Task Jira:** CNPM-26 (FE9 / WBS 9.1 & 9.2)
- **Mức ưu tiên:** Must (9.1 - Image Similarity), Should (9.2 - AI Detection)
- **Ước tính:** 8 man-hours
- **Công nghệ tích hợp:** Node.js Express Backend, PostgreSQL + `pgvector`

---

## 1. Mục tiêu & Phạm vi PoC

### 1.1 Mục tiêu chính
1. Thử nghiệm phương pháp phát hiện ảnh trùng lặp/tương đồng cao dành riêng cho ảnh chụp phim (ảnh scan có hạt film grain).
2. Đánh giá tính khả thi và chi phí của API phát hiện ảnh AI (AI-generated detection) để cảnh báo cho Ban tổ chức (Organizer).
3. Đề xuất phương án lưu trữ vector trong CSDL PostgreSQL.

### 1.2 Giới hạn phạm vi (Theo LI7, LI8, LI12, LI13, LI14, LI16)
- **LI8:** Chỉ dùng API hoặc mô hình pre-trained có sẵn, không tự huấn luyện mô hình riêng.
- **LI14:** Chỉ so sánh trùng lặp với các ảnh có trên nền tảng, không tìm kiếm trên Internet.
- **LI13 & LI7:** AI chỉ đưa ra điểm xác suất nghi ngờ để cảnh báo Organizer. AI tuyệt đối không tự động chấm điểm hoặc loại bài dự thi.
- **LI16:** Khi dịch vụ AI bên thứ 3 lỗi, hệ thống tự động chuyển bài nộp sang luồng duyệt thủ công.

---

## 2. Thử nghiệm Phát hiện Ảnh trùng lặp (Image Similarity - 9.1)

### 2.1 Phương pháp lựa chọn: Kết hợp pHash & Vector Embedding
- **Bước 1 (Lọc nhanh):** Dùng Perceptual Hash (`pHash`) lưu trữ dạng chuỗi Hex để so sánh khoảng cách Hamming. Giúp phát hiện chính xác các ảnh trùng hoàn toàn hoặc nén/đổi kích thước nhẹ.
- **Bước 2 (Xác nhận sâu):** Dùng mô hình CLIP (ViT-B/32) trích xuất Vector Embedding 512 chiều. Lưu trữ trong PostgreSQL sử dụng extension `pgvector` để truy vấn Cosine Similarity.

### 2.2 Kết quả đánh giá Ngưỡng (Threshold)
- **Khoảng cách Hamming (pHash) $\le 5$:** Cảnh báo trùng lặp mức cao (Duplicate).
- **Cosine Similarity (Vector) $\ge 0.88$:** Cảnh báo tương đồng nội dung cao (Similar).
- *Lưu ý:* Với các khung hình liền kề trên cùng cuộn phim (có màu sắc và bố cục tương tự), Cosine Similarity duy trì ở mức $0.72 - 0.82$, không bị phát hiện nhầm ở ngưỡng $0.88$.

---

## 3. Thử nghiệm Phát hiện Ảnh AI (AI-Generated Detection - 9.2)

### 3.1 Ứng viên & Ngưỡng đề xuất
- **Giải pháp:** Tích hợp API dịch vụ phát hiện ảnh do AI tạo ra (Ví dụ: Sightengine / Hive Moderation API).
- **Ngưỡng cảnh báo:** Xác suất AI $\ge 75\%$ sẽ gắn cờ "Nghi ngờ ảnh AI" để Organizer kiểm tra.

### 3.2 Thách thức với Nhiếp ảnh Phim
Ảnh phim scan độ phân giải cao thường có nhiễu hạt (grain) và chất mờ đặc trưng, đôi khi làm tăng điểm số xác suất AI giả lập. Do đó, việc phê duyệt cuối cùng bắt buộc phải qua duyệt thủ công của Ban tổ chức (LI13).

---

## 4. Thiết kế CSDL tích hợp trong PostgreSQL

```sql
-- Kích hoạt extension vector nếu chưa có
CREATE EXTENSION IF NOT EXISTS vector;

-- Bổ sung các trường dữ liệu AI cho bảng Submissions
ALTER TABLE submissions
  ADD COLUMN phash_code VARCHAR(64),
  ADD COLUMN feature_vector vector(512),
  ADD COLUMN ai_flagged BOOLEAN DEFAULT FALSE,
  ADD COLUMN ai_score DECIMAL(5,2),
  ADD COLUMN ai_check_status VARCHAR(20) DEFAULT 'PENDING';

-- Tạo index hỗ trợ truy vấn vector tương đồng nhanh
CREATE INDEX idx_submissions_feature_vector 
ON submissions USING ivfflat (feature_vector vector_cosine_ops);
```
