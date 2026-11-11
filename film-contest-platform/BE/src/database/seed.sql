-- ====================================================================
-- Initial Seed Data for Film Contest Platform
-- Default Password for all demo accounts: password123
-- Bcrypt Hash: $2b$10$3euPcmQFCiblsZeEu5s7p.qG4vHw4z7Ovhw1qU3g4jG04T9363RVO
-- ====================================================================

-- 1. SEED DEFAULT USERS
INSERT INTO users (name, email, password_hash, role, status, bio) VALUES
('Quản trị viên Hệ thống', 'admin@filmcontest.vn', '$2b$10$3euPcmQFCiblsZeEu5s7p.qG4vHw4z7Ovhw1qU3g4jG04T9363RVO', 'administrator', 'active', 'Hệ thống Quản trị viên cấp cao'),
('Ban tổ chức Cuộc thi', 'organizer@filmcontest.vn', '$2b$10$3euPcmQFCiblsZeEu5s7p.qG4vHw4z7Ovhw1qU3g4jG04T9363RVO', 'organizer', 'active', 'Đại diện Ban tổ chức cuộc thi nhiếp ảnh phim'),
('Nhiếp ảnh gia Giám khảo', 'judge@filmcontest.vn', '$2b$10$3euPcmQFCiblsZeEu5s7p.qG4vHw4z7Ovhw1qU3g4jG04T9363RVO', 'judge', 'active', 'Giám khảo chuyên môn thể loại ảnh tư liệu và phong cảnh'),
('Thí sinh Mẫu', 'participant@filmcontest.vn', '$2b$10$3euPcmQFCiblsZeEu5s7p.qG4vHw4z7Ovhw1qU3g4jG04T9363RVO', 'participant', 'active', 'Nhiếp ảnh gia tự do đam mê phim 35mm')
ON CONFLICT (email) DO NOTHING;

-- 2. SEED MASTER DATA
-- Film Brands
INSERT INTO master_data (type, value, description) VALUES
('film_brand', 'Kodak', 'Thương hiệu phim màu và đen trắng huyền thoại từ Mỹ'),
('film_brand', 'Fujifilm', 'Hãng phim nổi tiếng của Nhật Bản với tone màu xanh lá đặc trưng'),
('film_brand', 'Ilford', 'Chuyên gia sản xuất các dòng phim đen trắng chất lượng cao từ Anh'),
('film_brand', 'Cinestill', 'Phim điện ảnh chuyển đổi cho máy ảnh tĩnh (35mm, 120)'),
('film_brand', 'Lomography', 'Thương hiệu phim phong cách sáng tạo nghệ thuật'),
('film_brand', 'Fomapan', 'Dòng phim đen trắng cổ điển giá thành hợp lý từ Cộng hòa Séc')
ON CONFLICT DO NOTHING;

-- Film Stocks
INSERT INTO master_data (type, value, description) VALUES
('film_stock', 'Kodak Portra 400', 'Phim màu âm bản hạt mịn, tái tạo màu da xuất sắc'),
('film_stock', 'Kodak Portra 160', 'Phim chân dung hạt siêu mịn, độ tương phản dịu nhẹ'),
('film_stock', 'Kodak Gold 200', 'Phim màu tone ấm cổ điển, rất được ưa chuộng'),
('film_stock', 'Kodak ColorPlus 200', 'Phim màu phổ thông ấm áp phong cách vintage'),
('film_stock', 'Kodak Tri-X 400', 'Huyền thoại phim đen trắng độ tương phản cao của ảnh báo chí'),
('film_stock', 'Fujicolor C200', 'Phim màu đa dụng, sắc nét, màu sắc tự nhiên'),
('film_stock', 'Fuji Superia X-TRA 400', 'Phim tốc độ 400 màu sắc rực rỡ'),
('film_stock', 'Ilford HP5 Plus 400', 'Phim đen trắng linh hoạt có dải tương phản rộng'),
('film_stock', 'Ilford FP4 Plus 125', 'Phim đen trắng hạt mịn chi tiết cao'),
('film_stock', 'Cinestill 800T', 'Phim cân bằng ánh sáng vonfram (Tungsten) với quầng sáng đỏ đặc trưng'),
('film_stock', 'Cinestill 400D', 'Phim màu ban ngày hiện đại độ bão hòa cao'),
('film_stock', 'Fomapan 100 Classic', 'Phim đen trắng truyền thống phong cách retro')
ON CONFLICT DO NOTHING;

