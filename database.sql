CREATE DATABASE IF NOT EXISTS du_lieu_tuyendung CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE du_lieu_tuyendung;

CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_dang_nhap VARCHAR(50) UNIQUE NOT NULL,
    mat_khau VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    vai_tro VARCHAR(20) NOT NULL,
    so_dien_thoai VARCHAR(20),
    dia_diem VARCHAR(100),
    vi_tri_mong_muon VARCHAR(100),
    ky_nang TEXT,
    kinh_nghiem VARCHAR(100),
    tom_tat TEXT,
    ten_file_cv VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS bai_dang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tieu_de VARCHAR(255) NOT NULL,
    ten_cong_ty VARCHAR(255) NOT NULL,
    ten_dang_nhap_ntd VARCHAR(50) NOT NULL,
    dia_diem VARCHAR(200) NOT NULL,
    nganh_nghe VARCHAR(100) NOT NULL,
    muc_luong VARCHAR(100),
    ky_nang_yeu_cau VARCHAR(255),
    mo_ta TEXT,
    ngay_dang DATE,
    FOREIGN KEY (ten_dang_nhap_ntd) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS don_ung_tuyen (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_bai_dang INT NOT NULL,
    ten_dang_nhap_ung_vien VARCHAR(50) NOT NULL,
    ten_dang_nhap_ntd VARCHAR(50) NOT NULL,
    diem_phu_hop INT DEFAULT 0,
    trang_thai VARCHAR(50) DEFAULT 'Chờ xử lý',
    ngay_ung_tuyen DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_bai_dang) REFERENCES bai_dang(id) ON DELETE CASCADE,
    FOREIGN KEY (ten_dang_nhap_ung_vien) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE,
    FOREIGN KEY (ten_dang_nhap_ntd) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tin_nhan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_don INT NOT NULL,
    nguoi_gui VARCHAR(50) NOT NULL,
    noi_dung TEXT NOT NULL,
    thoi_gian DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_don) REFERENCES don_ung_tuyen(id) ON DELETE CASCADE,
    FOREIGN KEY (nguoi_gui) REFERENCES nguoi_dung(ten_dang_nhap) ON DELETE CASCADE
);

-- Dữ liệu tài khoản mẫu
INSERT IGNORE INTO nguoi_dung (ten_dang_nhap, mat_khau, ho_ten, email, vai_tro, ky_nang, dia_diem, vi_tri_mong_muon) VALUES
('ungvien_demo', '123456', 'Nguyễn Văn Ứng Viên', 'ungvien@gmail.com', 'ung_vien', 'Python, SQL, FastAPI, Git', 'Đà Nẵng', 'Python Developer'),
('fpt_software', '123456', 'Công ty FPT Software', 'recruitment@fpt.com', 'nha_tuyen_dung', '', '', ''),
('vng_corp', '123456', 'Tập đoàn VNG', 'hr@vng.com.vn', 'nha_tuyen_dung', '', '', ''),
('viettel_group', '123456', 'Tập đoàn Viettel', 'tuyendung@viettel.com.vn', 'nha_tuyen_dung', '', '', ''),
('shopee_vn', '123456', 'Shopee Việt Nam', 'careers@shopee.vn', 'nha_tuyen_dung', '', '', '');

-- Dữ liệu bài đăng mẫu
INSERT INTO bai_dang (tieu_de, ten_cong_ty, ten_dang_nhap_ntd, dia_diem, nganh_nghe, muc_luong, ky_nang_yeu_cau, mo_ta, ngay_dang) VALUES
('Lập trình viên Senior Python / FastAPI', 'Công ty FPT Software', 'fpt_software', 'Đà Nẵng (Khu công nghệ cao)', 'Công nghệ thông tin', '20 - 35 triệu', 'Python, FastAPI, SQL, Docker, Git', 'Phát triển Microservices bằng Python / FastAPI và tối ưu CSDL MySQL.', CURDATE()),
('Kỹ sư Trí tuệ Nhân tạo (AI / Machine Learning Engineer)', 'Tập đoàn VNG', 'vng_corp', 'TP. Hồ Chí Minh (Quận 7)', 'Trí tuệ nhân tạo', '30 - 50 triệu', 'Python, Machine Learning, TensorFlow, PyTorch, SQL', 'Nghiên cứu và triển khai các mô hình Machine Learning / Deep Learning.', CURDATE()),
('Chuyên viên Phân tích Dữ liệu (Data Analyst)', 'Shopee Việt Nam', 'shopee_vn', 'Hà Nội (Cầu Giấy)', 'Phân tích dữ liệu', '18 - 28 triệu', 'SQL, Python, PowerBI, Excel, Tableau', 'Phân tích hành vi người dùng và xây dựng dashboard báo cáo trực quan.', CURDATE()),
('Lập trình viên Frontend (ReactJS / TypeScript)', 'Tập đoàn Viettel', 'viettel_group', 'Hà Nội & Đà Nẵng', 'Công nghệ thông tin', '15 - 25 triệu', 'ReactJS, TypeScript, HTML, CSS, Git', 'Xây dựng giao diện Web responsive và tích hợp RESTful API.', CURDATE());

-- Đơn ứng tuyển & tin nhắn mẫu để test Chat Box
INSERT INTO don_ung_tuyen (id_bai_dang, ten_dang_nhap_ung_vien, ten_dang_nhap_ntd, diem_phu_hop, trang_thai)
SELECT id, 'ungvien_demo', 'fpt_software', 85, 'Chờ xử lý' FROM bai_dang WHERE ten_dang_nhap_ntd = 'fpt_software' LIMIT 1;

INSERT INTO tin_nhan (id_don, nguoi_gui, noi_dung)
SELECT id, 'ungvien_demo', 'Chào Anh/Chị tuyển dụng, em đã nộp CV ứng tuyển vị trí này ạ!' FROM don_ung_tuyen WHERE ten_dang_nhap_ung_vien = 'ungvien_demo' LIMIT 1;
