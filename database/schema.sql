-- 1. Bảng USERS
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('candidate', 'recruiter', 'admin')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng CANDIDATES
CREATE TABLE candidates (
    candidate_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(100),
    skills_list TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bảng RESUMES
CREATE TABLE resumes (
    resume_id SERIAL PRIMARY KEY,
    candidate_id INT REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    file_url VARCHAR(500) NOT NULL,
    parsed_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Bảng COMPANIES
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    recruiter_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

-- 5. Bảng JOB_POSTS
CREATE TABLE job_posts (
    job_id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(company_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    requirements TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Bảng APPLICATIONS
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    job_id INT REFERENCES job_posts(job_id) ON DELETE CASCADE,
    candidate_id INT REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    resume_id INT REFERENCES resumes(resume_id) ON DELETE CASCADE,
    matching_score FLOAT DEFAULT 0.0,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
