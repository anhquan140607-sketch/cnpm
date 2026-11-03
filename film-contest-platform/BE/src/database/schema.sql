-- ====================================================================
-- AI-Powered Film Photography Contest Management Platform
-- Database Schema (PostgreSQL)
-- Based on Docs/08-architecture-and-erd.md & Docs/05-srs.md
-- ====================================================================

-- Drop tables in reverse dependency order if recreating
DROP TABLE IF EXISTS refresh_tokens CASCADE;
DROP TABLE IF EXISTS activity_logs CASCADE;
DROP TABLE IF EXISTS archive_items CASCADE;
DROP TABLE IF EXISTS awards CASCADE;
DROP TABLE IF EXISTS evaluation_scores CASCADE;
DROP TABLE IF EXISTS evaluations CASCADE;
DROP TABLE IF EXISTS judge_assignments CASCADE;
DROP TABLE IF EXISTS ai_check_results CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;
DROP TABLE IF EXISTS frames CASCADE;
DROP TABLE IF EXISTS film_rolls CASCADE;
DROP TABLE IF EXISTS master_data CASCADE;
DROP TABLE IF EXISTS registrations CASCADE;
DROP TABLE IF EXISTS rounds CASCADE;
DROP TABLE IF EXISTS criteria CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS contests CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 1. USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('administrator', 'organizer', 'judge', 'participant')),
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    avatar_url VARCHAR(500),
    phone VARCHAR(50),
    bio TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. CONTESTS TABLE
CREATE TABLE contests (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    theme VARCHAR(255) NOT NULL,
    description TEXT,
    regulations TEXT,
    submission_start TIMESTAMP WITH TIME ZONE NOT NULL,
    submission_end TIMESTAMP WITH TIME ZONE NOT NULL,
    judging_start TIMESTAMP WITH TIME ZONE NOT NULL,
    judging_end TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'open', 'closed', 'judging', 'published', 'archived')),
    config_locked BOOLEAN NOT NULL DEFAULT FALSE,
    banner_url VARCHAR(500),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. CATEGORIES TABLE
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    contest_id INTEGER NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    max_photos_per_participant INTEGER NOT NULL DEFAULT 3 CHECK (max_photos_per_participant > 0),
    submission_rules TEXT,
    award_structure TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. CRITERIA TABLE
