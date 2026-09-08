-- 1. Thêm người dùng mẫu (1 Admin, 2 Recruiter, 2 Candidate)
INSERT INTO users (email, password_hash, full_name, role) VALUES
('admin@gmail.com', 'hash_pass_admin', 'Quản Trị Viên', 'admin'),
('recruiter1@techcorp.com', 'hash_pass_rec1', 'Nguyễn Văn Tuyển', 'recruiter'),
('recruiter2@aistudio.com', 'hash_pass_rec2', 'Trần Thị Dụng', 'recruiter'),
('candidate1@gmail.com', 'hash_pass_cand1', 'Lê Văn Lập Trình', 'candidate'),
('candidate2@gmail.com', 'hash_pass_cand2', 'Phạm Thị Dữ Liệu', 'candidate');

-- 2. Thêm thông tin Hồ sơ Ứng viên (Candidates)
INSERT INTO candidates (user_id, title, skills_list) VALUES
(4, 'Backend Developer', 'Python, FastAPI, PostgreSQL, Docker, Git'),
(5, 'AI/Data Engineer', 'Python, PyTorch, Pandas, Scikit-learn, SQL');

-- 3. Thêm thông tin Công ty (Companies)
INSERT INTO companies (recruiter_id, company_name, location) VALUES
(2, 'Công ty Công nghệ TechCorp', 'Hà Nội'),
(3, 'Giải pháp AI Studio', 'TP. Hồ Chí Minh');

-- 4. Thêm bài đăng tuyển dụng mẫu (Job Posts)
INSERT INTO job_posts (company_id, title, requirements) VALUES
(1, 'Lập trình viên Python Backend', 'Yêu cầu 1+ năm kinh nghiệm với Python/FastAPI, thành thạo PostgreSQL, biết Docker là lợi thế.'),
(2, 'Kỹ sư AI / Machine Learning', 'Thành thạo Python, PyTorch/TensorFlow, có kinh nghiệm xử lý ngôn ngữ tự nhiên (NLP) và bóc tách dữ liệu.');

-- 5. Thêm CV mẫu (Resumes)
INSERT INTO resumes (candidate_id, file_url, parsed_content) VALUES
(1, 'https://storage.example.com/cvs/cv_levanlaptrinh.pdf', 'Lê Văn Lập Trình - Kinh nghiệm: 2 năm Python Backend, FastAPI, MySQL, Docker.'),
(2, 'https://storage.example.com/cvs/cv_phamthidulieu.pdf', 'Phạm Thị Dữ Liệu - Kinh nghiệm: 1.5 năm AI Engineer, PyTorch, NLP, LangChain.');

-- 6. Thêm lượt ứng tuyển mẫu kèm điểm AI Matching (Applications)
INSERT INTO applications (job_id, candidate_id, resume_id, matching_score) VALUES
(1, 1, 1, 88.5),
(2, 2, 2, 92.0);
