-- Task: C21-13 | Database Schema ERD cho Nền tảng Cuộc thi Nhiếp ảnh Phim
-- Hệ quản trị: PostgreSQL
-- Số lượng bảng: 9

-- 1. Bảng Roles (Phân quyền người dùng)
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Bảng Users (Hồ sơ người dùng & Thí sinh - CNPM-136)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(role_id),
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    portfolio_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bảng Contest Templates (Đặc tả Template tái sử dụng - CNPM-148)
CREATE TABLE contest_templates (
    template_id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) NOT NULL,
    description TEXT,
    created_by INT REFERENCES users(user_id)
);

-- 4. Bảng Contests (Thông tin Cuộc thi)
CREATE TABLE contests (
    contest_id SERIAL PRIMARY KEY,
    template_id INT REFERENCES contest_templates(template_id),
    title VARCHAR(200) NOT NULL,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'DRAFT'
);

-- 5. Bảng Scoring Criteria (Tiêu chí chấm điểm & Preset Film - CNPM-135, CNPM-146)
CREATE TABLE scoring_criteria (
    criteria_id SERIAL PRIMARY KEY,
    contest_id INT REFERENCES contests(contest_id),
    criteria_name VARCHAR(100) NOT NULL,
    weight_percentage DECIMAL(5,2) NOT NULL,
    description TEXT
);

-- 6. Bảng Submissions (Quản lý vòng đời bài nộp - CNPM-50)
CREATE TABLE submissions (
    submission_id VARCHAR(50) PRIMARY KEY,
    contest_id INT REFERENCES contests(contest_id),
    user_id INT REFERENCES users(user_id),
    title VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING_AI_REVIEW',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Bảng Media Assets (Ảnh dự thi, Contact Sheet & PoC AI - CNPM-54, CNPM-26)
CREATE TABLE media_assets (
    asset_id SERIAL PRIMARY KEY,
    submission_id VARCHAR(50) REFERENCES submissions(submission_id),
    asset_type VARCHAR(50) NOT NULL, -- 'FINAL_IMAGE', 'CONTACT_SHEET'
    file_url VARCHAR(255) NOT NULL,
    ai_verification_status VARCHAR(50) DEFAULT 'UNVERIFIED'
);

-- 8. Bảng Judgments (Phân công Giám khảo chấm thi)
CREATE TABLE judgments (
    judgment_id SERIAL PRIMARY KEY,
    submission_id VARCHAR(50) REFERENCES submissions(submission_id),
    judge_id INT REFERENCES users(user_id),
    status VARCHAR(20) DEFAULT 'ASSIGNED'
);

-- 9. Bảng Scores (Điểm số chi tiết)
CREATE TABLE scores (
    score_id SERIAL PRIMARY KEY,
    judgment_id INT REFERENCES judgments(judgment_id),
    criteria_id INT REFERENCES scoring_criteria(criteria_id),
    score_value DECIMAL(5,2) NOT NULL,
    comments TEXT
);