-- ISO
INSERT INTO master_data (type, value, description) VALUES
('iso', '50', 'ISO thấp cho điều kiện nắng gắt, phơi sáng'),
('iso', '100', 'ISO tiêu chuẩn ngoài trời sáng'),
('iso', '160', 'ISO chuyên dụng ảnh chân dung ngoài trời'),
('iso', '200', 'ISO đa dụng ban ngày'),
('iso', '400', 'ISO linh hoạt trong nhà và ngoài trời'),
('iso', '800', 'ISO chụp chiều tối hoặc ánh sáng yếu'),
('iso', '1600', 'ISO chụp ban đêm hoặc thể thao'),
('iso', '3200', 'ISO chụp đêm không cần chân máy')
ON CONFLICT DO NOTHING;

-- Film Formats
INSERT INTO master_data (type, value, description) VALUES
('film_format', '35mm (135)', 'Khổ phim phổ biến nhất kích thước khung hình 24x36mm'),
('film_format', '120 (Medium Format)', 'Khổ trung 6x4.5, 6x6, 6x7, 6x9 chi tiết vượt trội'),
('film_format', '4x5 (Large Format)', 'Khổ phim tấm chuyên nghiệp cho kiến trúc và phong cảnh'),
('film_format', '110 (Pocket)', 'Khổ phim bỏ túi thu nhỏ phong cách độc đáo')
ON CONFLICT DO NOTHING;

-- Cameras
INSERT INTO master_data (type, value, description) VALUES
('camera', 'Leica M6', 'Máy ảnh Rangefinder 35mm cơ học kinh điển'),
('camera', 'Canon AE-1', 'Máy ảnh SLR 35mm phổ biến nhất thế giới'),
('camera', 'Nikon FM2', 'Máy ảnh cơ hoàn toàn với màn trập 1/4000s huyền thoại'),
('camera', 'Olympus OM-1', 'Máy SLR nhỏ gọn với kính ngắm sáng rõ'),
('camera', 'Pentax K1000', 'Máy ảnh cơ bền bỉ lý tưởng cho người mới bắt đầu'),
('camera', 'Hasselblad 500C/M', 'Máy ảnh khổ trung 6x6 ngắm qua gương lật từ Thụy Điển'),
('camera', 'Mamiya RB67', 'Máy khổ trung 6x7 nổi tiếng với lưng xoay ngang dọc'),
('camera', 'Rolleiflex 2.8F', 'Máy ảnh 2 mắt TLR 6x6 với ống kính Carl Zeiss Planar')
ON CONFLICT DO NOTHING;

-- Lenses
INSERT INTO master_data (type, value, description) VALUES
('lens', '50mm f/1.4', 'Ống kính tiêu chuẩn khẩu độ lớn linh hoạt'),
('lens', '50mm f/1.8', 'Ống kính góc nhìn mắt người sắc nét'),
('lens', '35mm f/2', 'Tiêu cự vàng cho thể loại ảnh đời thường và phóng sự'),
('lens', '28mm f/2.8', 'Ống kính góc rộng phong cảnh và kiến trúc'),
('lens', '85mm f/1.4', 'Ống kính chân dung xóa phông cao cấp'),
('lens', '80mm f/2.8 (Medium Format)', 'Ống kính tiêu chuẩn trên khổ trung 6x6')
ON CONFLICT DO NOTHING;

-- Labs (Phòng lab tráng & scan phim)
INSERT INTO master_data (type, value, description) VALUES
('lab', 'Crop Lab', 'Lab tráng scan phim chuyên nghiệp tại Hà Nội & TP.HCM'),
('lab', 'Nadar Lab', 'Lab phim chất lượng cao với dịch vụ scan Frontier & Noritsu'),
('lab', 'LLab', 'Lab tráng phim uy tín tại TP.HCM'),
('lab', 'Darkroom Studio Lab', 'Lab nghệ thuật tự tráng và rọi ảnh thủ công'),
('lab', 'AEG Film Lab', 'Dịch vụ tráng scan phim đen trắng và màu')
ON CONFLICT DO NOTHING;