CREATE TABLE criteria (
    id SERIAL PRIMARY KEY,
    contest_id INTEGER NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE, -- NULL means applicable to all categories
    name VARCHAR(150) NOT NULL,
    description TEXT,
    weight NUMERIC(5, 2) NOT NULL CHECK (weight > 0 AND weight <= 100),
    max_score NUMERIC(5, 2) NOT NULL DEFAULT 10.00 CHECK (max_score > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. ROUNDS TABLE
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    contest_id INTEGER NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    sequence INTEGER NOT NULL DEFAULT 1,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. REGISTRATIONS TABLE
CREATE TABLE registrations (
    id SERIAL PRIMARY KEY,
    participant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contest_id INTEGER NOT NULL REFERENCES contests(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_participant_contest_category UNIQUE (participant_id, contest_id, category_id)
);

-- 7. MASTER_DATA TABLE (Film brands, stocks, ISO, formats, cameras, lenses, labs, scanners)
CREATE TABLE master_data (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL CHECK (type IN ('film_brand', 'film_stock', 'iso', 'film_format', 'camera', 'lens', 'lab', 'scanner')),
    value VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. FILM_ROLLS TABLE
CREATE TABLE film_rolls (
    id SERIAL PRIMARY KEY,
    participant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    roll_name VARCHAR(150),
    film_brand_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    film_stock_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    iso_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    film_format_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    camera_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    lens_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    lab_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    scanner_id INTEGER REFERENCES master_data(id) ON DELETE RESTRICT,
    scan_specs TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. FRAMES TABLE
CREATE TABLE frames (
    id SERIAL PRIMARY KEY,
    film_roll_id INTEGER NOT NULL REFERENCES film_rolls(id) ON DELETE CASCADE,
    frame_number INTEGER NOT NULL CHECK (frame_number > 0 AND frame_number <= 72),
    shooting_location VARCHAR(255),
    shooting_date DATE,
    shutter_speed VARCHAR(50),
    aperture VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_roll_frame_number UNIQUE (film_roll_id, frame_number)
);

-- 10. SUBMISSIONS TABLE
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    frame_id INTEGER NOT NULL REFERENCES frames(id) ON DELETE RESTRICT,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    participant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_path VARCHAR(500) NOT NULL,
    thumbnail_path VARCHAR(500),
    negative_ref_path VARCHAR(500),
    status VARCHAR(50) NOT NULL DEFAULT 'submitted' CHECK (status IN ('submitted', 'under_verification', 'accepted', 'rejected', 'needs_revision', 'withdrawn')),
    rejection_reason TEXT,
    keywords VARCHAR(500),
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. AI_CHECK_RESULTS TABLE
CREATE TABLE ai_check_results (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('duplicate', 'ai_generated', 'content_moderation')),
    score NUMERIC(5, 4) NOT NULL, -- Confidence/Similarity score e.g. 0.9850
    matched_submission_id INTEGER REFERENCES submissions(id) ON DELETE SET NULL,
    details JSONB,
    decision VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (decision IN ('pending', 'flagged', 'cleared')),
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 12. JUDGE_ASSIGNMENTS TABLE
CREATE TABLE judge_assignments (
    id SERIAL PRIMARY KEY,
    judge_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    round_id INTEGER NOT NULL REFERENCES rounds(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_judge_category_round UNIQUE (judge_id, category_id, round_id)
);

-- 13. EVALUATIONS TABLE
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    judge_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    comment TEXT,
    confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_judge_submission UNIQUE (judge_id, submission_id)
);

-- 14. EVALUATION_SCORES TABLE
CREATE TABLE evaluation_scores (
    id SERIAL PRIMARY KEY,
    evaluation_id INTEGER NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    criterion_id INTEGER NOT NULL REFERENCES criteria(id) ON DELETE CASCADE,
    score NUMERIC(5, 2) NOT NULL CHECK (score >= 0),
    CONSTRAINT uq_evaluation_criterion UNIQUE (evaluation_id, criterion_id)
);

-- 15. AWARDS TABLE
CREATE TABLE awards (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL, -- First Prize, Second Prize, Honorable Mention...
    rank INTEGER NOT NULL,
    prize_amount VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 16. ARCHIVE_ITEMS TABLE
CREATE TABLE archive_items (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE UNIQUE,
    metadata_snapshot JSONB NOT NULL,
    judging_comments TEXT,
    archived_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 17. ACTIVITY_LOGS TABLE
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id INTEGER,
    details JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. REFRESH_TOKENS TABLE
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- Indexes for Performance & Search
-- ====================================================================
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_contests_status ON contests(status);
CREATE INDEX idx_categories_contest ON categories(contest_id);
CREATE INDEX idx_criteria_contest ON criteria(contest_id);
CREATE INDEX idx_master_data_type ON master_data(type, status);
CREATE INDEX idx_film_rolls_participant ON film_rolls(participant_id);
CREATE INDEX idx_frames_roll ON frames(film_roll_id);
CREATE INDEX idx_submissions_status ON submissions(status);
CREATE INDEX idx_submissions_category ON submissions(category_id);
CREATE INDEX idx_submissions_participant ON submissions(participant_id);
CREATE INDEX idx_ai_check_submission ON ai_check_results(submission_id);
CREATE INDEX idx_evaluations_judge ON evaluations(judge_id);
CREATE INDEX idx_evaluations_submission ON evaluations(submission_id);
CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created ON activity_logs(created_at);