-- Scanners
INSERT INTO master_data (type, value, description) VALUES
('scanner', 'Noritsu HS-1800', 'Máy scan công nghiệp độ phân giải cao và màu sắc trong trẻo'),
('scanner', 'Fuji Frontier SP-3000', 'Máy scan màu pastel đặc trưng của Fujifilm'),
('scanner', 'Pakon F135 Plus', 'Máy scan 35mm tái tạo màu da Kodak chân thực'),
('scanner', 'Epson Perfection V850 Pro', 'Máy flatbed scan chuyên dụng cho phim khổ lớn 120 và 4x5')
ON CONFLICT DO NOTHING;

-- 3. SEED A SAMPLE CONTEST
INSERT INTO contests (
    title, theme, description, regulations, 
    submission_start, submission_end, judging_start, judging_end, 
    status, config_locked, created_by
) VALUES (
    'Khoảnh Khắc Analog 2026',
    'Nhịp sống Việt Nam qua lăng kính phim',
    'Cuộc thi thường niên tôn vinh vẻ đẹp của nhiếp ảnh phim analog, ghi lại những câu chuyện đời thường, văn hoá và con người Việt Nam.',
    'Chỉ chấp nhận ảnh chụp bằng máy ảnh phim thật (35mm, 120, Large Format). Mỗi tác phẩm phải cung cấp thông tin cuộn phim và số khung hình.',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP + INTERVAL '30 days',
    CURRENT_TIMESTAMP + INTERVAL '31 days',
    CURRENT_TIMESTAMP + INTERVAL '45 days',
    'open',
    FALSE,
    (SELECT id FROM users WHERE email = 'organizer@filmcontest.vn' LIMIT 1)
) ON CONFLICT DO NOTHING;

-- 4. SEED SAMPLE CATEGORIES
INSERT INTO categories (contest_id, name, max_photos_per_participant, submission_rules, award_structure)
SELECT 
    c.id,
    'Đời sống thường nhật (Street Life)',
    3,
    'Chụp trên lãnh thổ Việt Nam trong năm 2026. Ảnh không được can thiệp kỹ thuật số sai lệch sự thật.',
    '1 Giải Nhất (10.000.000 VNĐ + Kỷ niệm chương), 1 Giải Nhì, 2 Giải Ba, 3 Giải Khuyến khích'
FROM contests c WHERE c.title = 'Khoảnh Khắc Analog 2026'
ON CONFLICT DO NOTHING;

INSERT INTO categories (contest_id, name, max_photos_per_participant, submission_rules, award_structure)
SELECT 
    c.id,
    'Chân dung & Con người (Portrait)',
    2,
    'Tập trung vào cảm xúc và chân dung con người. Chấp nhận cả phim màu và phim đen trắng.',
    '1 Giải Nhất (8.000.000 VNĐ), 1 Giải Nhì, 1 Giải Ba'
FROM contests c WHERE c.title = 'Khoảnh Khắc Analog 2026'
ON CONFLICT DO NOTHING;

-- 5. SEED SAMPLE CRITERIA
INSERT INTO criteria (contest_id, category_id, name, description, weight, max_score)
SELECT 
    c.id, 
    NULL, 
    'Chất lượng nghệ thuật & Ý tưởng (Artistic & Concept)', 
    'Bố cục, thông điệp truyền tải, cảm xúc nghệ thuật và sự sáng tạo', 
    40.00, 
    10.00
FROM contests c WHERE c.title = 'Khoảnh Khắc Analog 2026'
ON CONFLICT DO NOTHING;

INSERT INTO criteria (contest_id, category_id, name, description, weight, max_score)
SELECT 
    c.id, 
    NULL, 
    'Kỹ thuật nhiếp ảnh phim (Analog Craftsmanship)', 
    'Kỹ thuật phơi sáng, kiểm soát hạt, độ nét và tính chất màu sắc của cuộn phim', 
    35.00, 
    10.00
FROM contests c WHERE c.title = 'Khoảnh Khắc Analog 2026'
ON CONFLICT DO NOTHING;

INSERT INTO criteria (contest_id, category_id, name, description, weight, max_score)
SELECT 
    c.id, 
    NULL, 
    'Tính xác thực & Câu chuyện (Storytelling & Authenticity)', 
    'Độ chân thật, thông tin khung hình và câu chuyện đi cùng tác phẩm', 
    25.00, 
    10.00
FROM contests c WHERE c.title = 'Khoảnh Khắc Analog 2026'
ON CONFLICT DO NOTHING;
